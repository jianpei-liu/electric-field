import numpy as np
from mayavi import mlab


class Matter:
    def __init__(self, position, quantity, mom=0, coordinate=1):
        self.position = position
        self.quantity = quantity
        self.coordinate = coordinate
        self.mom = mom

    def move(self):
        # TODO 更新下一时间步长的所有必需要力学量
        pass

class Field:
    def __init__(self, length=32, width=32, height=32, precision=1):
        """
        初始化各个参数
        :param length: 空间的长,默认32,最好是偶数
        :param width: 宽,默认32,最好是偶数
        :param height: 高,默认32,最好是偶数
        :param precision: 精细度,默认1,越小最细腻，越卡顿
        self.space: 描绘空间点
        self.matters: 电荷实例对象
        self.phi: 空间中各点电势
        """
        x = int(length/2)
        y = int(width/2)
        z = int(height/2)
        self.space = np.mgrid[-x:x:precision, -y:y:precision, -z:z:precision]
        self.matters = []
        self.phi = None

    @staticmethod
    def distance(position_1, position_2):
        """
        获得空间中各点与电荷的距离
        :param position_1: 全空间坐标[x,y,z]，多维数组形式，其中x,y,z也是多维数组形式
        :param position_2: 一点坐标[x,y,z], 多维数组形式
        :return: 返回距离
        """
        r_2 = (position_1[0] - position_2[0]) ** 2 + (position_1[1] - position_2[1]) ** 2 + (
                    position_1[2] - position_2[2]) ** 2
        return np.sqrt(r_2)

    def mater_position(self, p):
        """
        将电子实例的坐标转化为多维数组
        :param p: 电荷的坐标，例：(x,y,z)
        :return: 电荷坐标的多维数组
        """
        i, j, k = np.ones(self.space.shape)
        i = i * p[0]
        j = j * p[1]
        k = k * p[2]
        return np.array([i, j, k])

    def update_potential(self):
        """
        更新真空场中各点电势
        空间中各个点的电势,矩阵形式
        """
        for matter in self.matters:
            r = self.distance(self.space, self.mater_position(matter.position))
            with np.errstate(divide='ignore', invalid='ignore'):
                if self.phi is not None:
                    self.phi = self.phi+np.true_divide(matter.quantity, r)
                    self.phi[~np.isfinite(self.phi)] = 0
                else:
                    self.phi = np.true_divide(matter.quantity, r)
                    self.phi[~np.isfinite(self.phi)] = 0

    def add(self, matter):
        """
        向真空场中添加一个电荷
        :param matter:外部电子实例
        :return: 无
        """
        self.matters.append(matter)

    def grad(self):
        return np.gradient(-self.phi)


if __name__ == "__main__":
    a = Matter((-8, 0, 0), +5, 0)
    b = Matter((8, 0, 0), +5, 0)
    field = Field(precision=1)
    field.add(a)
    field.update_potential()
    field.add(b)
    field.update_potential()
    x, y, z = field.space

    u, v, w = field.grad()

    # mlab.quiver3d(x, y, z, u, v, w, mode='2dhooked_arrow', scale_factor=1)
    # u, v, w = field.phi
    # mlab.flow(x, y, z, u, v, w, seedtype='plane', seed_resolution=8, seed_visible=False)
    mlab.flow(x, y, z, u, v, w, seedtype='sphere', seed_resolution=8, seed_visible=True)
    mlab.points3d(-8, 0, 0, scale_factor=1)
    mlab.points3d(8, 0, 0, scale_factor=1)
    mlab.outline()
    mlab.show()
