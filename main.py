import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "/..")))
from models.tools import *

if __name__ == '__main__':
    plt.figure(figsize=(5, 5))
    charges = [charge(-1, [-1, 0]), charge(-1, [1, 0]), charge(-1, [0, 1]),charge(3, [0, -1])]
    charges = sorted(charges, key=lambda e: e.q, reverse=True)
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
        angle_ranges = alphas_born(hit_list, C.pos, R)
        for angle_range in angle_ranges:
            alphas = angle_extractor(angle_range, E_range, C.pos, dr, charges, np.pi, np.pi / 6)
            for alpha in alphas:
                point = plot_born(charges, size, C, alpha, R, dt)
                if len(point) > 0:
                    hit_list.append(point)

    plot_charges(charges)
    plt.title('electric-field')
    plt.savefig(r'D:/py/electric-field/-1、-1、-1、3.jpg')
    plt.show()

