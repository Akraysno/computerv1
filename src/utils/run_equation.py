import sys, os
sys.path.insert(0, os.path.dirname(__file__) + "/utils")
sys.path.insert(0, os.path.dirname(__file__) + "/class")
from verif_equation import verifEquation
from equation import Equation
from resolve_equation import resolveEquation

def runEquation(equation:str):
    equation = equation.replace(' ', '')
    if (len(equation) == 0):
        return
    if (verifEquation(equation) == False):
        return

def runTests():
    equation = Equation(0, 0, 0)
    print("A=", equation.a, "   B=", equation.b, "   C=", equation.c, "   Delta=", equation.delta, "   Roots=", equation.roots())
    equation = Equation(4, 4, 1)
    print("A=", equation.a, "   B=", equation.b, "   C=", equation.c, "   Delta=", equation.delta, "   Roots=", equation.roots())
    equation = Equation(1, 1, 11)
    print("A=", equation.a, "   B=", equation.b, "   C=", equation.c, "   Delta=", equation.delta, "   Roots=", equation.roots())
    equation = Equation(2, 10, 2)
    print("A=", equation.a, "   B=", equation.b, "   C=", equation.c, "   Delta=", equation.delta, "   Roots=", equation.roots())
