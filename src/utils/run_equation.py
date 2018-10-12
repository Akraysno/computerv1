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
    sys.stdout.write("\n)3x=0 : ")
    runEquation(")3x=0")
    sys.stdout.write("\n3)x(=0 : ")
    runEquation("3)x(=0")
    sys.stdout.write("\n(3x+2)=0 : ")
    runEquation("(3x+2)=0")
    sys.stdout.write("\n(2)=0 : ")
    runEquation("(2)=0") 