from utils import atoi

class Polynome:
    values = []

    def __init__(self, raw:str):
        self.values = []
        if len(raw) > 0:
            value:int = 0
            degres:int = 0
            i:int = 0
            if (len(raw) > 0):
                value = atoi(raw)
                if raw[0] == '-' or raw[0] == '+':
                    i = 1
                tempI = i
                while i < len(raw):
                    if '0' <= raw[i] <= '9':
                        i += 1
                    else:
                        break
                if tempI == i:
                    value = 1
                raw = raw[i:]
                if len(raw) > 0:
                    if raw[0] == 'x':
                        degres = 1
                        if len(raw) > 1:
                            #value = value if value != 0 else 1
                            if raw[1] == '^':
                                degres = atoi(raw[2:])
                            else:
                                value = value * atoi(raw[1:]) if value != 0 else atoi(raw[1:])
            length = len(self.values)
            if length < degres + 1:
                for j in range(length, degres + 1):
                    self.values.append(0)
            self.values[degres] += value

    def __repr__(self):
        return self.toString()

    def toString(self):
        length = len(self.values)
        equation = ""
        for i in range(length - 1, -1, -1):
            value = self.values[i]
            if value != 0:
                if len(equation) > 0:
                    if value >= 0:
                        equation += " + "
                    else:
                        equation += " - "
                        value *= -1
                equation += str(value)
                if i != 0:
                    equation += "x"
                    if i != 1:
                        equation += "^"+str(i)
        return equation