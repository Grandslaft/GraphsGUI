import tkinter as tk
import customtkinter as ctk
import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure

import numpy as np

from ..functions.external_functions import (
    save_data_to_file,
    write_data_to_xyz_file,
    write_data_to_vtk_file,
)

import inspect

import multiprocessing
import src.global_parameters as gp

matplotlib.use("TkAgg")

AWAIT_TIME = 100


# function to run calculations in the external process
def run_in_process(result_queue, func, kwargs):
    for output in func(kwargs):
        result_queue.put(output)

def figure_draw(func):
    def wrapper(self, *args, **kwargs):
        # Extract necessary arguments
        subplot_ind = args[1]

        self.axs[subplot_ind].set_title(
            self.current_function["graph_titles"][subplot_ind]
        )

        # Execute the plotting function
        func(self, *args, **kwargs)

        # Change axis titles
        axis_titles = self.current_function["axis_titles"][subplot_ind]
        self.axs[subplot_ind].set_xlabel(axis_titles[0])
        self.axs[subplot_ind].set_ylabel(axis_titles[1])

        # Change axis scale
        axis_scales = self.current_function["scale"][subplot_ind]
        self.axs[subplot_ind].set_xscale(axis_scales[0])
        self.axs[subplot_ind].set_yscale(axis_scales[1])

        # Change axis limits if specified
        axis_lims = self.current_function["lim"][subplot_ind]
        self.axs[subplot_ind].set_xlim(axis_lims[0])
        self.axs[subplot_ind].set_ylim(axis_lims[1])

        # Draw the figure and update the widget
        self.graph.draw()  # Draw the figure
        # self.graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)  # Create a widget

    return wrapper


# custom toolbar for the graph on the base of NavigationToolbar2Tk
class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # delete unnecessary buttons
        self.children["!button3"].pack_forget()
        self.children["!button2"].pack_forget()
        self.children["!button5"].pack_forget()
        # depending on the light mode, change buttons' color
        if gp.SYSTEM_LIGHT_MODE == "Light":
            self.config(background="#eaecf0")
            for button in self.winfo_children():
                button.config(background="#eaecf0")
        else:
            self.config(background="#385091")
            for button in self.winfo_children():
                button.config(background="#385091")


# main class for the frame with graph on the base of ctk.CTkFrame
class GraphFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.process = None
        self.current_function = None

        # Change the graph style depending on whether the light or dark mode is active
        if gp.SYSTEM_LIGHT_MODE == "Light":
            plt.style.use(
                os.path.join(gp.CURRENT_DIR, "src", "styles", "pacoty.mplstyle")
            )
        else:
            plt.style.use(
                os.path.join(
                    gp.CURRENT_DIR, "src", "styles", "pitayasmoothie-dark.mplstyle"
                )
            )

        # create figure
        self.fig = Figure(dpi=100)
        self.gs = matplotlib.gridspec.GridSpec(
            1, 1, figure=self.fig, left=0.1, right=0.95, top=0.95, bottom=0.1
        )
        self.axs = []
        self.axs.append(self.fig.add_subplot(self.gs[0]))
        self.cbars = []

        # calculate coordinates
        theta = np.linspace(0, 2 * np.pi, 100)
        x = 16 * (np.sin(theta) ** 3)
        y = (
            13 * np.cos(theta)
            - 5 * np.cos(2 * theta)
            - 2 * np.cos(3 * theta)
            - np.cos(4 * theta)
        )

        self.axs[-1].plot(x, y)  # plot the graph

        # create widget for custom tkinter
        self.graph = FigureCanvasTkAgg(self.fig, master=self)
        # self.gs.constrained_layout(self.fig)
        self.graph.draw()
        self.graph.get_tk_widget().pack(
            side=tk.TOP,
            fill=tk.BOTH,
            padx=gp.INNER_PAD,
            pady=gp.INNER_PAD,
            expand=True,
        )
        # create toolbar
        self.toolbar = CustomToolbar(canvas=self.graph, window=self, pack_toolbar=True)
        self.toolbar.pack(
            side=tk.BOTTOM, fill="both", padx=gp.INNER_PAD, pady=(0, gp.INNER_PAD)
        )

        # create default vars
        self.default_file_name = None  # default name for the file
        self.result_queue = (
            multiprocessing.Queue()
        )  # A queue is used to store results from the process, as they could be lost otherwise

    # check if all required parameters are available
    def params_validation(self):
        try:
            for key in self.current_function["required_params"]:
                self.params.get(key)
        except NameError as e:
            self.master.show_error_message(f"Немає значення параметру(ів): {e}")

    # function to check whether function gave the results
    def check_result_queue(self):
        try:
            # Try to get the result from the queue
            data = self.result_queue.get_nowait()
            self.master.eval_progress_bar.set(data[0])  # update progress bar
            if data[2]:
                self.update_plots(data[1], data[2])
            self.master.after(AWAIT_TIME, self.check_result_queue)  # keep checking
            return
            # If we get the needed result, we update the plot.

        # If no result yet, keep checking
        except multiprocessing.queues.Empty:
            self.master.after(AWAIT_TIME, self.check_result_queue)

    # check if var is lambda
    def check_if_lambda(self, var):
        # since the var could be a lambda function that is customized based on parameters, we check if it is callable
        if callable(var):
            function = var  # get title function
            params = list(
                inspect.signature(function).parameters
            )  # get all needed parameters' names
            params_to_pass = {
                param_name: self.params[param_name]
                for param_name in params
                if param_name in self.params
            }  # get their values
            return function(**params_to_pass)  # return resulting value
        return var  # if not a function, return itself

    # canvas cleaner
    def clear_canvas(self):
        # clear color bars if there are any (for heatmaps)
        for cbar in self.cbars:
            if cbar:
                cbar.remove()
        self.cbars.clear()

        for ax in range(len(self.axs)):  # clear figure
            self.axs[ax].remove()
        self.axs.clear()
        # update figure
        self.graph.draw_idle()

    # plot function that is called from main.py
    def plot(self, fun_num, **kwargs):
        self.current_function = self.master.functions[fun_num]  # store called function
        self.params = kwargs  # store parameters
        self.params_validation()  # parameters validation, if there are all needed for current function
        # save num of rows and cols for subplots
        self.nrows, self.ncols = (
            self.current_function["graph_sublots"]["nrows"],
            self.current_function["graph_sublots"]["ncols"],
        )
        # subplots grid
        self.gs = matplotlib.gridspec.GridSpec(
            self.nrows,
            self.ncols,
            figure=self.fig,
            left=0.1,
            right=0.95,
            top=0.95,
            bottom=0.1,
            hspace=0.3,
            wspace=0.25,
        )
        # lists for plots and cbars
        self.axs = []
        self.cbars = []

        # end of calculation
        maxes = [value for key, value in self.params.items() if "max_" in key]
        self.end_iter = maxes[0] if len(maxes) > 0 else -100

        # export files every {specified value}
        write_interval = [
            value for key, value in self.params.items() if "write_every_" in key
        ]
        self.every_iter = write_interval[0] if len(maxes) > 0 else -1

        # flag which tells when to save files
        self.time_to_save = self.every_iter

        # add folder's name to save path
        folder_name = self.check_if_lambda(self.current_function["folder_name"])
        self.functions_save_path = os.path.join(self.master.save_path, folder_name)

        # create a process
        if self.process is None or not self.process.is_alive():
            self.process = multiprocessing.Process(
                target=run_in_process,
                args=(
                    self.result_queue,
                    self.current_function["function"],
                    kwargs,
                ),
            )
            self.process.start()  # start the process

            # After AWAIT_TIME milliseconds, check for any results using the self.check_result_queue function
            self.master.after(AWAIT_TIME, self.check_result_queue)

    # function to update the plot once the needed result is received
    def update_plots(self, iteration, data):
        self.clear_canvas()
        for subplot_ind in range(len(self.current_function["graph_titles"])):
            self.axs.append(
                self.fig.add_subplot(
                    self.gs[subplot_ind // self.ncols, subplot_ind % self.ncols]
                )
            )
            self.draw_plot(data[subplot_ind], subplot_ind)

        self.export_files(iteration, data)

    # Decorator on the plot function
    @figure_draw
    def draw_plot(self, data, subplot_ind):
        # plot logic
        match self.current_function["graph_types"][
            subplot_ind
        ]:  # match/case to call the right plot function
            case "lines":  # in case its a lines plot
                for coord_group in range(0, int(len(data) / 2)):
                    # Create first group
                    x = data[0 + 2 * coord_group]
                    y = data[1 + 2 * coord_group]
                    # Plot the line
                    self.axs[subplot_ind].plot(x, y)
            case "heatmap":  # in case it's a heatmap
                im_size = int(self.params["Size"])  # extract image size
                # plot a heatmap
                im = self.axs[subplot_ind].imshow(
                    data.reshape(im_size, im_size), cmap="coolwarm"
                )
                self.axs[subplot_ind].grid(False)
                # Create colorbar
                self.cbars.append(
                    self.axs[subplot_ind].figure.colorbar(
                        im, ax=self.axs[subplot_ind], cmap="coolwarm"
                    )
                )
                self.cbars[-1].formatter = matplotlib.ticker.FormatStrFormatter("%.2f")
                self.cbars[-1].update_ticks()
                # cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    def check_if_path_is_valid(self):
        # if path is valid, end program
        if os.path.isdir(self.functions_save_path):
            return
        # if not create a folder
        os.makedirs(self.functions_save_path)

    def export_files(self, iteration, data):
        if self.master.export_check.get():  # if the user requested an export
            self.check_if_path_is_valid()
            if (
                iteration >= 0 and iteration >= self.time_to_save
            ):  # and it's time to write
                # save all the heatmap plots positions
                heatmap_plots = [
                    (i, x)
                    for i, x in enumerate(self.axs)
                    if self.current_function["graph_types"][i] == "heatmap"
                ]
                for ind, ax in heatmap_plots:  # for all heatmaps
                    # update params for export files names
                    self.params["name_start"] = self.current_function["heatmap_prefix"][
                        ind
                    ]
                    self.params["time"] = int(iteration)
                    # create file name
                    file_name = self.check_if_lambda(
                        self.current_function["default_file_name"]
                    )
                    # complete save path
                    save_path = os.path.join(self.functions_save_path, file_name)
                    if self.master.files_to_save["png"]:  # if save plot is requested
                        extent = ax.get_tightbbox(self.fig.canvas.renderer).transformed(
                            self.fig.dpi_scale_trans.inverted()
                        )
                        # Expand the width by 1.1 times and keep the height the same
                        expanded_extent = extent.expanded(1.25, 1)
                        # Translate the bounding box to the right by half of the additional width
                        translated_extent = expanded_extent.translated(
                            extent.width * 0.5 * (1.25 - 1), 0
                        )
                        self.fig.savefig(
                            f"{save_path}.png", bbox_inches=translated_extent
                        )
                    if self.master.files_to_save[
                        "xyz"
                    ]:  # if save plot data in xyz is requested
                        write_data_to_xyz_file(
                            f"{save_path}.xyz", data[ind], self.params["Size"]
                        )
                    if self.master.files_to_save[
                        "vtk"
                    ]:  # if save plot data in vtk is requested
                        write_data_to_vtk_file(
                            f"{save_path}.vtk", data[ind], self.params["Size"]
                        )
                self.time_to_save += self.every_iter

            if iteration == self.end_iter:  # if its the end of calculations
                self.params["name_start"] = "" if self.end_iter == -100 else "Prec"
                file_name = self.check_if_lambda(
                    self.current_function["default_file_name"]
                )
                save_path = os.path.join(self.functions_save_path, file_name)
                save_data_to_file(
                    f"{save_path}.dat",
                    data,
                    self.current_function["dat_data"],
                    self.current_function["dat_cols"],
                )
                os.startfile(self.master.save_path)
