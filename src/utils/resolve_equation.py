def replace_str(text:str, start_index:int, end_index: int, replacement:str = ''):
    return '%s%s%s'%(text[:start_index],replacement,text[start_index+end_index:])

def check_for_x(member: str, index: int):
    #cas 1: x et nomber collé
    if (i > 0) and (member[i - 1].isdigit()):
        member = replace_str(member, i, i + 1, "*x")
    elif (i < len(member) - 1) and (member[i + 1].isdigit()):
        member = replace_str(member, i, i + 1, "x*")
    return member

def is_operator(char):
    if (char == '+') or (char == '-') or (char == '*') or (char == '/'):
        return True
    return False

def get_left_index(member:str, index: int):
    i = 0
    if (index - i > 0):
        if member[index - 1].isdigit():
            i += 1
            while (index - i >= 0) and (member[index - i].isdigit()):
                i += 1
        elif member[index - 1] == 'x':
            i += 1
        elif member[index - 1] == ')':
            #appelle recurcif pour remplacer ce qui se trouve dans les parentheses
            i += 1
            while (index - i >= 0) and (member[index - i] != '('):
                i += 1
    return i

def get_right_index(member:str, index: int):
    i = 0
    if (index + i < len(member)):
        if (member[index + 1].isdigit()) or (member[index + 1] == '+') or (member[index + 1] == '-'):
            i += 1
            if (member[index + i] == '+') or (member[index + i] == '-'):
                i += 1
                while (index + i < len(member)) and (member[index + i].isdigit()):
                    i += 1
        elif member[index + 1] == '(':
            i += 1
            #appelle recurcif pour remplacer ce qui se trouve dans les parentheses
            while (index + i < len(member)) and (member[index - i] != ')'):
                i += 1
    return i

#def addParentheses(member: str):
member = "x3+4*2*x/2"
i = 0
print(member)
while i < len(member):
    #print(i, member[i])
    if member[i] == 'x':
        member = check_for_x(member, i)
    i += 1
print(member)
i = 0
while i < len(member):
    #print(i, member[i])
    if member[i] == 'x':
        member = check_for_x(member, i)
        print(member)
    if (member[i] == '*'):
        left_index = get_left_index(member, i)
        right_index = get_right_index(member, i)
        str_to_replace = "("+member[i - left_index:i + right_index + 1]+")"
        print(left_index, i, right_index, str_to_replace)
        member = replace_str(member, i - left_index, i + right_index + 1, str_to_replace)
    """
    if (member[i] == '*'):
        left_index = 0
        right_index = 0
        #possibilities: 2 * x, 2 * -x, x * 2, x * -2
        if check_for_x(member, i) == True:

        #while member[i - left_index]:
        member = replace_str_index(member, i, '333')
        print(member)
    """
    i += 1
    print(member)
print(member)


def simplifyMember(member: str):
    member = addParentheses(member)

def resolveEquation(equation:str):
    equation_left = equation[0:equation.find('=')]
    equation_right = equation[equation.find('=') + 1:len(equation) - 1]
    member_left = simplifyMember(equation_left)
    member_right = simplifyMember(equation_right)

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
