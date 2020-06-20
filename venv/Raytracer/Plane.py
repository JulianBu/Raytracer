import numpy as np

class Plane(object):
    # Braucht auch noch Material
    def __init__(self, point, normal, mat):
        self.point = point
        self.normal = normal / np.linalg.norm(normal)
        self.mat = mat

    def __repr__(self):
        return 'Ebene(%s,%s)' %(repr(self.point), repr(self.normal))

    def intersectionparameter(self, ray):
        op = ray.origin - self.point
        a = np.dot(op, self.normal)
        b = np.dot(ray.direction, self.normal)
        if b:
            temp = -(a/b)
            if temp > 0:
                return -(a/b)
            else:
                return None
        else:
            return None

    def normalat(self, p):
        return self.normal