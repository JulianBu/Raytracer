from Camera import Camera
from StandardMat import StandardMat as sm
from Checkerboard import Checkerboard as cm
from Sphere import Sphere
from Light import Light
from Plane import Plane
from Rectangle import Rectangle
from Ray import Ray
import numpy as np
import multiprocessing as mp
import imageio as im

class Raytracer():


    def __init__(self, shadow, reflection, objectInput, pwid, phei):
        self.shadow = shadow
        self.reflection = reflection
        self.objectInput = objectInput
        self.pwid = pwid
        self.phei = phei

        self.cameraData(self.pwid, self.phei)
        self.cam = Camera(self.e, self.c, self.up, self.fow, self.aspectratio, self.height, self.width)
        self.image = np.zeros((self.height, self.width, 3))
        self.loadColorsAndLight()

        #Erstellen der gewuenschten Objekte
        self.objects = []
        if self.objectInput == 'objects':
            self.loadObjects()
        if self.objectInput == 'squirrel':
            self.loadSquirrel()


    def cameraData(self, width, height):
        self.width = width  # pixel width
        self.height = height  # pixel height
        self.e = np.array([0, 1.8, 10])  # Eye
        self.c = np.array([0, 3, 0])  # Center des Objekts
        self.up = np.array([0, 1, 0])  # Up Vektor zu e
        self.fow = 45  # Field of View
        self.aspectratio = 1  # Aspectratio


    def loadColorsAndLight(self):
        self.rot = sm(np.array([200, 0, 0]), self.reflection)
        self.gruen = sm(np.array([0, 200, 0]), self.reflection)
        self.blau = sm(np.array([0, 0, 200]), self.reflection)
        self.gelb = sm(np.array([200, 200, 0]))
        self.grey2 = sm(np.array([100, 100, 100]), self.reflection)
        self.grey = cm(np.array([200, 200, 200]), np.array([0, 0, 0]))
        self.background_color = np.array([0, 0, 0])
        self.licht = Light(np.array([-30, 30, 10]), np.array([255, 255, 255]))


    def loadObjects(self):
        print("____Load standard Objects____")
        self.objects = [
            Sphere(np.array([0, 5, 1]), 1, self.rot),
            Sphere(np.array([-1.5, 2, 1]), 1, self.gruen),
            Sphere(np.array([1.5, 2, 1]), 1, self.blau),
            Plane(np.array([0,-2,5]), np.array([0,1,0]), self.grey),
            Rectangle(np.array([-1.5,2,1]), np.array([1.5,2,1]), np.array([0,5,1]), self.gelb)
        ]


    def loadSquirrel(self):
        print("____Load the fast Squirrel____")
        file = open('squirrel_aligned_lowres.obj')
        vertices = []
        faces = []
        for lines in file:
            if lines.split()[0] == 'v':
                vertices.append(tuple((-float(lines.split()[1]), float(lines.split()[2]), -float(lines.split()[3]))))
            if lines.split()[0] == 'f':
                faces.append(tuple((int(lines.split()[1]), int(lines.split()[2]), int(lines.split()[3]))))

        self.objects.append(Plane(np.array([0,-2,5]), np.array([0,1,0]), self.grey))
        triscount = 0
        for face in faces:
            self.objects.append(Rectangle(np.array(vertices[face[0]-1]), np.array(vertices[face[1]-1]), np.array(vertices[face[2]-1]), self.grey2))
            triscount += 1

        print(triscount, "Dreiecke erstellt. Starte Rendern.")


    def raytracing(self):
        print("____Start Raycasting____")
        rays = self.cam.calcRays(self.width, self.height)

        thredpool = mp.Pool(mp.cpu_count())
        ergebnis = thredpool.map(self.calcColor, rays) # Erstellen der farben
        thredpool.close()

        i = 0
        for x in range(self.width):
            for y in range(self.height):
                self.image[self.height-y-1][x] = ergebnis[i]
                i += 1

        if self.objectInput == 'objects':
            savestr = 'sheres_Rectangle' + str(self.pwid) + 'x' + str(self.phei) + '.png'
        if self.objectInput == 'squirrel':
            savestr = 'squirrel' + str(self.pwid) + 'x' + str(self.phei) + '.png'

        im.imsave(savestr, self.image)
        print("Image saved as", savestr, "\n____Done____")


    def calcColor(self, ray, level=0, maxlevel=1):
        #für Rekursionsabbruch
        if level > maxlevel:
            return self.background_color

        hit = self.calcIntersection(ray)
        if hit:
            obj, hitdist = hit
        else:
            return self.background_color

        objectColor = obj.mat.colorat(ray.pointatparameter(hitdist))
        phong = self.phongColor(obj, ray, hitdist)
        color = objectColor * phong

        #Schatten
        if self.shadow:
            if self.isInShadows(ray, hitdist):
                color *= 0.4  # Je höher der Wert desto Heller der Schatten

        #Spiegelung
        if self.reflection:
            if obj.mat.spiegeln and level < maxlevel:
                hitpoint = ray.pointatparameter(hitdist)
                dir = ray.direction
                nor = obj.normalat(hitpoint)
                newRay = Ray(hitpoint, dir - 2*np.dot(nor,dir)*nor)
                color += self.calcColor(newRay, level+1)
        return color


    def calcIntersection(self, ray):
        maxdist = float('inf')
        obj = None

        for object in self.objects:
            hitdist = object.intersectionparameter(ray)
            if hitdist and 0 < hitdist < maxdist:
                maxdist = hitdist
                obj = object

        if obj is not None:
            return obj, maxdist
        return None


    def isInShadows(self, ray, hitdist):
        if hitdist == float('inf'):
            return False

        hitpoint = ray.pointatparameter(hitdist)
        nv = self.licht.pos - hitpoint
        nnv = nv / np.linalg.norm(nv)

        lichtRay = Ray(hitpoint, nnv)
        maxdist = self.licht.distance(lichtRay)

        for obj in self.objects:
            hitdist = obj.intersectionparameter(lichtRay)
            if hitdist:
                if 0.001 <= hitdist <= maxdist:
                    return True


    def phongColor(self, obj, ray, hitdist):
        hit = ray.pointatparameter(hitdist)

        #ambienter Anteil ca*ka
        ca = self.licht.color
        ka = obj.mat.ambient
        ambient = ca * ka

        #diffuser Anteil cin*kd*cos(fi)
        cin = ca
        kd = obj.mat.diffuse
        l = (self.licht.pos - hit) / np.linalg.norm(self.licht.pos - hit)
        n = obj.normalat(hit)
        ln = np.dot(l, n)
        if ln <= 0:
            ln = 0
        diffuse = cin * kd * ln

        #specularer Anteil cin*ks*<lr, -d>^n
        ks = obj.mat.specular
        lr = (-l) - (2 * np.dot(-l, n) * n)
        lr = lr / np.linalg.norm(lr)
        d = ray.direction
        lrd = np.dot(lr, -d)
        specular = cin * ks * lrd**obj.mat.oberflache

        phong = ambient + diffuse + specular
        return phong


if __name__ == "__main__":
    schatten = True
    spiegelung = False
    standardObjekte = 'objects'
    squirrel = 'squirrel'
    pwid = 500
    phei = 500
    rt = Raytracer(schatten, spiegelung, squirrel, pwid, phei)
    rt.raytracing()