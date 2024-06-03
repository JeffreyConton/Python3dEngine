from engine.core import Core
from engine.renderer import Renderer
from engine.terrain import Terrain
import pygame
import time
from OpenGL.GL import *


def main():
    width, height = 800, 600
    core = Core(width, height)
    renderer = Renderer()

    resolution = 10
    seed = 42
    terrain = Terrain(100, 100, resolution, seed)
    core.terrain = terrain
    renderer.add_object(terrain)

    running = True
    mouse_grabbed = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mouse_grabbed = not mouse_grabbed
                    pygame.event.set_grab(mouse_grabbed)
                    pygame.mouse.set_visible(not mouse_grabbed)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not mouse_grabbed:
                    mouse_grabbed = True
                    pygame.event.set_grab(mouse_grabbed)
                    pygame.mouse.set_visible(not mouse_grabbed)

        if mouse_grabbed:
            core.handle_input()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            core.update_camera()
            renderer.render(core)
            pygame.display.flip()

            # Debugging information
            fps = clock.get_fps()
            print(f"FPS: {fps:.2f}, Vertices: {terrain.vertices.shape[0]}, Faces: {len(terrain.indices) // 3}")

        clock.tick(60)  # Cap the frame rate at 60 FPS

    pygame.quit()


if __name__ == "__main__":
    main()