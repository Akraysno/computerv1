def resolveEquation(equation:str):
    equation_left = equation[0:equation.find('=')]
    equation_right = equation[equation.find('=') + 1:len(equation) - 1]
    member_left = resolveMember(equation_left, 0)
    member_right = resolveMember(equation_right, 0)

#return Equation()
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
