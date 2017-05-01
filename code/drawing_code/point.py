class Point2d(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __lt__(self, other):
        if isinstance(other, Point2d):
            if self.x < other.x:
                return True
            elif self.x == other.x:
                return self.y < other.y
            else:
                return False
        else:
            return NotImplemented

    def dist_sq(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return dx*dx + dy*dy

    @staticmethod
    def midpoint(a, b):
        return Point2d(0.5 * (a.x + b.x), 0.5 * (a.y + b.y))

class KineticPoint2d(Point2d):
    def __init__(self,x,y,dx,dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        

    def __str__(self):
        return('pos({},{}) | vel({},{})'.format(self.x,self.y,self.dx,self.dy))

    def position_at(self, t):
        x_prime = self.x + t * self.dx
        y_prime = self.y + t * self.dy
        return Point2d(x_prime, y_prime)

    def advance_dt(self, dt):
        k = 1.0
        self.x = self.x + k * dt * self.dx
        self.y = self.y + k * dt * self.dy