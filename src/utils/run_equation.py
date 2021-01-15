from equation import Equation
from random import random
from math import floor
from fractions import Fraction
from decimal import Decimal

def runEquation(equation:str, equationOptions= {}):
    try:
        eq = Equation(equation, equationOptions)
        eq.resolve()
    except ValueError as err:
        print('Error : ' + err.args[0])

def runRandomEquation(equationOptions = {}):
    try:
        eq = Equation(genretateRandomValidatedEquation(), equationOptions)
        eq.resolve()
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
