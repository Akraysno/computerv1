from utils import atoi

class Polynome:
    degres = 1
    value = 0

    def __init__(self, raw:str, value:int, degres:int):
        if len(raw) > 0:
            value:int = 0
            degres:int = 0
            i:int = 0
            if (len(raw) > 0):
                value = atoi(raw)
                if raw[0] == '-':
                    i = 1
                if raw[0] == '+':
                    i = 1
                while i < len(raw):
                    if '0' <= raw[i] <= '9':
                        i += 1
                    else:
                        break
                raw = raw[i:]
                if len(raw) > 0:
                    if raw[0] == 'x':
                        if len(raw) > 1:
                            value = value if value != 0 else 1
                            if raw[1] == '^':
                                degres = atoi(raw[2:])
                            else:
                                value = value * atoi(raw[1:]) if value != 0 else atoi(raw[1:])
            self.degres = degres
            self.value = value
        else:
            self.value = value
            self.degres = degres

    def toString(self):
        print('{\n\tdegres : ',self.degres,'\n\tvalue : ', self.value, '\n}')

    def add(self, polynome):
        print("add", polynome.degres, polynome.value)
        if (self.degres == polynome.degres):
            return Polynome("", self.value + polynome.value, self.degres)
        return False

    def sub(self, polynome):
        print("sub", polynome.degres, polynome.value)
        if (self.degres == polynome.degres):
            return Polynome("", self.value - polynome.value, self.degres)
        return False

    def mul(self, polynome):
        print("mul", polynome.degres, polynome.value)
        return Polynome("", self.value * polynome.value, self.degres + polynome.degres)

    def div(self, polynome):
        print("div", polynome.degres, polynome.value)
        return Polynome("", self.value / polynome.value, self.degres - polynome.degres)
