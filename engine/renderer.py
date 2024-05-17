from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

class Renderer:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self):
        for obj in self.objects:
            obj.draw()

class Object3D:
    def __init__(self):
        pass

    def draw(self):
        pass