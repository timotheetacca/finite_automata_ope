import csv
import os


class finite_automata:
    def __init__(self, filepath):
        self.filepath = filepath
        self.nb_symbols = 0
        self.nb_initial_states = 0
        self.list_initial_states = []
        self.nb_final_states = 0
        self.list_final_states = []
        self.dict_transitions = {}
        self.list_symbols = []

    def get_fa_information(self):
        # Check if the file exists
        if not os.path.exists(self.filepath):
            print(f"You don't have any file named '{self.filepath}' ⚠ ")
            return

        # Read the automaton file and split it into lines
        with open(self.filepath, "r") as fa:
            lines = []
            for line in fa.readlines():
                lines.append(line.strip())
            fa.close()

            # Read the lines and gather information for the automata
            self.nb_symbols = int(lines[0])
            self.nb_initial_states = int(lines[2].split(" ")[0])
            self.nb_final_states = int(lines[3].split(" ")[0])
            self.list_initial_states = lines[2].split(" ")[1:]
            self.list_final_states = lines[3].split(" ")[1:]

            # Go through transitions and add any new symbols to the list
            for i in range(int(lines[4])):
                # Split the line to get the second element, which is the symbol
                if (lines[i + 5]).split(" ")[1] not in self.list_symbols:
                    self.list_symbols.append((lines[i + 5]).split(" ")[1])

            # Create a dictionary to store where each state goes for each symbol
            for transition in lines[5:]:

                # split_transition is of the form [source state, symbol, target state]
                split_transition = transition.split(" ")

                # Check if transition[0] and transition[2] are in the dict, if not add them with empty symbols list
                for j in [0, 2]:
                    if self.dict_transitions.get(split_transition[j]) is None:
                        # Add the states
                        self.dict_transitions[split_transition[j]] = {}
                        for symbol in self.list_symbols:
                            # Add the symbols
                            self.dict_transitions[split_transition[j]][symbol] = []

                # Add every corresponding states to their symbol
                self.dict_transitions[split_transition[0]][split_transition[1]].append(split_transition[2])

    def get_csv_from_fa(self, csv_filepath):
        with open(csv_filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            # Write the header of the CSV with symbols as column names, leaving two cells empty for alignment
            writer.writerow(["", ""] + self.list_symbols)

            # Write each state to the CSV, marking initial states with '>' and final states with '<'
            for state in self.dict_transitions.keys():
                if state != "P":
                    if state in self.list_initial_states and state in self.list_final_states:
                        row = ["=", state]
                    elif state in self.list_initial_states:
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
                            row.append(",".join(sorted(transition)))
                        else:
                            row.append("--")
                    writer.writerow(row)

            # Write the sink line at the end of the csv
            if "P" in self.dict_transitions.keys():
                row = ["", "P"]
                for _ in self.list_symbols:
                    # For the sink, every transition goes to itself
                    row.append("P")
                writer.writerow(row)

    def get_fa_information_from_csv(self, csv_filepath):
        with open(csv_filepath, "r", newline="") as csvfile:
            reader = list(csv.reader(csvfile, delimiter=";"))

            # Extract symbols from the header starting from the third column
            self.list_symbols = reader[0][2:]
            self.nb_symbols = len(self.list_symbols)

            # Set the empty dictionary
            self.dict_transitions = {}
            for row in reader[1:]:
                state = row[1]
                self.dict_transitions[state] = {}

            for state in self.dict_transitions:
                for symbol in self.list_symbols:
                    self.dict_transitions[state][symbol] = []

            # Get initial and final states
            self.list_initial_states = []
            self.list_final_states = []
            for row in reader[1:]:
                state_marker = row[0]
                state = row[1]

                if state_marker == ">" or state_marker == "=":
                    self.list_initial_states.append(state)
                if state_marker == "<" or state_marker == "=":
                    self.list_final_states.append(state)

                # Get the transitions information
                for i in range(self.nb_symbols):
                    symbol = self.list_symbols[i]
                    transition = row[2 + i]
                    if transition != "--":
                        self.dict_transitions[state][symbol] = transition.split(",")

            # Update counts
            self.nb_initial_states = len(self.list_initial_states)
            self.nb_final_states = len(self.list_final_states)

    def write_fa_to_txt(self, txt_filepath):
        with open(txt_filepath, "w") as txtfile:
            txtfile.write(f"{self.nb_symbols}\n")
            txtfile.write(f"{len(self.dict_transitions)}\n")
            txtfile.write(f"{self.nb_initial_states} {' '.join(self.list_initial_states)}\n")
            txtfile.write(f"{self.nb_final_states} {' '.join(self.list_final_states)}\n")

            # Get all the transitions
            transitions = []
            for state in self.dict_transitions:
                for symbol in self.list_symbols:
                    for transition in self.dict_transitions[state][symbol]:
                        transitions.append((state, symbol, transition))

            # Write umber of transitions
            txtfile.write(f"{len(transitions)}\n")

            # Write each transition
            for state, symbol, transition in transitions:
                txtfile.write(f"{state} {symbol} {transition}\n")

    def is_deterministic(self, display=False):
        # Check if the automaton has more than 1 initial state, if yes, the automaton is not deterministic
        if self.nb_initial_states > 1:
            if display:
                print("Your automaton is not deterministic. There are several initial states ⚠ \n")
            return False

        # Check if a state has more than 1 transition for a given symbol, if yes, the automaton is not deterministic
        for state in self.dict_transitions:
            for symbol in self.list_symbols:
                if len(self.dict_transitions[state][symbol]) > 1:
                    if display:
                        print(
                            f"Your automaton is not deterministic. State {state} has {len(self.dict_transitions[state][symbol])} transitions for symbol '{symbol}' ⚠ \n")
                    return False

        return True

    def is_complete(self, display=False):
        # Check if there are empty transitions, if yes, the automaton is not deterministic
        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                if not self.dict_transitions[state][symbol]:
                    if display:
                        print(f"Your automaton is not complete. State {state} has no transitions for symbol '{symbol}' ⚠ \n")
                    return False
        return True

    def is_standard(self, display=False):
        # If a FA has more than 1 initial state, it is not standard
        if self.nb_initial_states != 1:
            return False

        initial_state = self.list_initial_states[0]

        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                if initial_state in self.dict_transitions[state][symbol]:
                    if display:
                        print(f"Your automaton is not standard. {state} goes to the initial state ⚠ \n")
                    return False

        return True

    def completion(self):
        # Link all the empty transitions to the sink state
        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                if not self.dict_transitions[state][symbol]:
                    self.dict_transitions[state][symbol] = ["P"]

        # Add the sink state
        self.dict_transitions["P"] = {}
        for symbol in self.list_symbols:
            self.dict_transitions["P"][symbol] = ["P"]

    def determinization(self):
        # If the old automaton was complete, the new one will also be complete
        old_fa_was_completed = self.is_complete()

        # Save old initial states if there is more than one, will be used later
        old_initial_states = []

        # If there are multiple initial states, create a combined initial state
        if len(self.list_initial_states) > 1:
            old_initial_states = self.list_initial_states
            new_initial_state = "|".join(sorted(self.list_initial_states))
            self.list_initial_states = [new_initial_state]
            self.nb_initial_states = 1

            # Initialize transitions for the new initial state
            self.dict_transitions[new_initial_state] = {}
            for symbol in self.list_symbols:
                self.dict_transitions[new_initial_state][symbol] = []

            # Create the transitions for the new initial state
            for sub_state in new_initial_state.split("|"):
                for symbol in self.list_symbols:
                    for transition in self.dict_transitions[sub_state][symbol]:
                        # If not a sink state and not already in the transition list, add it
                        if transition != "P" and transition not in self.dict_transitions[new_initial_state][symbol]:
                            self.dict_transitions[new_initial_state][symbol].append(transition)

        # Remove all the old initial states to avoid creating new states from a transition of initial states
        states_to_process = list(self.dict_transitions.keys())
        for state in old_initial_states:
            if state in states_to_process:
                states_to_process.remove(state)

        new_states = []

        # Process only the given states
        for state in states_to_process:
            new_final_state = False

            # Check if the current state is a final state
            for sub_state in state.split("|"):
                if sub_state in self.list_final_states:
                    new_final_state = True

            # If the current state is a final state, add it to the list of final states
            if new_final_state and state not in self.list_final_states:
                self.list_final_states.append(state)
                self.nb_final_states += 1

            # Process each symbol
            for symbol in self.list_symbols:
                transitions = []

                # Collect all transitions for the current state and symbol
                for sub_state in state.split("|"):
                    for transition in self.dict_transitions[sub_state][symbol]:
                        if transition != "P" and transition not in transitions:
                            transitions.append(transition)

                # If there are transitions, create a new combined state
                if transitions:
                    new_state = "|".join(sorted(transitions))

                    # If the new state doesn't exist, add it to the dictionary and process it later
                    if new_state not in self.dict_transitions:
                        new_states.append(new_state)
                        self.dict_transitions[new_state] = {}
                        for new_state_symbol in self.list_symbols:
                            self.dict_transitions[new_state][new_state_symbol] = []

                    # Update the current state's transition to the new combined state
                    self.dict_transitions[state][symbol] = [new_state]

        # Recursively process new combined states
        if new_states:
            self.determinization()

        # After processing all new states, clean up the original states
        self.cleanup_original_states()

        # If the old automaton was complete, complete the new one
        if old_fa_was_completed:
            self.completion()

    def standardization(self):
        dict_transition_initial_state = {"i": {}}
        for symbol in self.list_symbols:
            dict_transition_initial_state["i"][symbol] = []

        for initial_state in self.list_initial_states:
            for symbol in self.list_symbols:
                for state_to_add in self.dict_transitions[initial_state][symbol]:
                    if state_to_add not in dict_transition_initial_state["i"][symbol]:
                        dict_transition_initial_state["i"][symbol].append(state_to_add)

        self.nb_initial_states = 1
        self.list_initial_states = ["i"]
        self.dict_transitions["i"] = dict_transition_initial_state["i"]

    def cleanup_original_states(self):
        # List to store reachable states and start from initial state
        reachable_states = []
        list_states = self.list_initial_states[:]

        while len(list_states) > 0:
            current_state = list_states.pop(0)
            if current_state not in reachable_states:
                reachable_states.append(current_state)

                for symbol in self.list_symbols:
                    for state in self.dict_transitions[current_state][symbol]:

                        if state not in list_states and state not in reachable_states:
                            list_states.append(state)

        # Keep reachable states from the automata dict_transitions
        new_dict_transitions = {}
        for state in self.dict_transitions:
            if state in reachable_states:
                new_dict_transitions[state] = self.dict_transitions[state]

        self.dict_transitions = new_dict_transitions

    def determinization_and_completion(self, csv_filepath):
        if not self.is_deterministic():
            self.determinization()

        if not self.is_complete():
            self.completion()

        self.get_csv_from_fa(csv_filepath)

    def complementary(self):
        if not self.is_deterministic():
            self.determinization()

        if not self.is_complete():
            self.completion()

        # Save all the old final states and erase the final state list
        old_list_final_states = self.list_final_states
        self.list_final_states = []
        for state in self.dict_transitions.keys():
            # If the current state was a final state, it becomes a normal state and vice versa
            if state not in old_list_final_states and state not in self.list_initial_states:
                self.list_final_states.append(state)


