import io
from io import StringIO
# f =  StringIO("1\n0\n0\n1\n1\n0\n1\n")
# States = ['S1', 'S2', 'S3']
event_actions = {
    'S1_1': {0: 'T<15', 1: '35<T'},
    'S2_1': {0: 'T<25', 1: '40<T'},
    'S2_2': {0: 'T<35', 1: '45<T'},
    'S2_3': {0: 'T<40'},
    'S3_1': {0: 'T<10', 1: '30<T'},
    'S3_2': {0: 'T<5', 1: '12<T'},
    'S3_3': {1: '7<T'} 
}
next_state = {
    'S1': {
        'T<15': 'S3',
        '35<T': 'S2'
    },
    'S2': {
        'T<25': 'S1'
    },
    'S3': {
        '30<T': 'S2'
    }
}

state_mappers = {
    'S2': {
        'S2_1': {
            '40<T': 'S2_2',
            'T<25': 'S2_OUT'            
        },
        'S2_2': {
            '45<T': 'S2_3',
            'T<35': 'S2_1'
        },
        'S2_3': {
            'T<40':'S2_2'
        },
        'S2_OUT': {
            '35<T': 'S2_1'
        }
    }, 
    'S1': {
        'S1_1': {
            'T<15': 'S1_OUT',
            '35<T': 'S1_OUT'
        },
        'S1_OUT': {
        }
        
    }, 
    'S3': {
        'S3_1': {
            'T<10': 'S3_2',
            '30<T': 'S3_OUT'            
        },
        'S3_2': {
            'T<5': 'S3_3',
            '12<T': 'S3_1'
        },
        'S3_3': {
            '7<T':'S3_2'
        },
        'S3_OUT': {
            'T<15': 'S3_1'
        }
    }
}

action_map= {
    'S1': 'Heater: OFF, Cooler: OFF',
    'S2': 'Heater: OFF, Cooler: ON',
    'S3': 'Heater: ON, Cooler: OFF',
    'S1_1': None,
    'S2_1': 'CRS = 4RPS',
    'S2_2': 'CRS = 6RPS',
    'S2_3': 'CRS = 8RPS',
    'S3_1': 'Power = 10W',
    'S3_2': 'Power = 20W',
    'S3_3': 'Power = 30W'
}

default_states = {
    'S1': 'S1_1',
    'S2': 'S2_1',
    'S3': 'S3_1'
}
out_states = {
    'S1': 'S1_OUT',
    'S2': 'S2_OUT',
    'S3': 'S3_OUT'
}
def print_read_message(state):
    state_actions_dict = event_actions[state]
    print('Please select the next possible event...')
    for key in state_actions_dict:
        message = str(key) + ' : ' + state_actions_dict[key]
        print(message)
    

def read_event(state):
    print_read_message(state)
    # txt = f.readline().strip()
    txt =input().strip()
    if not txt.isalnum(): raise Exception('System Failure.')
    option = int(txt)
    if option not in event_actions[state].keys():
        raise Exception('System Failure.')
    return event_actions[state][option]

    

def action(state: str):
    if state is None: return
    action = action_map[state]
    print(f'At State {state}, action: {action} has been performed.')


def call_super_state(state, state_mapper, default_state, out_state):
    action(state)
    PS = default_state
    e = None
    while(PS != out_state):
        action(PS)
        e = read_event(PS)
        PS = state_mapper[PS][e]
    return e



def run(init_state: str):
    PS = init_state
    while(True):
        e = call_super_state(state= PS, 
                             state_mapper= state_mappers[PS], 
                             default_state= default_states[PS], 
                             out_state= out_states[PS]
                            )
        PS = next_state[PS][e]
        if PS not in States:
            raise Exception('System Failure.')
        


run('S1')
        


    
    
