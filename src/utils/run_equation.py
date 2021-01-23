from equation import Equation
from random import random
from math import floor
from fractions import Fraction
from decimal import Decimal

def printEquationResult(equation: Equation, rawEquation: str):
    print('Equation           : '+rawEquation+'\n')
    if equation.error:
        print(equation.error)
    else:
        if len(equation.steps) > 1:
            for i in range(0, len(equation.steps)):
                if i == 0:
                    print('Simplification     : '+equation.steps[i])
                else:
                    print('                     '+equation.steps[i])
            print('')
        print('Forme réduite      : '+equation.reduced+'\n')
        print('Degré du polynome  : '+str(equation.polynomialDegree)+'\n')
        if equation.polynomialDegreeTooHigh is True:
            print("Le degré du polynome est trop grand. Il doit être compris entre 0 et 2.")
        elif equation.sidesNotEquals is True:
            print("L'équation n'a pas de solution car les deux côtés de l'égalité ne sont pas égaux.")
        elif equation.allNumbersAsSolution is True: 
            print("Tous les nombres Réels (ℝ) sont solution")
        else:
            if equation.polynomialDegree == 2:
                print('Discriminant (𝚫)   : '+str(equation.delta).rstrip('0').rstrip('.')+'\n')
            if len(equation.roots) == 1:
                if (equation.polynomialDegree == 2) and (equation.delta == 0):
                    print("Le discriminant est nul, l'équation n'a qu'une solution.")
                print('La solution est    : x = '+str(equation.roots[0]))
            elif len(equation.roots) == 2:
                if equation.polynomialDegree == 2:
                    if equation.delta < 0:
                        print("Le discriminant est négatif, l'équation a deux solutions complexes (ℂ).")
                    if equation.delta > 0:
                        print("Le discriminant est positif, l'équation à deux solutions.")
                print('Les solutions sont : x1 = '+str(equation.roots[0]))
                print('                     x2 = '+str(equation.roots[1]))

def runEquation(equation:str):
    try:
        eq = Equation(equation)
        printEquationResult(eq, equation)
    except ValueError as err:
        print('Error : ' + err.args[0])

def runRandomEquation():
    try:
        equation = genretateRandomValidatedEquation()
        eq = Equation(equation)
        printEquationResult(eq, equation)
    except ValueError as err:
        print('Error : ' + err.args[0])

def genretateRandomValidatedEquation():
    memberLeft = generateRandomValidatedMemberEquation()
    memberRight = generateRandomValidatedMemberEquation() if floor(random() * 2) == 1 else '0'
    return memberLeft + ' = ' + memberRight

def generateRandomValidatedMemberEquation():
    member = ''
    if floor(random() * 100) > 25:
        member += generateRandomNumberAsString(len(member) > 0)
        member += 'x^2'
    if floor(random() * 100) > 25:
        member += generateRandomNumberAsString(len(member) > 0)
        member += 'x'
    if floor(random() * 100) > 25:
        member += generateRandomNumberAsString(len(member) > 0)
    return member if len(member) > 0 else '0'

def generateRandomNumberAsString(spacesAroundOperator: bool):
    operators = ['+', '-']#, '*', '/']
    ope = operators[floor(random() * 2)]
    numberString = ''
    number = floor(random() * 10) + 1
    neg = True if floor(random() * 2) == 1 else False
    if (ope == '-') and (neg == True):
        ope = '+'
    elif (ope == '-') or (neg == True):
        ope = '-'
    numberString += ' '+ope+' ' if spacesAroundOperator == True else '-' if neg == True else ''
    numberString += str(number)
    return numberString
