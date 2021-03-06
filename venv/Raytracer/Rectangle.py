import numpy as np


class Rectangle(object):
    def __init__(self, a, b, c, mat):
        self.a = a
        self.b = b
        self.c = c
        self.u = self.b - self.a  # Richtungsvektor
        self.v = self.c - self.a  # Richtungsvektor
        self.mat = mat

    def __repr__(self):
        return 'Dreieck(%s,%s,%s)' % (repr(self.a), repr(self.b), repr(self.c))

    def intersectionparameter(self, ray):
        w = ray.origin - self.a
        dv = np.cross(ray.direction, self.v)
        dvu = np.dot(dv, self.u)
        if dvu == 0.0:
            return None
        wu = np.cross(w, self.u)
        r = np.dot(dv, w) / dvu
        s = np.dot(wu, ray.direction) / dvu
        # Prüft ob e in Dreieck liegt
        if 0 <= r <= 1 and 0 <= s <= 1 and r+s <= 1:
            return np.dot(wu, self.v) / dvu
        else:
            return None

    def normalat(self, p):
        temp = np.cross(self.u, self.v)
        return temp / np.linalg.norm(temp)
