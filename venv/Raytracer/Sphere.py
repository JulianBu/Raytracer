import numpy as np
from StandardMat import StandardMat


class Sphere(object):

    def __init__(self, center, raduis, mat):
        self.center = center
        self.radius = raduis
        self.mat = mat


    def __repr__(self):
        return 'Kugel(%s,%s)' %(repr(self.center), repr(self.radius))

    # Schnittpunkt zwischen Kugel und Strahl
    def intersectionparameter(self, ray):
        co = self.center - ray.origin
        v = np.dot(co, ray.direction)  # dot ist skalarprodukt
        discriminant = (v*v) - np.dot(co, co) + (self.radius*self.radius)
        if discriminant < 0:
            return None
        else:
            return v - np.sqrt(discriminant)

    def normalat(self, p):
        return (p - self.center) / np.linalg.norm(p - self.center)

    def colorat(self, p):
        return self.col.farbe

