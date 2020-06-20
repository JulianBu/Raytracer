import numpy as np

class Checkerboard(object):
    def __init__(self, a, b, spiegeln=False):
        self.base = a # Farbe 1
        self.other = b # Farbe 2
        self.spiegeln = spiegeln # Spiegelung

        self.baseColor = (1,1,1)
        self.otherColor = (0,0,0)
        self.ambient =  1.0
        self.diffuse = 0.6
        self.specular = 0.2
        self.checkSize = 1
        self.oberflache = 32

    def colorat(self, p):
        p = p * (1.0 / self.checkSize)
        t = 0
        for x in p:
            if x == float('inf') or not np.isfinite(x):
                return np.array([255,255,255])
            t += int(abs(x) + 0.5)

        if t % 2:
            return self.other
        return self.base

    def material(self):
        return self.material()
