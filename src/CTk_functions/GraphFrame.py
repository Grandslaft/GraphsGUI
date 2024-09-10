import tkinter as tk
import customtkinter

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import numpy as np

from ..functions import heatmap

import inspect

import multiprocessing

AWAIT_TIME = 100

matplotlib.use('TkAgg')

def run_in_thread(result_queue, func, kwargs):
    for output in func(**kwargs):
        result_queue.put(output)

class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = customtkinter.CTkLabel(self, text='СумДУ')
        self.label.pack()
        
        self.fig = Figure(dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.fig.set_constrained_layout(True)
        
        self.graph = FigureCanvasTkAgg(self.fig, master=self)
        toolbar = NavigationToolbar2Tk(self.graph, self, pack_toolbar=True)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM, fill='both')
        
        theta = np.linspace(0, 2 * np.pi, 100)
        x = 16 * ( np.sin(theta) ** 3 )
        y = 13 * np.cos(theta) - 5* np.cos(2*theta) - 2 * np.cos(3*theta) - np.cos(4*theta)
        
        self.ax.scatter(x,y)
        
        self.export_file = dict()
        
        self.result_queue = multiprocessing.Queue()
        
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
    
    def params_check(self):
        try:
            for key in self.current_function.get('required_params'):
                self.params.get(key)
        except NameError as e:
            self.master.values_textbox.delete("0.0", "end")
            self.master.values_textbox.insert("0.0", f"Немає значення параметру(ів): {e}")
    
    def plot(self, fun_num, **kwargs):
        self.current_function = self.master.functions[fun_num]
        
        self.params = kwargs
        thread = multiprocessing.Process(
            target=run_in_thread, 
            args=(
                self.result_queue, 
                self.current_function['function'], 
                kwargs,
            )
        )
        thread.start()
        
        self.master.after(AWAIT_TIME, self.check_result_queue)
    
    def update_plot(self, data):
        match self.current_function['graph_type']:
            case 'lines':
                self.lines_plot(data)
    
    def lines_plot(self, data):
        if callable(self.current_function['graph_title']):
            title_function = self.current_function['graph_title']
            title_params = list(inspect.signature(title_function).parameters)
            params_to_pass = {param_name: self.params[param_name] for param_name in title_params if param_name in self.params}
            self.label.configure(text=self.current_function['graph_title'](**params_to_pass))
        else:
            self.current_function['graph_title']
        
        self.params_check()
        
        for coord_group in range(1, int(len(data)/2) + 1):
            x = data[0+2*(coord_group-1)]
            y = data[1+2*(coord_group-1)]
            
            self.export_file[coord_group] = {
                'x': x,
                'y': y,
            }
            
            self.ax.plot(x, y)
        
        self.ax.set_xlabel(self.current_function['axis_titles']['x_label'])
        self.ax.set_ylabel(self.current_function['axis_titles']['y_label'])
        
        if self.current_function['scale'] is not None:
            scale_options = self.current_function['scale']
            self.ax.set_xscale(scale_options['x'])
            self.ax.set_yscale(scale_options['y'])
        
        if self.current_function['lim'] is not None:
            lim_options = self.current_function['lim']
            self.ax.set_xlim(lim_options['x'])
            self.ax.set_ylim(lim_options['y'])
        
        # if self.current_function['lim'] is not None:
        #     lim_options = self.current_function['lim']
        #     for lims in lim_options.items():
        #         if lims[-1][-1] == 'absolute':
        #             if lims[0] == 'x':
        #                 self.ax.set_xlim(lims[-1][0])
        #             elif lims[0] == 'y':
        #                 self.ax.set_ylim(lims[-1][0])
        #         elif lims[-1][-1] == 'relative':
        #             if lims[0] == 'x':
        #                 left, right = plt.xlim()
        #                 axis_range = right - left
        #                 rel_lims = set(value * axis_range for value in lims[-1][0])
        #                 self.ax.set_xlim(rel_lims)
        #             elif lims[0] == 'y':
        #                 left, right = plt.xlim()
        #                 axis_range = right - left
        #                 rel_lims = set(value * axis_range for value in lims[-1][0])
        #                 self.ax.set_ylim(rel_lims)

        self.graph.draw()
        
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)

    def check_result_queue(self):
        try:
            # Try to get the result from the queue
            data = self.result_queue.get_nowait()
            
            if data[-1] == 'progress':
                self.master.eval_progress_bar.set(data[0])
                self.master.after(AWAIT_TIME, self.check_result_queue)
            else:
                
                self.update_plot(data)
        except multiprocessing.queues.Empty:
            # If no result yet, keep checking
            self.master.after(AWAIT_TIME, self.check_result_queue)
        
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

    def clear_canvas(self):
        self.master.eval_progress_bar.set(0)
        self.ax.clear()
        
        if hasattr(self, 'cbar') and self.cbar is not None:
            try:
                self.cbar.remove()
            except Exception as e:
                print(f"Error removing colorbar: {e}")
            self.cbar = None
            
        self.graph.draw()
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)