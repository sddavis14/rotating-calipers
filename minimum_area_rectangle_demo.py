#!/usr/bin/env python3

import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from matplotlib import pyplot
import numpy as np
from minimum_area_rectangle import compute_bounding_rectangle
import math
import sys

points = np.empty(shape=(0, 2), dtype=np.float64)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim([0, 17])
ax.set_ylim([0, 10])
ax.set_aspect(1)
plt.xticks([])
plt.yticks([])


def draw_rect(rect, color):
    prev_lines = []
    for i in range(0, 4):
        line = plt.plot(rect[[i, (i + 1) % 4], 0],
                        rect[[i, (i + 1) % 4], 1],
                        f'{color}--')
        prev_lines.append(line)
    return prev_lines


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
    print('Pressed', event.key)
    sys.stdout.flush()
    if event.key == 'enter':
        if points.shape[0] < 3:
            print('Not enough points provided')
            return

        hull = ConvexHull(points)
        hull_points = points[hull.vertices, :]

        if hull.vertices.shape[0] < 3:
            print('Not enough vertices on the convex hull')
            return

        for hull_idx in range(0, hull.vertices.shape[0]):
            point_idx = hull.vertices[hull_idx]
            point_idx_next = hull.vertices[(hull_idx + 1) % hull.vertices.shape[0]]
            plt.plot(points[[point_idx, point_idx_next], 0],
                     points[[point_idx, point_idx_next], 1],
                     '-')

        fig.canvas.draw()

        best_area = 1.0e100
        best_rect = None
        for rect in compute_bounding_rectangle(hull_points):
            prev_lines = draw_rect(rect, 'r')

            homo_p_1 = np.concatenate([rect[0, :], np.array([1])], 0)
            homo_p_2 = np.concatenate([rect[1, :], np.array([1])], 0)
            homo_p_3 = np.concatenate([rect[2, :], np.array([1])], 0)
            homo_p_4 = np.concatenate([rect[3, :], np.array([1])], 0)

            area_det_1 = np.stack([homo_p_1, homo_p_2, homo_p_3])
            area_det_2 = np.stack([homo_p_2, homo_p_3, homo_p_4])
            area = 0.5 * (math.fabs(np.linalg.det(area_det_1)) + math.fabs(np.linalg.det(area_det_2)))
            print(area)
            if area < best_area:
                best_area = area
                best_rect = rect

            fig.canvas.draw()
            pyplot.pause(1.5)

            for line in prev_lines:
                for line2 in line:
                    line2.remove()

            fig.canvas.draw()
            pyplot.pause(0.25)

        plt.title('Found the minimum area rectangle with area \n' + '{0:.4}'.format(best_area))

        draw_rect(best_rect, 'g')

        fig.canvas.draw()
        pyplot.pause(0.25)


fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('key_press_event', on_press)

plt.title('Click to create some points. Press enter to execute the algorithm.')

plt.show()

