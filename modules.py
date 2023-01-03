class Node:
    def __init__(self, index: int, value: float, angle: int, iter: int) -> None:
        self.index = index
        self.value = value
        self.angle = angle
        self.iter = iter

    def __str__(self) -> str:
        return f"value:{self.value} angle:{self.angle}"

    def __repr__(self) -> str:
        return f"value:{self.value} angle:{self.angle}"


class Tree:
    def __init__(self) -> None:
        self.nodes = [[Node(0, 1, 90, 0)]]
        self.iter = 0

    def add_layer(self, values: list[float], angles: list[int]) -> None:
        self.nodes.append(
            [Node(i, values[i], angles[i], self.iter) for i in range(len(angles))]
        )

    def __str__(self) -> str:
        return str(
            "\n".join(
                [(" ".join([str(n) for n in ns])).center(240, " ") for ns in self.nodes]
            )
        )
