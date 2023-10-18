States = ['S1', 'S2', 'S3']
Events = []
next_state = {}


def read_event():
    pass

def action(State):
    pass

def call_S1():
    action['S1']
    pass

def call_S2():
    action['S2']
    pass

def call_S3():
    action['S3']
    pass



def run(init_state: str):
    PS = init_state
    while(True):
        NS = None
        match PS:
            case 'S1':
                e = call_S1()
                NS = next_state['S1'][e]
            case 'S2':
                e = call_S1()
                NS = next_state['S2'][e]
            case 'S3':
                e = call_S1()
                NS = next_state['S3'][e]
            case _ :
                return 'Error'
        PS = NS

    
    
