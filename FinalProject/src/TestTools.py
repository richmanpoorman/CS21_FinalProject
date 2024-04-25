TEST_FILE = "Test.txt"

SHOULD_PRINT = False

def outputInit():
    if not SHOULD_PRINT:
        return
    with open(TEST_FILE, "w") as file:
        file.write("")

def outputLn(message : str):
    if not SHOULD_PRINT:
        return
    with open(TEST_FILE, "a") as file:
        if message:
            file.write(message + "\n")
        else:
            file.write("None\n")