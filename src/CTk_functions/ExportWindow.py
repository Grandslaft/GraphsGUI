from tkinter import filedialog
import customtkinter

import src.global_parameters as gp

# export window class on the base of Top Level window customtkinter.CTkToplevel
class ExportWindow(customtkinter.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Вікно експорту")
        self.geometry("500x200") # window size
        self.grab_set() # focus on this window
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Create label that will act as the title
        self.label = customtkinter.CTkLabel(
            self, text="Експорт графіку та розрахованих значень",
            font=customtkinter.CTkFont(
                size=20, weight="bold"
            )
        ) 
        self.label.grid(
            row=0, column=0, 
            padx=(gp.OUTER_PAD, gp.OUTER_PAD), pady=2*gp.OUTER_PAD, 
            columnspan=2, sticky='w'
        )
        
        # Export buttons frame
        self.export_buttons_frame = customtkinter.CTkFrame(self, fg_color='transparent')
        self.export_buttons_frame.grid(
            row=1, column=0, 
            padx=gp.OUTER_PAD, pady=(0, gp.OUTER_PAD),
            sticky='nsew'
        )
        self.export_buttons_frame.grid_rowconfigure(0, weight=1)
        self.export_buttons_frame.grid_columnconfigure((0,1), weight=1)
        
        # button for the files' export
        self.files_export = customtkinter.CTkButton(
            master=self.export_buttons_frame,
            text='Експортувати файли', fg_color="transparent", 
            border_width=2, text_color=("gray10", "#DCE4EE"), 
            command=self.save_files
        )
        self.files_export.grid(
            row=0, column=0, 
            padx=(0, gp.OUTER_PAD), pady=0,
            sticky='nsew'
        )
        # button for the graph export
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
    
    # function, that writes data into the file
    def write_data_to_file(fname, x, y):
        f = open(fname, "w")
        for i in range(len(x)):
            line = str(x[i]) + '\t' + str(y[i]) + '\n'
            f.write(line)
        f.close()
    
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
    def export_graph(self):
        # function to open a dialog window for choosing the save directory, specifying the file name, and selecting the file type
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"),
                    ("JPEG files", "*.jpg"),
                    ("All files", "*.*")],
            initialfile=self.master.graph_frame.label.cget("text"),
            title="Оберіть місце збереження графіку"
        )
        if file_path == '': # if window was closed, end function
            return
        # save the graph
        self.master.graph_frame.ax.set_title(self.master.graph_frame.label.cget("text"))
        self.master.graph_frame.fig.savefig(file_path)
        