import numpy as np

from bokeh.plotting import figure, output_file, show


def plot_series():
    output_file("patch.html")

    p = figure(plot_width=400, plot_height=400, x_axis_type="datetime")

    p.multi_line([[1, 3, 2], [3, 4, 6, 6]], [[2, 1, 4], [4, 7, 8, 5]],
                 color=["firebrick", "navy"], alpha=[0.8, 0.3], line_width=4)
    show(p)

    #output_file("stocks.html", title="stocks.py example")

    #show(gridplot([p], plot_width=400, plot_height=400))  # open a browser

if __name__ == "__main__":
    """Main function for executing the run script.

    System parameters are loaded from file and passed to calculate_mandelbrot,
    where data structures are defined and various Mandelbrot implementations are executed:
    """
    plot_series()