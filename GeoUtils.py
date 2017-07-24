import csv
import re
import matplotlib.path as mplPath
import itertools
from pandas import read_csv
import numpy as np


class Plane:
    def __init__(self, id, max_rad, min_rad, cells, edges):
        self.id = id
        self.min_rad = min_rad
        self.max_rad = max_rad
        self.cells = cells
        self.edges = edges

    def is_contain(self, p_x, p_y):
        rad = (p_x ** 2 + p_y ** 2) ** 0.5

        if self.min_rad < rad < self.max_rad:
            return True
        else:
            return any([e.is_contains(p_x, p_y) for e in self.edges])


class Cell:
    def __init__(self, coordinates, full, large, edge):
        self.coordinates = coordinates
        self.full = full
        self.large = large
        self.edge = edge

    def is_contain(self, p_x, p_y):
        return self.coordinates.contains_point((p_x, p_y))


def get_plane_indices(file):
    indices = {line_no: line for line_no, line in enumerate(file) if re.search('[a-zA-Z]+', line) is None}

    return indices


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def read_plane(geometry_file, plane_details, start, end):
    plane_details = [float(i) for i in plane_details.split()]
    plane_id, max_rad, min_rad = plane_details[0], plane_details[2], plane_details[3]

    cells, edges = []
    df = read_csv(geometry_file, sep=' ', skiprows=lambda x: x not in range(start + 1, end), nrows=end - start,
                  names=['flag', 'num', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'x5', 'y5', 'x6', 'y6', 'x7',
                         'y7', ], header=None, index_col=False)

    for index, row in df.iterrows():
        full = True if 'F' in row.flag else False
        large = True if 'O' in row.flag else False
        edge = True if 'e' in row.flag else False

        coordinates = np.empty((0, 2))
        for i in range(1, row.num + 1):
            xi, yi = row[2 * i], row[2 * i + 1]
            coordinates = np.vstack((coordinates, (xi, yi)))

        polyPath = mplPath.Path(coordinates)

        curr_cel = Cell(polyPath, full, large, edge)
        cells.append(curr_cel)
        if edges:
            edges.append(curr_cel)

    plane = Plane(plane_id, max_rad, min_rad, cells, edges)

    return plane


def read_planes(geometry_file):
    with open(geometry_file, 'rb') as geometry_file:
        planes_indices = get_plane_indices(geometry_file)
    
        planes = [read_plane(geometry_file, planes_indices[start], start, end) for start, end in
                  pairwise(planes_indices.keys())]

    return planes

def point_inside_poly(planes, p_x, p_y):
    return any([plane.is_contain(p_x, p_y) for plane in planes])

def remove_spaces():
    readfile = open('fullgeometry.txt')
    writefile = open('fullgeometry_.txt', "w+")

    r = lambda line: re.sub(' +', ' ', line)

    for line in readfile:
        writefile.write(r(line))
    readfile.close()
    writefile.close()


def main():
    geometry_file_path = "_fullgeometry.txt"
    planes = read_planes(geometry_file_path)


if __name__ == '__main__':
    main()
