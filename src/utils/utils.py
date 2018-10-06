def replaceSigns(string: str):
    while True:
        equation = equation.replace('-+', '-')
        equation = equation.replace('+-', '-')
        equation = equation.replace('--', '+')
        equation = equation.replace('++', '+')
        if (equation.find('-+') == -1) and (equation.find('+-') == -1) and (equation.find('++') == -1) and (equation.find('--') == -1):
            break
    return equation
