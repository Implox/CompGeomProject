import pred
from point import Point2d
from boundinnerclass import BoundInnerClass

class DCEL:
    def __init__(self):
        self.vertices = []
        self.half_edges = []
        self.faces = []
        self.outer_face = self.Face()

    def get_cycle_from(self, e):
        yield e
        current = e.next
        while current is not e:
            yield current
            current = current.next

    def split_face(self, e1, e2):
        # Check whether call is legal, return early if necessary
        if e1.face is not e2.face or \
            e1.next is e2 or \
            e1.prev is e2 or \
            e1 is e2: return

        # Create a new face for the second half of the split
        new_face = self.Face()

        # Create new half-edges for the splitting edge
        s1 = self.HalfEdge(e2.origin, e1.face)
        s2 = self.HalfEdge(e1.origin, new_face)
        s1.make_twins(s2)

        # Insert new half-edges into the cyclic lists
        e2.prev.make_next(s1)
        e1.prev.make_next(s2)
        s1.make_next(e1)
        s2.make_next(e2)

        # Make sure all half-edges point to the correct face
        for e in self.get_cycle_from(e2):
            e.face = new_face

        # Make sure that each face correctly refers to an incident half-edge
        new_face.incident_edge = e2
        e1.face.incident_edge = e1

    @BoundInnerClass
    class HalfEdge:
        def __init__(self, dcel, origin, face):
            self.dcel = dcel
            self.origin = origin
            self.face = face
            self.twin = None
            self.next = None
            self.prev = None

            origin.outgoing_edge = self
            face.incident_edge = self
            self.dcel.half_edges.append(self)

        def get_destination(self):
            return self.twin.origin

        def make_twins(self, other):
            self.twin = other
            other.twin = self

        def make_next(self, other):
            self.next = other
            other.prev = self

        def split_in_half(self):
            # Create a vertex for the midpoint
            mid = self.dcel.Vertex(
                Point2d.midpoint(self.origin, self.get_destination().coord))

            # Create the two new half-edges
            n1 = self.dcel.HalfEdge(mid, self.face)
            n2 = self.dcel.HalfEdge(mid, self.twin.face)

            # Set next/prev pointers
            n1.make_next(self.next)
            self.make_next(n1)

            n2.make_next(self.twin)
            self.twin.make_next(n2)

            # Set twin pointers
            self.twin.make_twins(n1)
            self.make_twins(n2)

        def is_legal(self):
            outer_face = self.dcel.outer_face
            if self.face is outer_face or self.twin.face is outer_face:
                return True

            a = self.origin.coord
            c = self.next.origin.coord
            d = self.prev.origin.coord
            b = self.twin.next.next.origin.coord
            return not pred.in_circle(a, b, c, d)

        def remove(self):
            outer_face = self.dcel.outer_face
            if self.face is outer_face or \
               self.twin.face is outer_face or \
               self.face is self.twin.face: return

            next1 = self.next
            prev1 = self.twin.prev
            next2 = self.twin.next
            prev2 = self.prev

            prev1.make_next(next1)
            prev2.make_next(next2)

            self.dcel.half_edges.remove(self)
            self.dcel.half_edges.remove(self.twin)
            self.dcel.faces.remove(next2.face)
            for e in self.dcel.get_cycle_from(next1):
                e.face = next1.face
            next1.face.incident_edge = next1

        def flip(self):
            outer_face = self.dcel.outer_face
            if self.face is outer_face or \
               self.twin.face is outer_face: return

            a = self.origin.coord
            c = self.next.origin.coord
            d = self.prev.origin.coord
            b = self.twin.next.next.origin.coord

            if pred.is_rht(a, b, c) or \
               pred.is_rht(b, c, d) or \
               pred.is_rht(c, d, a) or \
               pred.is_rht(d, a, b): return

            edge_a = self.next.next
            edge_b = self.twin.next.next

            self.remove()
            self.dcel.split_face(edge_a, edge_b)

    @BoundInnerClass
    class Vertex:
        def __init__(self, dcel, coord):
            self.coord = coord
            self.outgoing_edge = None
            dcel.vertices.append(self)

    @BoundInnerClass
    class Face:
        def __init__(self, dcel):
            self.incident_edge = None
            dcel.faces.append(self)

if __name__ == '__main__':
    dcel = DCEL()
    face = dcel.Face()

    [a, d, b, c] = [dcel.HalfEdge(dcel.Vertex(Point2d(x, y)), face)
                    for x in [-1, 1] 
                    for y in [-1, 1]]
    [at, bt, ct, dt] = [dcel.HalfEdge(e.origin, dcel.outer_face) 
                        for e in [b, c, d, a]]
    a.make_next(b); at.make_next(dt) # d <- c
    b.make_next(c); bt.make_next(at) # | ff ^
    c.make_next(d); ct.make_next(bt) # v ff |
    d.make_next(a); dt.make_next(ct) # a -> b

    a.make_twins(at)
    b.make_twins(bt)
    c.make_twins(ct)
    d.make_twins(dt)