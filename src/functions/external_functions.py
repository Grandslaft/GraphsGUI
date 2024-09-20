import matplotlib.pyplot as plt

# line breaks a string if it exceeds wraplength characters length
def wrap_text(text, wraplength):
    words = text.split()
    wrapped_text = ""
    line_length = 0
    newline_count = 0

    for word in words:
        current_length = line_length + len(word) + 1
        if current_length > wraplength:
            wrapped_text += "\n" + word
            line_length = len(word)
            newline_count += 1
        else:
            if wrapped_text:
                wrapped_text += " " + word
            else:
                wrapped_text = word
            line_length += len(word) + 1

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