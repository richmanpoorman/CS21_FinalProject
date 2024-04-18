from GameProcess import GameProcess
from Erpy import stdio_port_connection
from term import Atom, Pid

from TestTools import outputLn, outputInit

class GameRunner: 
    def __init__(self):
        self.logic = GameProcess()
        self.inbox, self.port = stdio_port_connection()


    def run(self):
        outputLn("at top of running loop")
        # TODO:: Self.inbox is ending unexpectedly when sent message
        for msg in self.inbox:
            outputLn("in __updateModel")
            # self.__sendUpdates()
            # self.updateModel(msg)
            # self.runLogic()
        outputLn("Finished Running")



outputInit()
GameRunner() 