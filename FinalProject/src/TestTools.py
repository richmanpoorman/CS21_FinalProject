TEST_FILE = "Test.txt"

SHOULD_PRINT = False

def outputInit():
    '''
        Params  : (None)
        Purpose : Clears out the test file
        Return  : (None)
    '''
    if not SHOULD_PRINT:
        return
    with open(TEST_FILE, "w") as file:
        file.write("")

def outputLn(message : str):
    '''
        Params  : (str) message := The message to print to the log file
        Purpose : Print a line to the test file
        Return  : None
    '''
    if not SHOULD_PRINT:
        return
    with open(TEST_FILE, "a") as file:
        if message:
            file.write(message + "\n")
        else:
            file.write("None\n")