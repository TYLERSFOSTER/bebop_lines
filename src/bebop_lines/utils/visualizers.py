"""
Utility for visualizing melodic lines
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from bebop_lines.solvers.pivots import pivot_score
from bebop_lines.utils.gen_filenames import get_timestamped_filename


def visualize_score(degrees_list : list[int], filename : str | None=None):
    """
    Saves a PNG visualization of a given melodic line, with shading
    indicating the local curvature of the line.

    Args:
        degree_list : A list of integers representing a melodic line as
            a list of scale degrees
        filename : (optional) The name to use when savign the visualization
    
    Returns:
        None
    """
    ys = degrees_list
    shades = pivot_score(degrees_list)
    N = len(ys)

    shade_array = np.array(shades)
    shade_norm = shade_array / max(shade_array)

    _, ax = plt.subplots()

    plot_color = (0.2, 0.2, 0.7)

    for i in range(N):
        if i == 0 or i == N - 1:
            rect_color = plot_color
        else:
            rect_color = str(1 - shade_norm[i])
        ax.add_patch(Rectangle((i, ys[i]), 1, 1, color=rect_color))

    ax.plot([
        n + 0.5 for n in range(N)],
        [y + 0.5 for y in ys],
        color=plot_color, linestyle='-', zorder=5
    )
    ax.scatter([n + 0.5 for n in range(N)], [y + 0.5 for y in ys], color=plot_color, s=30, zorder=6
    )
    ax.scatter([n + 0.5 for n in range(N)], [y + 0.5 for y in ys], color="white", s=5, zorder=7
    )

    ax.set_xlim(0, N)
    ax.set_ylim(0.0, max(ys)+1)
    ax.set_xticks(range(N))
    ax.set_yticks(range(max(ys)+1))
    ax.set_aspect('equal')
    plt.grid(True, which='both', color='lightblue', linestyle='-', linewidth=0.75)

    # Axis labels: red and bold
    ax.set_xlabel("Index", color='red', fontweight='bold')
    ax.set_ylabel("Value", color='red', fontweight='bold')

    # Ticks: red and smaller
    ax.tick_params(axis='both', colors='red', labelsize=8)

    # Tick label text bold
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight('bold')

    # Axes lines (spines) red
    for spine in ax.spines.values():
        spine.set_color('red')

    # Make tick label text bold
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontweight('bold')
        label.set_color('red')

    # Axis labels and title red and bold
    ax.xaxis.label.set_color('red')
    ax.xaxis.label.set_fontweight('bold')
    ax.yaxis.label.set_color('red')
    ax.yaxis.label.set_fontweight('bold')
    ax.title.set_color('red')
    ax.title.set_fontweight('bold')

    # Make axis lines (spines) red
    for spine in ax.spines.values():
        spine.set_color('red')

# Title: red and bold
    ax.set_title("Piano Roll Line with Curvature Gradient", color='red', fontweight='bold')
    plt.xlabel("Index")
    plt.ylabel("Value")

    if not isinstance(filename, str):
        filename = get_timestamped_filename(prefix="plot", ext="png", outdir="outputs/figs")

    plt.savefig(filename)
    plt.show()
    plt.clf()
