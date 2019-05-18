import math
import re
from utils import atoi
from utils import atof
from utils import checkForX
from utils import replaceSigns
from utils import find_nth_overlapping
from fractions import Fraction
from decimal import Decimal

OPERATORS = ['+', '-', '*', '/']

def isOperator(token):
    return token in OPERATORS

# TODO fix values for x^-n
class Equation:
    operations = {}
    equation = ''
    __valuesMemberLeft = []
    __valuesMemberRight = []
    __equationMemberLeft = ''
    __equationMemberRight = ''
    __lastStepPrint = ''
    __options = {
        'printSteps': False,
        'rootsAsFraction': True
    }

    def __init__(self, equation:str, options = {}):
        self.operations = {
            '+': lambda src, dest: self.add(src, dest),
            '*': lambda src, dest: self.mul(src, dest),
            '/': lambda src, dest: self.div(src, dest),
            '-': lambda src, dest: self.sub(src, dest),
        }
        self.__options['printSteps'] = True if (options['printSteps'] and options['printSteps'] == True) else False
        self.__options['rootsAsFraction'] = True if (options['rootsAsFraction'] and options['rootsAsFraction'] == True) else False
        self.__verifyAndSimplifyMembers(equation)
    
    def __repr__(self):
        return self.__toString(self.__valuesMemberLeft) + ' = ' + self.__toString(self.__valuesMemberRight)

    def __toString(self, values):
        length = len(values)
        equation = ''
        for i in range(length - 1, -1, -1):
            value = values[i]
            if value != 0:
                if len(equation) > 0:
                    if value >= 0:
                        equation += ' + '
                    else:
                        equation += ' - '
                        value *= -1
                equation += str(value)
                if i != 0:
                    equation += 'x'
                    if i != 1:
                        equation += '^'+str(i)
            elif value == 0 and length == 1:
                equation += str(value)
        return equation

    def __verifyCharPosition(self, equation:str):
        print('\nequation:', equation)

        equation = equation.lower()

        # Verify Forbidden characters
        forbiddenChar = re.search('[^0123456789+\- *\/^x=.]+', equation)
        if forbiddenChar:
            raise ValueError('Synthax error forbidden char at position ' + str(find_nth_overlapping(equation, forbiddenChar.group(0), 1)))

        # Verify equality
        if equation.count('=') != 1:
            if equation.count('=') == 0:
                raise ValueError('Synthax error : Missing \'=\'')
            raise ValueError('Synthax error at char ' + str(find_nth_overlapping(equation, '=', 2)))

        # Search particular case: ^[+|-][0-9][.][0-9]x
        searchFailNumber = re.search('\^([\-|+]?[0-9]*\.[0-9]|[\-|+]?[0-9]*[.]?[0-9]*\s*x{1})', equation)
        if searchFailNumber:
            raise ValueError('Synthax error at char ' + str(find_nth_overlapping(equation, searchFailNumber.group(0), 1) + 1))

        # Search particular case where dot is not between numbers
        searchFailDot = re.search('([^0-9]\.[^0-9]|[^0-9]\.|\.[^0-9])', equation)
        if (searchFailDot):
            raise ValueError('Synthax error at char ' + str(find_nth_overlapping(equation, searchFailDot.group(0), 1) + 1) )

        # Search particular case: space between numbers
        searchFailNumber = re.search('(\d +\d)', equation)
        if searchFailNumber:
            raise ValueError('Synthax error at char ' + str(find_nth_overlapping(equation, searchFailNumber.group(0), 1) + 1))

        # TODO create exception for n / x^-k

        #verify char positions, x can be placed anywhere
        maxLen = len(equation)
        for i in range(0, maxLen):
            if (i == 0) and (find_nth_overlapping('-+0123456789x', equation[i], 1) == -1):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '^') and ((i == 0) or re.search('^(\^[+|\s]*[0-9]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '=') and ((i == 0) or re.search('^(=[\-|+|\s]*[0-9|x]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '+') and (re.search('^(\+[\-|+|\s]*[0-9|x]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '-') and (re.search('^(\-[\-|+|\s]*[0-9|x]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '*') and ((i == 0) or re.search('^(\*[\-|+|\s]*[0-9|x]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == '/') and ((i == 0) or re.search('^(\/[\-|+|\s]*[0-9]+)', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i].isdigit()) and (re.search('^([0-9][^\^])', equation[i:]) == None) and (re.search('^([0-9])$', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
            if (equation[i] == ' ') and (re.search('(\s[^\^])', equation[i:]) == None) and (re.search('^(\s)$', equation[i:]) == None):
                raise ValueError('Synthax error at char ' + str(i))
        
        return self.__transformEquation(equation)

    def __transformEquation(self, equation: str):
        # Remove spaces
        equation = equation.replace(' ', '')
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
                value = atof(element)
                valueIsNeg = True if element[0] == '-' else False
                if element[0] == '-' or element[0] == '+':
                    i = 1
                tempI = i
                dotFound = False
                while i < len(element):
                    if element[i].isdigit():
                        i += 1
                    elif (element[i] == '.') and (dotFound == False):
                        dotFound = True
                        i += 1
                    else:
                        break
                if tempI == i:
                    value = 1 if valueIsNeg == False else -1
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

    def __verifyAndSimplifyMembers(self, equation:str):
        self.equation = self.__verifyCharPosition(equation)
        left = self.equation[0:self.equation.find('=')]
        right = self.equation[self.equation.find('=') + 1: len(self.equation)]
        self.__simplifyMembers(left, right)

    def __simplifyMembers(self, leftMember, rightMember):
        self.__equationMemberLeft = leftMember
        self.__equationMemberRight = rightMember
        print('Simplify equation: \n') if self.__options['printSteps'] == True else 0
        self.__valuesMemberLeft = self.__simplifyMember(self.__equationMemberLeft, self.__equationMemberRight, 'left')
        self.__valuesMemberRight = self.__simplifyMember(self.__equationMemberRight, self.__toString(self.__valuesMemberLeft), 'right')

        test = self.__toString(self.operations['-']([0], self.__valuesMemberRight))
        test = test if test[0] == '-' else '+' + test

        valuesMemberLeft = self.operations['-'](self.__valuesMemberLeft, self.__valuesMemberRight)
        valuesMemberLeft = list(reversed(valuesMemberLeft))
        maxLen = len(self.__valuesMemberLeft) - 1
        while (valuesMemberLeft[0] == 0) and (len(valuesMemberLeft) > 1):
            valuesMemberLeft.pop(0)
        self.__valuesMemberLeft = list(reversed(valuesMemberLeft))
        self.__valuesMemberRight = [0]
        print('') if self.__options['printSteps'] == True else 0
        print('Reduced form:', self)

    def __simplifyMember(self, equation, otherMember, currentSideMember):
        leftMember = equation if currentSideMember == 'left' else otherMember
        rightMember = equation if currentSideMember == 'right' else otherMember
        self.__printStep(leftMember, rightMember) if self.__options['printSteps'] == True else 0

        if len(equation) > 0:
            eq = equation
            # Split equation
            for operator in OPERATORS:
                eq = eq.replace(operator, ' '+operator+' ')
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
                        if (formattedElems[i] == '*') or (formattedElems[i] == '/'):
                            mulDivOpe = True
                            break
                for i in range(0, lenElems):
                    if isOperator(formattedElems[i]):
                        if (formattedElems[i] == '*') or (formattedElems[i] == '/') or (mulDivOpe == False):
                            currentOpe = formattedElems[i - 1 : i + 2 : 1]
                            formattedElems[i - 1] = self.operations[currentOpe[1]](currentOpe[0], currentOpe[2])
                            del formattedElems[i:i + 2]
                            break
                form = ''
                for elem in formattedElems:
                    if isOperator(elem) == True:
                        form += elem
                    else:
                        form += self.__toString(elem) 
                leftMember = form if currentSideMember == 'left' else otherMember
                rightMember = form if currentSideMember == 'right' else otherMember
                self.__printStep(leftMember, rightMember) if self.__options['printSteps'] == True else 0
            return formattedElems[0]

    def __printStep(self, left:str, right:str):
        left = left.replace(' ', '')
        right = right.replace(' ', '')
        for operator in OPERATORS:
            left = left.replace(operator, ' '+operator+' ')
            right = right.replace(operator, ' '+operator+' ')
        if left[0] == ' ':
            left = left.replace(' - ', '-', 1)
        if right[0] == ' ':
            right = right.replace(' - ', '-', 1)
        printStep = left + ' = ' + right
        if (printStep != self.__lastStepPrint):
            self.__lastStepPrint = printStep
            print(printStep)

    def getDelta(self):
        return (math.pow(self.__valuesMemberLeft[1], 2)) - (4 * self.__valuesMemberLeft[2] * self.__valuesMemberLeft[0])

    def resolve(self):
        self.__valuesMemberLeft
        lenVal = len(self.__valuesMemberLeft)
        degre = lenVal - 1
        print('Polynomial degree:', str(degre))
        # transform to fraction with : Fraction( Decimal( str( float ) ) )
        if degre > 2:
            raise ValueError('Polynomial degree too high')
        roots = self.roots()
        if (degre == 0):
            if (roots[0] != 0):
                print('Equation sans solution')
            else:
                print('Tous les nombres sont solution')
        if (degre == 1):
            print('roots:\n\tx =', str(roots[0]).rstrip('0').rstrip('.'))
        if (degre == 2):
            print('Delta:', str(self.getDelta()).rstrip('0').rstrip('.') if self.getDelta() != 0 else '0')
            if len(roots) == 1:
                print('roots:\n\tx =', roots[0])
            else:
                print('roots:\n\tx1 =', roots[0], '\n\tx2 =', roots[1])
        
    def roots(self):
        #print(self.__options)
        values = self.__valuesMemberLeft
        a = values[2] if len(values) >= 3 else 0
        b = values[1] if len(values) >= 2 else 0
        c = values[0] if len(values) >= 1 else 0
        if a != 0:
            delta = self.getDelta()
            if delta > 0:
                rootOne = (- b - math.sqrt(delta)) / (2 * a)
                rootTwo = (- b + math.sqrt(delta)) / (2 * a)
                rootOneAsString = str(rootOne).rstrip('0').rstrip('.') if rootOne != 0 else '0'
                rootTwoAsString = str(rootTwo).rstrip('0').rstrip('.') if rootTwo != 0 else '0'
                rootOneAsFraction = Fraction(rootOne)
                rootTwoAsFraction = Fraction(rootTwo)
                rootOneAsFraction2 = Fraction(rootOneAsString)
                rootTwoAsFraction2 = Fraction(rootTwoAsString)
                #print(rootOne, rootOneAsString, rootOneAsFraction, rootOneAsFraction2)
                #print(rootTwo, rootTwoAsString, rootTwoAsFraction, rootTwoAsFraction2)
                return [rootOneAsString, rootTwoAsString]
            if delta == 0:
                root = (- b) / (2 * a)
                rootAsString = str(root).rstrip('0').rstrip('.') if root != 0 else '0'
                return [(- b) / (2 * a)]
            if delta < 0:
                partOne = (- b ) / (2 * a)
                partTwo = (math.sqrt(math.fabs(delta))) / (2 * a)
                rootOnePartTwoSign = ' + ' if (partTwo < 0) else ' - '
                rootTwoPartTwoSign = ' - ' if (partTwo < 0) else ' + '
                partOneAsString = str(partOne).rstrip('0').rstrip('.') if partOne != 0 else ''
                partTwoAsString = str(math.fabs(partTwo)).rstrip('0').rstrip('.') if partTwo != 0 else ''
                root_one = partOneAsString + (rootOnePartTwoSign if (partOne != 0) or (partOne < 0) else '') + partTwoAsString +'i'
                root_two = partOneAsString + (rootOnePartTwoSign if (partOne != 0) or (partOne < 0) else '') + partTwoAsString +'i'
                return [root_one, root_two]
        elif b != 0:
            return [- c / b]
        else :
            return [c]

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