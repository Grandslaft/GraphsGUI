import customtkinter
import numpy as np
import json

class ExportWindow(customtkinter.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Вікно експорту")
        self.geometry("500x200")
        self.grab_set()
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.label = customtkinter.CTkLabel(
            self, text="Експорт графіку та розрахованих значень",
            font=customtkinter.CTkFont(
                size=20, weight="bold"
            )
        ) 
        self.label.grid(
            row=0, column=0, 
            padx=(20, 20), pady=50, 
            columnspan=2, sticky='w'
        )
        
        self.export_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.export_buttons_frame.grid(
            row=1, column=0, 
            padx=20, pady=(0, 20),
            sticky='nsew'
        )
        self.export_buttons_frame.grid_rowconfigure(0, weight=1)
        self.export_buttons_frame.grid_columnconfigure((0,1), weight=1)
        
        self.files_export = customtkinter.CTkButton(
            master=self.export_buttons_frame,
            text='Експортувати файли', fg_color="transparent", 
            border_width=2, text_color=("gray10", "#DCE4EE"), 
            command=self.save_files
        )
        self.files_export.grid(
            row=0, column=0, 
            padx=(0, 20), pady=0,
            sticky='nsew'
        )
        
        self.img_export = customtkinter.CTkButton(
            master=self.export_buttons_frame,
            text='Експортувати графік', fg_color="transparent", 
            border_width=2, text_color=("gray10", "#DCE4EE"), 
            command=self.export_graph
        )
        self.img_export.grid(
            row=0, column=1, 
            sticky='nsew'
        )
    
    def save_files(self):
        # Convert any ndarray objects to lists for JSON serialization
        def convert_to_serializable(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_serializable(i) for i in obj]
            return obj

        serializable_data = convert_to_serializable(self.master.graph_frame.export_file)
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, ensure_ascii=False, indent=4)
    
    def export_graph(self):
        self.master.graph_frame.fig.savefig('graph.png')