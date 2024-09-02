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