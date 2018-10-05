import math

class Equation:
    # Ax² + Bx + C
    a = 0
    b = 0
    c = 0
    delta = 0

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.delta = self.getDelta()

    def toString(self):
        return "wip"

    def getDelta(self):
        return (math.pow(self.b, 2)) - (4 * self.a * self.c)

    def roots(self):
        if self.a != 0:
            if self.delta > 0:
                root_one = (- self.b - math.sqrt(self.delta)) / (2 * self.a)
                root_two = (- self.b + math.sqrt(self.delta)) / (2 * self.a)
                return [root_one, root_two]
            if self.delta == 0:
                return (- self.b) / (2 * self.a)
            if self.delta < 0:
                part_one = (- self.b ) / (2 * self.a)
                part_two = (math.sqrt(math.fabs(self.delta))) / (2 * self.a)
                root_one_part_two_sign = " + " if (part_two < 0) else " - "
                root_two_part_two_sign = " - " if (part_two < 0) else " + "
                root_one = str(part_one) + root_one_part_two_sign + str(math.fabs(part_two)) +"i"
                root_two = str(part_one) + root_two_part_two_sign + str(math.fabs(part_two)) +"i"
                return [root_one, root_two]
        elif self.b != 0:
            return - self.c / self.b
        else :
            return self.c
