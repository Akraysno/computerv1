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

def authorizeCharPosition(string: str):
    for i in range(0, len(string) - 1):
        if (string[i] == '^'):
            if (i == 0) or (i == len(string) - 1) or (string[i - 1].isdigit() == False) or (string[i + 1].isdigit() == False):
                return False
        if (string[i] == '*') or (string[i] == '/'):
            if (i == 0) or (i == len(string) - 1) or (string[i - 1].isdigit() == False) or (string[i - 1] != '(') or (string[i + 1].isdigit() == False) or (string[i + 1] != ')') or (string[i + 1] != '+') or (string[i + 1] != '-'):
                return False
        if (string[i] == '+') or (string[i] == '-'):
            if (i == len(string) - 1) or (string[i + 1].isdigit() == False):
                return False
    return True

def replaceSigns(string: str):
    while True:
        string = string.replace('-+', '-')
        string = string.replace('+-', '-')
        string = string.replace('--', '+')
        string = string.replace('++', '+')
        if (string.find('-+') == -1) and (string.find('+-') == -1) and (string.find('++') == -1) and (string.find('--') == -1):
            break
    return string
