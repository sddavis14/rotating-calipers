#!/usr/bin/env python3

import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from matplotlib import pyplot
import numpy as np
from minimum_area_rectangle import compute_bounding_rectangle
import math
import sys


class RotatingCalipersDemo:
    points = None
    fig = None
    ax = None
    text = None
    running_state = 'clicking'

    def __init__(self):
        self.fig = plt.figure()
        self.reset()

    def reset(self):
        plt.clf()

        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim([0, 17])
        self.ax.set_ylim([0, 10])
        self.ax.set_aspect(1)

        plt.xticks([])
        plt.yticks([])
        plt.title('Click to create some points. Press enter to execute the algorithm.')

        self.text = pyplot.text(0.35, 9.25, 'Area: ')
        self.text.set_fontsize(12)
        self.running_state = 'clicking'
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_press)

        self.points = np.empty(shape=(0, 2), dtype=np.float64)
        self.fig.canvas.draw()

    def on_click(self, event):
        if self.running_state == 'executing':
            return
        if self.running_state == 'complete':
            print('Clearing plot')
            self.reset()

        if event.xdata is None:
            print('Clicked outside the graph area')
            return

        plt.plot(event.xdata, event.ydata, 'o')
        self.points = np.append(self.points, np.array([[event.xdata, event.ydata]]), axis=0)

        self.fig.canvas.draw()

    def on_press(self, event):
        print('Pressed', event.key)
        sys.stdout.flush()
        if event.key == 'enter':
            if self.points.shape[0] < 3:
                print('Not enough points provided')
                return

            hull = ConvexHull(self.points)
            hull_points = self.points[hull.vertices, :]

            if hull.vertices.shape[0] < 3:
                print('Not enough vertices on the convex hull')
                return

            self.running_state = 'executing'

            draw_hull(hull, self.points)

            self.fig.canvas.draw()

            best_area = 1.0e100
            best_rect = None
            for rect in compute_bounding_rectangle(hull_points):
                prev_lines = draw_rect(rect, 'r')
                area = compute_area_of_rect(rect)
                self.text.set_text('Area: ' + '{0:.4}'.format(area))
                self.fig.canvas.draw()

                if area < best_area:
                    best_area = area
                    best_rect = rect

                pyplot.pause(1)

                remove_lines(prev_lines)

            draw_rect(best_rect, 'g')
            self.text.set_text('Minimum Area: ' + '{0:.4}'.format(best_area))
            self.fig.canvas.draw()
            self.running_state = 'complete'

    def run(self):
        plt.show()


def remove_lines(prev_lines):
    for line in prev_lines:
        for line2 in line:
            line2.remove()


def compute_area_of_rect(rect):
    homo_p_1 = np.concatenate([rect[0, :], np.array([1])], 0)
    homo_p_2 = np.concatenate([rect[1, :], np.array([1])], 0)
    homo_p_3 = np.concatenate([rect[2, :], np.array([1])], 0)
    homo_p_4 = np.concatenate([rect[3, :], np.array([1])], 0)
    area_det_1 = np.stack([homo_p_1, homo_p_2, homo_p_3])
    area_det_2 = np.stack([homo_p_2, homo_p_3, homo_p_4])
    area = 0.5 * (math.fabs(np.linalg.det(area_det_1)) + math.fabs(np.linalg.det(area_det_2)))
    return area


def draw_hull(hull, points):
    for hull_idx in range(0, hull.vertices.shape[0]):
        point_idx = hull.vertices[hull_idx]
        point_idx_next = hull.vertices[(hull_idx + 1) % hull.vertices.shape[0]]
        plt.plot(points[[point_idx, point_idx_next], 0],
                 points[[point_idx, point_idx_next], 1],
                 '-', color='magenta')


def draw_rect(rect, color):
    prev_lines = []
    for i in range(0, 4):
        line = plt.plot(rect[[i, (i + 1) % 4], 0],
                        rect[[i, (i + 1) % 4], 1],
                        ':', color=f'{color}')
        prev_lines.append(line)
    return prev_lines


if __name__ == '__main__':
    demo = RotatingCalipersDemo()
    demo.run()
