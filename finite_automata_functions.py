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
                split_transition = transition.split(" ")
                # Check if transition[0] and transition[2] are in the dict, if not add them with empty symbols list
                for j in range(0, 3, 2):
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
                        # If the transition isn't empty, convert each state to a string
                        for i in range(len(transition)):
                            transition[i] = str(transition[i])
                        # Join the list into a single string separated by commas if there is more than 1 element
                        row.append(".".join(transition))

                    else:
                        row.append("--")

                writer.writerow(row)

            if self.dict_sink != {}:
                row = ["", "P"]
                for i in self.list_symbols:
                    # For the sink, every transition goes to itself
                    row.append("P")
                writer.writerow(row)

    def is_deterministic(self):
        # Check if the automaton has more than 1 initial state, if yes, the automaton is not deterministic
        if self.nb_initial_states > 1:
            print("Your automaton is not deterministic. There are several initial states ⚠ \n")
            return False

        # Check if a state has more than 1 transition for a given symbol, if yes, the automaton is not deterministic
        for state in self.dict_transitions:
            for symbol in self.list_symbols:
                if len(self.dict_transitions[state][symbol]) > 1:
                    print(f"Your automaton is not deterministic. State {state} has "
                          f"{len(self.dict_transitions[state][symbol])} transitions for symbol '{symbol}' ⚠ \n")
                    return False

        return True

    def is_complete(self):
        # Check if there are empty transitions, if yes, the automaton is not deterministic
        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                if self.dict_transitions[state][symbol] == []:
                    print(f"Your automaton is not complete. State {state} has no transitions for symbol '{symbol}' ⚠ \n")
                    return False
        return True

    def completion(self):
        # Link all the empty transitions to the sink state
        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                if self.dict_transitions[state][symbol] == []:
                    self.dict_transitions[state][symbol] = ["P"]

        # Add the sink state
        self.dict_sink["P"] = {}
        for i in range(self.nb_symbols):
            self.dict_sink["P"][self.list_symbols[i]] = ["P"]

    def determinization_and_completion_automaton(self, states_to_process=None):
        # Start with all existing states unless specific ones are given
        if states_to_process == None:
            states_to_process = list(self.dict_transitions.keys())

        new_states = []

        # Process only the given states
        for state in states_to_process:
            for symbol in self.list_symbols:

                # Check if the transition has more than 1 state for the same symbol, if yes, create a new combined state
                if len(self.dict_transitions[state][symbol]) > 1:
                    new_state = ""
                    for i in range(len(self.dict_transitions[state][symbol])):
                        # Split the new state with ".", so you can differentiate 10 from 1.0
                        if len(new_state) > 0:
                            new_state += f"|{self.dict_transitions[state][symbol][i]}"
                        else:
                            new_state += f"{self.dict_transitions[state][symbol][i]}"

                    # If the new state doesn't exist, add it
                    if new_state not in self.dict_transitions:
                        new_states.append(new_state)

                        # Create an empty key with all empty symbol
                        self.dict_transitions[new_state] = {}
                        for i in range(len(self.list_symbols)):
                            self.dict_transitions[new_state][self.list_symbols[i]] = ["P"]

                        # Split the new state to get all the added states
                        new_state_components = new_state.split("|")

                        for sub_state in new_state_components:
                            # Loop through each part of the new combined state
                            for symbol in self.list_symbols:
                                for transition in self.dict_transitions[sub_state][symbol]:

                                    # Skip transitions to the sink state ("P")
                                    if transition != "P":
                                        # If the new state's transition is P, replace it with the current transition.
                                        if self.dict_transitions[new_state][symbol] == ['P']:
                                            self.dict_transitions[new_state][symbol] = [transition]

                                        if transition not in self.dict_transitions[new_state][symbol]:
                                            # If the transition doesn't exist yet,  add it to the list of transitions
                                            self.dict_transitions[new_state][symbol].append(transition)

        # Repeat for the new combined states until no more can be created
        if new_states:
            self.determinization_and_completion_automaton(new_states)


