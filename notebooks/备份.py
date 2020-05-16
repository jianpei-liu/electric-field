import numpy as np
from matplotlib import pyplot as plt
from scipy.integrate import ode


class charge:
    def __init__(self, q, pos):
        self.q = q
        self.pos = pos


def vector(q, pos, x, y):
    return q * (x - pos[0]) / ((x - pos[0]) ** 2 + (y - pos[1]) ** 2) ** (1.5), \
           q * (y - pos[1]) / ((x - pos[0]) ** 2 + (y - pos[1]) ** 2) ** (1.5)


def vector_total(x, y, charges):
    Ex, Ey = 0, 0
    for C in charges:
        E = vector(C.q, C.pos, x, y)
        Ex = Ex + E[0]
        Ey = Ey + E[1]
    return [Ex, Ey]


length = lambda l: np.sqrt(l[0] ** 2 + l[1] ** 2)


def vector_n(x, y, charges):  #
    return length(vector_total(x, y, charges))


def vector_dir(t, y, charges):
    Ex, Ey = vector_total(y[0], y[1], charges)
    n = length([Ex, Ey])
    return [Ex / n, Ey / n]


def point_ruler(E_range, pos, charges, degree, dr):
    down, up = E_range
    x, y = pos
    n = vector_n(dr * np.cos(degree) + x, dr * np.sin(degree) + y, charges)
    with np.errstate(divide='ignore', invalid='ignore'):
        scale = np.true_divide((up - down), (n - down))
    if np.isinf(scale):
        return np.nan
    return scale


def extremum_born(dr, charges, degree_range):
    down, up = degree_range
    num = int((up - down) / np.pi * 180)
    phi = np.linspace(down, up, num)
    En = vector_n(dr * np.cos(phi), dr * np.sin(phi), charges)
    return [min(En), max(En)]


def angle_extractor(angle_range, E_range, pos, dr, charges, angle_standard, angle_grad):
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


def plot_born(charges, size, Charge, angle, R, dt):
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
    for C in Cs:
        if C.q > 0:
            plt.plot(C.pos[0], C.pos[1], 'bo', ms=8 * np.sqrt(C.q))
        if C.q < 0:
            plt.plot(C.pos[0], C.pos[1], 'ro', ms=8 * np.sqrt(-C.q))


if __name__ == '__main__':
    plt.figure(figsize=(5, 5))
    charges = [charge(-1, [-1, 0]),  charge(np.sqrt(3), [1, 0])]
    size = [-2, -2, 2, 2]
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(size[0], size[2])
    plt.ylim(size[1], size[-1])
    R = 0.01
    dr = 0.1
    hit_list = []
    for C in charges:
        dt = 0.8 * R
        if C.q < 0:
            dt = -dt
        E_range = extremum_born(dr, charges, degree_range=[0, 2 * np.pi])
        if len(hit_list) > 0 :
            angle_ranges = []
            hit_list = np.array(hit_list)-C.pos
            phi = map(lambda l:np.arctan2(l[1], l[0]), hit_list)
            phi = list(phi)
            hit_list = sorted(phi)
            print('🛫')
            for i in range(len(hit_list)):
                try:
                    angle_ranges.append([hit_list[i], hit_list[i + 1]])
                except IndexError:
                    angle_ranges.append([hit_list[i], np.pi])
                    angle_ranges.append([-np.pi, hit_list[0]])
            for angle_range in angle_ranges:
                alphas = angle_extractor(angle_range, E_range, C.pos, dr, charges, np.pi * 2, np.pi / 6)
                for alpha in alphas:
                    hit_list = plot_born(charges, size, C, alpha, R, dt)
        else:
            angle_range = [-np.pi, np.pi]
            alphas = angle_extractor(angle_range, E_range, C.pos, dr, charges, np.pi, np.pi / 6)
            for alpha in alphas:
                point = plot_born(charges, size, C, alpha, R, dt)
                if len(point)>0:
                    hit_list.append(point)

    plot_charges(charges)
    plt.show()
    plt.title('fuck')
