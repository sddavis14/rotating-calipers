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


def compute_bounding_rectangle(points1, points2):
    # Chose the extreme points along each axis
    p1_idx1 = np.argmin(points1[:, 0])
    p2_idx1 = np.argmin(points1[:, 1])
    p3_idx1 = np.argmax(points1[:, 0])
    p4_idx1 = np.argmax(points1[:, 1])

    p1_idx2 = np.argmin(points2[:, 0])
    p2_idx2 = np.argmin(points2[:, 1])
    p3_idx2 = np.argmax(points2[:, 0])
    p4_idx2 = np.argmax(points2[:, 1])

    # The box starts axis aligned
    vec_1 = np.array([0, 1])
    vec_2 = np.array([-1, 0])
    vec_3 = np.array([0, -1])
    vec_4 = np.array([1, 0])

    angle = 0
    counter = 0
    init_p2 = p2_idx1
    init_p4 = p4_idx2
    flag = 0
    while True:
        if counter and (init_p2 == p2_idx1) and (init_p4 == p4_idx2):
            flag = 1
        p11 = points1[p1_idx1]
        p21 = points1[p2_idx1]
        p31 = points1[p3_idx1]
        p41 = points1[p4_idx1]
        
        p12 = points2[p1_idx2]
        p22 = points2[p2_idx2]
        p32 = points2[p3_idx2]
        p42 = points2[p4_idx2]

        # Form the bounding box points by calculating the 4 intersections
        rec_p11 = line_intersection(vec_1, p11, vec_2, p21)
        rec_p21 = line_intersection(vec_2, p21, vec_3, p31)
        rec_p31 = line_intersection(vec_3, p31, vec_4, p41)
        rec_p41 = line_intersection(vec_4, p41, vec_1, p11)

        rec_p12 = line_intersection(vec_1, p12, vec_2, p22)
        rec_p22 = line_intersection(vec_2, p22, vec_3, p32)
        rec_p32 = line_intersection(vec_3, p32, vec_4, p42)
        rec_p42 = line_intersection(vec_4, p42, vec_1, p12)

        rec1 = np.stack([rec_p11, rec_p21, rec_p31, rec_p41])
        rec2 = np.stack([rec_p12, rec_p22, rec_p32, rec_p42])

        yield (p21, p42), rec1, rec2, angle  # return all the rectangles

        p11_next = points1[next_point_idx(p1_idx1, points1)]
        p21_next = points1[next_point_idx(p2_idx1, points1)]
        p31_next = points1[next_point_idx(p3_idx1, points1)]
        p41_next = points1[next_point_idx(p4_idx1, points1)]

        p12_next = points2[next_point_idx(p1_idx2, points2)]
        p22_next = points2[next_point_idx(p2_idx2, points2)]
        p32_next = points2[next_point_idx(p3_idx2, points2)]
        p42_next = points2[next_point_idx(p4_idx2, points2)]

        side_vec_11 = p11_next - p11
        side_vec_21 = p21_next - p21
        side_vec_31 = p31_next - p31
        side_vec_41 = p41_next - p41

        side_vec_12 = p12_next - p12
        side_vec_22 = p22_next - p22
        side_vec_32 = p32_next - p32
        side_vec_42 = p42_next - p42

        angle_11 = vector_angle(side_vec_11, vec_1)
        angle_21 = vector_angle(side_vec_21, vec_2)
        angle_31 = vector_angle(side_vec_31, vec_3)
        angle_41 = vector_angle(side_vec_41, vec_4)

        angle_12 = vector_angle(side_vec_12, vec_1)
        angle_22 = vector_angle(side_vec_22, vec_2)
        angle_32 = vector_angle(side_vec_32, vec_3)
        angle_42 = vector_angle(side_vec_42, vec_4)

        angles = [angle_21, angle_42]
        min_angle_idx = np.argmin(angles)
        min_angle = angles[min_angle_idx]

        if min_angle_idx == 0:
            p2_idx1 = next_point_idx(p2_idx1, points1)
            if angle_11 < angle_21:
                p1_idx1 = next_point_idx(p1_idx1, points1)
            if angle_31 < angle_21:
                p3_idx1 = next_point_idx(p3_idx1, points1)
            if angle_41 < angle_21:
                p4_idx1 = next_point_idx(p4_idx1, points1)
            if angle_12 < angle_21:
                p1_idx2 = next_point_idx(p1_idx2, points2)
            if angle_22 < angle_21:
                p2_idx2 = next_point_idx(p2_idx2, points2)
            if angle_32 < angle_21:
                p3_idx2 = next_point_idx(p3_idx2, points2)
        elif min_angle_idx == 1:
            p4_idx2 = next_point_idx(p4_idx2, points2)
            if angle_12 < angle_42:
                p1_idx2 = next_point_idx(p1_idx2, points2)
            if angle_22 < angle_42:
                p2_idx2 = next_point_idx(p2_idx2, points2)
            if angle_32 < angle_42:
                p3_idx2 = next_point_idx(p3_idx2, points2)
            if angle_11 < angle_42:
                p1_idx1 = next_point_idx(p1_idx1, points1)
            if angle_31 < angle_42:
                p3_idx1 = next_point_idx(p3_idx1, points1)
            if angle_41 < angle_42:
                p4_idx1 = next_point_idx(p4_idx1, points1)

        # rotate clockwise by min_angle
        vec_1 = rotate_vec(vec_1, -min_angle)
        vec_2 = rotate_vec(vec_2, -min_angle)
        vec_3 = rotate_vec(vec_3, -min_angle)
        vec_4 = rotate_vec(vec_4, -min_angle)

        angle = angle + min_angle
        counter += 1
        if flag:
            break
