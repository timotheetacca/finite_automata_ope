import csv, os

class finite_automata:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nb_symbols = 0
        self.nb_states = 0
        self.nb_initial_states = 0
        self.list_initial_states = []
        self.nb_final_states = 0
        self.list_final_states = []
        self.nb_transitions = 0
        
        # Of the form : {key: {symbol_1: [ ], symbol_2: [ ] }}
        self.dict_transitions = {} 
        
        self.dict_sink = {}
        self.list_symbols = []

    def get_fa_information(self):
        # Check if the file exists
        if not os.path.exists(self.file_path):
            print(f"You don't have any file named '{self.file_path}' ⚠ ")
            return

        with open(self.file_path, "r") as fa:
            # Read the automaton file and split it into lines
            lines = []
            for line in fa.readlines():
                lines.append(line.strip())

            # Read the lines and gather information for the automata
            self.nb_symbols = int(lines[0])
            self.nb_states = int(lines[1])
            self.nb_initial_states = int(lines[2].split(" ")[0])
            self.nb_final_states = int(lines[3].split(" ")[0])
            self.nb_transitions = int(lines[4])
            self.list_initial_states = lines[2].split(" ")[1:]
            self.list_final_states = lines[3].split(" ")[1:]

            # Go through transitions and add any new symbols to the list
            for i in range(self.nb_transitions):
                # Split the line to get the second element, which is the symbol
                if (lines[i + 5]).split(" ")[1] not in self.list_symbols:
                    self.list_symbols.append((lines[i + 5]).split(" ")[1])

            # Create a dictionary to store where each state goes for each symbol
            for transition in lines[5:]:     
                
                # split_transition is of the form [source state, symbol, target state]
                split_transition = transition.split(" ")    
                
                # Check if transition[0] and transition[2] are in the dict, if not add them with empty symbols list
                for j in [0,2]:
                    if self.dict_transitions.get(split_transition[j]) == None:
                        
                        # Add the states
                        self.dict_transitions[split_transition[j]] = {}

                        for i in range(self.nb_symbols):
                            # Add the symbols
                            self.dict_transitions[split_transition[j]][self.list_symbols[i]] = []

                # Add every corresponding states to their symbol
                self.dict_transitions[split_transition[0]][split_transition[1]].append(split_transition[2])
                

    def get_csv_from_fa(self, output_filepath):
        with open(output_filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            # Write the header of the CSV with symbols as column names, leaving two cells empty for alignment
            writer.writerow(["", ""] + self.list_symbols)

            # Write each state to the CSV, marking initial states with '>' and final states with '<'
            for state in self.dict_transitions.keys():
                if state in self.list_initial_states:
                    row = [">", state]
                elif state in self.list_final_states:
                    row = ["<", state]
                else:
                    row = ["", state]

                for symbol in self.list_symbols:
                    # Get the list of transitions for the symbol of a state
                    transition = self.dict_transitions[state].get(symbol)

                    if len(transition) > 0:
                        # Join the list into a single string separated by commas if there is more than 1 element
                        row.append("|".join(sorted(transition)))
                    else:
                        row.append("--")

                writer.writerow(row)

            if self.dict_sink != {}:
                row = ["", "P"]
                for i in self.list_symbols:
                    # For the sink, every transition goes to itself
                    row.append("P")
                writer.writerow(row)

    def is_deterministic(self, display=False):
        # Check if the automaton has more than 1 initial state, if yes, the automaton is not deterministic
        if self.nb_initial_states > 1:
            if display == True:
                print("Your automaton is not deterministic. There are several initial states ⚠ \n")
            return False

        # Check if a state has more than 1 transition for a given symbol, if yes, the automaton is not deterministic
        for state in self.dict_transitions:
            for symbol in self.list_symbols:
                if len(self.dict_transitions[state][symbol]) > 1:
                    if display == True:
                        print(f"Your automaton is not deterministic. State {state} has "
                            f"{len(self.dict_transitions[state][symbol])} transitions for symbol '{symbol}' ⚠ \n")
                    return False

        return True

    def is_complete(self, display=False):
        # Check if there are empty transitions, if yes, the automaton is not deterministic
        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                if self.dict_transitions[state][symbol] == []:
                    if display == True:
                        print(f"Your automaton is not complete. State {state} has no transitions for symbol '{symbol}' ⚠ \n")
                    return False
        return True
    
    def is_standard(self, display=False):
        
        # If a FA has more than 1 initial state, it is not standard
        if(self.nb_initial_states != 1): 
            return False
        
        initial_state = self.list_initial_states[0]
        
        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                if initial_state in  self.dict_transitions[state][symbol]:
                    if display == True :
                        print(f"Your automaton is not standard. {state} goes to the initial state ⚠ \n")
                    return False
            
        return True
        

    def completion(self):
        """
        Function that completes the automaton with a sink state
        """
        
        # Link all the empty transitions to the sink state
        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                if self.dict_transitions[state][symbol] == []:
                    self.dict_transitions[state][symbol] = ["P"]
                    
        # Add the sink state
        self.dict_sink["P"] = {}
        for i in range(self.nb_symbols):
            self.dict_sink["P"][self.list_symbols[i]] = ["P"]

    def determinization(self, states_to_process=None):
        """
        Function that determinizes the automaton
        """
        
        # Start with all existing states unless specific ones are given
        old_fa_was_completed = self.is_complete()
        if states_to_process is None:
            states_to_process = list(self.dict_transitions.keys())
        new_states = []

        # Process only the given states
        for state in states_to_process:
            for symbol in self.list_symbols:
                transitions = []

                # Collect all transitions for the current state and symbol
                for sub_state in state.split("|"):
                    if sub_state in self.dict_transitions:
                        for transition in self.dict_transitions[sub_state][symbol]:
                            if transition != "P" and transition not in transitions:
                                transitions.append(transition)

                if len(transitions) > 1:
                    # Create a new combined state for multiple transitions, excluding "P"
                    new_state = "|".join(sorted(transitions))
                    if new_state not in self.dict_transitions:
                        new_states.append(new_state)
                        # Initialize the new state with empty transitions
                        self.dict_transitions[new_state] = {}
                        for list_symbols_i in self.list_symbols:
                            self.dict_transitions[new_state][list_symbols_i] = []

                        # Inherit transitions from the components of the new state
                        for sub_state in transitions:
                            if sub_state in self.dict_transitions:
                                for list_symbols_i in self.list_symbols:
                                    for transition in self.dict_transitions[sub_state][list_symbols_i]:
                                        # Skip transitions to the sink state ("P")
                                        if transition != "P":

                                            # If the new state's transition is P, replace it with the current transition.
                                            if self.dict_transitions[new_state][list_symbols_i] == []:
                                                self.dict_transitions[new_state][list_symbols_i] = [transition]

                                            elif transition not in self.dict_transitions[new_state][list_symbols_i]:
                                                # If the transition doesn't exist yet,  add it to the list of transitions
                                                self.dict_transitions[new_state][list_symbols_i].append(transition)


        # Recursively process new combined states
        if new_states:
            self.determinization(new_states)

        # After processing all new states, clean up the original states
        self.cleanup_original_states()

        if old_fa_was_completed == True:
            self.completion()


    def cleanup_original_states(self):
        # List to store reachable states
        reachable_states = []

        # If there are multiple initial states, create a combined initial state
        if len(self.list_initial_states) > 1:
            new_initial_state = "|".join(sorted(self.list_initial_states))
            self.list_initial_states = [new_initial_state]
            self.nb_initial_states = 1
        # Start from initial state
        list_states = list(self.list_initial_states)

        while len(list_states) > 0:
            current_state = list_states[-1]
            list_states = list_states[:-1]
            if current_state not in reachable_states:
                reachable_states.append(current_state)

                # Check if the state still exists
                if current_state in self.dict_transitions:
                    for symbol in self.list_symbols:
                        # Loop between all the transitions of the state we are currently on
                        for transition in self.dict_transitions[current_state][symbol]:

                            # If the there is more than 1 transition for the state, join it as the new_state
                            if len(self.dict_transitions[current_state][symbol]) > 1:
                                transition = "|".join(sorted(self.dict_transitions[current_state][symbol]))

                            # If the transition we are on isn't a sink state and is reachable, keep it for the table
                            if transition != "P" and transition not in reachable_states:
                                list_states.append(transition)


        # Remove original states that are part of a combined state and are not reachable
        for state in list(self.dict_transitions.keys()):
            if ("|" not in state) and (state not in reachable_states):
                self.dict_transitions.pop(state)
