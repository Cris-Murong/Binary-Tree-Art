from modules import Tree
from op import save_img, grow
import argparse


def argument():
    parser = argparse.ArgumentParser(description="Binary Tree Art")
    parser.add_argument("-num", default=5, type=int)
    parser.add_argument("-size", default=12, type=int)

    return parser


if __name__ == "__main__":
    args = argument().parse_args()

    for i in range(args.num):
        tree = Tree()
        for _ in range(args.size):
            grow(tree, 18, 0.2, 1)
            # print(tree)

        save_img(tree, (1250, 2375), 250, 2, f"img/2-{i}.jpg")

# tree = Tree()

# for _ in range(12):
#     grow(tree, 0, 0, 0)
#     # print(tree)
# save_img(tree, (1250, 2375), 250, 2, f"img/ver2/0.jpg")

# for i in range(2, 180, 2):
#     change_angles(tree, 2, 0)
#     save_img(tree, (1250, 2375), 250, 2, f"img/ver2/{i}.jpg")
