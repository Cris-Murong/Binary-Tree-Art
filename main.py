import argparse
import modules
import json


def argument() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Binary Tree Art 2.0")
    parser.add_argument(
        "mode",
        default="img",
        type=str,
        help="img(generate an image)/seq(generate a sequence)",
    )
    parser.add_argument(
        "-render_to",
        default="img/sample.jpg",
        type=str,
        help="address to save rendered image to (default: 'img/sample.jpg')",
    )
    parser.add_argument(
        "-load_from", default="", type=str, help="address to load .json file from"
    )
    parser.add_argument(
        "-dump_to", default="", type=str, help="address to dump .json file to"
    )

    parser.add_argument(
        "-seq_len",
        default=10,
        type=int,
        help="length of sequence [only useful at seq mode]",
    )

    return parser


def setup_tree(args: argparse.Namespace) -> modules.Tree_Node:
    if args.load_from:
        with open(args.load_from, "r") as f:
            data = json.load(f)
            tree = modules.Tree_Node.convert_from_list(data)
    else:
        exp = modules.Exp_Func(
            base=2,
            y_shift=0.85,
            y_stretch=(0.6 - 0.85) / (2**10),
        )
        generator = modules.Tree_Generator(exp)
        tree = generator.generate()
    return tree


if __name__ == "__main__":
    args = argument().parse_args()
    if args.mode == "img":
        tree = setup_tree(args)
        render = modules.Tree_Render((2500, 2500))
        render.render_node(tree, (1250, 2375), 300, 0, 10, "left")
        render.save_image(args.render_to)
        if args.dump_to:
            with open(args.dump_to, "w") as f:
                data = tree.convert_to_list()
                json.dump(data, f)
                print(f"{args.dump_to} saved...")

    if args.mode == "seq":
        tree = setup_tree(args)
        delta_tree_generator = modules.Tree_Generator(
            modules.Exp_Func(base=1, y_shift=-1), 0, 0, 0
        )
        delta_tree = delta_tree_generator.generate(10)
        delta_tree.size = 0
        angle_rand_func = modules.Gaussian_Func(0, 0.1)
        seq_generator = modules.Tree_Sequence(tree, delta_tree, angle_rand_func)
        tree_seq = seq_generator.create_sequence(50, 15)

        render = modules.Tree_Render((2500, 2500))
        dot_index = str(args.render_to).index(".")
        for i, tree in enumerate(tree_seq):
            render.render_node(tree, (1250, 2375), 300, 0, 10, "left")
            render.save_image(
                f"{args.render_to[:dot_index]}{i}{args.render_to[dot_index:]}"
            )
            render.reset()

        if args.dump_to:
            dot_index = str(args.dump_to).index(".")
            for i, tree in enumerate(tree_seq):
                data = tree.convert_to_list()
                file_name = f"{args.dump_to[:dot_index]}{i}{args.dump_to[dot_index:]}"
                with open(file_name, "w") as f:
                    json.dump(data, f)
                    print(f"{file_name} saved...")
