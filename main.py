from engine.core import Core
from engine.renderer import Renderer
from engine.terrain import Terrain
import pygame
import time

def main():
    width, height = 800, 600
    core = Core(width, height)
    print("Core initialized")

    renderer = Renderer()
    print("Renderer initialized")

    # Procedural terrain
    terrain = Terrain(50, 50)
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
            core.update_camera()
            renderer.render(core)
            print("Frame rendered")

        time.sleep(0.01)  # Add a small delay to avoid high CPU usage

    pygame.quit()
    print("Program terminated")

if __name__ == "__main__":
    main()