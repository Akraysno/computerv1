def verifBrackets(string: str, index: int):
    lenStr = len(string)
    i = index
    while i < lenStr:
        if string[i] == '(':
            i = i + verif_brackets(string[i+1:lenStr], 0) + 2
            if string[i - 1] != ')':
                return 0
            continue
        if string[i] == '{':
            i = i + verif_brackets(string[i+1:lenStr], 0) + 2
            if string[i - 1] != '}':
                return 0
            continue
        if string[i] == '[':
            i = i + verif_brackets(string[i+1:lenStr], 0) + 2
            if string[i - 1] != ']':
                return 0
            continue
        if string[i] == ')' or string[i] == '}' or string[i] == ']':
            return i
        i += 1
    return 1

def verifNbBrackets(string: str):
    nb_a = 0
    nb_c = 0
    nb_p = 0
    i = -1
    lenStr = len(string)
    for i in range(0, lenStr - 1):
        if string[i] == '[':
            nb_c += 1
        if string[i] == ']':
            nb_c -= 1
        if string[i] == '{':
            nb_a += 1
        if string[i] == '}':
            nb_a -= 1
        if string[i] == '(':
            nb_p += 1
        if string[i] == ')':
            nb_p -= 1
    return True if (nb_a == 0 and nb_c == 0 and nb_p == 0) else False;

def brackets(string: str):
    if verifNbBrackets(string) == False:
        return False
    return True if verifBrackets(string, 0) == 1 else False
