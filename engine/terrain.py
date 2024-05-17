import numpy as np
from noise import pnoise2
from OpenGL.GL import *

class Terrain:
    def __init__(self, width, height, scale=10.0, octaves=6, persistence=0.5, lacunarity=2.0):
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.vertices, self.colors, self.indices = self.generate_terrain()

    def generate_terrain(self):
        vertices = []
        colors = []
        indices = []

        for z in range(self.height):
            for x in range(self.width):
                y = pnoise2(x / self.scale, z / self.scale, octaves=self.octaves, persistence=self.persistence, lacunarity=self.lacunarity) * 10
                vertices.append((x, y, z))
                color = self.get_color(y)
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

        return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32), np.array(indices, dtype=np.uint32)

    def get_color(self, y):
        if y < -5:
            return [0, 0, 1, 1]  # Blue for water
        elif y < 0:
            return [0, 1, 0, 1]  # Green for lowlands
        elif y < 5:
            return [0.5, 0.25, 0, 1]  # Brown for midlands
        else:
            return [1, 1, 1, 1]  # White for highlands

    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glColorPointer(4, GL_FLOAT, 0, self.colors)

        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, self.indices)

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)