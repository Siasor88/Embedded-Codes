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
            for state in self.transition.keys():
                for key in (self.transition[state].keys()):
                    self.events.add(key)
        self.events = sorted(list(self.events))
        return self.events


class Generator:
    def get_state_binary_bit(self, state: int, n: int):
        if n < state: raise Exception('Invalid Input')
        res = str(n) + '\'b'
        for i in range(1, n + 1):
            if i == n - state + 1:
                res += '1'
            else:
                res += '0'
        return res

    def generate_verilog_code(self, sys: System):
        code = 'module System(input start_system,\n'
        inputs = sys.all_events()

        outputs = ['action_' + str(s) for s in sys.all_states()]
        for input in inputs:
            code += '\t\tinput ' + input + ',\n'

        for output in outputs:
            code += '\t\toutput reg ' + output + ', \n'

        code += '\t\toutput reg system_failure\n);\n'
        state_count = len(sys.all_states())
        code += 'reg [' + str(state_count) + ':1] state;\n'
        code += 'always@(\n\t\tstart_system '
        for event in sys.all_events():
            code += ' or\n\t\t' + event
        code += '\n)\nbegin\n'

        init_state = str(state_count) + '\'b' + '0' * state_count

        code += f'if (start_system and state == {init_state}) begin\n'
        code += '\t' + 'state <= ' + self.get_state_binary_bit(1, state_count) + ';\n'
        code += '\tsystem_failure <= 1\'b0;\n'
        code += 'end\n'

        for event in sys.all_events():
            code += 'else if (' + event + ')\nbegin\n'
            code += '\tcase(state)\n'
            for state in sys.all_states():
                code += '\t' + self.get_state_binary_bit(state, state_count) + ':\n'
                code += '\t\tbegin\n'
                next_state = None
                if event in sys.transition[state]:
                    next_state = self.get_state_binary_bit(sys.transition[state][event], state_count)
                else:
                    code += '\t\tsystem_failure <= 1\'b1;\n'
                    next_state = init_state
                code += '\t\tstate <= ' + next_state + ';\n'
                code += '\t\tend\n'
            code += '\tdefault: \n'
            code += '\t\tbegin\n'
            code += '\t\tsystem_failure <= 1\'b1;\n'
            code += '\t\tstate <= ' + init_state + ';\n'
            code += '\t\tend\n'
            code += '\tendcase\n'
            code += 'end\n'

        code += 'always@(state) begin \n'
        code += '\tcase(state) \n'
        for state in sys.all_states():
            code += '\t' + self.get_state_binary_bit(state, state_count) + ':\n'
            code += '\t\tbegin\n'
            code += '\t\t' + f'action_{state} <= 1\'b1;\n'
            for st in sys.all_states():
                if st != state:
                    code += '\t\t' + f'action_{st} <= 1\'b0;\n'
            code += '\t\tend\n'
        code += '\tdefault: \n'
        code += '\t\tbegin\n'
        code += '\t\tsystem_failure <= 1\'b1;\n'
        code += '\t\tstate <= ' + init_state + ';\n'
        code += '\t\tend\n'
        code += '\tendcase\n'
        code += 'end\n'
        code += 'endmodule'
        return code


Sample_transition = {
    1: {'e1': 2, 'e2': 3, 'e3': 2},
    2: {'e1': 3, 'e2': 1, 'e3': 3},
    3: {'e1': 1, 'e2': 2, 'e3': 1}
}

sys = System(states=[1, 2, 3], transition=Sample_transition)
gen = Generator()
code = gen.generate_verilog_code(sys=sys)
print(code)