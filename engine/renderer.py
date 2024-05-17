from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import pygame

class Renderer:
    def __init__(self):
        self.objects = []
        print("Renderer: Initialized")

    def add_object(self, obj):
        self.objects.append(obj)
        print("Renderer: Object added")

    def render(self, core):
        frustum = core.calculate_frustum()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for obj in self.objects:
            if core.object_in_frustum(frustum, obj):
                obj.draw()
        pygame.display.flip()
        print("Renderer: Frame rendered")


class Object3D:
    def __init__(self):
        pass

    def draw(self):
        pass