import numpy as np
from mayavi import mlab


# TODO 物质类

class charge:
    """
    电荷类
    """

    def __init__(self, q, pos):
        self.q = q
        self.pos = pos


class Matter:
    def __init__(self, quantity, position, mom, coordinate=1):
        self.position = position
        self.quantity = quantity
        self.coordinate = coordinate
        self.mom = mom

    def move(self):
        # TODO 更新下一时间步长的所有必需要力学量
        pass
