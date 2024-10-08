import tkinter as tk
import customtkinter as ctk

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

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
gp.Light_mode('System')
ctk.set_default_color_theme(os.path.join(gp.CURRENT_DIR, 'src', 'styles', 'theme.json'))

'''
Explained Parameters of the Functions Dictionary Needed for Adding New Graphs to the GUI

button_name: The label displayed on the button and used as the Graph Widget's title.

params_explanation: A brief explanation of the required parameters for the function.

graph_sublots: Defines the layout of subplots (rows and columns).

graph_titles: A list of titles for individual graphs, either static or dynamically generated.

graph_types: Specifies the type of graph (e.g., lines, heatmap).

required_params: A dictionary of required parameters with default values.

axis_titles: Titles for the x and y axes of the graphs.

scale: Defines the scale for both x and y axes (e.g., linear, log).

lim: Specifies axis limits; None if no specific limit is required.

function: The function that generates the graph.

name_start: The prefix for saving heatmap plot data.

prec_col_name: The prefix for saving precipitate-related data.

folder_name: Defines the folder name for saving files, static or dynamically generated.

default_file_name: The default file name for saving output, static or dynamically generated.
'''

functions = [
    dict(
        button_name = "Фазова діаграма для сплаву Fe-Cr-Al у рівноважних умовах",
        params_explanation = "Введіть параметр xAl (від 0 до 0.2)",
        graph_sublots=dict(
            nrows=2,
            ncols=2
        ),
        graph_titles = [
            'Просторовий розподіл Хрому', 
            'Просторовий розподіл Алюмінію', 
            'Еволюція середнього розміру преципітатів Хрому', 
            'Еволюція густини преципітатів Хрому'
        ],
        graph_types = [
            'heatmap',
            'heatmap',
            'lines',
            'lines'
        ],
        required_params = dict(
            Cr0 = 0.3,
            Al0 = 0.05,
            T = 710,
            max_t = 1000,
            write_every_t = 200,
            Size = 64,
        ),
        axis_titles = [
            [None, None],
            [None, None],
            ['Time [hours]', '<Rp> [nm]'],
            ['Time [hours]', 'N x 10^(-27) [m^-3]']
        ],
        scale = [
            ['linear', 'linear'],
            ['linear', 'linear'],
            ['log', 'log'],
            ['log', 'log'],
        ],
        lim = [
            [None, None],
            [None, None],
            [None, None],
            [None, None],
        ],
        function = FeCr_phase_graph,
        name_start = [
            'Cr(r)',
            'Al(r)'
        ],
        prec_col_name = 'Time [hours]',
        folder_name = lambda Size, Cr0, Al0, T: f"M{int(Size)}_Cr{int(Cr0)*100}%Al{int(Al0)*100}%_T{int(T)}",
        default_file_name = lambda name_start, Size, time, Cr0, Al0, T: f"{name_start}{int(Size)}_t{int(time)}_Cr{int(Cr0)*100}%Al{int(Al0)*100}%_T{int(T)}",
    ),
    dict(
        button_name = "Фазова діаграма для опроміненого сплаву Fe-Cr-Al",
        params_explanation = "Введіть параметри xCr, xAl (від 0 до 0.2), N (Натуральне число), r0 (Натуральне число)",
        graph_sublots=dict(
            nrows=2,
            ncols=2
        ),
        graph_titles = [
            'Просторовий розподіл Хрому', 
            'Просторовий розподіл Алюмінію', 
            'Еволюція середнього розміру преципітатів Хрому', 
            'Еволюція густини преципітатів Хрому'
        ],
        graph_types = [
            'heatmap',
            'heatmap',
            'lines',
            'lines'
        ],
        required_params = dict(
            Cr0 = 0.3,
            Al0 = 0.05,
            T = 710,
            K = 1E-6,
            N = 30,
            r0 = 1,
            max_dose = 6,
            write_every_dose = 1,
            Size = 64,
        ),
        axis_titles = [
            [None, None],
            [None, None],
            ['Dose [dpa]', '<Rp> [nm]'],
            ['Dose [dpa]', 'N x 10^(-27) [m^-3]']
        ],
        scale = [
            ['linear', 'linear'],
            ['linear', 'linear'],
            ['log', 'log'],
            ['log', 'log'],
        ],
        lim = [
            [None, None],
            [None, None],
            [None, None],
            [None, None],
        ],
        function = FeCrAl_phase_graph,
        name_start = [
            'Cr(r)',
            'Al(r)'
        ],
        precipitates_prefix = 'Dose [dpa]',
        folder_name = lambda Size, Cr0, Al0, T, K, N, r0: f"M{int(Size)}_Cr{int(Cr0)*100}%Al{int(Al0)*100}%_T{int(T)}_K{int(K)*1e6}E-6_N{int(N)}_r0{int(r0)}",
        default_file_name = lambda name_start, Size, time, Cr0, Al0, T, K, N, r0: f"{name_start}{int(Size)}_t{int(time)}_Cr{int(Cr0)*100}%Al{int(Al0)*100}%_T{int(T)}_K{int(K)*1e6}E-6_N{int(N)}_r0{int(r0)}",
    ),
]

# main window of the GUI created using custom Tkinter
class App(ctk.CTk):
    def __init__(self, functions):
        super().__init__()
        
        self.functions = functions
        self.save_path = ''
        
        # configure window
        self.title("Графіки")
        self.geometry(f"{1500}x{800}")
        self.minsize(1500, 800)
        
        # configure grid layout (3x3)
        self.grid_columnconfigure((0,1), weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # sidebar frame for buttons and window customization
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(
            row=0, column=0, 
            rowspan=4, 
            sticky="nsew"
        )
        self.sidebar_frame.grid_rowconfigure((2), weight=1)
        
        image_path = os.path.join(gp.CURRENT_DIR, 'src', 'images', 'sumdu_logo_v2.png')
        
        # SumDU logo
        self.logo = ctk.CTkLabel(
            self.sidebar_frame, 
            text='Сумський\nДержавний\nУніверситет',
            font=ctk.CTkFont(
                size=14, weight="bold"
            ),
            image=ctk.CTkImage(
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
        self.sidebar_buttons_title = ctk.CTkLabel(
            self.sidebar_frame, 
            text='Оберіть функцію',
            font=ctk.CTkFont(
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
        self.sidebar_buttons_frame = ctk.CTkScrollableFrame(
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
            button_text, new_line_count = wrap_text(graph['button_name'], 160, ctk.CTkButton(self))
            self.sidebar_button[graph['button_name']] = ctk.CTkButton(
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
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Тема застосунку:", anchor="w")
        self.appearance_mode_label.grid(
            row=3, column=0, 
            padx=gp.OUTER_PAD, 
            pady=(gp.INNER_PAD, 0), 
            sticky='ew'
        )
        
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Системна", "Світла", "Темна"],
            corner_radius=gp.CORNER_RADIUS,
            dropdown_fg_color=["#e6e7ed", "#1a1b26"],
            dropdown_hover_color=["#325882", "#324578"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(
            row=4, column=0, 
            padx=gp.OUTER_PAD, 
            pady=(gp.INNER_PAD, gp.INNER_PAD),
            sticky='ew'
        )
        
        # Scaling options
        self.scaling_label = ctk.CTkLabel(
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
        self.scaling_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["80%", "90%", "100%", "110%", "120%"],
            corner_radius=gp.CORNER_RADIUS,
            command=self.change_scaling_event
        )
        self.scaling_optionemenu.grid(
            row=6, column=0, 
            padx=gp.OUTER_PAD, 
            pady=(gp.INNER_PAD, gp.OUTER_PAD),
            sticky='ew'
        )
        
        # Label for parameters' explanation  
        # A StringVar to track the label's text
        self.param_expl_text = ctk.StringVar() 
        self.param_expl_box = ctk.CTkLabel(
            self,
            textvariable=self.param_expl_text,
            height=100,
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
        self.input_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color=["#d6d8df", "#1a1b26"],
            corner_radius=gp.CORNER_RADIUS
        )
        self.input_frame.grid(
            row=1, column=1, 
            padx=(gp.OUTER_PAD, 0), 
            pady=(gp.OUTER_PAD, 0), 
            sticky="nsew"
        )
        self.input_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.export_check = ctk.CTkCheckBox(
            self, text="Експортувати Файли", 
            command=self.if_export_clicked,
            onvalue=True, offvalue=False  # Set onvalue to True and offvalue to False
        )
        self.export_check.grid(
            row=2, column=1, 
            padx=(gp.OUTER_PAD, 0), 
            pady=(gp.OUTER_PAD, 0), 
            sticky="nsew"
        )

        # update and export buttons
        self.function_buttons_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.function_buttons_frame.grid(
            row=3, column=1, 
            padx=(gp.OUTER_PAD, 0), 
            pady=(gp.OUTER_PAD, gp.OUTER_PAD), 
            sticky="nsew"
        )
        self.function_buttons_frame.grid_columnconfigure((0, 1), weight=1)
        self.function_buttons_frame.grid_rowconfigure(0, weight=1)
        
        self.update_button = ctk.CTkButton(
            master=self.function_buttons_frame, 
            text='Оновити',
            corner_radius=gp.CORNER_RADIUS,
            command=self.update_figure
        )
        self.update_button.grid(
            row=0, column=0, 
            padx=(0, gp.INNER_PAD), 
            sticky="nsew"
        )
        
        self.export_button = ctk.CTkButton(
            master=self.function_buttons_frame, 
            text='Експортувати',
            corner_radius=gp.CORNER_RADIUS,
            state='normal' if self.export_check.get() else 'disabled',
            command=self.open_export_config
        )
        #TODO implement import mechanic
        self.export_button.grid(row=0, column=1, sticky="nsew")
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
            sticky="nsew", rowspan=3
        )
        
        # Progress Bar for calculations
        self.eval_progress_bar = ctk.CTkProgressBar(
            self, 
            mode='determinate', 
            height=20, 
            corner_radius=gp.CORNER_RADIUS,
        )
        self.eval_progress_bar.set(0)
        self.eval_progress_bar.grid(
            row=3, column=2, 
            padx=gp.OUTER_PAD, 
            pady=gp.OUTER_PAD, 
            sticky="ew"
        )
        
        # default values
        self.appearance_mode_optionemenu.set("Системна")
        self.scaling_optionemenu.set("100%")
        self.label_text_change("Оберіть граф, щоб з'явилися поля вводу") 

    # Appearance changer
    def change_appearance_mode_event(self, new_appearance_mode: str):
        theme_map = {  # dict to translate parameters
            "Світла": "Light",
            "Темна": "Dark",
            "Системна": "System"
        }
        ctk.set_appearance_mode(theme_map[new_appearance_mode]) # change appearance in custom_tkinter
        
        gp.Light_mode(theme_map[new_appearance_mode]) # change global parameter to change others' appearance
        # Reset Graph Frame
        matplotlib.pyplot.close(self.graph_frame.fig)
        self.graph_frame.toolbar.destroy()
        self.graph_frame = GraphFrame(
            self, 
            fg_color=["#d6d8df", "#1a1b26"],
            corner_radius=gp.CORNER_RADIUS
        )
        self.graph_frame.grid(
            row=0, column=2, 
            padx=gp.OUTER_PAD, 
            pady=(gp.OUTER_PAD, 0), 
            sticky="nsew", rowspan=3
        )
        
    # Window's scale changer
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
    
    # generator for input boxes as they are not limited
    def render_input_boxes(self, input_boxes={}): 
        self.destroy_input_boxes() # destroy previous input boxes
        # If there are no parameters in the function, we just plot the graph
        if len(input_boxes) == 0: 
            self.inputs = dict()
            self.graph_frame.plot(self.flag)
            return
        # if there are parameters
        self.inputs = dict() # create var to store input boxes
        input_labels = list(input_boxes.keys()) # save parameters' names
        for inp_num in range(len(input_boxes)): # for each parameter
            # create label with its name
            ctk.CTkLabel(
                self.input_frame, 
                text=f"{input_labels[inp_num]}:", 
                font=ctk.CTkFont(
                    size=14, weight="bold"
                )
            ).grid(
                row=inp_num, column=0, 
                padx=gp.INNER_PAD, 
                pady=(gp.INNER_PAD, 0), 
                sticky="w"
            )
            # and create input form
            self.inputs[input_labels[inp_num]] = ctk.CTkEntry(
                self.input_frame, 
                placeholder_text=input_boxes[input_labels[inp_num]]
            )
            self.inputs[input_labels[inp_num]].grid(
                row=inp_num, column=1, 
                padx=(0, gp.INNER_PAD*2), 
                pady=(gp.INNER_PAD, 0), 
                sticky="nsew"
            )
    
    # function that destroys input boxes
    def destroy_input_boxes(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
    
    # if export button check is clicked
    def if_export_clicked(self):
        if self.export_check.get(): # is export checkbox is checked (requested)
            self.export_button.configure(state='normal') # make export button clickable
            return
        # if it was unchecked, make it unclickable
        self.export_button.configure(state='disabled')

    # handler for the button click, which calls 
    def function_call(self, graph, function_number):
        self.flag = function_number # flag to know what function's been called
        # kill the ongoing calculation process, if it exists
        if hasattr(self.graph_frame, 'process'): 
            self.graph_frame.process.kill()
            del self.graph_frame.process
        self.graph_frame.clear_canvas() # clear figure canvas
        self.label_text_change(graph["params_explanation"])
        # self.param_expl_box.configure(text=graph["params_explanation"]) # change a content of the label, that explains parameters
        self.graph_frame.label.configure(text=graph["button_name"]) # change title of the figure to the default(button's) name
        self.eval_progress_bar.set(0) # set progress bar to 0
        self.render_input_boxes(graph["required_params"]) # render input boxes
        
    # action on the click of 'update' button
    def update_figure(self):
        # if user requester export, but save path isn't specified
        if self.export_check.get() and self.save_path == '':
            # raise error
            self.label_text_change('Налаштуйте експорт')
            self.param_expl_box.configure(
                text_color="red"
            )
            return
        
        # kill the ongoing calculation process, if it exists
        if hasattr(self.graph_frame, 'process'): 
            self.graph_frame.process.kill()
            del self.graph_frame.process
        
        self.graph_frame.clear_canvas() # clear figure canvas
        # return basic text for the selected function
        self.label_text_change(self.functions[self.flag]["params_explanation"]) 
        if len(self.functions[self.flag]['required_params']) == 0:
            self.graph_frame.plot(self.flag) # if there're no parameters, we plot a figure
        
        # If no, we check if all values are numbers. If so, we plot a figure with its parameters
        try:
            params = dict()
            for key, value in self.inputs.items():
                param_value = value.get() # get parameter's value
                if param_value == '': # if empty aka user didn't specified 
                    param_value = value._placeholder_text # get standart value from the placeholder of entry
                params[key] = float(param_value) # transform to float
            self.graph_frame.plot(self.flag, **params)                
        except ValueError as e: # if value cannont be transformed into float, raise an error
            self.label_text_change(f"Невірне значення параметру {e}")
            self.param_expl_box.configure(
                # text=f"Невірне значення параметру {e}",
                text_color="red"
            )
            
    # export window caller
    def open_export_config(self):
        # if there's no export window, we create one
        if self.export_window is None or not self.export_window.winfo_exists():
            self.export_window = ExportWindow(self)
            
        self.export_window.focus()  # if window exists focus it
    
    # save export configuration
    def get_export_params(self):
        # get save path
        self.save_path = self.export_window.path_text_box.get("1.0", "end-1c")
        # get flags for what files to save
        self.files_to_save = dict(
            png = self.export_window.graph_export.get(),
            xyz = self.export_window.file_export_xyz.get(),
            vtk = self.export_window.file_export_vtk.get(),
        )
        # close export window
        self.export_window.destroy()
    
    # function to change label's text with prior text wrapping
    def label_text_change(self, new_text):
        expl_box_width = self.param_expl_box.winfo_width()
        wrapped_text, _ = wrap_text(
            text=new_text, 
            wraplength_px=expl_box_width - 2 * gp.ELEMENTS_PAD if expl_box_width > 50 else 300, 
            obj=self.param_expl_box
        )
        self.param_expl_text.set(wrapped_text)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = App(functions=functions)
    app.mainloop()