import pygame as py:
class InputListener:
    def __init__(self):
        pass 


    def checkAndSendInput(self):
        for event in py.get():
            inputValue = map()
            if event == py.QUIT:
                inputValue["QUIT"] = None 
            elif event == py.KEYDOWN:
                inputValue["KEY"] = event.key
            
            self.sendInput(inputValue)

    
    def sendInput(self, inputValue : map):
        # TODO: Use the erlang channel to send the (string, value) map over
        pass 