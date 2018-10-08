import sys, os
sys.path.insert(0, os.path.dirname(__file__) + "/utils")
sys.path.insert(0, os.path.dirname(__file__) + "/class")
from verif_equation import verifEquation
from equation import Equation
from resolve_equation import resolveEquation
from run_equation import runEquation
from run_equation import runTests

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
    if (equationInput == "t") or (equationInput == "test"):
        runTests()
        continue
    runEquation(equationInput)

print("A la prochaine !")
