import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sin, cos, radians

class Core:
    def __init__(self, width, height):
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        glEnable(GL_DEPTH_TEST)
        self.width = width
        self.height = height
        self.camera_pos = [0, 0, -5]
        self.angle_h = 0  # Horizontal angle
        self.angle_v = 0  # Vertical angle
        self.set_projection(width, height)
        self.update_camera()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

    def set_projection(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (width / height), 0.1, 100.0)

    def update_camera(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x = self.camera_pos[0] + cos(radians(self.angle_h)) * cos(radians(self.angle_v))
        y = self.camera_pos[1] + sin(radians(self.angle_v))
        z = self.camera_pos[2] + sin(radians(self.angle_h)) * cos(radians(self.angle_v))
        gluLookAt(self.camera_pos[0], self.camera_pos[1], self.camera_pos[2], x, y, z, 0, 1, 0)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        move_speed = 0.1
        if keys[pygame.K_w]:
            self.camera_pos[0] += move_speed * cos(radians(self.angle_h))
            self.camera_pos[2] += move_speed * sin(radians(self.angle_h))
        if keys[pygame.K_s]:
            self.camera_pos[0] -= move_speed * cos(radians(self.angle_h))
            self.camera_pos[2] -= move_speed * sin(radians(self.angle_h))
        if keys[pygame.K_a]:
            self.camera_pos[0] += move_speed * sin(radians(self.angle_h))
            self.camera_pos[2] -= move_speed * cos(radians(self.angle_h))
        if keys[pygame.K_d]:
            self.camera_pos[0] -= move_speed * sin(radians(self.angle_h))
            self.camera_pos[2] += move_speed * cos(radians(self.angle_h))
        if keys[pygame.K_SPACE]:
            self.camera_pos[1] += move_speed
        if keys[pygame.K_LCTRL]:
            self.camera_pos[1] -= move_speed

        if pygame.event.get_grab():
            center_x, center_y = self.width // 2, self.height // 2
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_dx = mouse_x - center_x
            mouse_dy = mouse_y - center_y

            sensitivity = 0.1
            self.angle_h += mouse_dx * sensitivity
            self.angle_v -= mouse_dy * sensitivity

            self.angle_v = max(-90, min(90, self.angle_v))  # Limit vertical angle to avoid flipping
            self.update_camera()

            pygame.mouse.set_pos((center_x, center_y))

    def run(self, renderer):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.event.set_grab(False)
                    pygame.mouse.set_visible(True)
                if event.type == pygame.MOUSEBUTTONDOWN and not pygame.event.get_grab():
                    pygame.event.set_grab(True)
                    pygame.mouse.set_visible(False)

            self.handle_input()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            renderer.render()
            pygame.display.flip()
            pygame.time.wait(10)

        pygame.quit()