from verif_equation import verif_equation

print ("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
print ("5 - 4 * X - 9.3 * 9 * -X^2 = -X^0")
print ("5 + X4 - 9.3X^2 = 1 * X^0")

while True:
    equation = input("\nEntrez une équation: ").upper()
    if (equation == "q") or (equation == "quit") or (equation == "exit"):
        break
    equation = equation.replace(' ', '')
    if (verif_equation(equation) == False):
        print ("ERROR: Synthax error")
        continue
    print ("Equation is valide")

print("A la prochaine !")
