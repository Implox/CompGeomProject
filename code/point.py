class Point2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __cmp__(self, other):
        if isinstance(other, Point2d):
            cmp_x = self.x.cmp(other.x)
            return cmp_x if cmp_x != 0 else self.y.cmp(other.y)
        else:
            return NotImplemented

    def dist_sq(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return dx*dx + dy*dy

    @staticmethod
    def midpoint(a, b):
        return Point2d(0.5 * (a.x + b.x), 0.5 * (a.y + b.y))
