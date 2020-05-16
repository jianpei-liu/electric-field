import numpy as np


# TODO 场空间的类

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
        x = int(length / 2)
        y = int(width / 2)
        z = int(height / 2)
        self.space = np.mgrid[-x:x:precision, -y:y:precision, -z:z:precision]
        self.matters = []
        self.phi = None

    def potential(self):
        # TODO 计算此时的全空间各点的电势
        pass

    def update_matter(self):
        # TODO 更新场内所有电荷的力学量
        pass

    def AMR(self):
        # TODO 自适应网格细化
        pass


def yanhuafangc():
    # TODO 演化方程
    pass
