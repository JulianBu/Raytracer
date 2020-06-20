import numpy as np

class Light(object):

    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

    def distance(self, ray):
        return (self.pos[0] - ray.origin[0]) / ray.direction[0]