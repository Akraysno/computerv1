import math
import re
from polynome import Polynome
from utils import atoi
from utils import checkForX
from utils import authorizeChar
from utils import replaceSigns
from utils import authorizeCharPosition
from utils import find_nth_overlapping

from copy import deepcopy

OPERATORS = ['+', '-', '*', '/']

def isOperator(token):
    return token in OPERATORS

class Equation:
    # [c, b, a]
    values = []
    operations = {}
    equation = ""

    __valuesMemberLeft = []
    __valuesMemberRight = []
    __equationMemberLeft = ""
    __equationMemberRight = ""

    def __init__(self, *args, **kwargs):
        self.values = []
        self.equation = ""
        self.operations = {
            '+': lambda eq1, eq2: eq1.add(eq2),
            '*': lambda eq1, eq2: eq1.mul(eq2),
            '/': lambda eq1, eq2: eq1.div(eq2),
            '-': lambda eq1, eq2: eq1.sub(eq2),
        }
        equation = ""
        values = []
        if (kwargs.get("equation")):
            self.equation = self.__verifyCharPosition(kwargs.get("equation"))
            self.__equationMemberLeft = self.equation[0:self.equation.find('=')]
            self.__equationMemberRight = self.equation[self.equation.find('=') + 1: len(self.equation)]
        elif (kwargs.get("polynome")):
            polynome = kwargs.get("polynome")
            values = (lambda polynome: polynome.values)(polynome)
            values = (lambda polynome: polynome.values)(polynome)

        self.equation = equation
        self.values = values

    def __repr__(self):
        return self.__toString(self.__valuesMemberLeft) + " = " + self.__toString(self.__valuesMemberRight)

    def __toString(self, values):
        length = len(values)
        equation = ""
        for i in range(length - 1, -1, -1):
            value = values[i]
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

    def __verifyCharPosition(self, equation:str):
        print("equation: ", equation)

        equation = equation.lower()

        # Verify Forbidden characters
        forbiddenChar = re.search('[^0123456789+\- *\/^x=]+', equation)
        if forbiddenChar:
            raise ValueError('Synthax error forbidden char at position ' + str(find_nth_overlapping(equation, forbiddenChar.group(0), 1)))

        # Verify equality
        if equation.count('=') != 1:
            if equation.count('=') == 0:
                raise ValueError("Synthax error : Missing '='")
            raise ValueError('Synthax error at char ' + str(find_nth_overlapping(equation, '=', 2)))

        # Search particular case: ^[+|-][0-9]x
        searchFailNumber = re.search('(\^[\-|+]?[0-9]+\s*x{1})', equation)
        if searchFailNumber:
            raise ValueError('Synthax error at char ' + str(find_nth_overlapping(equation, searchFailNumber.group(0), 1) + 1))

        # Search particular case: space between numbers
        searchFailNumber = re.search('(\d +\d)', equation)
        if searchFailNumber:
            raise ValueError('Synthax error at char ' + str(find_nth_overlapping(equation, searchFailNumber.group(0), 1) + 1))

        #verify char positions, x can be placed anywhere
        maxLen = len(equation)
        for i in range(0, maxLen):
            print(i, equation[i], equation[i:])            
            if (i == 0) and (find_nth_overlapping("-+0123456789x", equation[i], 1) == -1):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '^') and ((i == 0) or re.search('^(\^[\-|+|\s]*[0-9]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '=') and ((i == 0) or re.search('^(=[\-|+|\s]*[0-9|x]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '+') and (re.search('^(\+[\-|+|\s]*[0-9|x]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '-') and (re.search('^(\-[\-|+|\s]*[0-9|x]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '*') and ((i == 0) or re.search('^(\*[\-|+|\s]*[0-9|x]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '/') and ((i == 0) or re.search('^(\/[\-|+|\s]*[0-9|x]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i].isdigit()) and (re.search('^([0-9][^\^])', equation[i:]) == None) and (re.search('^([0-9])$', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == ' ') and (re.search('(\s[^\^])', equation[i:]) == None) and (re.search('^(\s)$', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
        
        return self.__transformEquation(equation)

    def __transformEquation(self, equation):
        # Remove spaces
        equation = equation.strip(' ')
        # Replace and remove signs [+|-]
        equation = replaceSigns(equation)
        # Add * around x
        equation = checkForX(equation)
        return equation

    def simplify(self, printSteps: bool):
        if len(self.equation) > 0:
            eq = self.equation
            # Split equation
            for operator in OPERATORS:
                eq = eq.replace(operator, " "+operator+" ")
            equationElements = eq.split()

            #Fix elements at first position
            if (equationElements[0] == '-') or (equationElements[0] == '+'):
                opeTemp = equationElements.pop(0)
                equationElements[0] = opeTemp + equationElements[0]
            
            # Replace equation elements by Equation object
            formattedElems = []
            for elem in equationElements:
                value = elem
                if isOperator(value) == False:
                    value = Equation(polynome=Polynome(elem))
                formattedElems.append(value)

            # Parse equation elements and do operations
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
                            formattedElems[i - 1] = self.operations[currentOpe[1]](currentOpe[0], currentOpe[2])
                            del formattedElems[i:i + 2]
                            break
                if printSteps == True:
                    print("Step :", formattedElems)
            self.values = formattedElems[0].values
            self.equation = ""

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

    def add(self, values):
        lenSelf = len(self.values)
        lenValues = len(values)
        maxLen = lenSelf if lenSelf >= lenValues else lenValues
        for i in range(0, maxLen):
            if lenSelf < i + 1:
                for j in range(lenSelf, i + 1):
                    self.values.append(0)
            value = self.values[i]
            if i < lenValues:
                value += values[i]
            self.values[i] = value
        return self

    def sub(self, values):
        lenSelf = len(self.values)
        lenValues = len(values)
        maxLen = lenSelf if lenSelf >= lenValues else lenValues
        for i in range(0, maxLen):
            if lenSelf < i + 1:
                for j in range(lenSelf, i + 1):
                    self.values.append(0)
            value = self.values[i]
            if i < lenValues:
                value -= values[i]
            self.values[i] = value
        return self

    def mul(self, values):
        newValues = []
        lenSelf = len(self.values)
        lenValues = len(values)
        for i in range(0, lenSelf):
            for j in range(0, lenValues):
                degre = i + j
                lenVal = len(newValues)
                if lenVal < degre + 1:
                    for k in range(lenVal, degre + 1):
                        newValues.append(0)
                val = self.values[i] * values[j]
                newValues[degre] += val
        self.values = newValues
        return self

    def div(self, values):
        newValues = []
        lenSelf = len(self.values)
        lenValues = len(values)
        for i in range(0, lenSelf):
            for j in range(0, lenValues):
                degre = i - j
                lenVal = len(newValues)
                if lenVal < degre + 1:
                    for k in range(lenVal, degre + 1):
                        newValues.append(0)
                if values[j] != 0:
                    val = self.values[i] / values[j]
                    newValues[degre] += val
        self.values = newValues
        return self