from OpenGL.GL import *
import pygame


class Renderer:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self, core):
        # Ensure the core's camera is set correctly
        core.update_camera()

        # Render each object
        for obj in self.objects:
            obj.draw()
            print("Terrain: Drawn")