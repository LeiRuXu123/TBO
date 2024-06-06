class PushdownAutomaton:
    def __init__(self, states, alphabet, stack_alphabet, transition_function, start_state, accept_states, start_stack_symbol):
        self.states = states
        self.alphabet = alphabet
        self.stack_alphabet = stack_alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.start_stack_symbol = start_stack_symbol
        self.current_state = start_state
        self.stack = [start_stack_symbol]

    def reset(self):
        self.current_state = self.start_state
        self.stack = [self.start_stack_symbol]

    def process_input(self, input_string):
        self.reset()
        for char in input_string:
            if char in self.alphabet:
                state_stack_pair = (self.current_state, self.stack[-1])
                if state_stack_pair in self.transition_function and char in self.transition_function[state_stack_pair]:
                    self.current_state, stack_action = self.transition_function[state_stack_pair][char]
                    if stack_action == 'pop':
                        self.stack.pop()
                    elif stack_action != 'nop':
                        self.stack.append(stack_action)
                else:
                    return False
            else:
                raise ValueError(f"Invalid character {char} in input string.")
        
        return self.current_state in self.accept_states and self.stack == [self.start_stack_symbol]

# Membuat dan Menguji Pushdown Automaton
states = {'q0', 'q1', 'q2'}
alphabet = {'a', 'b'}
stack_alphabet = {'$', 'A'}
transition_function = {
    ('q0', '$'): {'a': ('q0', 'A'), 'b': ('q1', 'pop')},
    ('q0', 'A'): {'a': ('q0', 'A'), 'b': ('q1', 'pop')},
    ('q1', 'A'): {'b': ('q1', 'pop'), 'a': ('q0', 'A')},
    ('q1', '$'): {'a': ('q0', 'A')}
}
start_state = 'q0'
accept_states = {'q1'}
start_stack_symbol = '$'

# Membuat instance dari PushdownAutomaton
pda = PushdownAutomaton(states, alphabet, stack_alphabet, transition_function, start_state, accept_states, start_stack_symbol)

# Menguji automaton dengan beberapa input string dan mencetak hasilnya
test_strings = ['ab', 'aabb', 'aaabbb', 'aaaabbbb', 'aaabbb']
for s in test_strings:
    print(f"Input: {s}, Accepted: {pda.process_input(s)}")
