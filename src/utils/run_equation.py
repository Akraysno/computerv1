import sys, os
sys.path.insert(0, os.path.dirname(__file__) + "/../utils")
sys.path.insert(0, os.path.dirname(__file__) + "/../class")
from verif_equation import verifEquation
from equation import Equation
from utils import check_for_x
from utils import replaceSigns

def treat_member(member: str):
    print("member : ", member)

def resolve_equation(equation: str):
    equation_left = equation[0:equation.find('=')]
    equation_right = equation[equation.find('=') + 1: len(equation)]
    treat_member(equation_left)
    treat_member(equation_right)

def runEquation(equation:str):
    equation = equation.replace(' ', '')
    if (len(equation) == 0):
        return
    equation = replaceSigns(equation)
    equation = check_for_x(equation)
    if (verifEquation(equation) == False):
        return
    resolve_equation(equation)

def runTests():
    equation = Equation(0, 0, 0)
    equation.toString()
    equation = Equation(4, 4, 1)
    equation.toString()
    equation = Equation(1, 1, 11)
    equation.toString()
    equation = Equation(2, 10, 2)
    equation.toString()
    sys.stdout.write("\n= : ")
    runEquation("=")
    sys.stdout.write("\n3= : ")
    runEquation("3=")
    sys.stdout.write("\n=3 : ")
    runEquation("=3")
    sys.stdout.write("\nx=3 : ")
    runEquation("x=3")
    sys.stdout.write("\n3x + 2 = 0 : ")
    runEquation("3x + 2 = 0")