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
    steps = []
    __valuesMemberLeft = {}
    __valuesMemberRight = {}
    __equationMemberLeft = ''
    __equationMemberRight = ''
    __lastStepPrint = ''
    __options = {
        'printSteps': False,
        'rootsAsFraction': True
    }

    def __init__(self, equation:str, options = {}):
        self.operations = {}
        self.equation = ''
        self.steps = []
        self.__valuesMemberLeft = {}
        self.__valuesMemberRight = {}
        self.__equationMemberLeft = ''
        self.__equationMemberRight = ''
        self.__lastStepPrint = ''
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

    def __toString(self, values: dict):
        equation = ''
        keys = list(values.keys())
        nbKey = len(keys)
        keys = sorted(keys, reverse=True)
        for i in keys:
            value = values[i]
            if value != 0:
                if len(equation) > 0:
                    if value >= 0:
                        equation += ' + '
                    else:
                        equation += ' - '
                        value *= -1
                if i == 0: 
                    equation += str(value)
                else:
                    if value == -1:
                        equation += '-'
                    elif value != 1:
                        equation += str(value)
                if i != 0:
                    equation += 'x'
                    if i != 1:
                        equation += '^'+str(i)
            elif value == 0 and nbKey == 1:
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
            if (equation[i] == '^') and ((i == 0) or re.search('^(\^[-|+|\s]*[0-9]+)', equation[i:]) == None):
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
        equation = equation.replace(' ', '')
        # Replace and remove signs [+|-]
        equation = replaceSigns(equation)
        # Add * around x
        equation = checkForX(equation)
        return equation

    def __transformElementToValues(self, element: str):
        values = dict()
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
            if degres in values:
                values[degres] += value
            else:
                values[degres] = value
        return values

    def __verifyAndSimplifyMembers(self, equation:str):
        self.equation = self.__verifyCharPosition(equation)
        left = self.equation[0:self.equation.find('=')]
        right = self.equation[self.equation.find('=') + 1: len(self.equation)]
        self.__simplifyMembers(left, right)

    def __simplifyMembers(self, leftMember, rightMember):
        self.__equationMemberLeft = leftMember
        self.__equationMemberRight = rightMember
        self.__valuesMemberLeft = self.__simplify(self.__equationMemberLeft, self.__equationMemberRight)
        self.__valuesMemberRight = {0: 0}
        keys = list(self.__valuesMemberLeft.keys())
        keys = sorted(keys)
        if (len(keys) > 0) and (keys[0] < 0):
            formattedMember = self.__counterNegativeDegre(self.__valuesMemberLeft)
            self.__valuesMemberLeft = self.__simplifyFormatted(formattedMember, [{0:0}])
        if (self.__options['printSteps'] is True) and (len(self.steps) > 1):
            print('Simplify equation:')
            for line in self.steps:
                print('\t'+line)
        print('Reduced form:', self)

    def __simplify(self, leftMember, rightMember):
        self.__printStep(leftMember, rightMember, False) if self.__options['printSteps'] == True else 0
        leftFormatted = self.__convertMember(leftMember)
        rightFormatted = self.__convertMember(rightMember)
        return self.__simplifyFormatted(leftFormatted, rightFormatted)

    def __simplifyFormatted(self, leftFormatted, rightFormatted):
        if (len(rightFormatted) > 0):
            firstElem = rightFormatted[0]
            firstKeys = list(firstElem.keys())
            noNullValue = False
            for key in firstKeys:
                if firstElem[key] != 0:
                    noNullValue = True
            if (len(rightFormatted) > 1) or (noNullValue is True):
                for i in range(0, len(rightFormatted)):
                    if isOperator(rightFormatted[i]) is True:
                        if rightFormatted[i] == '-':
                            elem = rightFormatted[i + 1]
                            keys = list(elem.keys())
                            key = keys[0]
                            rightFormatted[i + 1][key] *= -1
                            rightFormatted[i] = '+'
                    else:
                        if i == 0:
                            leftFormatted.append('+')
                        keys = list(rightFormatted[i].keys())
                        for key in keys:
                            rightFormatted[i][key] *= -1
                    leftFormatted.append(rightFormatted[i])
        rightFormatted = [{0: 0}]
        
        self.__formattedToString(leftFormatted, rightFormatted)

        # Parse equation elements and do operations
        while len(leftFormatted) > 1:
            lenElems = len(leftFormatted)
            mulDivOpe = False
            for i in range(0, lenElems):
                if isOperator(leftFormatted[i]):
                    if (leftFormatted[i] == '*') or (leftFormatted[i] == '/'):
                        mulDivOpe = True
                        break
            for i in range(0, lenElems):
                if isOperator(leftFormatted[i]):
                    if (leftFormatted[i] == '*') or (leftFormatted[i] == '/') or (mulDivOpe == False):
                        currentOpe = leftFormatted[i - 1 : i + 2 : 1]
                        leftFormatted[i - 1] = self.operations[currentOpe[1]](currentOpe[0], currentOpe[2])
                        del leftFormatted[i:i + 2]
                        break
            self.__formattedToString(leftFormatted, rightFormatted)
        return leftFormatted[0]

    def __counterNegativeDegre(self, member: dict):
        keys = list(member.keys())
        sortedKeys = sorted(keys)
        if (len(sortedKeys) > 0) and (sortedKeys[0] < 0):
            degre = sortedKeys[0]
            counterDegre = abs(degre)
            counterElem = {}
            counterElem[counterDegre] = 1
            formattedMember = []
            for key in keys:
                if member[key] != 0:
                    if len(formattedMember) > 0:
                        formattedMember.append('+')
                    currentElem = {}
                    currentElem[key] = member[key]
                    formattedMember.append(currentElem)
                    formattedMember.append('*')
                    counterElem = {}
                    counterElem[counterDegre] = 1
                    formattedMember.append(counterElem)
            return formattedMember
        else:
            return [{0: 0}]

    def __formattedToString(self, leftFormatted, rightFormatted):
        leftMember = ''
        rightMember = ''
        for elem in leftFormatted:
            if isOperator(elem) == True:
                leftMember += elem
            else:
                leftMember += self.__toString(elem) 
        for elem in rightFormatted:
            if isOperator(elem) == True:
                rightMember += elem
            else:
                rightMember += self.__toString(elem) 
        self.__printStep(leftMember, rightMember, False) if self.__options['printSteps'] == True else 0

    def __convertMember(self, member):
        formattedMember = []
        if len(member) > 0:
            eq = member
            # Split equation
            for operator in OPERATORS:
                eq = eq.replace(operator, ' '+operator+' ')
            eq = eq.replace('^ + ', '^+')
            eq = eq.replace('^ - ', '^-')
            equationElements = eq.split()

            #Fix elements at first position
            if (equationElements[0] == '-') or (equationElements[0] == '+'):
                opeTemp = equationElements.pop(0)
                equationElements[0] = opeTemp + equationElements[0]
            
            # Replace equation elements by list of integer
            for elem in equationElements:
                value = elem
                if isOperator(value) == False:
                    value = self.__transformElementToValues(elem)
                formattedMember.append(value)
        return formattedMember

    def __printStep(self, left:str, right:str, printCurrent:bool):
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
        printStep = printStep.replace('  ', ' ')
        printStep = printStep.replace('- -', '+')
        printStep = printStep.replace('- +', '-')
        printStep = printStep.replace('+ +', '+')
        printStep = printStep.replace('+ -', '-')
        printStep = printStep.replace('^ - ', '^-')
        printStep = printStep.replace('^ + ', '^')
        if (printStep != self.__lastStepPrint):
            self.__lastStepPrint = printStep
            self.steps.append(printStep)
            print(printStep) if printCurrent is True else 0

    def getDelta(self):
        a = self.__valuesMemberLeft[2] if 2 in self.__valuesMemberLeft else 0
        b = self.__valuesMemberLeft[1] if 1 in self.__valuesMemberLeft else 0
        c = self.__valuesMemberLeft[0] if 0 in self.__valuesMemberLeft else 0
        return (math.pow(b, 2)) - (4 * a * c)

    def resolve(self):
        keys = list(self.__valuesMemberLeft.keys())
        keys = sorted(keys, reverse=True)
        degre = 0
        for key in keys:
            if self.__valuesMemberLeft[key] != 0:
                degre = key
                break
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
            currentRoot = str(roots[0])
            currentRoot = currentRoot.rstrip('0') if '.' in currentRoot else currentRoot
            currentRoot = currentRoot.rstrip('.')
            print('roots:\n\tx =', currentRoot)
        if (degre == 2):
            currentDelta = str(self.getDelta())
            currentDelta = currentDelta.rstrip('0') if '.' in currentDelta else currentDelta
            currentDelta = currentDelta.rstrip('.')
            print('Delta:', currentDelta)
            if len(roots) == 1:
                currentRoot = str(roots[0])
                currentRoot = currentRoot.rstrip('0') if '.' in currentRoot else currentRoot
                currentRoot = currentRoot.rstrip('.')
                print('roots:\n\tx =', currentRoot)
            else:
                currentRoot1 = str(roots[0])
                currentRoot1 = currentRoot1.rstrip('0') if '.' in currentRoot1 else currentRoot1
                currentRoot1 = currentRoot1.rstrip('.')
                currentRoot2 = str(roots[1])
                currentRoot2 = currentRoot2.rstrip('0') if '.' in currentRoot2 else currentRoot2
                currentRoot2 = currentRoot2.rstrip('.')
                print('roots:\n\tx1 =', currentRoot1, '\n\tx2 =', currentRoot2)
        
    def roots(self):
        #print(self.__options)
        values = self.__valuesMemberLeft
        a = values[2] if 2 in values else 0
        b = values[1] if 1 in values else 0
        c = values[0] if 0 in values else 0
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

    def add(self, src: dict, dest: dict):
        for key in dest:
            if key in src:
                src[key] += dest[key]
            else:
                src[key] = dest[key]
        return src

    def sub(self, src: dict, dest: dict):
        for key in dest:
            if key in src:
                src[key] -= dest[key]
            else:
                src[key] = dest[key] * -1
        return src

    def mul(self, src: dict, dest: dict):
        res = dict()
        for keyS in src:
            for keyD in dest:
                currentValue = 0
                currentKey = keyD + keyS
                if currentKey in res:
                    currentValue = res[currentKey]
                currentValue += src[keyS] * dest[keyD]
                res[currentKey] = currentValue
        return res

    def div(self, src: dict, dest: dict):
        """
        ⚠️ Ne fonctionne que si dest ne contient qu'un element à l'heure actuelle ⚠️
        """
        print('__DIV', src, dest)
        keys = list(dest.keys())
        keyD = keys[0] if len(keys) > 0 else None
        if keyD is None:
            return src
        res = dict()
        for keyS in src:
            currentValue = 0
            if keyS == keyD:
                if 0 in res:
                    currentValue = res[0]
                currentValue += src[keyS] / dest[keyD]
                res[0] = currentValue
            elif keyD == 0:
                if keyS in res:
                    currentValue = res[keyS]
                currentValue += src[keyS] / dest[keyD]
                res[keyS] = currentValue
            else:
                currentKey = keyS - keyD
                if currentKey in res:
                    currentValue = res[currentKey]
                currentValue = src[keyS] / dest[keyD]
                res[currentKey] = currentValue
        return res