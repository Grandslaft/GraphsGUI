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
    
    def plot(self, graph_type, **kwargs):
        match graph_type:
            case 'graph 1':
                self.graph_1()
            case 'graph 2':
                self.sin_func()
            case 'graph 3':
                self.cos_func(kwargs)
            case 'graph 4':
                self.heatmap_func() 

    def graph_1(self):
        self.label.configure(text='Графік Серця')
        
        theta = np.linspace(0, 2 * np.pi, 100)
        x = 16 * ( np.sin(theta) ** 3 )
        y = 13 * np.cos(theta) - 5* np.cos(2*theta) - 2 * np.cos(3*theta) - np.cos(4*theta)
        
        self.form_export(x=x, y=y)
        
        self.ax.scatter(x,y)

        self.graph.draw()
        
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
        
    def sin_func(self):
        self.label.configure(text='Графік Сінуса')
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        
        self.form_export(x=x, y=y)
        
        self.ax.scatter(x, y)
        
        self.graph.draw()
        
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
    
    def cos_func(self, params):
        self.label.configure(text='Графік Косінуса з параметром a')
        needed_params = ['a_param']
        try:
            for key in needed_params:
                params.get(key)
        except NameError as e:
            self.master.values_textbox.delete("0.0", "end")
            self.master.values_textbox.insert("0.0", f"Немає значення параметру(ів): {e}")
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.cos(params.get('a_param')*x)
        
        self.form_export(x=x, y=y)

        self.ax.scatter(x, y)
        
        self.graph.draw()
        
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
        
    def heatmap_func(self):
        self.label.configure(text='Теплова карта')
        x = np.linspace(0, 10, 10)
        y = np.linspace(0, 10, 10)
        
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)
        
        self.form_export(x=X, y=Y, z=Z)
        
        _, self.cbar = heatmap(X, Y, Z, ax=self.ax,
                   cmap="YlGn", cbarlabel="heatmap example")
        
        self.graph.draw()
        
        self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)

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