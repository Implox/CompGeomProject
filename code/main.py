from point import *
from dcel import *
from algorithm import *
import random
WIDTH = 1000
HEIGHT = 800
NUM_POINTS = 20


def to_x(coord_x):
    return int(round(coord_x + (WIDTH/2)))

def to_y(coord_y):
    return int(round((HEIGHT/2)-coord_y))

def triangulate_random_point_set(seed, num):
    S = make_random_point_set(num,WIDTH,HEIGHT)
    global triangulation 
    triangulation = triangulation_incremental(S)
    return triangulation

def make_random_point(width, height):
    x = round(random.uniform(0.25, 0.75) * width - (width * 0.5), 2)
    y = round(random.uniform(0.25, 0.75) * height - (height * 0.5), 2)
    dx = round(random.randint(-5,5))
    dy = round(random.randint(-5,5))
    return KineticPoint2d(x, y, dx , dy)

def make_random_point_set(n, width, height):
    return [make_random_point(width, height) for _ in range(n)]

def face_coords(dcel, face):
    ie = face.incident_edge
    return [e.origin.coord for e in dcel.get_cycle_from(ie)]

def advance(dcel, dt):
    vertiecs = dcel.vertices
    for e in vertiecs:
        e.coord.advance_dt(dt)

#instead of using this method you could just call delaunify again
#cause it does the same thing.  IDK which one would be more efficient
def check_incircle(dcel):
    #to be called after advance
    half_edges = dcel.half_edges
    is_all_legal = True
    for e in half_edges:
        if not e.is_legal():
            is_all_legal = False
    return is_all_legal

def find_violations(dcel):
    half_edges = dcel.half_edges
    for e in half_edges:
        if not e.is_legal():
           yield e.face.circumcircle()
            

if __name__ == '__main__':
    #random.seed(0)

    WIDTH = 800
    HEIGHT = 600
    NUM_POINTS = 20
    S = make_random_point_set(NUM_POINTS, WIDTH, HEIGHT)
    delaunay = make_delaunay(S)

    for (p, r) in delaunay.circumcircles():
        print(str(p), r)