import sys, os, signal
sys.path.insert(0, os.path.dirname(__file__) + "/utils")
sys.path.insert(0, os.path.dirname(__file__) + "/class")
from run_equation import runEquation
from run_equation import runTests

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

#Add "man" and "help" command
try:
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        equationInput = input("\nEntrez une équation: ")
        equationInput = equationInput.lower().strip(" ")
        if (equationInput == "q") or (equationInput == "quit") or (equationInput == "exit"):
            exit()
        elif (equationInput == "t") or (equationInput == "test"):
            runTests()
            continue
        else:
            runEquation(equationInput)
except EOFError:
    print("\nError: EOFError")
    exit()
