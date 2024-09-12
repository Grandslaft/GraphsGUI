import matplotlib.pyplot as plt

def heatmap(X, Y, Z, row_labels=None, col_labels=None, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}
    
    # Plot the heatmap
    im = ax.pcolormesh(X, Y, Z, shading='auto', **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    return im, cbar

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