from brackets import brackets
from utils import authorizeChar
from utils import replaceSigns
from utils import authorizeCharPosition

def verifEquation(equation: str):
    if equation.count('=') != 1:
        print("SynthaxError: Mauvais nombre de '='")
        return False
    equation = replaceSigns(equation)
    equation_left = equation[0:equation.find('=')]
    equation_right = equation[equation.find('=') + 1: len(equation)]
    if (len(equation_left) == 0) or (len(equation_right) ==0):
        print("SyntaxError: Half equation missing")
        return False
    if (brackets(equation_left) == False) or (brackets(equation_right) == False):
        print("SynthaxError: Brackets error")
        return False
    if (authorizeChar(equation_left) == False) or (authorizeChar(equation_right) == False):
        print("SynthaxError: Forbidden character")
        return False
    if (authorizeCharPosition(equation_left) == False) or (authorizeCharPosition(equation_right) == False):
        print("SynthaxError: Forbidden character position")
        return False
    return True
