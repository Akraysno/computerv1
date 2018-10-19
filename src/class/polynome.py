
class Polynome:
    degres = 1
    value = 0

    def __init__(self, value, degres):
        self.degres = degres
        self.value = value

    def add(self, polynome: Polynome):
        if (self.degres == polynome.degres):
            return Polynome(self.value + polynome.value, self.degres)

    def sub(self, polynome: Polynome):
        if (self.degres == polynome.degres):
            return Polynome(self.value - polynome.value, self.degres)

    def mult(self, polynome: Polynome):
        return Polynome(self.value * polynome.value, self.degres + polynome.degres)

    def div(self, polynome: Polynome):
        if (self.degres == polynome.degres):
            return Polynome(self.value / polynome.value, self.degres - polynome.degres)
