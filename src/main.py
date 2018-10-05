import sys, os
sys.path.insert(0, os.path.dirname(__file__) + "/utils")
from verif_equation import verif_equation

print ("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
print ("5 - 4 * X - 9.3 * 9 * -X^2 = -X^0")
print ("5 + X4 - 9.3X^2 = 1 * X^0")

run = True
while run == True:
    equation = input("\nEntrez une équation: ").lower()
    equation = equation.strip(" ")
    if (equation == "q") or (equation == "quit") or (equation == "exit"):
        run = False
        continue
    equation = equation.replace(' ', '')
    if (len(equation) == 0):
        continue
    if (verif_equation(equation) == False):
        print ("ERROR: Synthax error")
        continue
    print ("Equation is valide")


    """
    # Boucle de verification du formatage de la chaine
    if verif == "ERROR":
        run = 0
        print ("EQUATION PAS VALIDE")
    elif verif == "OK":
        print ("EQUATION VALIDE")

    while True:
        response = raw_input("\nRésoudre une nouvelle équation ? (Y/N): ").lower()
        if (response == "y") or (response == "yes"):
            run = 1
            break
        if (response == "n") or (response == "q") or (response == "quit") or (response == "non") or (response == "no"):
            run = 0
            break
"""
print("A la prochaine !")
