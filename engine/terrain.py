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
        print("Terrain: Initialized")

    def generate_terrain(self):
        vertices = []
        colors = []
        indices = []

        # Set the seed for reproducibility
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        # Parameters for Perlin noise
        base_frequency = 0.01
        base_amplitude = 3.0
        octaves = 4
        persistence = 0.4
        lacunarity = 2.0

        self.height_map = np.zeros((self.height * self.resolution, self.width * self.resolution))

        for z in range(self.height * self.resolution):
            for x in range(self.width * self.resolution):
                # Fractal Perlin noise
                y = 0
                amplitude = base_amplitude
                frequency = base_frequency
                for o in range(octaves):
                    y += pnoise2(x * frequency, z * frequency) * amplitude
                    amplitude *= persistence
                    frequency *= lacunarity
                self.height_map[z][x] = y

        half_width = (self.width * self.resolution) / 2.0
        half_height = (self.height * self.resolution) / 2.0

        for z in range(self.height * self.resolution):
            for x in range(self.width * self.resolution):
                y = self.height_map[z][x]
                # Scale and center the vertices
                vertices.append(((x - half_width) / self.resolution, y, (z - half_height) / self.resolution))
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

    def get_height(self, x, z):
        # Get the height of the terrain at the given (x, z) position
        ix = int((x + (self.width / 2)) * self.resolution)
        iz = int((z + (self.height / 2)) * self.resolution)
        if 0 <= ix < self.width * self.resolution and 0 <= iz < self.height * self.resolution:
            return self.height_map[iz][ix]
        return 0.0