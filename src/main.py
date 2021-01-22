import sys, os, signal, re
sys.path.insert(0, os.path.dirname(__file__) + '/utils')
sys.path.insert(0, os.path.dirname(__file__) + '/class')
from run_equation import runEquation
from run_equation import runRandomEquation

print('5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0')
print('5 - 4 * X - 9.3 * 9 * -X^2 = -X^0')
print('5 + X4 - 9.3X^2 = 1 * X^0')

def signal_handler(sig, frame):
    if (sig == 2):
        print('\n\nUse \'exit\' or \'quit\' commands next time !')
        exit()

def exit():
    print('A la prochaine !')
    os._exit(0)

#Add 'man' and 'help' command
try:
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        equationInput = input('\nEntrez une équation: ')
        equationInput = equationInput.lower().strip(' ')
        if len(equationInput) > 0:
            if (equationInput == 'q') or (equationInput == 'quit') or (equationInput == 'exit'):
                exit()
            elif equationInput == 't':
                runEquation('3x^2 + x - 4 +8x - 4x^2 + 2 = -2x-2')
            elif equationInput == 'g':
                runEquation('3/3/x=0')
            elif equationInput == 'g2':
                runEquation('3x^2 + x - 4 +8x - 4x^-2 + 2 = -2x-2')
            elif (equationInput == 'r') or (equationInput == 'ran') or (equationInput == 'random'):
                runRandomEquation()
                continue
            else:
                runEquation(equationInput)
except EOFError:
    print('\nError: EOFError')
    exit()
