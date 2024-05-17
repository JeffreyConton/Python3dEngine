import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class Core:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera_position = np.array([0.0, 1.0, 0.0], dtype=np.float32)  # Start at (0, 0, 0) with height 1
        self.camera_rotation = np.array([0.0, 0.0], dtype=np.float32)  # pitch, yaw
        self.movement_speed = 0.1
        self.mouse_sensitivity = 0.1
        self.gravity = 0.01
        self.jump_speed = 0.2
        self.vertical_velocity = 0.0
        self.on_ground = False
        self.terrain = None  # To be set externally

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        # OpenGL settings
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.update_projection_matrix()

    def update_projection_matrix(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, self.width / self.height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        movement = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        if keys[pygame.K_w]:
            movement[2] += self.movement_speed  # Changed from -= to +=
        if keys[pygame.K_s]:
            movement[2] -= self.movement_speed  # Changed from += to -=
        if keys[pygame.K_a]:
            movement[0] += self.movement_speed  # Changed from -= to +=
        if keys[pygame.K_d]:
            movement[0] -= self.movement_speed  # Changed from += to -=
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vertical_velocity = self.jump_speed
            self.on_ground = False

        # Apply movement
        forward_vector = self.get_forward_vector() * movement[2]
        right_vector = self.get_right_vector() * movement[0]
        self.camera_position += forward_vector + right_vector

        # Apply gravity
        self.vertical_velocity -= self.gravity
        self.camera_position[1] += self.vertical_velocity

        # Collision detection with the terrain
        self.check_collision()

        # Handle mouse movement
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        self.camera_rotation[1] -= mouse_dx * self.mouse_sensitivity
        self.camera_rotation[0] -= mouse_dy * self.mouse_sensitivity
        self.camera_rotation[0] = np.clip(self.camera_rotation[0], -90.0, 90.0)

        # Debug prints
        print(f"Camera Position: {self.camera_position}, Rotation: {self.camera_rotation}")

    def get_forward_vector(self):
        yaw_rad = np.radians(self.camera_rotation[1])
        pitch_rad = np.radians(self.camera_rotation[0])
        return np.array([
            np.cos(pitch_rad) * np.sin(yaw_rad),
            np.sin(pitch_rad),
            np.cos(pitch_rad) * np.cos(yaw_rad)
        ], dtype=np.float32)

    def get_right_vector(self):
        yaw_rad = np.radians(self.camera_rotation[1])
        return np.array([
            np.cos(yaw_rad),
            0,
            -np.sin(yaw_rad)
        ], dtype=np.float32)

    def check_collision(self):
        if self.terrain:
            terrain_height = self.terrain.get_height(self.camera_position[0], self.camera_position[2])
            if self.camera_position[1] < terrain_height + 1.0:  # Adjust the offset as needed
                self.camera_position[1] = terrain_height + 1.0
                self.vertical_velocity = 0.0
                self.on_ground = True

    def update_camera(self):
        glLoadIdentity()
        pitch, yaw = self.camera_rotation
        x, y, z = self.camera_position
        look_at = self.camera_position + self.get_forward_vector()
        gluLookAt(x, y, z, look_at[0], look_at[1], look_at[2], 0, 1, 0)

    def calculate_frustum(self):
        # Calculate the view frustum
        pass

    def object_in_frustum(self, frustum, obj):
        # Check if an object is within the view frustum
        return True  # Simplified for now