from main import *
import random


num_points=20
random.seed(0)


def to_x(coord_x):
    return int(round(coord_x + (WIDTH/2)))

def to_y(coord_y):
    return int(round((HEIGHT/2)-coord_y))


def setup():
    size(WIDTH,HEIGHT)
    smooth(4)
    background(255)

    #idk how excatly you wanna do this
    triangulate_random_point_set(473,num_points)   



def draw():
    backgound(255)
    for f in triangulation.faces:
        if not f == triangulation.outer_face:
            fill(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            edges = triangulation.get_cycle_from(f.incidentEdge)
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
            stroke(0,255,0)
        line(to_x(e.origin.coord.x),to_y(e.origin.coord.y),to_x(e.twin.origin.coord.x),to_y(e.twin.origin.coord.y))
        stroke(0)

    #skipping the drawing the selected edge

    #draw vertices
    fill(255)
    stroke(0)
    for v in triangulation.vertices:
        ellipse(to_x(v.coord.x),to_y(v.coord.y),8,8)

    #next timestep
    advance(triangulation)
    #not sure how to implement the check for incicrlce







def triangulate_random_point_set(seed, num):
    S = make_random_point_set(num,WIDTH,HEIGHT)
    global triangulation 
    triangulation = triangulation_incremental(S)
