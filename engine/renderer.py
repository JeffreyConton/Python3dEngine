from OpenGL.GL import *
import pygame

class Renderer:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self, core):
        core.update_camera()
        for obj in self.objects:
            obj.draw()