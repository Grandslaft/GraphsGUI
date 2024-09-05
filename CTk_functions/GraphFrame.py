import tkinter as tk
import customtkinter

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import numpy as np

from ..functions import heatmap

matplotlib.use('TkAgg')

class GraphFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = customtkinter.CTkLabel(self, text='SumDU')
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
        
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
    
    def params_check(self, params):
        try:
            for key in self.current_function.get('required_params'):
                params.get(key)
        except NameError as e:
            self.master.values_textbox.delete("0.0", "end")
            self.master.values_textbox.insert("0.0", f"Немає значення параметру(ів): {e}")
    
    def plot(self, fun_num, **kwargs):
        self.current_function = self.master.functions[fun_num]
        match self.current_function.get('graph_type'):
            case 'lines':
                self.lines_plot(kwargs)
    
    def lines_plot(self, kwargs):
        self.label.configure(text=self.current_function.get('graph_title')(**kwargs) if callable(self.current_function.get('graph_title')) else self.current_function.get('graph_title'))
        
        self.params_check(kwargs)

        self.master.eval_progress_bar.start()
        x, y = self.current_function.get('function')(**kwargs)
        self.master.eval_progress_bar.stop()
        
        self.form_export(x=x, y=y)
        
        self.ax.plot(x,y)
        
        self.ax.set_xlabel(self.current_function.get('axis_titles')['x_label'])
        self.ax.set_ylabel(self.current_function.get('axis_titles')['y_label'])

        self.graph.draw()
        
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
        
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
        self.ax.clear()
        
        if hasattr(self, 'cbar') and self.cbar is not None:
            try:
                self.cbar.remove()
            except Exception as e:
                print(f"Error removing colorbar: {e}")
            self.cbar = None
            
        self.graph.draw()
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
            
    def form_export(self, **kwargs):
        self.export_file = kwargs