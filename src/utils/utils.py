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
            if (i == 0) or (i == len(string) - 1) or (string[i + 1].isdigit() == False) or (string[i - 1] != 'x'):
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

def replace_str(text:str, start_index:int, length: int, replacement:str = ''):
    return '%s%s%s'%(text[:start_index],replacement,text[start_index+length:])

def check_for_x(member: str):
    for i in range(0, len(member) - 1):
        if member[i] == 'x':
            if (i > 0) and (member[i - 1].isdigit()):
                member = replace_str(member, i, i , "*x")
            elif (i < len(member) - 1) and (member[i + 1].isdigit()):
                member = replace_str(member, i, 1, "x*")
    return member

def atoi(string:str):
    sign = 1
    i = 0
    if string[0] == '-':
        sign = -1
        i = 1

    if string[0] == '+':
        sign = 1
        i = 1

    num = 0
    while i < len(string):
        if '0' <= string[i] <= '9':
            num = num * 10 + ord(string[i]) - ord('0')
        else:
            break
        i += 1
    return num * sign