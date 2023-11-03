# General verilog code generatoer
import typing
from typing import List 

class System:
    def __init__(self, states: List[int], transition):
        self.states = states
        self.transition = transition
        self.all_events_available = False

    def all_states(self):
        return self.states
    
    def state_events(self, state):
        return self.transition[state]
    def all_events(self):
        if self.all_events_available:
            return self.events 
        else:
            self.all_events_available = True
            self.events = set()
            for state in self.transittion.keys():
                self.events.add(self.transition[state])
        return self.events
class Genertator:

    def get_state_binary_bit(self, state: int, n:int):
        if n < state: raise Exception('Invalid Input')
        res = str(n) + '\'b'
        for i in range(1, n + 1):
            if i == state:
                res +='1'
            else: res += '0'
        return res

    
    def generate_verilog_code(self, sys:System):
        code = 'module System(input start_system,\n'
        inputs = sys.all_events()

        outputs = ['action_' + s for s in sys.all_states()]
        for input in inputs:
            code += 'input ' + input + ',\n'

        for output in outputs:
            code += 'output reg' + output + ', \n'

        code += 'output reg system_failure)\n'
        state_count = len(sys.all_states[sys])
        code += 'reg ['+str(state_count)+':0] state;\n'
        code += 'always@(start_system '
        for event in sys.all_events():
            code += ' or\n' + event
        code += '\n)\n\tbegin\n'

        init_state = str(state_count) + '\'b' + '0' * state_count

        code += f'if (start_system and state == {init_state}) begin\n'
        code += '\t' + 'state <= ' + self.get_state_binary_bit(1, state_count) + ';\n'
        code += '\tsystem_failure <= 1\'b0;\n'
        code += 'end\n'

        for event in sys.all_events(): 
            code += 'else if (' + event + ')\n begin\n'
            code += '\tcase(state) begin\n'
            for state in sys.all_states():
                code += self.get_state_binary_bit(state, state_count) + ':\n'
                code += '\t\tbegin\n' 
                next_state = None
                if event in sys.transition[state]:
                    next_state = self.get_state_binary_bit(sys.transition[state][event])
                else:
                    code += '\t\tsystem_failure <= 1\'b1;\n'
                    next_state = init_state
                code += 'state <= ' + next_state + ';\n'
            code += 'default: '


            code += '\tend'
            code += 'end'
        code += 'endmodule'


