from __future__ import annotations

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from bebop_lines.solvers.pivots import pivot_score


def get_timestamped_filename(prefix="plot", ext="png", outdir="outputs/figs"):
    os.makedirs(outdir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = os.path.join(outdir, f"{prefix}_{timestamp}.{ext}")

    return filename


def visualize_scored(degrees_list : list[int], filename : str | None=None):
  ys = degrees_list
  shades = pivot_score(degrees_list)
  N = len(ys)

  shade_array = np.array(shades)
  shade_norm = shade_array / max(shade_array)

  fig, ax = plt.subplots()

  for i in range(N):
      ax.add_patch(Rectangle((i, ys[i]), 1, 1, color=str(1 - shade_norm[i])))

  ax.set_xlim(0, N)
  ax.set_ylim(-0.5, max(ys) + 1.5)
  ax.set_xticks(range(N))
  ax.set_yticks(range(max(ys)+1))
  ax.set_aspect('equal')
  ax.invert_yaxis()
  plt.grid(True, which='both', color='gray', linestyle='--', linewidth=0.5)

  plt.title("Grid Scatter with Shading")
  plt.xlabel("Index")
  plt.ylabel("Y Value")

  if not isinstance(filename, str):
    filename = get_timestamped_filename(prefix="plot", ext="png", outdir="outputs/figs")

  plt.savefig(filename)
  plt.show()