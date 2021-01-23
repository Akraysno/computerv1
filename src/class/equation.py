import math, re, json

OPERATORS = ['+', '-', '*', '/']

def isOperator(token):
    return token in OPERATORS

class Equation:
    __equationMemberLeft = ''
    __equationMemberRight = ''
    __lastStepPrint = ''
    __operations = {}
    __valuesMemberLeft = {}
    __valuesMemberRight = {}
    allNumbersAsSolution = False
    delta = 0
    equation = ''
    error = ''
    polynomialDegree = 0
    polynomialDegreeTooHigh = False
    reduced = ''
    roots = []
    sidesNotEquals = False
    steps = []

    def __init__(self, equation:str = '', options = {}):
        self.__equationMemberLeft = ''
        self.__equationMemberRight = ''
        self.__lastStepPrint = ''
        self.__operations = {
            '+': lambda src, dest: self.__add(src, dest),
            '*': lambda src, dest: self.__mul(src, dest),
            '/': lambda src, dest: self.__div(src, dest),
            '-': lambda src, dest: self.__sub(src, dest),
        }
        self.__valuesMemberLeft = {}
        self.__valuesMemberRight = {}
        self.allNumbersAsSolution = False
        self.delta = 0
        self.equation = equation.lower()
        self.error = ''
        self.polynomialDegree = 0
        self.polynomialDegreeTooHigh = False
        self.reduced = ''
        self.roots = []
        self.sidesNotEquals = False
        self.steps = []
        if self.__verifyAndSimplifyMembers() is True:
            self.__resolve()
    
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

    def __verifyAndSimplifyMembers(self):
        self.equation = self.equation.replace('²', '^2')
        if self.__verifyCharPosition() is True:
            self.__transformEquation()
            left = self.equation[0:self.equation.find('=')]
            right = self.equation[self.equation.find('=') + 1: len(self.equation)]
            self.__simplifyMembers(left, right)
            return True
        return False

    def __verifyCharPosition(self):
        # Verify Forbidden characters
        forbiddenChar = re.search('[^0123456789+\- *\/^x=.]+', self.equation)
        if forbiddenChar:
            self.error = 'Synthax error: Caractère non autorisé à la position '+str(self.__findNthOverlapping(self.equation, forbiddenChar.group(0), 1))+'.'
            return False

        # Verify equality
        if self.equation.count('=') != 1:
            if self.equation.count('=') == 0:
                self.error = 'Synthax error: Caractère \'=\' manquant.'
                return False
            self.error = 'Synthax error: Caractère \'=\' en trop à la position ' + str(self.__findNthOverlapping(self.equation, '=', 2))+'.'
            return False

        # Search particular case: ^[+|-][0-9][.][0-9]x
        searchFailNumber = re.search('^\^|\^$|\^([\-|+]?[0-9]*\.[0-9]*|[\-|+]?[0-9]*[.]?[0-9]*\s*x{1})', self.equation)
        if searchFailNumber:
            self.error = 'Synthax error: Caractère mal placé à la position ' + str(self.__findNthOverlapping(self.equation, searchFailNumber.group(0), 1) + 1)+'.'
            return False

        # Search particular case where dot is not between numbers
        searchFailDot = re.search('([^0-9]\.[^0-9]|[^0-9]\.|\.[^0-9]|\.[0-9]\.|\.$|^\.)', self.equation)
        if (searchFailDot):
            self.error = 'Synthax error: Caractère mal placé à la position ' + str(self.__findNthOverlapping(self.equation, searchFailDot.group(0), 1) + 1)+'.'
            return False

        # Search particular case: space between numbers
        searchFailNumber = re.search('(\d +\d)', self.equation)
        if searchFailNumber:
            self.error = 'Synthax error: Caractère mal placé à la position ' + str(self.__findNthOverlapping(self.equation, searchFailNumber.group(0), 1) + 1)+'.'
            return False

        #verify char positions, x can be placed anywhere
        maxLen = len(self.equation)
        for i in range(0, maxLen):
            if (i == 0) and (self.__findNthOverlapping('-+0123456789x', self.equation[i], 1) == -1):
                self.error = 'Synthax error: Caractère mal placé à la position ' + str(i)+'.'
                return False
            if (self.equation[i] == '^') and ((i == 0) or re.search('^(\^[-|+|\s]*[0-9]+)', self.equation[i:]) == None):
                self.error = 'Synthax error: Caractère mal placé à la position ' + str(i)+'.'
                return False
            if (self.equation[i] == '=') and ((i == 0) or re.search('^(=[\-|+|\s]*[0-9|x]+)', self.equation[i:]) == None):
                self.error = 'Synthax error: Caractère mal placé à la position ' + str(i)+'.'
                return False
            if (self.equation[i] == '+') and (re.search('^(\+[\-|+|\s]*[0-9|x]+)', self.equation[i:]) == None):
                self.error = 'Synthax error: Caractère mal placé à la position ' + str(i)+'.'
                return False
            if (self.equation[i] == '-') and (re.search('^(\-[\-|+|\s]*[0-9|x]+)', self.equation[i:]) == None):
                self.error = 'Synthax error: Caractère mal placé à la position ' + str(i)+'.'
                return False
            if (self.equation[i] == '*') and ((i == 0) or re.search('^(\*[\-|+|\s]*[0-9|x]+)', self.equation[i:]) == None):
                self.error = 'Synthax error: Caractère mal placé à la position ' + str(i)+'.'
                return False
            if (self.equation[i] == '/') and ((i == 0) or re.search('^(\/[\-|+|\s]*[0-9|x]+)', self.equation[i:]) == None):
                self.error = 'Synthax error: Caractère mal placé à la position ' + str(i)+'.'
                return False
            if (self.equation[i].isdigit()) and (re.search('^([0-9][^\^])', self.equation[i:]) == None) and (re.search('^([0-9])$', self.equation[i:]) == None):
                self.error = 'Synthax error: Caractère mal placé à la position ' + str(i)+'.'
                return False
            if (self.equation[i] == ' ') and (re.search('(\s[^\^])', self.equation[i:]) == None) and (re.search('^(\s)$', self.equation[i:]) == None):
                self.error = 'Synthax error: Caractère mal placé à la position ' + str(i)+'.'
                return False
        return True

    def __transformEquation(self):
        # Remove spaces
        self.equation = self.equation.replace(' ', '')
        # Replace and remove signs [+|-]
        self.equation = self.__replaceSigns(self.equation)
        # Add * around x
        self.equation = self.__checkForX(self.equation)

    def __transformElementToValues(self, element: str):
        values = dict()
        if len(element) > 0:
            value:int = 0
            degres:int = 0
            i:int = 0
            if (len(element) > 0):
                value = self.__atof(element)
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
                            if element[1] == '^':
                                degres = self.__atoi(element[2:])
                            else:
                                value = value * self.__atoi(element[1:]) if value != 0 else self.__atoi(element[1:])
            if degres in values:
                values[degres] += value
            else:
                values[degres] = value
        return values

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
        if len(self.steps) > 0:
            self.reduced = self.steps[-1]
        else:
            self.reduced = self.__toString(self.__valuesMemberLeft) + ' = ' + self.__toString(self.__valuesMemberRight)
            self.reduced = self.reduced.replace('.0 ', ' ')

    def __simplify(self, leftMember, rightMember):
        self.__addStep(leftMember, rightMember)
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
                        leftFormatted[i - 1] = self.__operations[currentOpe[1]](currentOpe[0], currentOpe[2])
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
        self.__addStep(leftMember, rightMember)

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

    def __addStep(self, left:str, right:str):
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
        printStep = printStep.replace('.0 ', ' ')
        if (printStep != self.__lastStepPrint):
            self.__lastStepPrint = printStep
            self.steps.append(printStep)

    def __calcDelta(self):
        a = self.__valuesMemberLeft[2] if 2 in self.__valuesMemberLeft else 0
        b = self.__valuesMemberLeft[1] if 1 in self.__valuesMemberLeft else 0
        c = self.__valuesMemberLeft[0] if 0 in self.__valuesMemberLeft else 0
        self.delta = (math.pow(b, 2)) - (4 * a * c)

    def __resolve(self):
        keys = list(self.__valuesMemberLeft.keys())
        keys = sorted(keys, reverse=True)
        self.polynomialDegree = 0
        for key in keys:
            if self.__valuesMemberLeft[key] != 0:
                self.polynomialDegree = key
                break
        if self.polynomialDegree > 2:
            self.polynomialDegreeTooHigh = True
        else:
            self.__calcRoots()
            if (self.polynomialDegree == 0):
                if (self.roots[0] != 0):
                    self.sidesNotEquals = True
                else:
                    self.allNumbersAsSolution = True
                self.roots = []

    def __calcRoots(self):
        values = self.__valuesMemberLeft
        a = values[2] if 2 in values else 0
        b = values[1] if 1 in values else 0
        c = values[0] if 0 in values else 0
        if a != 0:
            self.__calcDelta()
            if self.delta > 0:
                rootOne = (- b - math.sqrt(self.delta)) / (2 * a)
                rootTwo = (- b + math.sqrt(self.delta)) / (2 * a)
                rootOneAsString = str(rootOne).replace('.0 ', ' ')
                rootTwoAsString = str(rootTwo).replace('.0 ', ' ')
                self.roots = [rootOneAsString, rootTwoAsString]
            if self.delta == 0:
                root = (- b) / (2 * a)
                rootAsString = str(root).replace('.0 ', ' ')
                self.roots = [(- b) / (2 * a)]
            if self.delta < 0:
                currentDelta = self.delta * -1
                partOne = (- b ) / (2 * a)
                partTwo = (math.sqrt(currentDelta)) / (2 * a)
                rootOnePartTwoSign = '-' if (partTwo < 0) else '+'
                rootTwoPartTwoSign = '+' if (partTwo < 0) else '-'
                if partTwo < 0:
                    partTwo = partTwo * -1
                rootOne = ''
                rootTwo = ''
                if partOne != 0:
                    rootOne = str(partOne)
                    rootTwo = str(partOne)
                if partTwo != 0:
                    rootOneSpaces = False
                    rootTwoSpaces = False

                    if len(rootOne) > 0:
                        rootOne += ' '
                        rootOneSpaces = True
                    if (len(rootOne) > 0) or (rootOnePartTwoSign == '-'):
                        rootOne += rootOnePartTwoSign
                    if rootOneSpaces is True:
                        rootOne += ' '
                    if partTwo != 1:
                        rootOne += str(partTwo)
                    rootOne += 'i'

                    if len(rootTwo) > 0:
                        rootTwo += ' '
                        rootTwoSpaces = True
                    if (len(rootTwo) > 0) or (rootTwoPartTwoSign == '-'):
                        rootTwo += rootTwoPartTwoSign
                    if rootTwoSpaces is True:
                        rootTwo += ' '
                    if partTwo != 1:
                        rootTwo += str(partTwo)
                    rootTwo += 'i'
                self.roots = [rootOne, rootTwo]
        elif b != 0:
            self.roots = [- c / b]
        else :
            self.roots = [c]
        for i in range(0, len(self.roots)):
            self.roots[i] = str(self.roots[i]).replace('.0 ', ' ')
            self.roots[i] = str(self.roots[i]).rstrip('0').rstrip('.')
            self.roots[i] = str(self.roots[i]).replace('.0i', 'i')
            self.roots[i] = '0' if str(self.roots[i]) == '-0' else self.roots[i]     

    def __add(self, src: dict, dest: dict):
        for key in dest:
            if key in src:
                src[key] += dest[key]
            else:
                src[key] = dest[key]
        return src

    def __sub(self, src: dict, dest: dict):
        for key in dest:
            if key in src:
                src[key] -= dest[key]
            else:
                src[key] = dest[key] * -1
        return src

    def __mul(self, src: dict, dest: dict):
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

    def __div(self, src: dict, dest: dict):
        """
        ⚠️ Ne fonctionne que si dest ne contient qu'un element à l'heure actuelle ⚠️
        """
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

    def __replaceSigns(self, string: str):
        while True:
            string = string.replace('-+', '-')
            string = string.replace('+-', '-')
            string = string.replace('--', '+')
            string = string.replace('++', '+')
            string = string.replace('*+', '*')
            string = string.replace('/+', '/')
            if (string.find('-+') == -1) and (string.find('+-') == -1) and (string.find('++') == -1) and (string.find('--') == -1) and (string.find('*+') == -1) and (string.find('/+') == -1):
                break
        return string

    def __replaceString(self, text:str, start_index:int, lengthToReplace: int, replacement:str = ''):
        return text[0:start_index] + replacement + text[start_index + lengthToReplace:]

    def __checkForX(self, member: str, replaceBefore: bool = False):
        i = 0
        while i < len(member) - 1:
            if member[i] == 'x':
                if (replaceBefore == True) and (i > 0) and (member[i - 1].isdigit()):
                    member = self.__replaceString(member, i, 1, '*x')
                    i = i - 1
                elif (i < len(member) - 1) and (member[i + 1].isdigit()):
                    member = self.__replaceString(member, i, 1, 'x*')
            i += 1
        return member

    def __atoi(self, string:str):
        sign = 1
        i = 0
        if string[0] == '-':
            sign = -1
            i = 1

        if string[0] == '+':
            sign = 1
            i = 1

        num = 0
        while i < len(string):
            if '0' <= string[i] <= '9':
                num = num * 10 + ord(string[i]) - ord('0')
            else:
                break
            i += 1
        return num * sign

    def __atof(self, string:str):
        p = re.compile('^([+\|-]?[\d]+(\.[\d]*)?)')
        m = p.match(string)
        if m:
            result = m.groups()[0]
            if '.' in result:
                return float(result)
            else:
                return int(result)
        else:
            return 0

    def __findNthOverlapping(self, haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+1)
            n -= 1
        return start

    def toJSON(self):
        res = {}
        res['allNumbersAsSolution'] = self.allNumbersAsSolution,
        res['delta'] = self.delta,
        res['equation'] = self.equation,
        res['error'] = self.error,
        res['polynomialDegree'] = self.polynomialDegree,
        res['polynomialDegreeTooHigh'] = self.polynomialDegreeTooHigh,
        res['reduced'] = self.reduced,
        res['roots'] = self.roots,
        res['sidesNotEquals'] = self.sidesNotEquals,
        res['steps'] = self.steps
        return json.dumps(res)