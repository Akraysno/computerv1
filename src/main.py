import sys, os, signal, re
sys.path.insert(0, os.path.dirname(__file__) + "/utils")
sys.path.insert(0, os.path.dirname(__file__) + "/class")
from run_equation import runEquation
from run_equation import runTests
from run_equation import runRandomEquation

print("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
print("5 - 4 * X - 9.3 * 9 * -X^2 = -X^0")
print("5 + X4 - 9.3X^2 = 1 * X^0")

def signal_handler(sig, frame):
    if (sig == 2):
        print("\n\nUse 'exit' or 'quit' commands next time !")
        exit()

def exit():
    print("A la prochaine !")
    os._exit(0)

def updateEquationOptions(string: str, equationOptions):
    options = string.split()
    options.pop(0)
    if (len(options) > 0):
        for opt in options:
            if (re.search('^(-s|--steps)=', opt)):
                opts = opt.split('=')
                opts.pop(0)
                if len(opts) > 0 and (opts[0] == 'false' or opts[0] == 'true'):
                    equationOptions['printSteps'] = False if opts[0] == 'false' else True
                else:
                    print('Invalid steps option value : ' + opts[0])
            else:
                print('Invalid option : ' + opt)
    else:
        print('\tPrint steps by passing steps argument to true:\n\t\t[(-s | --steps)=(true | false)]\n\t\tCurrent value : ' + 'false' if equationOptions['printSteps'] == False else true)
    return equationOptions

equationOptions = {
    'printSteps': False
}
#Add "man" and "help" command
try:
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        equationInput = input("\nEntrez une équation: ")
        equationInput = equationInput.lower().strip(" ")
        print(equationOptions)
        if len(equationInput) > 0:
            if (equationInput == "q") or (equationInput == "quit") or (equationInput == "exit"):
                exit()
            elif (equationInput == "r") or (equationInput == "ran") or (equationInput == "random"):
                runRandomEquation(equationOptions)
                continue
            elif (equationInput == "t") or (equationInput == "test"):
                runTests()
            elif (len(equationInput) > 0) and ((equationInput.split()[0] == 'o') or (equationInput.split()[0] == 'options')):
                equationOptions = updateEquationOptions(equationInput, equationOptions)
            else:
                runEquation(equationInput, equationOptions)
except EOFError:
    print("\nError: EOFError")
    exit()
