def authorizeChar(string: str):
    charList = "0123456789+-*/^x"
    for i in range(0, len(string)):
        validChar = False
        for j in range(0, len(charList)):
            if (validChar == False) and string[i] == charList[j]:
                validChar = True
                break
        if validChar == False:
            return False
    return True

def authorizeCharPosition(string: str):
    for i in range(0, len(string)):
        if (string[i] == '^'):
            if (i == 0) or (i == len(string) - 1) or (string[i - 1].isdigit() == False) or (string[i + 1].isdigit() == False) or (string[i + 1] == 'x'):
                return False
        if (string[i] == '*') or (string[i] == '/'):
            if (i == 0) or (i == len(string) - 1):
                return False
            if (string[i - 1].isdigit() == False) and (string[i - 1] != 'x'):
                return False
            if (string[i + 1].isdigit() == False) and (string[i + 1] != 'x') and (string[i + 1] != '+'):
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
