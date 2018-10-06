from brackets import brackets
from utils import authorizeChar
from utils import replaceSigns

# return boolean => true no format error
def verifEquation(equation: str):
    if equation.count('=') != 1:
        print ("SynthaxError: Mauvais nombre de '='")
        return False
    equation = replaceSigns(equation)
    if brackets(equation) == False:
        print ("SynthaxError: Brackets error")
        return False
    if authorizeChar(equation, "0123456789+-*/^") == False:
        print ("SynthaxError: Forbidden charactere")
        return False
    return True
