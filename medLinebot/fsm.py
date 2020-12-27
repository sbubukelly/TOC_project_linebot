#from transitions import Machine
from transitions.extensions import GraphMachine as Machine

class TocMachine(object):
   
    def __init__(self, **machine_configs):
        self.machine = Machine(model=self,use_pygraphviz=False, **machine_configs)

    def drawFSM(self):
        self.get_graph().draw('my_state_diagram.png', prog='dot')

machine = TocMachine(
    states=["user", "Menu1", "Menu2","Menu3","subMenu"],
    transitions=[
        {
            "trigger": "is_going_to_Menu2",
            "source": "Menu1",
            "dest": "Menu2",
        },
        {
            "trigger": "is_going_to_Menu3",
            "source": "Menu2",
            "dest": "Menu3",
        },
        {
            "trigger": "is_going_to_subMenu",
            "source": "Menu3",
            "dest": "subMenu",
        },
        {"trigger": "go_back", "source": ["Menu1", "Menu2","Menu3","subMenu"], "dest": "user"},
        {"trigger": "start", "source": ["user","Menu1", "Menu2","Menu3","subMenu"], "dest": "Menu1"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)    
machine.drawFSM()


        