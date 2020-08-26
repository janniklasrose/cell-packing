"""Animate packing process."""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from polypacker import PolyPacker, plot_polygons
from polypacker.visualize import update_patch

from demo import make_polys  # ./demo.py


Nframes = 180

def packing():

    polygons0 = make_polys()
    packer = PolyPacker()
    packer.add_polygons(polygons0)

    att, rep = 0.01, 0.05
    polygons = []
    for _ in range(Nframes):
        packer.step(att, rep)
        polygons.append(packer.get_polygons('global'))

    return polygons


def anim():

    polygons = packing()

    fig, ax = plt.subplots()
    patches = plot_polygons(polygons[0], axis=ax)

    def init():
        ax.set_xlim(-2, +2)
        ax.set_ylim(-2, +2)
        ax.set_aspect('equal')
        return patches

    def update(frame):
        return [update_patch(patch, poly) for poly, patch in zip(polygons[frame], patches)]

    ani = FuncAnimation(fig, update, frames=Nframes, init_func=init, blit=True)
    ani.save('animation.mp4', fps=30, dpi=300)


if __name__ == "__main__":
    anim()
