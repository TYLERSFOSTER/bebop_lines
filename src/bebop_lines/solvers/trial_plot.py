import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

ys = [3, 1, 4, 2, 0, 1, 3]
shades = [10, 50, 90, 30, 70, 60, 20]
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

plt.show()
