#!/usr/bin/env python3

import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from matplotlib import pyplot
import numpy as np
from maxdist import compute_bounding_rectangle
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
        self.count = 0

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
        if not self.count:
            plt.plot(event.xdata, event.ydata, 'o', color = 'blue')
        elif self.count == 1:
            plt.plot(event.xdata, event.ydata, 'o', color = 'green')
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
            if self.count == 0:
                self.hull_points1 = self.points[hull.vertices, :]
            elif self.count == 1:
                self.hull_points2 = self.points[hull.vertices, :]

            if hull.vertices.shape[0] < 3:
                print('Not enough vertices on the convex hull')
                return

            #self.running_state = 'executing'

            draw_hull(hull, self.points, self.count)
            self.points = np.empty(shape=(0, 2), dtype=np.float64)
            self.count += 1

            self.fig.canvas.draw()
            
            if self.count == 2:
                self.start_compute(self.hull_points1, self.hull_points2)

    def start_compute(self, hp1, hp2):
        best_diam = -1.0e100
        best_diameter = None
        for pts, rec1, rec2, ang in compute_bounding_rectangle(hp1, hp2):
            diam = draw_diam(pts, 'black')
            rec1d = draw_rect1(rec1, pts[0], ang, 'black')
            rec2d = draw_rect2(rec2, pts[1], ang, 'black')
            diam_len = compute_dist(pts)
            self.text.set_text('Pair Distance: ' + '{0:.4}'.format(diam_len))
            self.fig.canvas.draw()

            if diam_len > best_diam:
                best_diam = diam_len
                best_diameter = pts

            pyplot.pause(1.5)

            remove_lines_(rec1d)
            remove_lines_(rec2d)
            remove_lines(diam)

        draw_diam(best_diameter, 'g')
        self.text.set_text('Maximum Distance: ' + '{0:.4}'.format(best_diam))
        self.fig.canvas.draw()
        self.running_state = 'complete'

    def run(self):
        plt.show()


def remove_lines(prev_lines):
    for line in prev_lines:
        for line2 in line:
            line2.remove()

def remove_lines_(prev_lines):
    for line in prev_lines:
        line.remove()


def compute_area_of_rect(rect):
    homo_p_1 = np.concatenate([rect[0, :], np.array([1])], 0)
    homo_p_2 = np.concatenate([rect[1, :], np.array([1])], 0)
    homo_p_3 = np.concatenate([rect[2, :], np.array([1])], 0)
    homo_p_4 = np.concatenate([rect[3, :], np.array([1])], 0)
    area_det_1 = np.stack([homo_p_1, homo_p_2, homo_p_3])
    area_det_2 = np.stack([homo_p_2, homo_p_3, homo_p_4])
    area = 0.5 * (math.fabs(np.linalg.det(area_det_1)) + math.fabs(np.linalg.det(area_det_2)))
    return area

def compute_dist(pts):
    p1x = pts[0][0]
    p1y = pts[0][1]
    p2x = pts[1][0]
    p2y = pts[1][1]
    return ((p1x - p2x)**2 + (p1y - p2y)**2)**0.5


def draw_hull(hull, points, cnt):
    if not cnt:
        col = 'blue'
    else:
        col = 'green'
    for hull_idx in range(0, hull.vertices.shape[0]):
        point_idx = hull.vertices[hull_idx]
        point_idx_next = hull.vertices[(hull_idx + 1) % hull.vertices.shape[0]]
        plt.plot(points[[point_idx, point_idx_next], 0],
                 points[[point_idx, point_idx_next], 1],
                 '-', color=col)


def draw_rect1(rect, x, angle, color):
    prev_lines = []
    p1, p2 = find_equidistant_points(rect[0], rect[1], x, angle, 3)
    line = plt.arrow(p1[0], p1[1], (p2[0] - p1[0]), (p2[1] - p1[1]), shape='full', length_includes_head=False, head_width=0.2, head_length=0.2, color = 'black')
    prev_lines.append(line)
    return prev_lines

def draw_rect2(rect, x, angle, color):
    prev_lines = []
    p1, p2 = find_equidistant_points(rect[2], rect[3], x, angle, 3)
    line = plt.arrow(p2[0], p2[1], (p1[0] - p2[0]), (p1[1] - p2[1]), shape='full', length_includes_head=False, head_width=0.2, head_length=0.2, color = 'black')
    prev_lines.append(line)
    return prev_lines

def draw_diam(pts, color):
    prev_lines = []
    line = plt.plot(np.array([pts[0][0], pts[1][0]]),
                    np.array([pts[0][1], pts[1][1]]),
                    ':', color=f'{color}')
    prev_lines.append(line)
    return prev_lines

def draw_rect(rect, points, color):
    prev_lines = []
    for i in range(0, 4, 1):
        line = plt.plot(rect[[i, (i + 1) % 4], 0],
                        rect[[i, (i + 1) % 4], 1],
                        color='black')
        prev_lines.append(line)

    return prev_lines

def find_equidistant_points(point1, point2, x, angle, desired_distance):
    flag = 0
    mid = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

    if (mid[0] - x[0]) == 0:
        #print('UNDEFINED')
        flag = 1
    else:
        slope = (mid[1] - x[1]) / (mid[0] - x[0])

    if not flag:
        dx = math.sqrt(desired_distance**2 / (1 + slope**2))
        dy = slope * dx

        new_point1 = np.array([mid[0] + dx, mid[1] + dy])
        new_point2 = np.array([mid[0] - dx, mid[1] - dy])
    else:

        new_point1 = np.array([mid[0], mid[1] + 3])
        new_point2 = np.array([mid[0], mid[1] - 3])

    if angle >= math.pi/2 and angle <= math.pi * 1.5:
        return new_point2, new_point1
    return new_point1, new_point2

if __name__ == '__main__':
    demo = RotatingCalipersDemo()
    demo.run()
