import os.path

import numpy as np


def write_polygons(filepath, polygons, comment='Polygons', binary=False):
    """Create a (legacy) VTK file with polygons."""
    extension = ".vtk"  # needs the period
    if os.path.splitext(filepath)[1] != extension:
        filepath += extension
    with open(filepath, 'w') as vtk_file:
        vtk_file.write('# vtk DataFile Version 2.0\n')
        vtk_file.write('%s\n' % comment)
        vtk_file.write('%s\n' % ('BINARY' if binary else 'ASCII'))
        add_polygons_to_vtk(vtk_file, polygons, binary=binary)


def add_polygons_to_vtk(vtk_file, polygons, binary=False):

    if binary:
        raise NotImplementedError('cannot write binary files yet')

    # size up the problem
    nPolygons = len(polygons)
    nPolyPts = np.zeros(nPolygons, dtype=int)
    points = np.empty((0, 2))
    for i in range(nPolygons):
        xy = np.array(polygons[i].exterior.xy).transpose()
        nPolyPts[i] = xy.shape[0]
        points = np.append(points, xy, axis=0)
    nPoints = points.shape[0]
    nPolyPts_ranges = np.insert(np.cumsum(nPolyPts), 0, 0)

    # write to file
    vtk_file.write('DATASET POLYDATA\n')

    # write all point coordinates (2D -> 3D with z=0)
    vtk_file.write('POINTS %d float\n' % nPoints)
    for x, y in points:
        vtk_file.write('%g %g %g\n' % (x, y, 0))

    # write all polygon connectivities
    size = np.sum(nPolyPts)+nPolygons  # dont forget the integer for poly size
    vtk_file.write('POLYGONS %d %d\n' % (nPolygons, size))
    for i in range(nPolygons):
        vtk_file.write('%d' % nPolyPts[i])
        for idx in range(nPolyPts_ranges[i], nPolyPts_ranges[i+1]):
            vtk_file.write(' %d' % idx)
        vtk_file.write('\n')
