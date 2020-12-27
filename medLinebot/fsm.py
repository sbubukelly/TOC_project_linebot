from transitions import Machine
#from transitions.extensions import GraphMachine as Machine

class TocMachine(object):
   
    def __init__(self, **machine_configs):
        self.machine = Machine(model=self,use_pygraphviz=False, **machine_configs)

    '''
    def drawFSM(self):
        self.get_graph().draw('my_state_diagram.png', prog='dot')
    '''


#machine.drawFSM()


        