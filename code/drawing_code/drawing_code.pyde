from main import *
import random
from algorithm import *
import time

num_points=10
#random.seed(0)
ADVANCE = False
global i 
i= 0

def setup():
    global S
    global triangulation
    size(WIDTH,HEIGHT)
    smooth(4)
    background(255)

    #idk how excatly you wanna do this
    S = make_random_point_set(num_points,WIDTH,HEIGHT)
    triangulation = triangulation_incremental(S)

def keyPressed():
    global triangulation
    global S
    global ADVANCE
    if keyPressed:
        if key == 'p':
            advance(triangulation, 0.3)
        if key == 'a' and check_incircle(triangulation):
            ADVANCE = True
        if key == 'd':
            triangulation = make_delaunay(S)
        if key == 'r':
            S = make_random_point_set(num_points,WIDTH,HEIGHT)
            triangulation = triangulation_incremental(S)

def draw():
    global triangulation
    global S
    global ADVANCE
    
    start_time = time.time()
    dt = 0.033 # One frame at 30fps

    background(255)
    for f in triangulation.faces:
        if not f == triangulation.outer_face:
            #fill(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            fill(216,191,216)
            edges = triangulation.get_cycle_from(f.incident_edge)
            beginShape()
            for he in edges:
                #here is where the coord conversion comes into play
                vertex(to_x(he.origin.coord.x),to_y(he.origin.coord.y))
            endShape(CLOSE)

    #draw edges
    stroke(0)
    for e in triangulation.half_edges:
        if e.is_legal():
            stroke(0,0,255)
        else:
            strokeWeight(3)
            stroke(255,0,0)

        line(to_x(e.origin.coord.x),
            to_y(e.origin.coord.y),
            to_x(e.twin.origin.coord.x),
            to_y(e.twin.origin.coord.y))
        stroke(0)
        strokeWeight(1)

    #draw vertices
    fill(255)
    stroke(0)
    for v in triangulation.vertices:
        ellipse(to_x(v.coord.x),to_y(v.coord.y),8,8)
        
    if ADVANCE and check_incircle(triangulation):
        advance(triangulation, dt)
    else:
        ADVANCE = False
        x = find_violation(triangulation)
        if x is not None:
            (p, r) = x
            noFill()
            strokeWeight(2)
            stroke(255, 0, 0)
            ellipse(to_x(p.x), to_y(p.y), r, r) 
            strokeWeight(1)       
    
    end_time = time.time()
    diff = end_time - start_time
    if diff > dt:
        time.sleep(diff - dt)
