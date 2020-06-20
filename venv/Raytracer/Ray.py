import numpy as np


class Ray(object):

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction / np.linalg.norm(direction)

    def __repr__(self):
        return 'Ray(%s,%s)' % (repr(self.origin), repr(self.direction))

    def pointatparameter(self, t):
        return self.origin + (self.direction * t)
