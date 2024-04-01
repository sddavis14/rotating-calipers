import math
import numpy as np


def next_point_idx(idx, points):
    if idx == 0:
        return points.shape[0] - 1
    else:
        return idx - 1


def vector_angle(v1, v2):
    return math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


def rotate_vec(v, angle):
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])
    return rotation_matrix @ v


def line_intersection(v1, p1, v2, p2):
    mat_1 = np.array([v1, -v2]).T
    mat_2 = (p2 - p1)
    result = np.linalg.inv(mat_1) @ mat_2
    return result[0] * v1 + p1


def compute_bounding_rectangle(points):
    # Chose the extreme points along each axis
    p1_idx = np.argmin(points[:, 0])
    p2_idx = np.argmin(points[:, 1])
    p3_idx = np.argmax(points[:, 0])
    p4_idx = np.argmax(points[:, 1])

    # The box starts axis aligned
    vec_1 = np.array([0, 1])
    vec_2 = np.array([-1, 0])
    vec_3 = np.array([0, -1])
    vec_4 = np.array([1, 0])

    angle = 0
    while angle < math.pi / 2:  # Rotate up to 90 degrees
        p1 = points[p1_idx]
        p2 = points[p2_idx]
        p3 = points[p3_idx]
        p4 = points[p4_idx]

        # Form the bounding box points by calculating the 4 intersections
        rec_p1 = line_intersection(vec_1, p1, vec_2, p2)
        rec_p2 = line_intersection(vec_2, p2, vec_3, p3)
        rec_p3 = line_intersection(vec_3, p3, vec_4, p4)
        rec_p4 = line_intersection(vec_4, p4, vec_1, p1)

        result = np.stack([rec_p1, rec_p2, rec_p3, rec_p4])

        yield result  # return all the rectangles

        p1_next = points[next_point_idx(p1_idx, points)]
        p2_next = points[next_point_idx(p2_idx, points)]
        p3_next = points[next_point_idx(p3_idx, points)]
        p4_next = points[next_point_idx(p4_idx, points)]

        side_vec_1 = p1_next - p1
        side_vec_2 = p2_next - p2
        side_vec_3 = p3_next - p3
        side_vec_4 = p4_next - p4

        angle_1 = vector_angle(side_vec_1, vec_1)
        angle_2 = vector_angle(side_vec_2, vec_2)
        angle_3 = vector_angle(side_vec_3, vec_3)
        angle_4 = vector_angle(side_vec_4, vec_4)

        angles = [angle_1, angle_2, angle_3, angle_4]
        min_angle_idx = np.argmin(angles)
        min_angle = angles[min_angle_idx]

        if min_angle_idx == 0:
            p1_idx = next_point_idx(p1_idx, points)
        elif min_angle_idx == 1:
            p2_idx = next_point_idx(p2_idx, points)
        elif min_angle_idx == 2:
            p3_idx = next_point_idx(p3_idx, points)
        elif min_angle_idx == 3:
            p4_idx = next_point_idx(p4_idx, points)

        # rotate clockwise by min_angle
        vec_1 = rotate_vec(vec_1, -min_angle)
        vec_2 = rotate_vec(vec_2, -min_angle)
        vec_3 = rotate_vec(vec_3, -min_angle)
        vec_4 = rotate_vec(vec_4, -min_angle)

        angle = angle + min_angle
