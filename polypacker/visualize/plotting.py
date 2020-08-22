import matplotlib.pyplot as plt


def plot_polygon(polygon, axis=None, **kwargs):
    """Plot a single polygon as a filled patch.
    Use kwargs to pass any instruction valid for pyplot.patches.
    """
    p = plot_polygons([polygon], axis, **kwargs)
    return p[0]  # p is of length 1


def plot_polygons(polygons, axis=None, **kwargs):
    """Plot a list of polygons as filled patches.
    Use kwargs to pass any instruction valid for pyplot.patches.
    """
    xyxy = [coord for polygon in polygons for coord in polygon.exterior.xy]
    p = (axis if axis is not None else plt.gca()).fill(*xyxy, **kwargs)
    return p
