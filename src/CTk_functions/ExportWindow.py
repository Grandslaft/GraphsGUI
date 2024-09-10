from tkinter import filedialog
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
    
    # # json save
    # def save_files(self):
    #     # Convert any ndarray objects to lists for JSON serialization
    #     def convert_to_serializable(obj):
    #         if isinstance(obj, np.ndarray):
    #             return obj.tolist()
    #         elif isinstance(obj, dict):
    #             return {k: convert_to_serializable(v) for k, v in obj.items()}
    #         elif isinstance(obj, list):
    #             return [convert_to_serializable(i) for i in obj]
    #         return obj

    #     serializable_data = convert_to_serializable(self.master.graph_frame.export_file)
        
    #     file_path = filedialog.asksaveasfilename(
    #         defaultextension=".json",
    #         filetypes=[("JSON files", "*.json"),
    #                 ("All files", "*.*")],
    #         title="Оберіть місце збереження даних"
    #     )
    #     with open(file_path, 'w', encoding='utf-8') as f:
    #         json.dump(serializable_data, f, ensure_ascii=False, indent=4)
    
    def write_data_to_file(fname, x, y):
        f = open(fname, "w")
        for i in range(len(x)):
            line = str(x[i]) + '\t' + str(y[i]) + '\n'
            f.write(line)
        f.close()
    
    def save_files(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".dat",
            filetypes=[("DAT files", "*.dat"),
                    ("All files", "*.*")],
            initialfile=self.master.graph_frame.default_file_name,
            title="Оберіть місце збереження даних"
        )
        if file_path == '':
            return
        if len(self.master.graph_frame.export_files) > 1:
            for file_num, file in enumerate(self.master.graph_frame.export_files):
                pos = file_path.rfind('.')
                new_file_path = file_path[:pos] + f'_line{file_num+1}' + file_path[pos:]
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(file)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.master.graph_frame.export_files[0])
    
    def export_graph(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")],
            initialfile=self.master.graph_frame.label.cget("text"),
            title="Оберіть місце збереження графіку"
        )
        if file_path == '':
            return
        self.master.graph_frame.ax.set_title(self.master.graph_frame.label.cget("text"))
        self.master.graph_frame.fig.savefig(file_path)
        