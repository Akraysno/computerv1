from utils import atoi

class Polynome:
    degres = 1
    value = 0

    def __init__(self, string:str):
        value:int = 0
        degres:int = 0
        i:int = 0

        if (len(string) > 0):
            value = atoi(string)
            if string[0] == '-':
                i = 1
            if string[0] == '+':
                i = 1
            while i < len(string):
                if '0' <= string[i] <= '9':
                    i += 1
                else:
                    break
            string = string[i:]
            print (string)
            if len(string) > 0:
                if string[0] == 'x':
                    if len(string) > 1:
                        value = value if value != 0 else 1
                        if string[1] == '^':
                            degres = atoi(string[2:])
                        else:
                            value = value * atoi(string[1:]) if value != 0 else atoi(string[1:])
        self.degres = degres
        self.value = value

    def toString(self):
        print('{\n\tdegres : ',self.degres,', value : ',self.value)

    def add(self, polynome):
        if (self.degres == polynome.degres):
            return Polynome(self.value + polynome.value, self.degres)

    def sub(self, polynome):
        if (self.degres == polynome.degres):
            return Polynome(self.value - polynome.value, self.degres)

    def mult(self, polynome):
        return Polynome(self.value * polynome.value, self.degres + polynome.degres)

    def div(self, polynome):
        if (self.degres == polynome.degres):
            return Polynome(self.value / polynome.value, self.degres - polynome.degres)
