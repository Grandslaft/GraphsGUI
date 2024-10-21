import matplotlib.pyplot as plt
import tkinter as tk

def get_label_font(obj):
    # Get the font object from the label
    font_obj = tk.font.Font(font=obj.cget("font"))
    
    # Extract the family (font name) and size from the font object
    font_family = font_obj.cget("family")
    font_size = font_obj.cget("size")
    
    # Return the font in the desired format
    return (font_family, font_size)

# line breaks a string if it exceeds wraplength characters length
def wrap_text(text, wraplength_px, obj):
    words = text.split()
    wrapped_text = ""
    line_length = 0
    newline_count = 0

    # Create a Font object for measuring text width
    label_font = get_label_font(obj)
    fnt = tk.font.Font(font=label_font)

    for word in words:
        # Measure the pixel width of the word
        word_width = fnt.measure(word)
        space_width = fnt.measure(' ')
        current_length = line_length + word_width + space_width

        # If the current word exceeds the wraplength, move it to a new line
        if current_length > wraplength_px:
            wrapped_text += "\n" + word
            line_length = word_width  # Start counting the length for the new line
            newline_count += 1
        else:
            if wrapped_text:
                wrapped_text += " " + word
            else:
                wrapped_text = word
            line_length += word_width + space_width

    return wrapped_text, newline_count


def saveImageFile(fname, data, Size):
    plt.imsave(fname, data.reshape(Size, Size), cmap='coolwarm')

def write_data_to_xyz_file(fname, data, Size):
    Size = int(Size)
    f = open(fname, "w")
    for i in range(Size):
        for j in range(Size):
            line = str(i) + '\t' + str(j) + '\t' + str(data.reshape(Size, Size)[i, j]) + '\n'
            f.write(line)
    f.close()

def write_data_to_vtk_file(fname, data, Size):
    Size = int(Size)
    f = open(fname, "w")
    f.write('# vtk DataFile Version 2.0')
    f.write('\n')
    f.write('Structured Grid 2D Dataset')
    f.write('\n')
    f.write('ASCII')
    f.write('\n')
    f.write('DATASET STRUCTURED_GRID')
    f.write('\n')
    line = 'DIMENSIONS ' + str(Size) + ' ' + str(Size) + ' ' + str(1) + '\n'
    f.write(line)
    line = 'POINTS ' + str(Size * Size * 1) + ' float \n'
    f.write(line)
    for i in range(Size):
        for j in range(Size):
            line = str(i + 1) + '\t' + str(j + 1) + '\t' + str(0) + '\n'
            f.write(line)
    line = 'POINT_DATA ' + str(Size *Size * 1) + '\n'
    f.write(line)
    f.write('SCALARS colors float\n')
    f.write('LOOKUP_TABLE default\n')
    for i in range(Size*Size):
        f.write(str(data[i]))
        f.write('\n')
    f.close()

def save_precipitates(fname, column_name, t, r, n):
    f = open(fname, "w")
    line = column_name + '\t<Rp> [nm]\tNp x 1E-27 [m^3]\n'
    f.write(line)
    for i in range(len(t)):
        line = str(t[i]) + '\t' + str(r[i]) + '\t' + str(n[i]) + '\n'
        f.write(line)
    f.close()
    
def write_data_to_file(fname, x, y):
    f = open(fname, "w")
    for i in range(len(x)):
        line = str(x[i]) + '\t' + str(y[i]) + '\n'
        f.write(line)
    f.close()
    
def save_data_to_file(fname, data, to_save_ind=[], column_names_set=None):
    
    def write_to_file(whole_path, set_of_data, column_names):
        with open(whole_path, "w") as f:
            # Write the column names if provided
            if column_names:
                line = column_names + '\n'
                f.write(line)
            
            # Transpose the list of args to iterate over rows
            for row in zip(*set_of_data):
                # Convert each element to a string and join with tabs
                line = '\t'.join(map(str, row)) + '\n'
                f.write(line)
                
    def multi_plot(data, column_names, fname_suf1=''):
        suffix_2 = lambda num: f'_line{num:.0f}'
        for index in range(0, int(len(data) / 2)):
            fname = f"{fname_parts[0]}{fname_suf1}{suffix_2(index+1)}.{fname_parts[1]}"
            column_names = column_names if column_names_set else None
            x = data[0 + 2 * index]
            y = data[1 + 2 * index]
            write_to_file(fname, [x, y], column_names)
    
    if '.' in fname:
        fname_parts = fname.rsplit('.', 1) 
          
    if len(to_save_ind) <= 1:
        if len(data[0]) > 2:
            multi_plot(data[0], column_names_set[0])
            return
        write_to_file(fname, data[0], column_names_set[0])
        return
    
    suffix = lambda num: f'_plot{num:.0f}'
    selected_data = [data[i] for i in to_save_ind]
    
    for num, data_part in enumerate(selected_data):
        
        if len(data_part) > 2:
            
            multi_plot(data_part, column_names[num], suffix(num+1))
            pass
            
        fname = f"{fname_parts[0]}{suffix(num+1)}.{fname_parts[1]}"
        column_names = column_names_set[num] if column_names_set else None
        write_to_file(fname, data_part, column_names)
    
    
        
    