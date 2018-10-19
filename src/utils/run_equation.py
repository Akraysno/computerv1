import sys
from verif_equation import verifEquation
from equation import Equation
from utils import check_for_x
from utils import replaceSigns
from polynome import Polynome


def eval_expression(expression):
    tokens = expression.split()
    print(tokens)
    rpn = infixToRPN(tokens)
    equation = RPNToEquation(rpn)
    return equation

def treat_member(member: str):
    member = member.replace('*', ' * ')
    member = member.replace('/', ' / ')
    member = member.replace('+', ' + ')
    member = member.replace('-', ' - ')
    stack = eval_expression(member)

def resolve_equation(equation: str):
    equation_left = equation[0:equation.find('=')]
    equation_right = equation[equation.find('=') + 1: len(equation)]
    treat_member(equation_left)
    treat_member(equation_right)

def runEquation(equation:str):
    equation = equation.replace(' ', '')
    if (len(equation) == 0):
        return
    equation = replaceSigns(equation)
    equation = check_for_x(equation)
    if (verifEquation(equation) == False):
        return
    resolve_equation(equation)

def runTests():
    """
    equation = Equation(0, 0, 0)
    equation.toString()
    equation = Equation(4, 4, 1)
    equation.toString()
    equation = Equation(1, 1, 11)
    equation.toString()
    equation = Equation(2, 10, 2)
    equation.toString()
    print("\n= : ")
    runEquation("=")
    print("\n3= : ")
    runEquation("3=")
    print("\n=3 : ")
    runEquation("=3")
    print("\nx=3 : ")
    runEquation("x=3")
    print("\n3x + 2 = 0 : ")
    runEquation("3x + 2 = 0")
    """
    print("\n3x^2 + 2 - x5 = 0 : ")
    runEquation("3x^2 + 2 - 5 * x = 0")


#Associativity constants for operators
LEFT_ASSOC = 0
RIGHT_ASSOC = 1
 
#Supported operators
OPERATORS = {
    '+' : (0, LEFT_ASSOC),
    '-' : (0, LEFT_ASSOC),
    '*' : (5, LEFT_ASSOC),
    '/' : (5, LEFT_ASSOC),
}
 
#Test if a certain token is operator
def isOperator(token):
    return token in OPERATORS.keys()
 
#Test the associativity type of a certain token
def isAssociative(token, assoc):
    if not isOperator(token):
        raise ValueError('Invalid token: %s' % token)
    return OPERATORS[token][1] == assoc
 
#Compare the precedence of two tokens
def cmpPrecedence(token1, token2):
    if not isOperator(token1) or not isOperator(token2):
        raise ValueError('Invalid tokens: %s %s' % (token1, token2))
    return OPERATORS[token1][0] - OPERATORS[token2][0]

    #Transforms an infix expression to RPN
def infixToRPN(tokens):
    out = []
    stack = []
    #For all the input tokens [S1] read the next token [S2]
    for token in tokens:
        if isOperator(token):
            # If token is an operator (x) [S3]
            while len(stack) != 0 and isOperator(stack[-1]):
                # [S4]
                if (isAssociative(token, LEFT_ASSOC)
                    and cmpPrecedence(token, stack[-1]) <= 0) or (isAssociative(token, RIGHT_ASSOC)
                    and cmpPrecedence(token, stack[-1]) < 0):
                    # [S5] [S6]
                    out.append(stack.pop())
                    continue
                break
            # [S7]
            stack.append(token)
        elif token == '(':
            stack.append(token) # [S8]
        elif token == ')':
            # [S9]
            while len(stack) != 0 and stack[-1] != '(':
                out.append(stack.pop()) # [S10]
            stack.pop() # [S11]
        else:
            out.append(token) # [S12]
    while len(stack) != 0:
        # [S13]
        out.append(stack.pop())
    return out

def RPNToEquation(rpn):
    print("rpn", rpn)
    stack = []
    secondStack = []

    #replace numbers by Polynomes
    """
    for token in rpn:
        if (isOperator(token)):
            stack.append(token)
        else:
            stack.append(Polynome(token, 0, 0))
    """
    #do operations
    for token in rpn:
        if (isOperator(token)):
            arg1 = rpn.pop()
            arg2 = rpn.pop()
            print(rpn)
            print(arg1, token, arg2)
            """
            if (token == '+'):
                res = arg1.add(arg2)
            if (token == '*'):
                res = arg1.mul(arg2)
            if (token == '-'):
                res = arg1.sub(arg2)
            if (token == '/'):
                res = arg1.div(arg2)
            
            if (res == False):
                print(False)
                secondStack.append(arg1)
                secondStack.append(arg2)
                secondStack.append(token)
            else:
                print(res)
                stack.append(res)
            """
        else:
            rpn.append(token)
    return rpn
