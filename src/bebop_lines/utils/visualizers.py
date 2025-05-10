"""
Utility for visualizing melodic lines
"""
from __future__ import annotations

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from bebop_lines.solvers.pivots import pivot_score


def get_timestamped_filename(prefix="plot", ext="png", outdir="outputs/figs"):
    """
    Return a string, to be used as a filename, that includes a timestamp

    Args:
      prefix : Prefix for the filename
      ext : Extension for the filename
      outdir : Output irectory to save the file in
    
    Returns
      The filename as a string
    """
    os.makedirs(outdir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = os.path.join(outdir, f"{prefix}_{timestamp}.{ext}")

    return filename


def visualize_scored(degrees_list : list[int], filename : str | None=None):
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

  fig, ax = plt.subplots()

  for i in range(N):
      ax.add_patch(Rectangle((i, ys[i]), 1, 1, color=str(1 - shade_norm[i])))

  ax.set_xlim(0, N)
  ax.set_ylim(0.0, max(ys))
  ax.set_xticks(range(N))
  ax.set_yticks(range(max(ys)+1))
  ax.set_aspect('equal')
  ax.invert_yaxis()
  plt.grid(True, which='both', color='gray', linestyle='--', linewidth=0.5)

  plt.title("Piano Roll Line with Curvature Gradient")
  plt.xlabel("Index")
  plt.ylabel("Value")

  if not isinstance(filename, str):
    filename = get_timestamped_filename(prefix="plot", ext="png", outdir="outputs/figs")

  plt.savefig(filename)
  plt.show()
  plt.clf()