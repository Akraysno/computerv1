from equation import Equation

def runEquation(equation:str):
    try:
        eq = Equation(equation)
        print(eq)
    except ValueError as err:
        print("Error : " + err.args[0])

def runTests():
    try:
        eq = Equation("3x + 2 + 5x * 2 - 3x^2 = 3x^2 + 2x + 5 * 2 - 3x")
        eq.resolve()
        print(eq)
    except ValueError as err:
        print("Error : " + err.args[0])
    