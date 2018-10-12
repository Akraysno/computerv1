def verifBrackets(string: str, index: int, root: bool):
    lenStr = len(string)
    i = index
    while i < lenStr:
        if string[i] == '(':
            i = i + verifBrackets(string[i+1:lenStr], 0) + 2
            if string[i - 1] != ')':
                return 0
            continue
        if string[i] == ')':
            return 0 if (root == True) and (i == 1) else i
        i += 1
    return 1

def verifNbBrackets(string: str):
    nb = 0
    i = -1
    lenStr = len(string)
    for i in range(0, lenStr):
        if string[i] == '(':
            nb += 1
        if string[i] == ')':
            nb -= 1
    return True if nb == 0 else False

def brackets(string: str):
    if verifNbBrackets(string) == False:
        return False
    return True if verifBrackets(string, 0, True) == 1 else False
