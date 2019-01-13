import sys
from verif_equation import verifEquation
from equation import Equation
from utils import checkForX
from utils import replaceSigns
from polynome import Polynome

OPERATORS = ['+', '-', '*', '/']

def isOperator(token):
    return token in OPERATORS

def eval_expression(expression):
    tokens = expression.split()
    print(tokens)
    currentIndex = 0
    for tok in tokens:
        if isOperator(tok) == False:
            tokens[currentIndex] = Equation(Polynome(tok))
        currentIndex += 1
    print(tokens)
    values = []
    if len(values) < 4 + 1:
        for i in range(len(values), 4 + 1):
            values.append(0)
    print(len(values))
    values[4] = 5
    print(values)
    currentIndex = 0
    for tok in tokens:
        currentOpe = []
        if tok == '*':
            currentOpe = tokens[currentIndex - 1 : currentIndex + 1 : 1]
            tokens[currentIndex - 1] = 'Multiplication'
            del tokens[currentIndex:currentIndex + 2]
        currentIndex += 1
        print(tokens)
                
    
    return 

def treat_member(member: str):
    member = member.replace('*', ' * ')
    member = member.replace('/', ' / ')
    member = member.replace('+', ' + ')
    member = member.replace('-', ' - ')
    stack = eval_expression(member)

def resolve_equation(equation: str):
    equation_left = Equation(equation=equation[0:equation.find('=')])
    equation_right = Equation(equation=equation[equation.find('=') + 1: len(equation)])
    print(equation_left, "=", equation_right)
    #TODO finir la resolution
    

def runEquation(equation:str):
    try:
        eq = Equation(equation=equation)
    except ValueError as err:
        print("Error : " + err.args[0])
    """
    equation = equation.strip(' ')
    if (len(equation) == 0):
        return
    equation = replaceSigns(equation)
    equation = checkForX(equation)
    if (verifEquation(equation) == False):
        return
    resolve_equation(equation)
    """

def runTests():
    """
    equation = Equation(0, 0, 0)
    equation.toString()
    equation = Equation(4, 4, 1)
    equation.toString()
    equation = Equation(1, 1, 11)
    equation.toString()
    equation = Equation(2, 10, 2)
    equation.toString()
    print("\n= : ")
    runEquation("=")
    print("\n3= : ")
    runEquation("3=")
    print("\n=3 : ")
    runEquation("=3")
    print("\nx=3 : ")
    runEquation("x=3")
    print("\n3x + 2 = 0 : ")
    runEquation("3x + 2 = 0")
    """
    #print("\n3x^2 + 2 - x5 = 0 : ")
    #runEquation("3x^2 + 2 - 5 * x = 0")
    """
    eq1 = Equation(Polynome("3x^2"))
    eq2 = Equation(Polynome("-4x"))
    print(eq1, " ; ",eq2)
    eq1.div(eq2)
    print(eq1)
    """
    eq3 = Equation(equation="3x+2+5x*2-3x^2")
    eq4 = Equation(equation="3x^3+2x+5*2-3x")
    eq3.simplify(True)
    eq4.simplify(True)
    eq3.sub(eq4)
    print(eq3)