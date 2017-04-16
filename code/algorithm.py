from dcel import *
from pred import *

def get_ccw_triangle(a, b, c):
    tri = DCEL()
    v1 = tri.Vertex(a)
    v2 = tri.Vertex(b)
    v3 = tri.Vertex(c)

    if not is_lht(a, b, c):
        # swap v2's and v3's values
        v2, v3 = v3, v2

    # Create inner face
    inner = tri.Face()

    # Create inner half-edges
    he12 = tri.HalfEdge(v1, inner)
    he23 = tri.HalfEdge(v2, inner)
    he31 = tri.HalfEdge(v3, inner)

    # Connect next/prev pointers on inner face
    he12.make_next(he23)
    he23.make_next(he31)
    he31.make_next(he12)

    # Create outer half-edges
    he21 = tri.HalfEdge(v1, tri.outer_face)
    he32 = tri.HalfEdge(v2, tri.outer_face)
    he13 = tri.HalfEdge(v3, tri.outer_face)

    # Connect next/prev pointers on outer face
    he21.make_next(he13)
    he32.make_next(he32)
    he13.make_next(he21)

    # Set twins
    he12.make_twins(he21)
    he23.make_twins(he32)
    he13.make_twins(he31)

    return tri

def triangulation_incremental(S):
    sort(S)
    triangulation = get_ccw_triangle(S[0], S[1], S[2])

    for k in range(3, len(S)):
        pk = S[k]
        he = triangulation.outer_face.incident_edge
        upper_tangent = None
        lower_tangent = None
        tangents = []

        while True:
            if is_same_side(pk, he.origin.coord, he.next.origin.coord, he.prev.origin.coord):
                tangents.append(he)
            he = he.next
            if he is triangulation.outer_face.incident_edge:
                break

        if len(tangents) == 2:
            new_vertex = triangulation.Vertex(pk)
            upper_tangent = tangents[0]
            lower_tangent = tangents[1]
            if not is_lht(pk, tangents[0].origin.coord, tangents[0].next.origin.coord):
                upper_tangent, lower_tangent = lower_tangent, upper_tangent

            new_face = triangulation.Face()

            upper1 = triangulation.HalfEdge(new_vertex, new_face)
            upper2 = triangulation.HalfEdge(upper_tangent.origin, triangulation.outer_face)

            lower1 = triangulation.HalfEdge(lower_tangent.origin, new_face)
            lower2 = triangulation.HalfEdge(new_vertex, triangulation.outer_face)

            upper1.make_twins(upper2)
            lower1.make_twins(lower2)

            upper_tangent.prev.make_next(upper2)
            upper2.make_next(lower2)

            upper1.make_next(upper_tangent)
            lower_tangent.prev.make_next(lower1)
            lower1.make_next(upper1)

            lower2.make_next(lower_tangent)

            for edge in triangulation.get_cycle_from(upper1):
                edge.face = new_face
            new_face.incident_edge = upper1
            triangulation.outer_face.incident_edge = lower2

            while upper1.next.next.next is not upper1:
                triangulation.split_face(upper1, upper1.next.next)
                upper1 = upper1.prev.twin
    return triangulation

def delaunify(triangulation):
    while True:
        flip_edge = None
        for he in triangulation.half_edges:
            if not he.is_legal():
                flip_edge = he
                break
        if flip_edge is not None:
            flip_edge.flip()
        else:
            break
