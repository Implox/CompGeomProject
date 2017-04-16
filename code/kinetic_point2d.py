from point import Point2d



class kinetic_point2d(Point2d):

    def __init__(self,x,y,vx,vy):
        super(kinetic_point2d,self).__init__(x,y)
        self.vx = vx
        self.vy = vy
        self.origin_x = x
        self.origin_y = y
        self.time = 0

    def __str__(self):
        return('pos({},{}) | vel({},{})'.format(self.x,self.y,self.vx,self.vy))

    
    def advance(self, t):
        self.x = self.x + t * self.vx
        self.y = self.y + t * self.vy
        self.time = self.time + t

    def go_to_time(self,end_time):
        dt = (end_time - self.time)/1000.0
        timeAt = self.time
        while timeAt < end_time:
            self.x = self.x + dt*self.vx
            self.y = self.y + dt*self.vy
            timeAt = timeAt + dt

        