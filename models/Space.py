import numpy as np
import gc


# TODO 废案

class Space:
    def __init__(self, length=32, width=32, precision=1):
        sp = []
        for i in range(length * precision):
            for j in range(width * precision):
                sp.append({"坐标": (i, j)})
        sp = np.array(sp)
        self.sp = sp.reshape(length * precision, width * precision)
        # self.length = length
        # self.width = width
        # self.precision = precision
        del sp
        gc.collect()

    def operator(self, string):
        data = np.array([i[string] for i in self.sp.flatten()])
        if len(data.shape) == 1:
            return data.reshape(self.sp.shape)
        else:
            nddata = []
            for dim in range(len(data.shape[1])):
                middata = np.array([i[dim] for i in data])
                nddata.append(middata)
            nddata = np.array(nddata)
            return nddata

    def append(self, **kwargs):
        name, data = list(kwargs.items())[0]
        for ci, cf in enumerate(data):
            for cj, ce in enumerate(cf):
                self.sp[ci, cj][name] = ce
