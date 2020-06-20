import numpy as np

class StandardMat(object):

    def __init__(self, farbe, spiegeln=False):
        self.farbe = farbe
        self.spiegeln = spiegeln

        self.ambient = 0.4
        self.diffuse = 0.4
        self.specular = 0.2
        self.oberflache = 32

    def colorat(self, p):
        return self.farbe

    def material(self):
        return self.material()