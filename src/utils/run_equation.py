import sys
from verif_equation import verifEquation
from equation import Equation
from utils import checkForX
from utils import replaceSigns

def runEquation(equation:str):
    try:
        eq = Equation(equation)
        print(eq)
    except ValueError as err:
        print("Error : " + err.args[0])

def runTests():
    eq = Equation("3x + 2 + 5x * 2 - 3x^2 = 3x^3 + 2x + 5 * 2 - 3x")
    print(eq)