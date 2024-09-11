import tkinter as tk
import customtkinter

import matplotlib

import multiprocessing

import matplotlib.pylab
import matplotlib.pyplot
import matplotlib.style

from src.CTk_functions import ExportWindow, GraphFrame
from src.functions.physics_graphs import FeCr_phase_graph, FeCrAl_phase_graph
from src.functions.external_functions import wrap_text
import src.global_parameters as gp

import os
from PIL import Image

matplotlib.use('TkAgg')

gp.CURRENT_DIR = os.path.dirname(__file__)

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
gp.Light_mode('System')
customtkinter.set_default_color_theme(os.path.join(gp.CURRENT_DIR, 'src', 'styles', 'theme.json'))

'''
Explained Parameters of the Functions Dictionary Needed for Adding New Graphs to the GUI

button_name: The name displayed on the button that triggers the function.

params_explanation: A brief explanation of the parameters required for the function.

graph_title: The title of the graph, which can be either a text string or a lambda function that generates the title based on the input parameters.

graph_type: The type of graph to be generated (e.g., “lines”).

required_params: A dictionary of parameters required by the function, with default values.

axis_titles: Titles for the x and y axes of the graph.

scale: A dictionary specifying the scale of the axes (e.g., 'linear', 'log').

lim: A dictionary specifying the limits for the x and y axes.

function: The function to be called to generate the graph.

default_file_name: The default name for the files to be saved, which can be either a text string or a lambda function that generates the name based on the input parameters.
'''
functions = [
    dict(
        button_name = "Фазова діаграма для сплаву Fe-Cr-Al у рівноважних умовах",
        params_explanation = "Введіть параметр xAl (від 0 до 0.2)",
        graph_title = lambda xAl: "Фазова діаграма для сплаву Fe-Cr" if xAl < 1E-5 else f"Фазова діаграма для сплаву Fe-Cr-{xAl*100}Al",
        graph_type = "lines",
        required_params = dict(
            xAl = 0.0,
        ),
        axis_titles = {
            "x_label": "xCr [%]", 
            "y_label": "T [K]"
        },
        scale = None,
        lim = dict(
            x=(gp.INNER_PAD, 90),
            y=None
        ),
        function = FeCr_phase_graph,
        default_file_name = lambda xAl: "T(xCr)_Al" if xAl < 1E-5 else f"T(xCr)_Al{xAl*100}%"
    ),
    dict(
        button_name = "Фазова діаграма для опроміненого сплаву Fe-Cr-Al",
        params_explanation = "Введіть параметри xCr, xAl (від 0 до 0.2), N (Натуральне число), r0 (Натуральне число)",
        graph_title = lambda xCr, xAl: f"Фазова діаграма для сплаву Fe-{xCr*100}%Cr-{xAl*100}%Al",
        graph_type = "lines",
        required_params = dict(
            xCr = 0.3,
            xAl = 0.05,
            N = 30,
            r0 = 4,
        ),
        axis_titles = {
            "x_label": "T [K]", 
            "y_label": "K [dpa/sec]"
        },
        scale = dict(
            x = 'linear',
            y = 'log'
        ),
        lim = dict(
            x=None,
            y=(1E-8, 1E-4)
        ),
        function = FeCrAl_phase_graph,
        default_file_name = lambda xCr, xAl, N, r0: f"K(T)_Cr{xCr*100}%Al{xAl*100}%_N{N}_r0{r0}"
    ),
]

# main window of the GUI created using custom Tkinter
class App(customtkinter.CTk):
    def __init__(self, functions):
        super().__init__()
        
        self.functions = functions

        # configure window
        self.title("Графіки")
        self.geometry(f"{1280}x{720}")
        

        # configure grid layout (3x3)
        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # sidebar frame for buttons and window customization
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(
            row=0, column=0, 
            rowspan=3, 
            sticky="nsew"
        )
        self.sidebar_frame.grid_rowconfigure((2), weight=1)
        
        image_path = os.path.join(gp.CURRENT_DIR, 'src', 'images', 'sumdu_logo_v2.png')
        
        # SumDU logo
        self.logo = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text='Сумський\nДержавний\nУніверситет',
            font=customtkinter.CTkFont(
                size=14, weight="bold"
            ),
            image=customtkinter.CTkImage(
                Image.open(image_path), 
                size=(50, 50)
            ),
            anchor='center',
            justify='left',
            compound='left',
            padx=gp.OUTER_PAD,
        )
        self.logo.grid(
            row=0, column=0, pady=(gp.OUTER_PAD, gp.INNER_PAD),
            sticky="ew"
        )
        
        # title of the frame
        self.sidebar_buttons_title = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text='Оберіть функцію',
            font=customtkinter.CTkFont(
                size=16,
            ),
            anchor='center',
            justify='left',
        )
        self.sidebar_buttons_title.grid(
            row=1, column=0, 
            pady=(0, 0),
            sticky="ew"
        )
        
        # functions' buttons frame
        self.sidebar_buttons_frame = customtkinter.CTkScrollableFrame(
            self.sidebar_frame, 
            fg_color=["#e6e7ed", "#1a1b26"],
            corner_radius=gp.CORNER_RADIUS,
        )
        self.sidebar_buttons_frame.grid(
            row=2, column=0, 
            padx=gp.OUTER_PAD, 
            pady=(gp.INNER_PAD, 50),
            sticky="nsew"
        )
        self.sidebar_buttons_frame.grid_columnconfigure(0, weight=1)
        
        # buttons generator
        self.sidebar_button = dict()
        for num, graph in enumerate(functions):
            button_text, new_line_count = wrap_text(graph['button_name'], 20)
            self.sidebar_button[graph['button_name']] = customtkinter.CTkButton(
                self.sidebar_buttons_frame, 
                text=button_text,
                height=28*new_line_count,
                corner_radius=gp.CORNER_RADIUS,
                command=lambda g=graph, fun_num=num: self.function_call(graph=g, function_number=fun_num)
            )
            self.sidebar_button[graph['button_name']].grid(
                row=num+1, column=0, 
                padx=gp.ELEMENTS_PAD, 
                pady=gp.INNER_PAD, 
                sticky='ew'
            )
            
        # light theme of the GUI
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Тема застосунку:", anchor="w")
        self.appearance_mode_label.grid(
            row=3, column=0, 
            padx=gp.OUTER_PAD, 
            pady=(gp.INNER_PAD, 0), 
            sticky='ew'
        )
        
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Системна", "Світла", "Темна"],
            corner_radius=gp.CORNER_RADIUS,
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(
            row=4, column=0, 
            padx=gp.OUTER_PAD, 
            pady=(gp.INNER_PAD, gp.INNER_PAD),
            sticky='ew'
        )
        
        # Scaling options
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text="Масштабування інтерфейсу:", 
            corner_radius=gp.CORNER_RADIUS,
            anchor="w"
        )
        self.scaling_label.grid(
            row=5, column=0, 
            padx=gp.OUTER_PAD, 
            pady=(gp.INNER_PAD, 0),
            sticky='ew'
        )
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, 
            values=["80%", "90%", "100%", "110%", "120%"],
            corner_radius=gp.CORNER_RADIUS,
            command=self.change_scaling_event
        )
        self.scaling_optionemenu.grid(
            row=gp.ELEMENTS_PAD, column=0, 
            padx=gp.OUTER_PAD, 
            pady=(gp.INNER_PAD, gp.OUTER_PAD),
            sticky='ew'
        )
        
        # Label for parameters' explanation      
        self.param_expl_box = customtkinter.CTkLabel(
            self,
            width=300,
            height=200,
            wraplength=300,
            fg_color= ["#d6d8df", "#1a1b26"],
            anchor='nw',
            justify='left',
            padx=gp.ELEMENTS_PAD, 
            pady=gp.INNER_PAD,
            corner_radius=gp.CORNER_RADIUS,
        )
        
        self.param_expl_box.grid(
            row=0, column=1,
            padx=(gp.OUTER_PAD, 0), 
            pady=(gp.OUTER_PAD, 0),
            sticky="nsew"
        )
        
        # frame for parameters' inputs
        self.input_frame = customtkinter.CTkFrame(
            self, 
            fg_color=["#d6d8df", "#1a1b26"],
            corner_radius=gp.CORNER_RADIUS)
        self.input_frame.grid(
            row=1, column=1, 
            padx=(gp.OUTER_PAD, 0), 
            pady=(gp.OUTER_PAD, 0), 
            sticky="nsew"
        )

        # update and export buttons
        self.function_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.function_buttons_frame.grid(
            row=2, column=1, 
            padx=(gp.OUTER_PAD, 0), 
            pady=(gp.OUTER_PAD, gp.OUTER_PAD), 
            sticky="nsew"
        )
        self.update_button = customtkinter.CTkButton(
            master=self.function_buttons_frame, 
            text='Оновити', fg_color="transparent", 
            border_width=2, text_color=("gray10", "#DCE4EE"), 
            corner_radius=gp.CORNER_RADIUS,
            command=self.update_figure
        )
        self.update_button.grid(
            row=0, column=0, 
            padx=(0, gp.OUTER_PAD), 
            sticky="ew"
        )
        
        self.export = customtkinter.CTkButton(
            master=self.function_buttons_frame, 
            text='Експортувати', fg_color="transparent", 
            border_width=2, text_color=("gray10", "#DCE4EE"), 
            corner_radius=gp.CORNER_RADIUS,
            command=self.export_files
        )
        self.export.grid(row=0, column=1, sticky="ew")
        
        self.export_window = None
        
        # Graph Frame
        self.graph_frame = GraphFrame(
            self, 
            fg_color=["#d6d8df", "#1a1b26"],
            corner_radius=gp.CORNER_RADIUS
        )
        self.graph_frame.grid(
            row=0, column=2, 
            padx=gp.OUTER_PAD, 
            pady=(gp.OUTER_PAD, 0), 
            sticky="nsew", rowspan=2
        )
        
        # Progress Bar for calculations
        self.eval_progress_bar = customtkinter.CTkProgressBar(
            self, 
            mode='determinate', 
            height=20, 
            corner_radius=gp.CORNER_RADIUS,
        )
        self.eval_progress_bar.set(0)
        self.eval_progress_bar.grid(
            row=2, column=2, 
            padx=gp.OUTER_PAD, 
            pady=gp.OUTER_PAD, 
            sticky="ew"
        )
        
        # default values
        self.appearance_mode_optionemenu.set("Системна")
        self.scaling_optionemenu.set("100%")
        self.param_expl_box.configure(text="Оберіть граф, щоб з'явилися поля вводу")

    # Appearance changer
    def change_appearance_mode_event(self, new_appearance_mode: str):
        
        theme_map = {           # dict to translate parameters
            "Світла": "Light",
            "Темна": "Dark",
            "Системна": "System"
        }
        customtkinter.set_appearance_mode(theme_map[new_appearance_mode]) # change appearance in custom_tkinter
        
        gp.Light_mode(theme_map[new_appearance_mode]) # change global parameter to change others' appearance
        # Reset Graph Frame
        matplotlib.pyplot.close(self.graph_frame.fig)
        self.graph_frame = GraphFrame(
            self, 
            fg_color=["#d6d8df", "#1a1b26"],
            corner_radius=gp.CORNER_RADIUS
        )
        self.graph_frame.grid(
            row=0, column=2, 
            padx=gp.OUTER_PAD, 
            pady=(gp.OUTER_PAD, 0), 
            sticky="nsew", rowspan=2
        )

    # Window's scale changer
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    # generator for input boxes as they are not limited
    def render_input_boxes(self, input_boxes={}): 
        self.destroy_input_boxes() # destroy previous input boxes
        if len(input_boxes) == 0: # If there are no parameters in the function, we just plot the graph
            self.inputs = dict()
            self.graph_frame.plot(self.flag)
            return
        # if there are parameters
        self.inputs = dict() # create var to store input boxes
        input_labels = list(input_boxes.keys()) # save parameters' names
        for inp_num in range(len(input_boxes)): # for each parameter
            # create label with its name
            customtkinter.CTkLabel(
                self.input_frame, 
                text=f"{input_labels[inp_num]}:", 
                font=customtkinter.CTkFont(
                    size=14, weight="bold"
                )
            ).grid(
                row=inp_num, column=0, 
                padx=gp.INNER_PAD, 
                pady=(gp.INNER_PAD, 0), 
                sticky="w"
            )
            # and create input form
            self.inputs[input_labels[inp_num]] = customtkinter.CTkEntry(
                self.input_frame, 
                placeholder_text=input_boxes[input_labels[inp_num]]
            )
            self.inputs[input_labels[inp_num]].grid(
                row=inp_num, column=1, 
                padx=(0, gp.INNER_PAD), 
                pady=(gp.INNER_PAD, 0), 
                sticky="nsew"
            )
            
    # function that destroys input boxes
    def destroy_input_boxes(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
    
    # handler for the button click, which calls 
    def function_call(self, graph, function_number):
        self.flag = function_number # flag to know what function's been called
        self.param_expl_box.configure(text=graph["params_explanation"]) # change a content of the label, that explains parameters
        self.graph_frame.label.configure(text=graph["button_name"]) # change title of the figure to the default(button's) name
        self.graph_frame.clear_canvas() # clear figure canvas
        self.render_input_boxes(graph["required_params"]) # render input boxes
    
    # action on the click of 'update' button
    def update_figure(self):
        self.graph_frame.clear_canvas() # clear figure canvas
        # if there're parameters, we plot a figure
        if len(self.functions[self.flag]['required_params']) == 0:
            self.graph_frame.plot(self.flag)
        # If no, we check if all value are numbers. If so, we plot a figure with its parameters
        try:
            params = dict()
            for key, value in self.inputs.items():
                params[key] = float(value.get())
            self.graph_frame.plot(self.flag, **params)                
        except ValueError as e:
            self.param_expl_box.configure(text=f"Невірне значення параметру {e}")
            
    # export window caller
    def export_files(self):
        # if there's no export window, we create one
        if self.export_window is None or not self.export_window.winfo_exists():
            self.toplevel_window = ExportWindow(self)
        self.toplevel_window.focus()  # if window exists focus it

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = App(functions=functions)
    app.mainloop()