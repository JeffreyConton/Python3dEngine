from engine.core import Core
from engine.renderer import Renderer, Object3D


def main():
    width, height = 800, 600
    core = Core(width, height)
    core.set_viewport(width, height)

    renderer = Renderer()

    # Example cube
    vertices = [
        (-1, -1, -1),
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, 1, 1)
    ]

    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]

    cube = Object3D(vertices, edges)
    renderer.add_object(cube)

    core.run(renderer)


if __name__ == "__main__":
    main()