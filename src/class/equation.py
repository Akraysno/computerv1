import math
from polynome import Polynome
from utils import atoi

from copy import deepcopy

OPERATORS = ['+', '-', '*', '/']

def isOperator(token):
    return token in OPERATORS

class Equation:
    # [c, b, a]
    values = []
    equation = ""
    equationElements = []

    def __init__(self, *args, **kwargs):
        self.values = []
        self.equation = ""
        self.equationElements = []
        equation = ""
        values = []
        if (kwargs.get("equation")):
            equation = kwargs.get("equation")
        elif (kwargs.get("polynome")):
            polynome = kwargs.get("polynome")
            values = (lambda polynome: polynome.values)(polynome)
        self.equation = equation
        self.values = values

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
        equation += " = 0"
        return equation

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

    def simplify(self, printSteps: bool):
        eq = self.equation
        for operator in OPERATORS:
            eq = eq.replace(operator, " "+operator+" ")
        #fix bug for "+" or "-" at first position
        equationElements = eq.split()
        self.equationElements = equationElements
        formattedElems = []
        for elem in equationElements:
            value = elem
            if isOperator(value) == False:
                value = Equation(polynome=Polynome(elem))
            formattedElems.append(value)

        while len(formattedElems) > 1:
            lenElems = len(formattedElems)
            mulDivOpe = False
            for i in range(0, lenElems):
                if isOperator(formattedElems[i]):
                    if (formattedElems[i] == "*") or (formattedElems[i] == "/"):
                        mulDivOpe = True
                        break
            for i in range(0, lenElems):
                if isOperator(formattedElems[i]):
                    if (formattedElems[i] == "*") or (formattedElems[i] == "/") or (mulDivOpe == False):
                        currentOpe = formattedElems[i - 1 : i + 2 : 1]
                        if currentOpe[1] == "*":
                            formattedElems[i - 1] = currentOpe[0].mul(currentOpe[2])
                        elif currentOpe[1] == "/":
                            formattedElems[i - 1] = currentOpe[0].div(currentOpe[2])
                        elif currentOpe[1] == "+":
                            formattedElems[i - 1] = currentOpe[0].add(currentOpe[2])
                        elif currentOpe[1] == "-":
                            formattedElems[i - 1] = currentOpe[0].sub(currentOpe[2])
                        del formattedElems[i:i + 2]
                        break
            if printSteps == True:
                print("Step :", formattedElems)
        self.values = formattedElems[0].values

    def add(self, ope):
        lenSelf = len(self.values)
        lenOpe = len(ope.values)
        maxLen = lenSelf if lenSelf >= lenOpe else lenOpe
        for i in range(0, maxLen):
            if lenSelf < i + 1:
                for j in range(lenSelf, i + 1):
                    self.values.append(0)
            value = self.values[i]
            if i < lenOpe:
                value += ope.values[i]
            self.values[i] = value
        return self

    def sub(self, ope):
        print(self, ope)
        lenSelf = len(self.values)
        lenOpe = len(ope.values)
        maxLen = lenSelf if lenSelf >= lenOpe else lenOpe
        for i in range(0, maxLen):
            if lenSelf < i + 1:
                for j in range(lenSelf, i + 1):
                    self.values.append(0)
            value = self.values[i]
            if i < lenOpe:
                value -= ope.values[i]
            self.values[i] = value
        return self

    def mul(self, ope):
        newValues = []
        lenSelf = len(self.values)
        lenOpe = len(ope.values)
        for i in range(0, lenSelf):
            for j in range(0, lenOpe):
                degre = i + j
                lenVal = len(newValues)
                if lenVal < degre + 1:
                    for k in range(lenVal, degre + 1):
                        newValues.append(0)
                val = self.values[i] * ope.values[j]
                newValues[degre] += val
        self.values = newValues
        return self

    def div(self, ope):
        newValues = []
        lenSelf = len(self.values)
        lenOpe = len(ope.values)
        for i in range(0, lenSelf):
            for j in range(0, lenOpe):
                degre = i - j
                lenVal = len(newValues)
                if lenVal < degre + 1:
                    for k in range(lenVal, degre + 1):
                        newValues.append(0)
                if ope.values[j] != 0:
                    val = self.values[i] / ope.values[j]
                    newValues[degre] += val
        self.values = newValues
        return self