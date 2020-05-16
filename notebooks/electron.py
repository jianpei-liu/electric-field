from numpy import *
from pylab import *
from scipy.integrate import ode


class charge:
    def __init__(self, q, pos):
        self.q = q
        self.pos = pos
def E_point_charge(q, a, x, y):
    return q * (x - a[0]) / ((x - a[0]) ** 2 + (y - a[1]) ** 2) ** (1.5), \
           q * (y - a[1]) / ((x - a[0]) ** 2 + (y - a[1]) ** 2) ** (1.5)
def E_total(x, y, charges):
    Ex, Ey = 0, 0
    for C in charges:
        E = E_point_charge(C.q, C.pos, x, y)
        Ex = Ex + E[0]
        Ey = Ey + E[1]
    return [Ex, Ey]
def E_dir(t, y, charges):
    Ex, Ey = E_total(y[0], y[1], charges)
    n = sqrt(Ex ** 2 + Ey * Ey)
    return [Ex / n, Ey / n]


def det_phi(y, charges):
    Ex, Ey = E_total(y[0], y[1], charges)
    n = sqrt(Ex ** 2 + Ey * Ey)
    return [Ex / n, Ey / n]

close('all')
figure(figsize=(6, 6))
charges = [charge(- sqrt(7), [1, 0]), charge(1, [-1, 0])]
x0, x1 = -2, 2
y0, y1 = -2, 2
R = 0.01
num = 0
angle_range = [0,2*pi]
angle_list=[]
for C in charges:
    dt = 0.8 * R
    if C.q < 0:
        dt = -dt
    if angle_range[0]<0:
        e = linspace(angle_range[0], -pi, int((24-num)/2))
        f = linspace(pi,angle_range[1],int((24-num)/2))
        alphas = hstack((e,f))

    else:
        alphas = linspace(angle_range[0], angle_range[1], 24 - num)
    for alpha in alphas:

        r = ode(E_dir)
        r.set_integrator('vode')
        r.set_f_params(charges)
        x = [C.pos[0] + cos(alpha) * R]
        y = [C.pos[1] + sin(alpha) * R]
        r.set_initial_value([x[0], y[0]], 0)
        while r.successful():
            r.integrate(r.t + dt)
            x.append(r.y[0])
            y.append(r.y[1])
            hit_charge = False
            for C2 in charges:
                if sqrt((r.y[0] - C2.pos[0]) ** 2 + (r.y[1] - C2.pos[1]) ** 2) < R:
                    hit_charge = True
                    num = num + 1
                    angle_list.append(r.y)
            if hit_charge or (not (x0 < r.y[0] and r.y[0] < x1)) or \
                    (not (y0 < r.y[1] and r.y[1] < y1)):
                break
        plot(x, y, '-k')
    midd = []
    for i in angle_list:
        thx,thy=det_phi(array(i),charges)
        midd.append(arctan2(thy,thx))
    angle_range=[min(midd),max(midd)]



for C in charges:
    if C.q > 0:
        plot(C.pos[0], C.pos[1], 'bo', ms=8 * sqrt(C.q))
    if C.q < 0:
        plot(C.pos[0], C.pos[1], 'ro', ms=8 * sqrt(-C.q))

xlabel('$x$')
ylabel('$y$')
gca().set_xlim(x0, x1)
gca().set_ylim(y0, y1)
show()