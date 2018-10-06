def authorizeChar(string: str, charList:str):
    for i in range(0, len(string) - 1):
        validChar = False
        for j in range(0, len(charList) -1):
            if (validChar == False) and string[i] == charList[j]:
                validChar = True
                break
        if validChar == False:
            return False
    return True

def replaceSigns(string: str):
    while True:
        equation = equation.replace('-+', '-')
        equation = equation.replace('+-', '-')
        equation = equation.replace('--', '+')
        equation = equation.replace('++', '+')
        if (equation.find('-+') == -1) and (equation.find('+-') == -1) and (equation.find('++') == -1) and (equation.find('--') == -1):
            break
    return equation
