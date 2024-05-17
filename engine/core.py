import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sin, cos, radians
import numpy as np

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
        print("Core: Initialized")

    def set_projection(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (width / height), 0.1, 100.0)
        print("Core: Projection set")

    def update_camera(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x = self.camera_pos[0] + cos(radians(self.angle_h)) * cos(radians(self.angle_v))
        y = self.camera_pos[1] + sin(radians(self.angle_v))
        z = self.camera_pos[2] + sin(radians(self.angle_h)) * cos(radians(self.angle_v))
        gluLookAt(self.camera_pos[0], self.camera_pos[1], self.camera_pos[2], x, y, z, 0, 1, 0)
        print("Core: Camera updated")

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
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            self.camera_pos[1] -= move_speed

        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        self.angle_h += mouse_dx * 0.1
        self.angle_v -= mouse_dy * 0.1

        # Limit vertical angle to prevent flipping
        self.angle_v = max(-89, min(89, self.angle_v))

        print("Core: Input handled")

    def calculate_frustum(self):
        proj = glGetFloatv(GL_PROJECTION_MATRIX).reshape(4, 4)
        modl = glGetFloatv(GL_MODELVIEW_MATRIX).reshape(4, 4)
        clip = np.dot(modl, proj)

        frustum = np.zeros((6, 4))

        # Extract the numbers for the RIGHT plane
        frustum[0] = [
            clip[3][0] - clip[0][0],
            clip[3][1] - clip[0][1],
            clip[3][2] - clip[0][2],
            clip[3][3] - clip[0][3]
        ]
        t = np.linalg.norm(frustum[0][:3])
        frustum[0] /= t

        # Extract the numbers for the LEFT plane
        frustum[1] = [
            clip[3][0] + clip[0][0],
            clip[3][1] + clip[0][1],
            clip[3][2] + clip[0][2],
            clip[3][3] + clip[0][3]
        ]
        t = np.linalg.norm(frustum[1][:3])
        frustum[1] /= t

        # Extract the BOTTOM plane
        frustum[2] = [
            clip[3][0] + clip[1][0],
            clip[3][1] + clip[1][1],
            clip[3][2] + clip[1][2],
            clip[3][3] + clip[1][3]
        ]
        t = np.linalg.norm(frustum[2][:3])
        frustum[2] /= t

        # Extract the TOP plane
        frustum[3] = [
            clip[3][0] - clip[1][0],
            clip[3][1] - clip[1][1],
            clip[3][2] - clip[1][2],
            clip[3][3] - clip[1][3]
        ]
        t = np.linalg.norm(frustum[3][:3])
        frustum[3] /= t

        # Extract the FAR plane
        frustum[4] = [
            clip[3][0] - clip[2][0],
            clip[3][1] - clip[2][1],
            clip[3][2] - clip[2][2],
            clip[3][3] - clip[2][3]
        ]
        t = np.linalg.norm(frustum[4][:3])
        frustum[4] /= t

        # Extract the NEAR plane
        frustum[5] = [
            clip[3][0] + clip[2][0],
            clip[3][1] + clip[2][1],
            clip[3][2] + clip[2][2],
            clip[3][3] + clip[2][3]
        ]
        t = np.linalg.norm(frustum[5][:3])
        frustum[5] /= t

        print("Core: Frustum calculated")
        return frustum

    def point_in_frustum(self, frustum, x, y, z):
        for p in frustum:
            if p[0] * x + p[1] * y + p[2] * z + p[3] <= 0:
                return False
        return True

    def object_in_frustum(self, frustum, obj):
        min_x, min_y, min_z, max_x, max_y, max_z = obj.get_bounding_box()
        for x in [min_x, max_x]:
            for y in [min_y, max_y]:
                for z in [min_z, max_z]:
                    if self.point_in_frustum(frustum, x, y, z):
                        return True
        return False