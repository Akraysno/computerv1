import sys, os, signal, re
sys.path.insert(0, os.path.dirname(__file__) + '/utils')
sys.path.insert(0, os.path.dirname(__file__) + '/class')
from run_equation import runEquation
from run_equation import runRandomEquation

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
            elif (equationInput == 'r') or (equationInput == 'ran') or (equationInput == 'random'):
                runRandomEquation()
                continue
            else:
                runEquation(equationInput)
except EOFError:
    print('\nError: EOFError')
    exit()
