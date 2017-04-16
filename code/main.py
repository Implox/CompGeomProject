from point import *
from dcel import *
from algorithm import *
import random

def make_random_point(width, height):
    x = random.uniform(0.0, 1.0) * width - (width * 0.5)
    y = random.uniform(0.0, 1.0) * height - (height * 0.5)
    return Point2d(x, y)

def make_random_point_set(n, width, height):
    random.seed(0)
    return [make_random_point(width, height) for _ in range(n)]

if __name__ == '__main__':
    WIDTH = 800
    HEIGHT = 600
    S = make_random_point_set(20, WIDTH, HEIGHT)
    triangulation = triangulation_incremental(S) 
    delaunify(triangulation)