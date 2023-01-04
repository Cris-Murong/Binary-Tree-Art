import argparse
import modules


def argument():
    parser = argparse.ArgumentParser(description="Binary Tree Art")
    parser.add_argument("-num", default=5, type=int)
    parser.add_argument("-layer", default=10, type=int)

    return parser


if __name__ == "__main__":
    args = argument().parse_args()

    layer = args.layer
    generator = modules.Tree_Generator()
    canvas = modules.Tree_Image((2500, 2500), layer)
    for i in range(args.num):
        node = generator.generate(layer)
        canvas.draw_node(node, (1250, 2375), 300, 0, 30)
        canvas.save_image(f"img/{i}.jpg")
        canvas.clear()
