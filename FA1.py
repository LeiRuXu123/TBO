class FiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state

    def reset(self):
        self.current_state = self.start_state

    def process_input(self, input_string):
        self.reset()
        for char in input_string:
            if char in self.alphabet:
                self.current_state = self.transition_function[self.current_state][char]
            else:
                raise ValueError(f"Invalid character {char} in input string.")
        
        return self.current_state in self.accept_states

# Membuat dan Menguji Finite Automaton
states = {'q0', 'q1'}
alphabet = {'a', 'b'}
transition_function = {
    'q0': {'a': 'q0', 'b': 'q1'},
    'q1': {'a': 'q0', 'b': 'q1'}
}
start_state = 'q0'
accept_states = {'q1'}

# Membuat instance dari FiniteAutomaton.
fa = FiniteAutomaton(states, alphabet, transition_function, start_state, accept_states)

# Menguji automaton dengan beberapa input string dan mencetak hasilnya.
test_strings = ['ab', 'aab', 'b', 'aaab', 'aaaa']
for s in test_strings:
    print(f"Input: {s}, Accepted: {fa.process_input(s)}")
