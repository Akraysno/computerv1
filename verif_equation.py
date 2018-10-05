from brackets import brackets

# return boolean => true no format error
def verif_equation(equation: str):
    if equation.count('=') != 1:
        print ("\nERROR: Mauvais nombre de '='")
        return False
    if brackets(equation) == False:
        print ("\nERROR: Brackets error")
        return False
    return True
