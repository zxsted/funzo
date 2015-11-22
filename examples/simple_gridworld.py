

from matplotlib import pyplot as plt

import numpy as np

from pylfd.domains.gridworld import GridWorld, GTransition
from pylfd.utils.data_structures import ValueFunction, Policy, QFunction
from pylfd.planners.exact import value_iteration


def main():
    gmap = [
        [1, 0, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 2],
        # [0, 0, 1, 0]
    ]
    g = GridWorld(gmap)

    fig = plt.figure()
    ax = fig.gca()

    ax = g.visualize(ax)

    # ------------------------
    print(g.A)
    print(g.S)

    controller = GTransition(g, 0.3)
    print(g.S[0])
    print(controller(0, 2))

    res = value_iteration(g)
    print(res['V'])
    print(res['Q'])
    print(res['pi'])

    plt.show()


if __name__ == '__main__':
    main()
