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

def advance(dcel):
    vertiecs = dcel.verticies
    for e in vertiecs:
        e.coord.advance_dt()

def check_incircle(dcel):
    #to be called after advance
    half_edges = dcel.half_edges
    is_all_legal = True
    for e in half_edges:
        if not e.is_legal():
            is_all_legal = False
    return is_all_legal
    


if __name__ == '__main__':
    random.seed(0)

    WIDTH = 800
    HEIGHT = 600
    NUM_POINTS = 20
    S = make_random_point_set(NUM_POINTS, WIDTH, HEIGHT)
    delaunay = make_delaunay(S)

    for (p, r) in delaunay.circumcircles():
        print(str(p), r)