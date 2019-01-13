import math
import re
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
    operations = {}
    equation = ""
    __valuesMemberLeft = []
    __valuesMemberRight = []
    __equationMemberLeft = ""
    __equationMemberRight = ""

    def __init__(self, equation:str):
        self.operations = {
            '+': lambda src, dest: self.add(src, dest),
            '*': lambda src, dest: self.mul(src, dest),
            '/': lambda src, dest: self.div(src, dest),
            '-': lambda src, dest: self.sub(src, dest),
        }
        self.equation = self.__verifyCharPosition(equation)
        self.__equationMemberLeft = self.equation[0:self.equation.find('=')]
        self.__equationMemberRight = self.equation[self.equation.find('=') + 1: len(self.equation)]
        self.__valuesMemberLeft = self.simplifyMember(self.__equationMemberLeft)
        self.__valuesMemberRight = self.simplifyMember(self.__equationMemberRight)
        self.__valuesMemberLeft = self.operations['-'](self.__valuesMemberLeft, self.__valuesMemberRight)
        self.__valuesMemberRight = [0]
    
    def __repr__(self):
        return self.__toString(self.__valuesMemberLeft) + " = " + self.__toString(self.__valuesMemberRight)

    def __toString(self, values):
        print(values)
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
            elif value == 0 and length == 1:
                equation += str(value)
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

    def __transformEquation(self, equation: str):
        # Remove spaces
        equation = equation.strip(' ')
        # Replace and remove signs [+|-]
        equation = replaceSigns(equation)
        # Add * around x
        equation = checkForX(equation)
        return equation

    def __transformElementToValues(self, element: str):
        values = []
        if len(element) > 0:
            value:int = 0
            degres:int = 0
            i:int = 0
            if (len(element) > 0):
                value = atoi(element)
                if element[0] == '-' or element[0] == '+':
                    i = 1
                tempI = i
                while i < len(element):
                    if '0' <= element[i] <= '9':
                        i += 1
                    else:
                        break
                if tempI == i:
                    value = 1
                element = element[i:]
                if len(element) > 0:
                    if element[0] == 'x':
                        degres = 1
                        if len(element) > 1:
                            #value = value if value != 0 else 1
                            if element[1] == '^':
                                degres = atoi(element[2:])
                            else:
                                value = value * atoi(element[1:]) if value != 0 else atoi(element[1:])
            length = len(values)
            if length < degres + 1:
                for j in range(length, degres + 1):
                    values.append(0)
            values[degres] += value
        return values

    def simplifyMember(self, equation):
        if len(equation) > 0:
            eq = equation
            # Split equation
            for operator in OPERATORS:
                eq = eq.replace(operator, " "+operator+" ")
            equationElements = eq.split()

            #Fix elements at first position
            if (equationElements[0] == '-') or (equationElements[0] == '+'):
                opeTemp = equationElements.pop(0)
                equationElements[0] = opeTemp + equationElements[0]
            
            # Replace equation elements by list of integer
            formattedElems = []
            for elem in equationElements:
                value = elem
                if isOperator(value) == False:
                    value = self.__transformElementToValues(elem)
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
                print("Step :", formattedElems)
            return formattedElems[0]

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

    def add(self, src, dest):
        lenSrc = len(src)
        lenDest = len(dest)
        maxLen = lenSrc if lenSrc >= lenDest else lenDest
        for i in range(0, maxLen):
            if lenSrc < i + 1:
                for j in range(lenSrc, i + 1):
                    src.append(0)
            value = src[i]
            if i < lenDest:
                value += dest[i]
            src[i] = value
        return src

    def sub(self, src, dest):
        lenSrc = len(src)
        lenDest = len(dest)
        maxLen = lenSrc if lenSrc >= lenDest else lenDest
        for i in range(0, maxLen):
            if lenSrc < i + 1:
                for j in range(lenSrc, i + 1):
                    src.append(0)
            value = src[i]
            if i < lenDest:
                value -= dest[i]
            src[i] = value
        return src

    def mul(self, src, dest):
        newValues = []
        lenSrc = len(src)
        lenDest = len(dest)
        for i in range(0, lenSrc):
            for j in range(0, lenDest):
                degre = i + j
                lenVal = len(newValues)
                if lenVal < degre + 1:
                    for k in range(lenVal, degre + 1):
                        newValues.append(0)
                val = src[i] * dest[j]
                newValues[degre] += val
        return newValues

    def div(self, src, dest):
        newValues = []
        lenSrc = len(src)
        lenDest = len(dest)
        for i in range(0, lenSrc):
            for j in range(0, lenDest):
                degre = i - j
                lenVal = len(newValues)
                if lenVal < degre + 1:
                    for k in range(lenVal, degre + 1):
                        newValues.append(0)
                if dest[j] != 0:
                    val = src[i] / dest[j]
                    newValues[degre] += val
        return newValues