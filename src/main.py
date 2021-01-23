import sys, os, signal, re
sys.path.insert(0, os.path.dirname(__file__) + '/utils')
sys.path.insert(0, os.path.dirname(__file__) + '/class')
from run_equation import runEquation
from run_equation import runRandomEquation

def signal_handler(sig, frame):
    if (sig == 2):
        exit()

def exit():
    os._exit(0)

def help():
    print('\033[4mCommandes disponibles :\033[0m')
    print('\t\033[1mrandom\033[0m : Générer une équation aléatoire')
    print('\t\033[1mexit\033[0m : Quitter le programme')
    print('')
    print('\033[4mExemple d\'équations valides :\033[0m')
    print('\t3x + 4x^2 - 5 = 0')
    print('\t2x = 3')
    print('\tx^0 + 1 = x^1')

try:
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        equationInput = input('\nEntrez une équation: ')
        equationInput = equationInput.lower().strip(' ')
        if len(equationInput) > 0:
            if (equationInput == 'q') or (equationInput == 'quit') or (equationInput == 'exit'):
                exit()
            elif (equationInput == 'r') or (equationInput == 'ran') or (equationInput == 'random'):
                runRandomEquation()
                continue
            elif (equationInput == 'h') or (equationInput == 'help'):
                help()
                continue
            else:
                runEquation(equationInput)
except EOFError:
    print('\nError: EOFError')
    exit()
