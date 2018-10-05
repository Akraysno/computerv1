def verif_brackets(string: str, index: int):
    lenStr = len(string)
    print("Verif brackets", string, index, lenStr)
    i = index
    while i < lenStr:
    #for i in range(index, lenStr - 1):
        print("boucle", i, string[i], string[i] == '(')
        if string[i] == '(':
            print("match (")
            i = i + verif_brackets(string[i+1:lenStr], 0) + 2
            if string[i - 1] != ')':
                print("match ( FAIL")
                return 0
            continue
        if string[i] == '{':
            print("match {")
            i = i + verif_brackets(string[i+1:lenStr], 0) + 2
            if string[i - 1] != '}':
                print("match { FAIL")
                return 0
            continue
        if string[i] == '[':
            print("match [")
            i = i + verif_brackets(string[i+1:lenStr], 0) + 2
            if string[i - 1] != ']':
                print("match [ FAIL")
                return 0
            continue
        if string[i] == ')' or string[i] == '}' or string[i] == ']':
            print("Match closure")
            return i
        i += 1
    print("return 1")
    return 1

def verif_nb_brackets(string: str):
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
    if verif_nb_brackets(string) == False:
        return False
    print("check number")
    brackets = verif_brackets(string, 0)
    print(brackets)
    return True if brackets == 1 else False
