import sys, os
sys.path.insert(0, os.path.dirname(__file__) + "/utils")
sys.path.insert(0, os.path.dirname(__file__) + "/class")
from verif_equation import verifEquation
from equation import Equation

print ("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
print ("5 - 4 * X - 9.3 * 9 * -X^2 = -X^0")
print ("5 + X4 - 9.3X^2 = 1 * X^0")

run = True

while run == True:
    equationInput = input("\nEntrez une équation: ").lower()
    equationInput = equationInput.strip(" ")
    if (equationInput == "q") or (equationInput == "quit") or (equationInput == "exit"):
        run = False
        continue
    equationInput = equationInput.replace(' ', '')
    if (len(equationInput) == 0):
        continue
    if (verifEquation(equationInput) == False):
        continue

    equation = Equation(0, 0, 0)
    print("A=", equation.a, "   B=", equation.b, "   C=", equation.c, "   Delta=", equation.delta, "   Roots=", equation.roots())
    equation = Equation(4, 4, 1)
    print("A=", equation.a, "   B=", equation.b, "   C=", equation.c, "   Delta=", equation.delta, "   Roots=", equation.roots())
    equation = Equation(1, 1, 11)
    print("A=", equation.a, "   B=", equation.b, "   C=", equation.c, "   Delta=", equation.delta, "   Roots=", equation.roots())
    equation = Equation(2, 10, 2)
    print("A=", equation.a, "   B=", equation.b, "   C=", equation.c, "   Delta=", equation.delta, "   Roots=", equation.roots())

print("A la prochaine !")
