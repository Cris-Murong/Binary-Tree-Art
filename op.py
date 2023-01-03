from copy import deepcopy
from math import cos, pi, sin
from random import uniform
from modules import Tree
from PIL import Image, ImageDraw


def grow(tree: Tree, d_angle: int, angle_shift: float, length_shift: float):
    tree.iter += 1

    values = []
    angles = []
    for n in tree.nodes[-1]:
        for i in [-1, 1]:
            angles.append(
                round(d_angle * uniform(1 - angle_shift, 1 + angle_shift) * i + n.angle)
                % 360
            )
            values.append(round(uniform(1 - length_shift, 1 + length_shift), 3))

    tree.add_layer(values, angles)


def change_angles(tree: Tree, d_angle: int, angle_shift: float):
    lr = -1  # left or right
    for i, iter in enumerate(tree.nodes):
        for n in iter:
            if i == 0:
                continue

            n.angle = (
                round(
                    d_angle * uniform(1 - angle_shift, 1 + angle_shift) * lr + n.angle
                )
                % 360
            )

            lr = 1 if lr == -1 else -1


def save_img(
    tree: Tree, start_coord: tuple[int], size: int, width: int, path: str
) -> None:
    img = Image.new("L", (2500, 2500), (255))
    draw_img = ImageDraw.Draw(img)

    draw_img.line(
        (start_coord, (start_coord[0], start_coord[1] - size)),
        fill=(0),
        width=tree.iter * width,
    )

    last_coords = [(start_coord[0], start_coord[1] - size)]
    for ns in tree.nodes[1:]:
        current_coords = []
        # print(last_coords)
        for i, n in enumerate(last_coords):

            for a in range(2):
                length = ns[i].value * (size // tree.iter * (tree.iter - ns[0].iter))
                x = round(cos(ns[i * 2 + a].angle * pi / 180) * length)
                y = round(sin(ns[i * 2 + a].angle * pi / 180) * length)

                draw_img.line(
                    xy=(n, (n[0] + x, n[1] - y)),
                    fill=(0),
                    width=(tree.iter - ns[0].iter) * width,
                )

                current_coords.append((n[0] + x, n[1] - y))
        last_coords = deepcopy(current_coords)

    img.save(path)
    print(f"{path} saved...")


if __name__ == "__main__":
    tree = Tree()
    for _ in range(12):
        grow(tree, 18, 0.5, 0.2)
        # print(tree)

    save_img(tree, (5000, 9500), 1000, 8)
