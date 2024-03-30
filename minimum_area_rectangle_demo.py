#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial import ConvexHull
import numpy as np
import sys

points = np.empty(shape=(0, 2), dtype=np.float64)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.spines[['bottom', 'left', 'right', 'top']].set_visible(False)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
plt.xticks([])
plt.yticks([])


def on_click(event):
    global points, ax
    if event.xdata is None:
        print('Clicked outside the graph area')
        return

    plt.plot(event.xdata, event.ydata, 'o')
    points = np.append(points, np.array([[event.xdata, event.ydata]]), axis=0)

    [p.remove() for p in ax.patches]

    fig.canvas.draw()


def on_press(event):
    global points, ax
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'enter':
        hull = ConvexHull(points)
        hull_points = points[hull.vertices, :]

        x_min = np.min(hull_points[:, 0])
        y_min = np.min(hull_points[:, 1])
        x_max = np.max(hull_points[:, 0])
        y_max = np.max(hull_points[:, 1])

        rect = patches.Rectangle((x_min, y_min),
                                 x_max - x_min,
                                 y_max - y_min,
                                 linewidth=1,
                                 edgecolor='magenta',
                                 facecolor='none')
        ax.add_patch(rect)

        for hull_idx in range(0, hull.vertices.shape[0]):
            point_idx = hull.vertices[hull_idx]
            point_idx_next = hull.vertices[(hull_idx + 1) % hull.vertices.shape[0]]
            plt.plot(points[[point_idx, point_idx_next], 0],
                     points[[point_idx, point_idx_next], 1],
                     '-')

        fig.canvas.draw()


fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('key_press_event', on_press)

plt.title('Draw some points')

plt.show()
