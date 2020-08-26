"""Demonstrate usage of polypacker."""

import time

import matplotlib.pyplot as plt

from polypacker import PolyPacker, CLI, GUI, write_polygons


def make_polys():
    square = [(-.5,-.5), (.5,-.5), (.5,.5), (-.5,.5)]
    diamond = [(0,-.5), (.5,0), (0,.5), (-.5,0)]
    triangle = [(-.5,-.5), (.5,-.5), (0,.5)]
    circle = [(0,-.5), (.35,-.35), (.5,0), (.35,.35), (0,.5), (-.35,.35), (-.5,0), (-.35,-.35)]
    shapes = [square, diamond, triangle, circle]
    polys = []
    for shape, (dx, dy) in zip(shapes, [(-.8,-1.), (-1,+.8), (+1.2,-1), (+1,+1.2)]):
        polys.append([(x+dx, y+dy) for x,y in shape])
    return polys


def run():

    packer = PolyPacker()
    packer.add_polygons(make_polys())

    Nsteps = 200
    update_every = 5
    cli, gui = CLI(Nsteps, update_every), GUI(Nsteps, update_every)
    cli.init()
    gui.init(packer.get_polygons('global'))

    for i in range(Nsteps):
        packer.step(0.01, 0.2)
        plt.pause(0.05)  # simulate a more computationally expensive step

        density = i/Nsteps
        collisions = i**2
        cli.do_update(i, None, density, collisions)
        gui.do_update(i, packer.get_polygons('global'), density, collisions)
        if cli.was_stopped or gui.was_stopped:
            print("User-terminated stop")
            break

    write_polygons('demo.vtk', packer.get_polygons('global'))
    gui._fig.savefig('demo.png', dpi=300)

    plt.ioff()  # otherwise won't halt
    plt.show()  # keep figure open


if __name__ == "__main__":
    run()
