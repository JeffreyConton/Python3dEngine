from engine.core import Core
from engine.renderer import Renderer
from engine.terrain import Terrain
import pygame
import time
from OpenGL.GL import *

def main():
    width, height = 800, 600
    core = Core(width, height)
    print("Core initialized")

    renderer = Renderer()
    print("Renderer initialized")

    # Increase resolution by setting a higher value
    resolution = 10  # Increased resolution for more detail
    seed = 42  # Fixed seed for reproducibility
    terrain = Terrain(50, 50, resolution, seed)
    core.terrain = terrain  # Pass the terrain to Core
    print("Terrain initialized")
    renderer.add_object(terrain)

    print("Starting main loop")
    running = True
    mouse_grabbed = True

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
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen and depth buffer
            core.update_camera()
            renderer.render(core)
            pygame.display.flip()  # Update the display
            print("Frame rendered")

        time.sleep(0.01)  # Add a small delay to avoid high CPU usage

    pygame.quit()
    print("Program terminated")

if __name__ == "__main__":
    main()