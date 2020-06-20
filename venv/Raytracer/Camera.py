from Ray import Ray
import numpy as np
import math

class Camera(object):


    def __init__(self, e, c, up, fow, aspectratio, wRes, hRes):
        self.e = e
        self.ce = c - e
        # koordinatensystem
        self.f = (c - e) / np.linalg.norm(self.ce)
        self.ce = np.cross(self.f, up)
        self.s = self.ce / np.linalg.norm(self.ce)
        self.u = np.cross(self.s, self.f)
        self.c = c
        self.up = up
        self.fow = fow
        self.aspectratio = aspectratio
        self.a = self.fow / 2
        # Betrachtungsgeometrie
        self.height = 2 * math.tan(self.a)
        self.width = aspectratio * self.height

        self.pixelWidth = self.width / (wRes - 1)
        self.pixelHeight = self.height / (hRes - 1)


    def getRay(self, x, y):
        xcomp = self.s * ((x * self.pixelWidth) - (self.width / 2))
        ycomp = self.u * ((y * self.pixelHeight) - (self.height / 2))
        return Ray(self.e, self.f + xcomp + ycomp)


    def calcRays(self, wRes, hRes):
        rays = []

        # Geht durch alle Pixel durch. Xcomp & YComp sagen wo der Pixel liegt.
        for x in range(wRes):
            for y in range(hRes):
                xcomp = self.s * ((x * self.pixelWidth) - (self.width / 2))
                ycomp = self.u * ((y * self.pixelHeight) - (self.height / 2))
                rays.append(Ray(self.e, self.f + xcomp + ycomp))
        return rays
