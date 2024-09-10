import tkinter as tk
import customtkinter

import matplotlib

import multiprocessing

from src.CTk_functions import ExportWindow, GraphFrame
from src.functions.physics_graphs import FeCr_phase_graph, FeCrAl_phase_graph
from src.functions.external_functions import wrap_text

matplotlib.use('TkAgg')

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

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
            x=(10, 90),
            y=None
        ),
        function = FeCr_phase_graph
    ),
    dict(
        button_name = "Фазова діаграма для опроміненого сплаву Fe-Cr-Al",
        params_explanation = "Введіть параметри xCr, xAl (від 0 до 0.2), N (Натуральне число), r0 (Натуральне число)",
        graph_title = lambda xAl: f"Фазова діаграма для сплаву Fe-Cr-{xAl*100}Al",
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
        function = FeCrAl_phase_graph
    ),
]

class App(customtkinter.CTk):
    def __init__(self, functions):
        super().__init__()
        
        self.functions = functions

        # configure window
        self.title("Графіки")
        self.geometry(f"{1280}x{720}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=8, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure((1), weight=1)
        
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text="Оберіть Графік", 
            font=customtkinter.CTkFont(
                size=20, weight="bold"
            )
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # buttons to graphs
        self.sidebar_buttons_frame = customtkinter.CTkScrollableFrame(self.sidebar_frame)
        self.sidebar_buttons_frame.grid_columnconfigure(0, weight=1)
        self.sidebar_buttons_frame.grid(
            row=1, column=0, 
            padx=20, pady=(10, 50),
            sticky="nsew"
        )
        self.sidebar_button = dict()
        for num, graph in enumerate(functions):
            button_text, new_line_count = wrap_text(graph['button_name'], 20)
            self.sidebar_button[graph['button_name']] = customtkinter.CTkButton(
                self.sidebar_buttons_frame, 
                text=button_text,
                height=28*new_line_count,
                command=lambda g=graph, fun_num=num: self.function_call(graph=g, function_number=fun_num)
            )
            self.sidebar_button[graph['button_name']].grid(row=num, column=0, padx=5, pady=10, sticky='ew')
            
        # light theme of GUI
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Тема застосунку:", anchor="w")
        self.appearance_mode_label.grid(
            row=2, column=0, 
            padx=20, pady=(10, 0), 
            sticky='ew'
        )
        
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Системна", "Світла", "Темна"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(
            row=3, column=0, 
            padx=20, pady=(10, 10),
            sticky='ew'
        )
        
        # Scaling options
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text="Масштабування інтерфейсу:", anchor="w"
        )
        self.scaling_label.grid(
            row=4, column=0, 
            padx=20, pady=(10, 0),
            sticky='ew'
        )
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, 
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event
        )
        self.scaling_optionemenu.grid(
            row=5, column=0, 
            padx=20, pady=(10, 20),
            sticky='ew'
        )

        # update and export buttons
        self.function_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.function_buttons_frame.grid(
            row=2, column=1, 
            padx=(20, 0), pady=(20, 20), 
            sticky="nsew"
        )
        self.update_button = customtkinter.CTkButton(
            master=self.function_buttons_frame, 
            text='Оновити', fg_color="transparent", 
            border_width=2, text_color=("gray10", "#DCE4EE"), 
            command=self.update_figure
        )
        self.update_button.grid(
            row=0, column=0, 
            padx=(0, 20), 
            sticky="ew"
        )
        
        self.export = customtkinter.CTkButton(
            master=self.function_buttons_frame, 
            text='Експортувати', fg_color="transparent", 
            border_width=2, text_color=("gray10", "#DCE4EE"), 
            command=self.export_files
        )
        self.export.grid(row=0, column=1, sticky="ew")
        
        self.export_window = None

        # create textboxes
        self.textbox = customtkinter.CTkTextbox(self, width=300, height=400)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # frame for inputs
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # frame for graph
        self.graph_frame = GraphFrame(self)
        self.graph_frame.grid(
            row=0, column=2, 
            padx=20, pady=(20, 0), 
            sticky="nsew", rowspan=2
        )
        
        self.eval_progress_bar = customtkinter.CTkProgressBar(self, mode='determinate', height=20)
        self.eval_progress_bar.set(0)
        self.eval_progress_bar.grid(
            row=2, column=2, 
            padx=20, pady=20, 
            sticky="ew"
        )
        
        # default values
        self.appearance_mode_optionemenu.set("Системна")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0", "Оберіть граф, щоб з'явилися поля вводу")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        theme_map = {
            "Світла": "Light",
            "Темна": "Dark",
            "Системна": "System"
        }
        customtkinter.set_appearance_mode(theme_map[new_appearance_mode])

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
    def render_input_boxes(self, input_boxes={}): 
        self.destroy_input_boxes()
        if len(input_boxes) != 0:
            self.inputs = dict()
            input_labels = list(input_boxes.keys())
            for inp_num in range(len(input_boxes)):
                customtkinter.CTkLabel(
                    self.input_frame, 
                    text=f"{input_labels[inp_num]}:", 
                    font=customtkinter.CTkFont(
                        size=14, weight="bold"
                    )
                ).grid(
                    row=inp_num, column=0, 
                    padx=10, pady=(10, 0), 
                    sticky="w"
                )
                self.inputs[input_labels[inp_num]] = customtkinter.CTkEntry(
                    self.input_frame, 
                    placeholder_text=input_boxes[input_labels[inp_num]]
                )
                self.inputs[input_labels[inp_num]].grid(
                    row=inp_num, column=1, 
                    padx=(0, 10), pady=(10, 0), 
                    sticky="nsew"
                )
        else:
            self.inputs = dict()
            self.graph_frame.plot(self.flag)
            
    def destroy_input_boxes(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
            
    def function_call(self, graph, function_number):
        self.flag = function_number
        self.textbox.delete("0.0", "end")
        self.textbox.insert("0.0", graph["params_explanation"])
        self.graph_frame.label.configure(text='СумДУ')
        self.graph_frame.clear_canvas()
        self.render_input_boxes(graph["required_params"]) 
    
    def update_figure(self):
        self.graph_frame.clear_canvas()
        
        if len(self.functions[self.flag]['required_params']) != 0:
            try:
                params = dict()
                for key, value in self.inputs.items():
                    params[key] = float(value.get())
                self.graph_frame.plot(self.flag, **params)                
            except ValueError as e:
                self.textbox.delete("0.0", "end")
                self.textbox.insert("0.0", f"Невірне значення параметру {e}")
        else:
            self.graph_frame.plot(self.flag)
    
    def export_files(self):
        if self.export_window is None or not self.export_window.winfo_exists():
            self.toplevel_window = ExportWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = App(functions=functions)
    app.mainloop()