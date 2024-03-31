from Display import Display
from InputListener import InputListener

class ClientRunner:
    def __init__(self):
        self.display       = Display() 
        self.inputListener = InputListener() 
        self.run() 

    def run(self):
        pass


ClientRunner()