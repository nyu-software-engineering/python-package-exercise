import argparse
import sys

from pyDeciders import flip_coin, magic_8_ball, pick_one, roll_dice, spin_wheel


def build_parser():
    parser = argparse.ArgumentParser(
        prog="decisions",
        description="Roll dice, flip coins, and spin a wheel.",
    )
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--seed", type=int, default=None)
    commands = parser.add_subparsers(dest="command", required=True)

    dice = commands.add_parser("dice", parents=[common], help="roll dice")
    dice.add_argument("-n", type=int, default=1)
    dice.add_argument("--sides", type=int, default=6)
    dice.set_defaults(run=lambda a: roll_dice(a.n, a.sides, a.seed))

    coin = commands.add_parser("coin", parents=[common], help="flip a coin")
    coin.add_argument("--times", type=int, default=1)
    coin.add_argument("--bias", type=float, default=0.5)
    coin.set_defaults(run=lambda a: flip_coin(a.times, a.bias, a.seed))

    wheel = commands.add_parser("wheel", parents=[common], help="spin a wheel")
    wheel.add_argument("options", nargs="+")
    wheel.add_argument("--weights", type=float, nargs="+", default=None)
    wheel.set_defaults(run=lambda a: spin_wheel(a.options, a.weights, a.seed))

    pick = commands.add_parser("pick", parents=[common], help="pick one option")
    pick.add_argument("options", nargs="+")
    pick.set_defaults(run=lambda a: pick_one(a.options, a.seed))

    ball = commands.add_parser("8ball", parents=[common], help="ask the magic 8 ball")
    ball.add_argument("question")
    ball.set_defaults(run=lambda a: magic_8_ball(a.question, a.seed))

    return parser


def print_result(result):
    if isinstance(result, (list, tuple)):
        print(" ".join(str(item) for item in result))
    else:
        print(result)


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        result = args.run(args)
    except NotImplementedError:
        print(f"decisions: {args.command} is not implemented yet", file=sys.stderr)
        return 1
    except ValueError as error:
        print(f"decisions: {error}", file=sys.stderr)
        return 1
    print_result(result)
    return 0
