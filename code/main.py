from point import *
from dcel import *
from algorithm import *
import random

def make_random_point(width, height):
    x = round(random.uniform(0.0, 1.0) * width - (width * 0.5), 2)
    y = round(random.uniform(0.0, 1.0) * height - (height * 0.5), 2)
    return Point2d(x, y)

def make_random_point_set(n, width, height):
    return [make_random_point(width, height) for _ in range(n)]

def face_coords(dcel, face):
    ie = face.incident_edge
    return [e.origin.coord for e in dcel.get_cycle_from(ie)]

if __name__ == '__main__':
    random.seed(0)

    WIDTH = 800
    HEIGHT = 600
    NUM_POINTS = 20
    S = make_random_point_set(NUM_POINTS, WIDTH, HEIGHT)
    delaunay = make_delaunay(S)

    for (p, r) in delaunay.circumcircles():
        print(str(p), r)