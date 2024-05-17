import numpy as np
from noise import pnoise2
from OpenGL.GL import *
from math import sin, cos
import random

class Terrain:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.vertices, self.colors, self.indices = self.generate_terrain()
        print("Terrain: Initialized")

    def generate_terrain(self):
        vertices = []
        colors = []
        indices = []

        for z in range(self.height):
            for x in range(self.width):
                # Generate a cool wave pattern for terrain height
                y = sin(x * 0.2) * cos(z * 0.2) * 5  # Adjusted for a more interesting pattern
                vertices.append((x, y, z))
                color = self.random_pastel_color()
                colors.append(color)

        for z in range(self.height - 1):
            for x in range(self.width - 1):
                top_left = z * self.width + x
                top_right = top_left + 1
                bottom_left = top_left + self.width
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