import tkinter as tk
import customtkinter

import matplotlib

from .CTk_functions import ExportWindow, GraphFrame

matplotlib.use('TkAgg')

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

NUMBER_OF_GRAPHS = 5

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Графіки")
        self.geometry(f"{1400}x{720}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_rowconfigure(2, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=NUMBER_OF_GRAPHS, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(NUMBER_OF_GRAPHS, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text="Оберіть Графік", 
            font=customtkinter.CTkFont(
                size=20, weight="bold"
            )
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # buttons to graphs
        self.sidebar_button = dict()
        function_sequence = [self.heart_graph, self.sin_graph, self.cos_graph, self.heatmap_graph]
        function_names = ['Графік Серця', 'Графік Сінуса', 'Графік Косінуса з параметром a', 'Теплова карта']
        for button_num in range(1, NUMBER_OF_GRAPHS):
            self.sidebar_button[button_num] = customtkinter.CTkButton(
                self.sidebar_frame, 
                text=function_names[button_num-1], 
                command=function_sequence[button_num - 1]
            )
            self.sidebar_button[button_num].grid(row=button_num, column=0, padx=20, pady=10, sticky='ew')
            
        # light mode of GUI
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=NUMBER_OF_GRAPHS+1, column=0, padx=20, pady=(10, 0))
        
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, 
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(
            row=NUMBER_OF_GRAPHS+2, 
            column=0, padx=20, pady=(10, 10)
        )
        
        # Scaling options
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, 
            text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(
            row=NUMBER_OF_GRAPHS+3, 
            column=0, padx=20, pady=(10, 0)
        )
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, 
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event
        )
        self.scaling_optionemenu.grid(
            row=NUMBER_OF_GRAPHS+4, 
            column=0, padx=20, pady=(10, 20)
        )

        # update and export buttons
        self.function_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.function_buttons_frame.grid(
            row=3, column=1, 
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
        self.textbox = customtkinter.CTkTextbox(self, width=300, height=200)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # create textbox
        self.values_textbox = customtkinter.CTkTextbox(self, width=300, height=50)
        self.values_textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="w")
        
        # frame for inputs
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=2, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
        # frame for graph
        self.graph_frame = GraphFrame(master=self)
        self.graph_frame.grid(row=0, column=2, padx=20, pady=20, sticky="nsew", rowspan=4)
        
        # default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0", "Оберіть граф, щоб з'явилися поля вводу")
        self.values_textbox.insert("0.0", "Немає значень для вводу")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        
    def render_input_boxes(self, input_boxes={}): 
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
                    placeholder_text=input_boxes.get(inp_num)
                )
                self.inputs[input_labels[inp_num]].grid(
                    row=inp_num, column=1, 
                    padx=(0, 10), pady=(10, 0), 
                    sticky="nsew"
                )
        else:
            for widget in self.input_frame.winfo_children():
                widget.destroy()
            self.inputs = dict()
            self.graph_frame.plot(self.flag)
                
    def heart_graph(self):
        self.flag = "graph 1"
        self.textbox.delete("0.0", "end")
        self.values_textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "СумДУ")
        self.values_textbox.insert("0.0", "Немає значень для вводу")
        self.render_input_boxes({})  

    def sin_graph(self):
        self.flag = "graph 2"
        self.textbox.delete("0.0", "end")
        self.values_textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Поле для виводу графіку Сінуса")
        self.values_textbox.insert("0.0", "Немає значень для вводу")
        self.render_input_boxes({})
        
    def cos_graph(self):
        self.flag = "graph 3"
        self.textbox.delete("0.0", "end")
        self.values_textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Поле для виводу графіку косінусу")
        self.values_textbox.insert("0.0", "Введіть значення параметру(ів): a")
        self.render_input_boxes({'a_param':1})
        
    def heatmap_graph(self):
        self.flag = "graph 4"
        self.textbox.delete("0.0", "end")
        self.values_textbox.delete("0.0", "end")
        self.textbox.insert("0.0", "Поле для виводу графіку теплової карти")
        self.values_textbox.insert("0.0", "Немає значень для вводу")
        self.render_input_boxes({})
    
    def update_figure(self):
        try:
            params = dict()
            for key, value in self.inputs.items():
                params[key] = float(value.get())
            self.graph_frame.plot(self.flag, **params)
        except AttributeError:
            self.graph_frame.plot(self.flag)
        except ValueError as e:
            self.values_textbox.delete("0.0", "end")
            self.values_textbox.insert("0.0", f"Невірне значення параметру {e}")
    
    def export_files(self):
        if self.export_window is None or not self.export_window.winfo_exists():
            self.toplevel_window = ExportWindow(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

if __name__ == "__main__":
    app = App()
    app.mainloop()