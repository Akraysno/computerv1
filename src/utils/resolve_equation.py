def resolveEquation(equation:str):
    equation_left = equation[0:equation.find('=')]
    equation_right = equation[equation.find('=') + 1:len(equation) - 1]
    member_left = resolveMember(equation_left, 0)
    member_right = resolveMember(equation_right, 0)

#return Equation()
#parse member and add parentheses aroud ^ * and /
"""
Si char 
    parse vers l'arriere et l'avant jusqu'a tomber sur un operateur
    si parenthese, evite tous les caracteres a l'interieur
parse member (mode: brackets)
    complete inline equation (mode: )
parse inline and reduct
merge inlines
reduct merge
resolve merge
"""
def resolveMember(member:str, index: int):
    lenStr = len(member)
    i = index
    while i < lenStr:
        if member[i] == '(':
            i = i + resolveMember(member[i+1:lenStr], 0) + 2
            if member[i - 1] != ')':
                return 0
            continue
        if member[i] == ')':
            return i
        i += 1
    return 1
