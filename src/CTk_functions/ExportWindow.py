from tkinter import filedialog
import customtkinter

import src.global_parameters as gp

# export window class on the base of Top Level window customtkinter.CTkToplevel
class ExportWindow(customtkinter.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Вікно експорту")
        self.geometry("500x400") # window size
        self.grab_set() # focus on this window
        self.grid_rowconfigure((1,2,3), weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # if there's default directory, choose it
        self.master.save_path = gp.CURRENT_DIR
        
        # Create label that will act as the title
        self.label = customtkinter.CTkLabel(
            self, text="Експорт графіків та розрахованих значень",
            anchor='center',
            font=customtkinter.CTkFont(
                size=20, weight="bold"
            )
        ) 
        self.label.grid(
            row=0, column=0, 
            padx=(gp.OUTER_PAD, gp.OUTER_PAD), pady=2*gp.OUTER_PAD, 
            sticky='nsew'
        )
        
        # select path frame
        self.select_path_frame = customtkinter.CTkFrame(
            self, 
            fg_color=["#d6d8df", "#1a1b26"],
            corner_radius=gp.CORNER_RADIUS
        )
        self.select_path_frame.grid(
            row=1, column=0, 
            padx=gp.OUTER_PAD, pady=(0, gp.OUTER_PAD), 
            sticky='nsew'
        )
        self.select_path_frame.grid_rowconfigure(0, weight=1)
        self.select_path_frame.grid_columnconfigure((0), weight=1)
        
        # textbox that will show current save path
        self.path_text_box = customtkinter.CTkTextbox(
            self.select_path_frame,
            height=28,
            activate_scrollbars=True,
            corner_radius=gp.CORNER_RADIUS,
        )
        self.path_text_box.grid(
            row=0, column=0, 
            padx=gp.INNER_PAD, pady=gp.INNER_PAD, 
            sticky='nsew'
        )
        self.path_text_box.insert("0.0", self.master.save_path)
        self.path_text_box.bind(
            "<KeyRelease>", 
            self.on_text_change
        )
        
        # button to call a window to choose directory
        self.choose_path = customtkinter.CTkButton(
            self.select_path_frame,
            text='Експортувати файли',
            command=self.select_path
        )
        self.choose_path.grid(
            row=0, column=1, 
            padx=(0, gp.INNER_PAD), pady=gp.INNER_PAD, 
            sticky='nsew'
        )
        
        self.data_to_save = customtkinter.CTkFrame(
            self, 
            fg_color=["#d6d8df", "#1a1b26"],
            corner_radius=gp.CORNER_RADIUS
        )
        self.data_to_save.grid(
            row=2, column=0, 
            padx=gp.OUTER_PAD, pady=(0, gp.OUTER_PAD), 
            sticky='nsew'
        )
        self.data_to_save.grid_rowconfigure((0,1,2), weight=1)
        self.data_to_save.grid_columnconfigure((0), weight=1)
        
        # graph save checkbox
        self.graph_export = customtkinter.CTkCheckBox(
            self.data_to_save, 
            text="Експортувати рисунки", 
            onvalue=True, offvalue=False
        )
        self.graph_export.grid(
            row=0, column=0, 
            padx=gp.INNER_PAD, 
            pady=(gp.INNER_PAD, gp.ELEMENTS_PAD), 
            sticky="nsew"
        )
        
        # file save checkbox .xyz
        self.file_export_xyz = customtkinter.CTkCheckBox(
            self.data_to_save, 
            text="Експортувати файли у .xyz", 
            onvalue=True, offvalue=False
        )
        self.file_export_xyz.grid(
            row=1, column=0, 
            padx=gp.INNER_PAD, 
            pady=(gp.ELEMENTS_PAD, gp.ELEMENTS_PAD), 
            sticky="nsew"
        )
        
        # file save checkbox .vtk
        self.file_export_vtk = customtkinter.CTkCheckBox(
            self.data_to_save, 
            text="Експортувати файли у .vtk", 
            onvalue=True, offvalue=False
        )
        self.file_export_vtk.grid(
            row=2, column=0, 
            padx=gp.INNER_PAD, 
            pady=(gp.ELEMENTS_PAD, gp.INNER_PAD), 
            sticky="nsew"
        )
        
        # save export params
        self.save_export_params = customtkinter.CTkButton(
            self,
            text='Зберегти параметри експорту',
            command=self.master.get_export_params
        )
        self.save_export_params.grid(
            row=3, column=0, 
            padx=gp.OUTER_PAD, pady=(0, gp.OUTER_PAD), 
            sticky='nsew'
        )
        
    
    # function, that writes data into the file
    def write_data_to_file(fname, x, y):
        f = open(fname, "w")
        for i in range(len(x)):
            line = str(x[i]) + '\t' + str(y[i]) + '\n'
            f.write(line)
        f.close()
    
    def on_text_change(self, event=None):
        self.master.save_path = self.path_text_box.get("1.0", "end-1c")  # Get all text
    
    def select_path(self):
        # function to open a dialog window for choosing the save directory, specifying the file name, and selecting the file type
        file_path = filedialog.askdirectory(
            initialdir=self.master.save_path,
            title="Оберіть місце збереження даних"
        )
        self.path_text_box.delete("0.0", "end")
        self.path_text_box.insert("0.0", file_path)
        if file_path == '': # if window was closed, end function
            return
        
    # save files function
    def save_files(self):
        # function to open a dialog window for choosing the save directory, specifying the file name, and selecting the file type
        file_path = filedialog.asksaveasfilename(
            defaultextension=".dat",
            filetypes=[("DAT files", "*.dat"),
                    ("All files", "*.*")],
            initialfile=self.master.graph_frame.default_file_name,
            title="Оберіть місце збереження даних"
        )
        if file_path == '': # if window was closed, end function
            return
        # if there only one file to export
        if len(self.master.graph_frame.export_files) <= 1:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.master.graph_frame.export_files[0])
            return
        # if there's more than one file to export
        for file_num, file in enumerate(self.master.graph_frame.export_files): # for every file
            pos = file_path.rfind('.') # find last point, which indicates file type
            new_file_path = file_path[:pos] + f'_line{file_num+1}' + file_path[pos:] # insert export number
            with open(new_file_path, 'w', encoding='utf-8') as f: # write the file
                f.write(file)
    
    # save the graph function
    def export_graph(self, file_name):
        # save the graph
        self.master.graph_frame.axs.set_title(self.master.graph_frame.label.cget("text"))
        self.master.graph_frame.fig.savefig(self.master.save_path+'/'+file_name+'.png')
        