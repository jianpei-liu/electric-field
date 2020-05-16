import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import ode
from models.matter import *


def vector(q, pos, x, y):
    """
    :param q: 源电荷
    :param pos: 源点位置
    :param x: 场点x
    :param y: 场点y
    :return: 场点电场强度
    """
    return q * (x - pos[0]) / ((x - pos[0]) ** 2 + (y - pos[1]) ** 2) ** (1.5), \
           q * (y - pos[1]) / ((x - pos[0]) ** 2 + (y - pos[1]) ** 2) ** (1.5)


def vector_total(x, y, charges):
    """
    :param x: 所有的点x
    :param y: 所有的点y
    :param charges: 所有的源电荷
    :return: 所有位置的电场强度
    """
    Ex, Ey = 0, 0
    for C in charges:
        E = vector(C.q, C.pos, x, y)
        Ex = Ex + E[0]
        Ey = Ey + E[1]
    return [Ex, Ey]


# 矢量模长
length = lambda l: np.sqrt(l[0] ** 2 + l[1] ** 2)


def vector_n(x, y, charges):
    """
    所有点的电场大小
    """
    return length(vector_total(x, y, charges))


def vector_dir(t, y, charges):
    """
    被积函数
    """
    Ex, Ey = vector_total(y[0], y[1], charges)
    n = length([Ex, Ey])
    return [Ex / n, Ey / n]


def point_ruler(E_range, pos, charges, degree, dr):
    """
    :param E_range: 场强的极值
    :param pos: 监测点位置
    :param charges: 源电荷
    :param degree: 角度
    :param dr: 监测点半径
    :return: 比例
    """
    down, up = E_range
    x, y = pos
    n = vector_n(dr * np.cos(degree) + x, dr * np.sin(degree) + y, charges)
    with np.errstate(divide='ignore', invalid='ignore'):
        scale = np.true_divide((up - down), (n - down))
    if np.isinf(scale):
        return np.nan
    return scale


def extremum_born(dr, charges, degree_range):
    """
    :param dr: 监测点半径
    :param charges: 源电荷
    :param degree_range: 角度范围
    :return: 场强极值
    """
    down, up = degree_range
    num = int((up - down) / np.pi * 180)
    phi = np.linspace(down, up, num)
    En = vector_n(dr * np.cos(phi), dr * np.sin(phi), charges)
    return [min(En), max(En)]


def angle_extractor(angle_range, E_range, pos, dr, charges, angle_standard, angle_grad):
    """
    :param angle_range: 角度范围
    :param E_range: 场强范围
    :param pos: 起点电荷
    :param dr: 监测点半径
    :param charges: 源电荷
    :param angle_standard: 缩放的标尺
    :param angle_grad: 最小角度间隔
    :return: 绘图起点角度
    """
    down, up = angle_range
    phi = [down]
    i = 0
    while abs(phi[i] - phi[0]) < up - down:
        ratio = point_ruler(E_range, pos, charges, phi[i - 1], dr)
        phi.append(phi[i - 1] + angle_standard * ratio)
        i = i + 1
    i = 1
    while True:
        try:
            if abs(phi[i] - phi[i - 1]) > angle_grad:
                i = i + 1
            else:
                phi.remove(phi[i])
        except IndexError:
            break
    return phi


def alphas_born(ang_list, pos, R):
    """
    :param ang_list:
    :param pos:
    :param R:
    :return: 生成真正的绘图起点
    """
    if len(ang_list) > 0:
        ranges = []
        ang_list = np.array(ang_list) - pos
        ang_list = ang_list.tolist()
        for ang in ang_list:
            if length(ang) > R:
                ang_list.remove(ang)
        degree = map(lambda l: np.arctan2(l[1], l[0]), ang_list)
        degree = list(degree)
        ang_list = sorted(degree)
        print('🛫')
        for ang in range(len(ang_list)):
            try:
                ranges.append([ang_list[ang], ang_list[ang + 1]])
            except IndexError:
                ranges.append([ang_list[ang], np.pi])
                ranges.append([-np.pi, ang_list[0]])
    else:
        ranges = [[-np.pi, np.pi]]
    return ranges


def plot_born(charges, size, Charge, angle, R, dt):
    """
    绘图函数
    """
    r = ode(vector_dir)
    r.set_integrator('vode')
    r.set_f_params(charges)
    C_x, C_y = Charge.pos
    x = [C_x + np.cos(angle) * R]
    y = [C_y + np.sin(angle) * R]
    r.set_initial_value([x[0], y[0]], 0)
    point_list = []
    x0, y0, x1, y1 = size
    while r.successful():
        r.integrate(r.t + dt)
        x.append(r.y[0])
        y.append(r.y[1])
        hit_flag = False
        for Charge2 in charges:
            C2_x, C2_y = Charge2.pos
            if length([r.y[0] - C2_x, r.y[1] - C2_y]) < R:
                hit_flag = True
                point_list = ([r.y[0], r.y[1]])
        if hit_flag or (not (x0 < r.y[0] < x1)) or \
                (not (y0 < r.y[1] < y1)):
            break
    if Charge.q > 0:
        plt.plot(x, y, '-b')
    else:
        plt.plot(x, y, '-r')
    return point_list


def plot_charges(Cs):
    """
    :param Cs:
    :return: 电荷点绘制
    """
    for C in Cs:
        if C.q > 0:
            plt.plot(C.pos[0], C.pos[1], 'bo', ms=8 * np.sqrt(C.q))
        if C.q < 0:
            plt.plot(C.pos[0], C.pos[1], 'ro', ms=8 * np.sqrt(-C.q))
