from engine.core import Core
from engine.renderer import Renderer
from engine.terrain import Terrain


def main():
    width, height = 800, 600
    core = Core(width, height)

    renderer = Renderer()

    # Procedural terrain
    terrain = Terrain(50, 50)
    renderer.add_object(terrain)

    core.run(renderer)


if __name__ == "__main__":
    main()