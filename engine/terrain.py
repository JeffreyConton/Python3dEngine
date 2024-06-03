import numpy as np
from noise import pnoise2
import random
from OpenGL.GL import *

class Terrain:
    def __init__(self, width, height, resolution, seed=None):
        self.width = width
        self.height = height
        self.resolution = resolution
        self.seed = seed
        self.vertices, self.colors, self.indices = self.generate_terrain()

    def generate_terrain(self):
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        base_frequency = 0.01
        base_amplitude = 3.0
        octaves = 4
        persistence = 0.4
        lacunarity = 2.0

        width_res = self.width * self.resolution
        height_res = self.height * self.resolution

        height_map = np.zeros((height_res, width_res), dtype=np.float32)
        for z in range(height_res):
            for x in range(width_res):
                y = sum(pnoise2(x * base_frequency * lacunarity**o, z * base_frequency * lacunarity**o) * base_amplitude * persistence**o for o in range(octaves))
                height_map[z, x] = y

        half_width = width_res / 2.0
        half_height = height_res / 2.0

        vertices = np.array([((x - half_width) / self.resolution, height_map[z, x], (z - half_height) / self.resolution) for z in range(height_res) for x in range(width_res)], dtype=np.float32)
        colors = np.array([self.random_pastel_color() for _ in range(height_res * width_res)], dtype=np.float32)
        indices = []

        for z in range(height_res - 1):
            for x in range(width_res - 1):
                top_left = z * width_res + x
                top_right = top_left + 1
                bottom_left = top_left + width_res
                bottom_right = bottom_left + 1
                indices.extend([top_left, bottom_left, top_right, top_right, bottom_left, bottom_right])

        self.height_map = height_map  # Save the height map for collision detection
        return vertices, colors, np.array(indices, dtype=np.uint32)

    def random_pastel_color(self):
        return [(random.random() + 1) / 2 for _ in range(3)] + [1]

    def draw(self):
        glShadeModel(GL_FLAT)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glColorPointer(4, GL_FLOAT, 0, self.colors)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, self.indices)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_VERTEX_ARRAY)
        glShadeModel(GL_SMOOTH)

    def get_height(self, x, z):
        ix = int((x + (self.width / 2)) * self.resolution)
        iz = int((z + (self.height / 2)) * self.resolution)
        if 0 <= ix < self.width * self.resolution and 0 <= iz < self.height * self.resolution:
            return self.height_map[iz][ix]
        return 0.0