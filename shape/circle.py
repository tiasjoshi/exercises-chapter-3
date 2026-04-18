class Circle:

    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius

    def __contains__(self, point):
        cx = self.centre[0]
        cy = self.centre[1]
        x = point[0]
        y = point[1]
        r = self.radius

        a = (x - cx)**2 + (y - cy)**2

        if a <= r**2:
            return True
