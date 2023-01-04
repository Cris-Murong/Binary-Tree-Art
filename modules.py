from dataclasses import dataclass
from random import uniform, random
from math import cos, pi, sin
from PIL import Image, ImageDraw


@dataclass
class Tree_Node:
    size: float
    angle: float
    layer: int
    left: "Tree_Node"
    right: "Tree_Node"
    end: bool = False

    def __str__(self) -> str:
        space = "|" + (" " * 5 + "|") * self.layer
        string = f"{space}size:{self.size} \n{space}angle:{self.angle} \n{space}left:\n{self.left} \n{space}right:\n{self.right}"
        return string.replace("\nNone", " END")


@dataclass
class Exponential:
    base: float
    x_shift: float = 0
    y_shift: float = 0
    x_stretch: float = 1
    y_stretch: float = 1

    def get_y(self, x: float) -> float:
        return (
            self.y_stretch * self.base ** (self.x_stretch * x - self.x_shift)
            + self.y_shift
        )


@dataclass
class Tree_Generator:
    """
    Parameters:
        - size_base - `.base` of `Exponential` for size
        - size_roof - `.y_shift` of `Exponential` for size
        - size_floor - `.y_stretch` of `Exponential` for size
        - brunching_angle - angles derived away from the parent node's `.angle`
        - vary_size - variation of `.size`
        - vary_angle - variation of `.angle`
        - end_rate - chance to stop brunching
    """

    size_base: float = 2.0
    size_roof: float = 0.6
    size_floor: float = 0.85
    brunching_angle: float = 18
    vary_size: float = 0.2
    vary_angle: float = 0.4
    end_rate: float = 0.001

    def generate(
        self,
        layer: int,
        base_size: int = 1,
        base_angle: int = 0,
    ) -> Tree_Node:
        """
        return a base `Tree_Node` of a random tree.

        Parameters:
            - layer - total branching layers
            - size - `.size` of the base `Tree_Node` (= 1)
            - angle - `.angle` of the base `Tree_Node` (= 0)

        Exceptions:
            - layer cannot be < 0
        """
        if layer <= 0:
            raise Exception("parameter 'layer' has to > 0")

        self.size_exp = Exponential(
            base=self.size_base,
            y_shift=self.size_floor,
            y_stretch=(self.size_roof - self.size_floor) / (self.size_base**layer),
        )

        base_node = Tree_Node(base_size, base_angle, 0, None, None)
        self._brunching(base_node, layer)
        return base_node

    def _brunching(self, base_node: Tree_Node, layer: int) -> None:
        """
        brunching the given `base_node`; recursively `_brunching` for every `Tree_Node`, until reach to the `layer`

        Parameters:
            - base_node - update the `.left` and `.right` with children `Tree_Node`s
            - layer - total branching layers
        """
        if layer == 0 or base_node.end:
            return

        nodes: list[Tree_Node] = []
        for i in (-1, 1):
            brunching_size = self.size_exp.get_y(base_node.layer)

            size = round(
                brunching_size
                + brunching_size * uniform(-self.vary_size, self.vary_size),
                3,
            )
            angle = round(
                (
                    self.brunching_angle
                    + self.brunching_angle * uniform(-self.vary_angle, self.vary_angle)
                )
                * i,
                3,
            )

            node = Tree_Node(
                size,
                angle,
                base_node.layer + 1,
                left=None,
                right=None,
                end=random() < self.end_rate,
            )
            self._brunching(node, layer - 1)
            nodes.append(node)
        base_node.left, base_node.right = nodes


class Tree_Image:
    def __init__(
        self,
        image_size: tuple[int],
        layer: int,
        width_base: float = 1.05,
        width_roof: float = 5,
        width_floor: float = 50,
        color_base: float = 1.2,
        color_roof: float = 100,
        color_floor: float = 20,
    ) -> None:
        """
        Parameters:
            - image_size - pixels of the .jpg file (x, y)
            - layer - layers or the `Tree_Node`
            - width_base / color_base - `.base` of `Exponential` for width / color
            - width_roof / color_roof - `.y_shift` of `Exponential` for width / color
            - width_floor / color_floor - `.y_stretch` of `Exponential` for width / color
        """
        self.image_size = image_size
        self.clear()

        self.color_exp = Exponential(
            base=color_base,
            y_shift=color_floor,
            y_stretch=(color_roof - color_floor) / (color_base**layer),
        )

        self.width_exp = Exponential(
            base=width_base,
            y_shift=width_floor,
            y_stretch=(width_roof - width_floor) / (width_base**layer),
        )

    def clear(self) -> None:
        """
        create the new `self.image` and `self.draw_img`
        """
        self.image = Image.new("L", self.image_size, (255))
        self.draw_img = ImageDraw.Draw(self.image)

    def draw_node(
        self,
        node: Tree_Node,
        base_coord: tuple[int],
        base_size: int,
        base_angle: float,
        base_width: int,
    ) -> None:
        """
        draw the given `node` on the `self.draw_img`; recursively `draw_node` for every children node
        """
        size = base_size * node.size
        angle = base_angle + node.angle
        x = base_coord[0] + round(cos((90 - angle) * pi / 180) * size)
        y = base_coord[1] - round(sin((90 - angle) * pi / 180) * size)

        color = round(self.color_exp.get_y(node.layer))
        width = round(self.width_exp.get_y(node.layer))

        self.draw_img.line(
            (base_coord, (x, y)),
            fill=color,
            width=width,
        )

        if node.layer < 3:
            self.draw_img.ellipse(
                (
                    (x - width / 2, y - width / 2),
                    (x + width / 2, y + width / 2),
                ),
                fill=color,
            )

        # recursively call the function for every children
        if node.left:
            self.draw_node(node.left, (x, y), size, angle, base_width)
        if node.right:
            self.draw_node(node.right, (x, y), size, angle, base_width)

    def save_image(self, path: str) -> None:
        """
        save the `self.image` as a .jpg file under the given `path`
        """
        self.image.save(path)
        print(f"{path} saved...")


# if __name__ == "__main__":
