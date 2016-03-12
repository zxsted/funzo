
import argparse

import matplotlib
matplotlib.use('Qt4Agg')

from matplotlib import pyplot as plt
from joblib import Parallel, delayed

import numpy as np

from funzo.domains.gridworld import GridWorld, GridWorldMDP
from funzo.domains.gridworld import GReward, GTransition
from funzo.planners.dp import PolicyIteration, ValueIteration


def main(map_name, planner):
    print(map_name)
    gmap = np.loadtxt(map_name)
    # gmap[12, 12] = 2

    world = GridWorld(gmap)
    R = GReward(domain=world)
    T = GTransition(domain=world, wind=0.2)

    g = GridWorldMDP(domain=world, reward=R, transition=T, discount=0.6)

    # ------------------------
    mdp_planner = PolicyIteration(verbose=0)
    if planner == 'VI':
        mdp_planner = ValueIteration(verbose=2)

    # res = Parallel(n_jobs=4)(mdp_planner(g))
    res = mdp_planner(g)
    V = res['V']
    print(V)
    # print(res['Q'])
    print(res['pi'])

    fig = plt.figure(figsize=(8, 8))
    ax = fig.gca()
    ax = world.visualize(ax, policy=res['pi'])

    # ------------------------

    plt.figure(figsize=(8, 8))
    plt.imshow(V.reshape(gmap.shape),
               interpolation='nearest', cmap='viridis', origin='lower',
               vmin=np.min(V), vmax=np.max(V))
    plt.title('Value function')
    plt.colorbar()

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--map", type=str, required=True,
                        help="Grid Map file")
    parser.add_argument("-p", "--planner", type=str, default="PI",
                        help="Planner to use: [PI, VI], default: PI")

    args = parser.parse_args()
    main(args.map, args.planner)
