import tkinter as tk
import customtkinter
import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import numpy as np

from ..functions import heatmap

import inspect

import multiprocessing
import src.global_parameters as gp

matplotlib.use('TkAgg')

AWAIT_TIME = 100

# function to run calculations in the external process
def run_in_process(result_queue, func, kwargs):
    for output in func(**kwargs):
        result_queue.put(output)

# custom toolbar for the graph on the base of NavigationToolbar2Tk
class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # delete unnecessary buttons
        self.children['!button3'].pack_forget()
        self.children['!button2'].pack_forget()
        self.children['!button5'].pack_forget()
        # depending on the light mode, change buttons' color
        if gp.SYSTEM_LIGHT_MODE == 'Light':
            self.config(background="#d5d8df")
            for button in self.winfo_children():
                button.config(background="#d5d8df")
        else:
            self.config(background="#414868")
            for button in self.winfo_children():
                button.config(background="#414868")

# main class for the frame with graph on the base of customtkinter.CTkFrame
class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # change corner radius
        self._corner_radius = kwargs['corner_radius']
        
        # label with the graph's name
        self.label = customtkinter.CTkLabel(
            self, 
            text='СумДУ',
            font=customtkinter.CTkFont(
                size=14,
            ),
        )
        self.label.pack(
            pady=(gp.ELEMENTS_PAD, gp.ELEMENTS_PAD)
        )

        # Change the graph style depending on whether the light or dark mode is active
        if gp.SYSTEM_LIGHT_MODE == 'Light':
            plt.style.use(os.path.join(gp.CURRENT_DIR, 'src', 'styles', 'pacoty.mplstyle'))
        else:
            plt.style.use(os.path.join(gp.CURRENT_DIR, 'src', 'styles', 'pitayasmoothie-dark.mplstyle'))
        
        # create figure
        self.fig = Figure(dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.fig.set_constrained_layout(True)
        
        # calculate coordinates
        theta = np.linspace(0, 2 * np.pi, 100)
        x = 16 * ( np.sin(theta) ** 3 )
        y = 13 * np.cos(theta) - 5* np.cos(2*theta) - 2 * np.cos(3*theta) - np.cos(4*theta)
        
        self.ax.scatter(x,y) # plot the graph
        
        # create widget for custom tkinter
        self.graph = FigureCanvasTkAgg(self.fig, master=self)
        self.graph.draw()
        self.graph.get_tk_widget().pack(
            side=tk.TOP, fill=tk.BOTH, 
            padx=gp.INNER_PAD,
            pady=(0, gp.INNER_PAD)
        )
        # create toolbar
        self.toolbar = CustomToolbar(canvas=self.graph, window=self, pack_toolbar=True)
        self.toolbar.update()
        self.toolbar.pack(
            side=tk.BOTTOM, fill='both',
            padx=gp.INNER_PAD,
            pady=(0, gp.INNER_PAD)
        )
        
        # create default vars
        self.export_files = [] # list for export files
        self.default_file_name = None # default name for the file
        self.result_queue = multiprocessing.Queue() # A queue is used to store results from the process, as they could be lost otherwise

    # check if all required parameters are available
    def params_validation(self):
        try:
            for key in self.current_function['required_params']:
                self.params.get(key)
        except NameError as e:
            self.master.param_expl_box.configure(text=f"Немає значення параметру(ів): {e}")
    
    # function to check whether function gave the results
    def check_result_queue(self):
        try:
            # Try to get the result from the queue
            data = self.result_queue.get_nowait()
            # if result is the value for the progress bar it means that calculations are ongoing
            if data[-1] == 'progress':
                self.master.eval_progress_bar.set(data[0]) # update progress bar
                self.master.after(AWAIT_TIME, self.check_result_queue) # keep checking
                return
            # If we get the needed result, we update the plot.
            self.update_plot(data)
        # If no result yet, keep checking
        except multiprocessing.queues.Empty:
            self.master.after(AWAIT_TIME, self.check_result_queue)
    
    # check if var is lambda
    def check_if_lambda(self, var):
        # since the var could be a lambda function that is customized based on parameters, we check if it is callable
        if callable(var):
            function = var # get title function
            params = list(inspect.signature(function).parameters) # get all needed parameters' names
            params_to_pass = {param_name: self.params[param_name] for param_name in params if param_name in self.params} # get their values
            return function(**params_to_pass) # return resulting value
        return var # if not a function, return itself

    # canvas cleaner
    def clear_canvas(self):
        self.master.eval_progress_bar.set(0) # set progress bar to 0
        self.export_files = [] # empty export files list
        self.ax.clear() # clear figure
        
        # clear color bar if there is any (for heatmap)
        if hasattr(self, 'cbar') and self.cbar is not None:
            try:
                self.cbar.remove()
            except Exception as e:
                print(f"Error removing colorbar: {e}")
            self.cbar = None
        
        # update figure
        self.graph.draw()
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
    
    # plot function that is called from main.py
    def plot(self, fun_num, **kwargs): 
        self.current_function = self.master.functions[fun_num] # store called function
        self.params = kwargs # store parameters
        self.params_validation() # parameters validation, if there are all needed for current function
        # create a process
        process = multiprocessing.Process(
            target=run_in_process, 
            args=(
                self.result_queue, 
                self.current_function['function'], 
                kwargs,
            )
        )
        process.start() # start the process
        # After AWAIT_TIME milliseconds, check for any results using the self.check_result_queue function
        self.master.after(AWAIT_TIME, self.check_result_queue)
    
    # function to update the plot once the needed result is received
    def update_plot(self, data):
        match self.current_function['graph_type']: # match/case to call the right plot function
            case 'lines':
                self.lines_plot(data)
    
    def lines_plot(self, data):
        # check if title is lambda function
        graph_title = self.check_if_lambda(self.current_function['graph_title'])
        self.label.configure(text=graph_title) # change title
        
        # check if filename is lambda function. Get the resulting name
        self.default_file_name = self.check_if_lambda(self.current_function['default_file_name'])
        
        # for a case if its multiple lines plot
        for coord_group in range(1, int(len(data)/2) + 1):
            # create first group
            x = data[0+2*(coord_group-1)]
            y = data[1+2*(coord_group-1)]
            
            self.ax.plot(x, y) # plot the line
            # write them into a string file_str
            file_str = ""
            for i in range(len(x)):
                file_str += str(x[i]) + '\t' + str(y[i]) + '\n'
            # add the resulting string to all export files
            self.export_files.append(file_str)
        # change axis titles
        self.ax.set_xlabel(self.current_function['axis_titles']['x_label'])
        self.ax.set_ylabel(self.current_function['axis_titles']['y_label'])
        # change axis scale if specified
        if self.current_function['scale'] is not None:
            scale_options = self.current_function['scale']
            self.ax.set_xscale(scale_options['x'])
            self.ax.set_yscale(scale_options['y'])
        # change axis limits if specified
        if self.current_function['lim'] is not None:
            lim_options = self.current_function['lim']
            self.ax.set_xlim(lim_options['x'])
            self.ax.set_ylim(lim_options['y'])
            
        self.graph.draw() # draw a figure
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH) # create a widget

    
    # # hitmap function. To be used
    # def heatmap_func(self):
    #     self.label.configure(text='Теплова карта')
    #     x = np.linspace(0, 10, 10)
    #     y = np.linspace(0, 10, 10)
        
    #     X, Y = np.meshgrid(x, y)
    #     Z = np.sin(X) * np.cos(Y)
        
    #     self.form_export(x=X, y=Y, z=Z)
        
    #     _, self.cbar = heatmap(X, Y, Z, ax=self.ax,
    #                cmap="YlGn", cbarlabel="heatmap example")
        
    #     self.graph.draw()
        
    #     self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)