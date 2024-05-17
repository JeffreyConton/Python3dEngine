import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sin, cos, radians  # Add this line

class Core:
    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)
        self.width = width
        self.height = height
        self.angle_h = 0  # Horizontal angle
        self.angle_v = 0  # Vertical angle
        self.set_projection(width, height)
        self.set_modelview()

    def set_projection(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (width / height), 0.1, 50.0)

    def set_modelview(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, -5, 0, 0, 0, 0, 1, 0)

    def set_viewport(self, width, height):
        glViewport(0, 0, width, height)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle_h -= 1
        if keys[pygame.K_RIGHT]:
            self.angle_h += 1
        if keys[pygame.K_UP]:
            self.angle_v -= 1
        if keys[pygame.K_DOWN]:
            self.angle_v += 1

        self.angle_v = max(-90, min(90, self.angle_v))  # Limit vertical angle to avoid flipping
        self.update_camera()

    def update_camera(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x = 5 * cos(radians(self.angle_h)) * cos(radians(self.angle_v))
        y = 5 * sin(radians(self.angle_v))
        z = 5 * sin(radians(self.angle_h)) * cos(radians(self.angle_v))
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)

    def run(self, renderer):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            renderer.render()
            pygame.display.flip()
            pygame.time.wait(10)

        pygame.quit()