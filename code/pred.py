def area_of_parallelogram(a, b, c):
    return (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y)

def is_lht(a, b, c):
    return area_of_parallelogram(a, b, c) > 0

def is_lht_or_on(a, b, c):
    return area_of_parallelogram(a, b, c) >= 0

def is_rht(a, b, c):
    return area_of_parallelogram(a, b, c) < 0

def is_rht_or_on(a, b, c):
    return area_of_parallelogram(a, b, c) <= 0

def is_same_side(a, b, c, d):
    return (is_lht(a, b, c) and is_lht(a, b, d) or
            is_rht(a, b, c) and is_rht(a, b, d))

def area_of_triangle(a, b, c):
    return 0.5 * area_of_parallelogram(a, b, c)

def in_circle(a, b, c, d):
    adx = a.x - d.x
    ady = a.y - d.y
    bdx = b.x - d.x
    bdy = b.y - d.y
    cdx = c.x - d.x
    cdy = c.y - d.y

    abdet = adx * bdy - bdx * ady
    bcdet = bdx * cdy - cdx * bdy
    cadet = cdx * ady - adx * cdy
    alift = adx * adx + ady * ady
    blift = bdx * bdx + bdy * bdy
    clift = cdx * cdx + cdy * cdy

    return (alift * bcdet + blift * cadet + clift * abdet) > 0
