TEST_FILE = "Test.txt"

def outputInit():
    with open(TEST_FILE, "w") as file:
        file.write("")

def outputLn(message : str):
    with open(TEST_FILE, "a") as file:
        if message:
            file.write(message + "\n")
        else:
            file.write("None\n")