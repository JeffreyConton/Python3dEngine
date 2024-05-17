import numpy as np
from noise import pnoise2
from OpenGL.GL import *
from math import sin, cos
import random

class Terrain:
    def __init__(self, width, height, resolution, seed=None):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.seed = seed
        self.vertices, self.colors, self.indices = self.generate_terrain()
        print("Terrain: Initialized")

    def generate_terrain(self):
        vertices = []
        colors = []
        indices = []

        # Set the seed for reproducibility
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        frequency = 0.1
        amplitude = 1.0
        octaves = 6

        height_map = np.zeros((self.height * self.resolution, self.width * self.resolution))
        gradient_map = np.zeros((self.height * self.resolution, self.width * self.resolution))

        for z in range(self.height * self.resolution):
            for x in range(self.width * self.resolution):
                y = 0
                for o in range(octaves):
                    freq = frequency * (2 ** o)
                    amp = amplitude * (0.5 ** o)
                    y += pnoise2(x * freq / self.resolution, z * freq / self.resolution) * amp
                height_map[z][x] = y

        for z in range(1, self.height * self.resolution - 1):
            for x in range(1, self.width * self.resolution - 1):
                height_center = height_map[z][x]
                height_right = height_map[z][x + 1]
                height_left = height_map[z][x - 1]
                height_up = height_map[z + 1][x]
                height_down = height_map[z - 1][x]

                gradient_x = (height_right - height_left) / 2
                gradient_z = (height_up - height_down) / 2
                gradient = np.sqrt(gradient_x ** 2 + gradient_z ** 2)

                gradient_map[z][x] = gradient

        max_gradient = np.max(gradient_map)

        for z in range(self.height * self.resolution):
            for x in range(self.width * self.resolution):
                y = height_map[z][x]
                gradient = gradient_map[z][x]
                y *= 1 - (gradient / max_gradient) ** 2  # Gradient trick to smooth the heights
                vertices.append((x / self.resolution, y, z / self.resolution))
                color = self.random_pastel_color()
                colors.append(color)

        for z in range(self.height * self.resolution - 1):
            for x in range(self.width * self.resolution - 1):
                top_left = z * self.width * self.resolution + x
                top_right = top_left + 1
                bottom_left = top_left + self.width * self.resolution
                bottom_right = bottom_left + 1

                indices.append(top_left)
                indices.append(bottom_left)
                indices.append(top_right)

                indices.append(top_right)
                indices.append(bottom_left)
                indices.append(bottom_right)

        print("Terrain: Vertices, colors, and indices generated")
        return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32), np.array(indices, dtype=np.uint32)

    def random_pastel_color(self):
        # Generate random pastel colors
        r = (random.random() + 1) / 2
        g = (random.random() + 1) / 2
        b = (random.random() + 1) / 2
        return [r, g, b, 1]

    def draw(self):
        glShadeModel(GL_FLAT)  # Enable flat shading

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glColorPointer(4, GL_FLOAT, 0, self.colors)

        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, self.indices)

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)

        glShadeModel(GL_SMOOTH)  # Reset to smooth shading after drawing
        print("Terrain: Drawn")

    def get_bounding_box(self):
        # Return the min and max coordinates for x, y, z
        return 0, -5, 0, self.width, 5, self.height