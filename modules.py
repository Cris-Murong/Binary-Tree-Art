from dataclasses import dataclass
from random import uniform, random, randint
from math import cos, pi, sin, e, sqrt
from PIL import Image, ImageDraw
from copy import deepcopy
from typing import Callable

# TODO float problem


@dataclass
class Tree_Node:
    size: float
    angle: float
    color: tuple[int]
    layer: int
    left: "Tree_Node"
    right: "Tree_Node"
    # dead: bool = False

    ## read and save
    def convert_to_list(self) -> dict:

        if self.left != None:
            left = self.left.convert_to_list()
        else:
            left = None
        if self.right != None:
            right = self.right.convert_to_list()
        else:
            right = None

        return {
            "size": self.size,
            "angle": self.angle,
            "color": self.color,
            "layer": self.layer,
            "left": left,
            "right": right,
        }

    def get_largest_layer(self) -> int:
        """return the largest layer number"""
        if self.left:
            return self.left.get_largest_layer()
        return self.layer

    @classmethod
    def convert_from_list(cls, data: dict) -> "Tree_Node":
        if data["left"]:
            left = cls.convert_from_list(data["left"])
        else:
            left = None
        if data["right"]:
            right = cls.convert_from_list(data["right"])
        else:
            right = None

        return cls(
            data["size"],
            data["angle"],
            (data["color"][0], data["color"][1], data["color"][2]),
            data["layer"],
            left,
            right,
        )

    def __str__(self) -> str:
        space = "|" + (" " * 5 + "|") * self.layer
        string = f"{space}size:{self.size} \n{space}angle:{self.angle} \n{space}left:\n{self.left} \n{space}right:\n{self.right}"
        return string.replace("\nNone", " END")


@dataclass
class Exp_Func:
    """
    y_stretch * base ^ (x_stretch * x - x_shift) + y_shift
    """

    base: float = e
    x_shift: float = 0
    y_shift: float = 0
    x_stretch: float = 1
    y_stretch: float = 1

    def find_y(self, x: float) -> float:
        """
        return the y of the given `x`
        """
        return (
            self.y_stretch * self.base ** (self.x_stretch * x - self.x_shift)
            + self.y_shift
        )


@dataclass
class Sine_Func:
    """
    y_stretch * sin(x_stretch * x - x_stretch) + y_shift
    """

    x_shift: float = 0
    y_shift: float = 0
    x_stretch: float = 1
    y_stretch: float = 1

    def find_y(self, x: float) -> float:
        """
        return the y of the given `x`
        """
        return self.y_stretch * sin(self.x_stretch * x - self.x_stretch) + self.y_shift


class Gaussian_Func:
    def __init__(self, mean: float, variance: float) -> None:
        self.variance = variance
        self.mean = mean
        # std * -3 ... std * 3
        cand_min = mean - variance * 3
        cand_range = variance * 6
        cand_step = cand_range / 18
        self.candidates = [cand_min + i * cand_step for i in range(18)]
        unweighed_pos = [self.find_y(n) for n in self.candidates]
        self.pos = self.weight_pos(unweighed_pos)

    @staticmethod
    def weight_pos(unweighed_pos: list[float]) -> list[float]:
        """weight the given unweighed possibility list"""
        total = sum(unweighed_pos)
        return [n / total for n in unweighed_pos]

    def find_y(self, x: float) -> float:
        """
        return the y of the given `x`
        """
        return (1 / (self.variance * sqrt(2 * pi))) * e ** (
            -1 / 2 * ((x - self.mean) / self.variance) ** 2
        )

    def random(self) -> float:
        rand = random()
        for i, n in enumerate(self.pos):
            rand -= n
            if rand <= 0:
                return self.candidates[i]


class Color_Convert:
    @staticmethod
    def rgb_to_hsl(r: int, g: int, b: int) -> tuple[int]:
        r /= 256
        g /= 256
        b /= 256

        c_max = max(r, g, b)
        c_min = min(r, g, b)
        d = c_max - c_min

        if d == 0:
            h = 0
        elif c_max == r:
            h = 60 * ((g - b) / d % 6)
        elif c_max == g:
            h = 60 * ((b - r) / d + 2)
        elif c_max == b:
            h = 60 * ((r - g) / d + 4)

        l = round((c_max + c_min) / 2, 2)

        if l == 0:
            s = 0
        else:
            s = d / (1 - abs(2 * l - 1))

        return (round(h), round(s, 3), round(l, 3))

    @staticmethod
    def hsl_to_rgb(h, s, l) -> tuple[int]:
        c = (1 - abs(2 * l - 1)) * s
        x = c * (1 - abs(h / 60 % 2 - 1))
        m = l - c / 2

        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        return (round((r + m) * 256), round((g + m) * 256), round((b + m) * 256))


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

    size_exp: Exp_Func
    # size_base: float = 2.0
    # size_roof: float = 0.6
    # size_floor: float = 0.85
    brunching_angle: float = 18
    vary_size: float = 0.2
    vary_angle: float = 0.4
    set_color: tuple[int] = None
    # end_rate: float = 0.001

    def generate(
        self,
        layer: int = 10,
    ) -> Tree_Node:
        """
        return a base `Tree_Node` of a random tree.

        Parameters:
            - layer - total branching layers

        Exceptions:
            - layer cannot be < 0
        """
        if layer <= 0:
            raise Exception("parameter 'layer' has to > 0")

        # self.size_exp = Exp_Func(
        #     base=self.size_base,
        #     y_shift=self.size_floor,
        #     y_stretch=(self.size_roof - self.size_floor) / (self.size_base**layer),
        # )
        if self.set_color:
            color = self.set_color
        else:
            color = (randint(0, 225), randint(0, 225), randint(0, 225))

        base_node = Tree_Node(1, 0, color, 0, left=None, right=None)

        self._brunching(base_node, layer, True)
        self._brunching(base_node, layer, False)

        return base_node

    def _brunching(
        self,
        node: Tree_Node,
        layer: int,
        brunch_left: bool,
    ) -> None:
        """
        brunching the given `base_node`; recursively `_brunching` for every `Tree_Node`, until reach to the given `layer`

        Parameters:
            - base_node - update the `.left` and `.right` with children `Tree_Node`s
            - layer - total branching layers
        """
        if layer == 0:  # base case
            return

        brunching_size = self.size_exp.find_y(node.layer)

        size = round(
            brunching_size + brunching_size * uniform(-self.vary_size, self.vary_size),
            3,
        )
        angle = round(
            (
                self.brunching_angle
                + self.brunching_angle * uniform(-self.vary_angle, self.vary_angle)
            )
            * (-1 if brunch_left else 1),
            3,
        )

        if self.set_color:
            color = self.set_color
        else:
            color = (randint(0, 225), randint(0, 225), randint(0, 225))

        child_node = Tree_Node(
            size,
            angle,
            color,
            node.layer + 1,
            left=None,
            right=None,
        )

        # brunch left
        self._brunching(child_node, layer - 1, True)
        # brunch right
        self._brunching(child_node, layer - 1, False)

        # nodes.append(node)
        if brunch_left:
            node.left = child_node
        else:
            node.right = child_node


# class Tree_Transformer:
class Tree_Sequence:
    def __init__(
        self,
        tree: Tree_Node,
        delta_tree: Tree_Node,
        rand_func: Gaussian_Func,
    ) -> None:
        self.tree = tree
        # self._convert_color_type(self.tree, Color_Convert.rgb_to_hsl)
        self.delta_tree = delta_tree
        self.rand_func = rand_func

    def create_sequence(self, frame_num: int, frame_len: int) -> list[Tree_Node]:
        data = []
        for i in range(frame_num):
            self._rand_d_tree_attr(self.delta_tree, "angle")
            for _ in range(frame_len):
                self._tree_attr_adder(self.tree, self.delta_tree, "angle")
                data.append(deepcopy(self.tree))

        return data

    def _rand_d_tree_attr(self, delta_tree: Tree_Node, attr_name: str):
        """adds a random value from `rand_func` to `attr_name` in `delta_tree`"""
        # input(delta_tree.size)
        rand = self.rand_func.random() - delta_tree.size
        delta_tree.__dict__[attr_name] += rand
        delta_tree.size += rand

        if delta_tree.left:
            self._rand_d_tree_attr(delta_tree.left, attr_name)
            self._rand_d_tree_attr(delta_tree.right, attr_name)

    def _tree_attr_adder(
        self, tree: Tree_Node, delta_tree: Tree_Node, attr_name: str
    ) -> None:
        """adds value of `attr_name` in `delta_tree` to `tree`"""
        tree.__dict__[attr_name] += delta_tree.__dict__[attr_name]

        if tree.left:
            self._tree_attr_adder(tree.left, delta_tree.left, attr_name)
            self._tree_attr_adder(tree.right, delta_tree.right, attr_name)

    # def apply_color_rule(self, color_rule: Sine_Func) -> None:
    #     """apply color rule to sequence"""
    #     print("applying the color rule...")
    #     for i in range(self.length):
    #         value = color_rule.find_y(i)
    #         self._color_adder(self.data[i], value)
    #         self._convert_color_type(self.data[i], Color_Convert.hsl_to_rgb)

    # def apply_angle_rule(self, angle_rule: Sine_Func, filter: Exp_Func) -> None:
    #     """apply angle rule to sequence"""
    #     print("applying the angle rule...")
    #     for i in range(self.length):
    #         value = angle_rule.find_y(i)

    #         self._tree_attr_adder(self.data[i], "angle", value, filter)

    # def _convert_color_type(self, tree: Tree_Node, converter: Callable) -> None:
    #     """converts every node in `tree` to hsl or rgb color format (recursive)"""
    #     x, y, z = tree.color
    #     tree.color = converter(x, y, z)

    #     if tree.left:
    #         self._convert_color_type(tree.left, converter)
    #         self._convert_color_type(tree.right, converter)

    # def _color_adder(self, tree: Tree_Node, value: float) -> None:
    #     """adds `value` to every node in `tree`"""
    #     h, s, l = tree.color
    #     h += value
    #     tree.color = (h, s, l)

    #     if tree.left:
    #         self._color_adder(tree.left, value)
    #         self._color_adder(tree.right, value)


class Tree_Render:
    def __init__(
        self,
        image_size: tuple[int],
        layer: int = 10,
        width_base: float = 1.01,
        width_roof: float = 0.5,
        width_floor: float = 30,
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
        self.reset()

        self.color_exp = Exp_Func(
            base=color_base,
            y_shift=color_floor,
            y_stretch=(color_roof - color_floor) / (color_base**layer),
        )

        self.width_exp = Exp_Func(
            base=width_base,
            y_shift=width_floor,
            y_stretch=(width_roof - width_floor) / (width_base**layer),
        )

    def reset(self) -> None:
        """
        create the new `self.image` and `self.draw_img`
        """
        self.image = Image.new("RGB", self.image_size, (0, 0, 0))
        self.draw_img = ImageDraw.Draw(self.image)

    def render_node(
        self,
        node: Tree_Node,
        base_coord: tuple[int],
        base_size: int,
        base_angle: float,
        base_width: int,
        direction: str,
    ) -> None:
        """
        draw the given `node` on the `self.draw_img`; recursively `draw_node` for every children node
        """
        size = base_size * node.size
        angle = base_angle + node.angle
        x = base_coord[0] + round(cos((90 - angle) * pi / 180) * size)
        y = base_coord[1] - round(sin((90 - angle) * pi / 180) * size)

        color = node.color
        width = round(self.width_exp.find_y(node.layer) * base_width)

        self.draw_img.line(
            (base_coord, (x, y)),
            fill=color,
            width=width,
        )

        # if node.layer < 3:
        #     self.draw_img.ellipse(
        #         (
        #             (x - width / 2, y - width / 2),
        #             (x + width / 2, y + width / 2),
        #         ),
        #         fill=color,
        #     )
        # recursively call the function for every children
        # from left
        if direction == "left":
            if node.left:
                self.render_node(node.left, (x, y), size, angle, base_width, "left")
                self.render_node(node.right, (x, y), size, angle, base_width, "right")
        # from right
        if direction == "right":
            if node.right:
                self.render_node(node.right, (x, y), size, angle, base_width, "right")
                self.render_node(node.left, (x, y), size, angle, base_width, "left")

    def save_image(self, path: str) -> None:
        """
        save the `self.image` as a .jpg file under the given `path`
        """
        self.image.save(path)
        print(f"{path} saved...")


if __name__ == "__main__":
    # h, s, l = Color_Convert.rgb_to_hsl(200, 20, 100)
    # print(h, s, l)
    # print(Color_Convert.hsl_to_rgb(h, s, l))
    # generator = Tree_Generator()
    # base_node = generator.generate(2)
    # print(base_node)
    func = Gaussian_Func(0, 3)
    generator = Tree_Generator()
    node = generator.generate(2)
    print(node)
