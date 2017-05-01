from main import *
import random
from algorithm import *


num_points=20
random.seed(0)
ADVANCE = False
global i 
i= 0


def setup():
    size(WIDTH,HEIGHT)
    smooth(4)
    background(255)

    #idk how excatly you wanna do this
    global S
    S = make_random_point_set(num_points,WIDTH,HEIGHT)
    global triangulation
    triangulation = triangulation_incremental(S)   



def draw():
    global triangulation
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
        line(to_x(e.origin.coord.x),to_y(e.origin.coord.y),to_x(e.twin.origin.coord.x),to_y(e.twin.origin.coord.y))
        stroke(0)
        strokeWeight(1)

    #skipping the drawing the selected edge

    #draw vertices
    fill(255)
    stroke(0)
    for v in triangulation.vertices:
        ellipse(to_x(v.coord.x),to_y(v.coord.y),8,8)

    #next timestep
    if (keyPressed) and (key =='a') and check_incircle(triangulation):
        advance(triangulation)
        
    if (keyPressed) and (key == 'd'):
        triangulation = make_delaunay(S)
    if (keyPressed) and (key=='p'):
        advance(triangulation)
    
    if (keyPressed) and key=='r':
        global S
        S = make_random_point_set(num_points,WIDTH,HEIGHT)
        global triangulation
        triangulation = triangulation_incremental(S) 
    

    
        
    
    
    