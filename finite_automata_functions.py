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
        self.dict_transition_epsilon = {}
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
                symbol = (lines[i + 5]).split(" ")[1]
                if symbol not in self.list_symbols:
                    self.list_symbols.append(symbol)

            # Create dictionaries to store transitions
            for transition in lines[5:]:
                # split_transition is of the form [source state, symbol, target state]
                split_transition = transition.split(" ")

                # Initialize dictionaries for the source state if not already present
                for state in [split_transition[0], split_transition[2]]:
                    if state not in self.dict_transitions:
                        self.dict_transitions[state] = {}
                        for symbol in self.list_symbols:
                            if symbol != "E":
                                self.dict_transitions[state][symbol] = []
                    if state not in self.dict_transition_epsilon:
                        self.dict_transition_epsilon[state] = []

                # IF the transition is Epsilon store it in the epsilon dict
                if split_transition[1] == "E":
                    self.dict_transition_epsilon[split_transition[0]].append(split_transition[2])
                else:
                    # Add non-epsilon transitions to dict_transitions
                    self.dict_transitions[split_transition[0]][split_transition[1]].append(split_transition[2])

    def get_csv_from_fa(self, csv_filepath):
        with open(csv_filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            # Determine if epsilon transitions exist
            has_epsilon = bool(self.dict_transition_epsilon)  # True if not empty, False if empty

            # Write the header of the CSV with symbols as column names
            header_symbols = []
            for symbol in self.list_symbols:
                if symbol != "E" or has_epsilon:
                    header_symbols.append(symbol)
            writer.writerow(["", ""] + header_symbols)

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
                        if symbol != "E" or has_epsilon:
                            if symbol == "E":
                                # Handle epsilon transitions
                                epsilon_transitions = self.dict_transition_epsilon.get(state, [])
                                if epsilon_transitions:
                                    row.append(",".join(sorted(epsilon_transitions)))
                                else:
                                    row.append("--")
                            else:
                                # Handle non-epsilon transitions
                                transition = self.dict_transitions[state].get(symbol, [])
                                if transition:
                                    row.append(",".join(sorted(transition)))
                                else:
                                    row.append("--")
                    writer.writerow(row)

            # Write the sink line at the end of the CSV
            if "P" in self.dict_transitions.keys():
                row = ["", "P"]
                for symbol in self.list_symbols:
                    if symbol != "E" or has_epsilon:
                        row.append("P")
                writer.writerow(row)

    def get_fa_information_from_csv(self, csv_filepath):
        with open(csv_filepath, "r", newline="") as csvfile:
            reader = list(csv.reader(csvfile, delimiter=";"))

            # Extract symbols from the header starting from the third column
            self.list_symbols = reader[0][2:]
            self.nb_symbols = len(self.list_symbols)

            # Initialize dictionaries
            self.dict_transitions = {}
            self.dict_transition_epsilon = {}
            for row in reader[1:]:
                state = row[1]
                self.dict_transitions[state] = {}
                self.dict_transition_epsilon[state] = []

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
                        if symbol == "E":
                            # Handle epsilon transitions
                            self.dict_transition_epsilon[state] = transition.split(",")
                        else:
                            # Handle non-epsilon transitions
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

            # Get all the transitions (including epsilon transitions)
            transitions = []
            for state in self.dict_transitions:
                for symbol in self.list_symbols:
                    if symbol == "E":
                        for transition in self.dict_transition_epsilon[state]:
                            transitions.append((state, symbol, transition))
                    else:
                        for transition in self.dict_transitions[state][symbol]:
                            transitions.append((state, symbol, transition))

            # Write number of transitions
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

        if self.dict_transition_epsilon != {}:
            if display:
                print("Your automaton is not deterministic. We found epsilon transitions ⚠ \n")
            return False

        # Check if a state has more than 1 transition for a given symbol, if yes, the automaton is not deterministic
        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                if symbol != "E":
                    # Skip epsilon transitions
                    if len(self.dict_transitions[state][symbol]) > 1:
                        if display:
                            print(
                                f"Your automaton is not deterministic. State {state} has {len(self.dict_transitions[state][symbol])} transitions for symbol '{symbol}' ⚠ \n")
                        return False
        if display:
            print("Your automaton is deterministic")
        return True

    def is_complete(self, display=False):
        # Check if there are empty transitions, if yes, the automaton is not complete
        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                # Skip epsilon transitions
                if symbol != "E":
                    if not self.dict_transitions[state][symbol]:
                        if display:
                            print(
                                f"Your automaton is not complete. State {state} has no transitions for symbol '{symbol}' ⚠ \n")
                        return False
        if display:
            print("Your automaton is complete")
        return True

    def is_standard(self, display=False):
        # If a FA has more than 1 initial state, it is not standard
        if self.nb_initial_states != 1:
            return False

        initial_state = self.list_initial_states[0]

        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                # Skip epsilon transitions
                if symbol != "E":
                    if initial_state in self.dict_transitions[state][symbol]:
                        if display:
                            print(f"Your automaton is not standard. {state} goes to the initial state ⚠ \n")
                        return False
        if display:
            print("Your automaton is standard")
        return True

    def completion(self):
        # Link all the empty transitions to the sink state
        for state in self.dict_transitions.keys():
            for symbol in self.list_symbols:
                if symbol != "E":
                    if not self.dict_transitions[state][symbol]:
                        self.dict_transitions[state][symbol] = ["P"]

        # Add the sink state
        self.dict_transitions["P"] = {}
        for symbol in self.list_symbols:
            if symbol != "E":
                self.dict_transitions["P"][symbol] = ["P"]

    def determinization(self):
        # If the old automaton was complete, the new one will also be complete
        old_fa_was_completed = self.is_complete()

        # Save old initial states if there is more than one, will be used later
        old_initial_states = []

        # Calculate epsilon closures for all states
        self.dict_transition_epsilon = self.epsilon_closure()

        # If there are epsilon transitions, process them
        if self.dict_transition_epsilon:
            for state in self.dict_transition_epsilon.keys():
                for transition in self.dict_transition_epsilon[state]:
                    for symbol in self.list_symbols:
                        if symbol != "E":
                            # If the value is a final state, add it to the dict_transition!
                            if transition in self.list_final_states:
                                if transition not in self.dict_transitions[state][symbol]:
                                    self.dict_transitions[state][symbol].append(transition)

                            # Else add the list of transitions
                            for sub_transition in self.dict_transitions[transition][symbol]:
                                if sub_transition not in self.dict_transitions[state][symbol]:
                                     self.dict_transitions[state][symbol].append(sub_transition)
            # Erase the epsilon transitions
            self.dict_transition_epsilon = {}

        # If there are multiple initial states, create a combined initial state
        if len(self.list_initial_states) > 1:
            old_initial_states = self.list_initial_states
            new_initial_state = "|".join(sorted(self.list_initial_states))
            self.list_initial_states = [new_initial_state]
            self.nb_initial_states = 1

            # Initialize transitions for the new initial state
            self.dict_transitions[new_initial_state] = {}
            for symbol in self.list_symbols:
                if symbol != "E":
                    self.dict_transitions[new_initial_state][symbol] = []

            # Create the transitions for the new initial state
            for sub_state in new_initial_state.split("|"):
                for symbol in self.list_symbols:
                    if symbol != "E":
                        for transition in self.dict_transitions[sub_state][symbol]:
                            # If not a sink state and not already in the transition list, add it
                            if transition != "P" and transition not in self.dict_transitions[new_initial_state][symbol]:
                                self.dict_transitions[new_initial_state][symbol].append(transition)

        # Remove all the old initial states to avoid creating new states from a transition of initial states
        states_to_process = list(self.dict_transitions.keys())
        for state in old_initial_states:
            if state in states_to_process:
                states_to_process.remove(state)

        # Use a list to track processed states
        processed_states = []

        while states_to_process:
            state = states_to_process.pop(0)
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
                if symbol != "E":
                    transitions = []

                    # Collect all transitions for the current state and symbol
                    for sub_state in state.split("|"):
                        for transition in self.dict_transitions[sub_state][symbol]:
                            if transition != "P" and transition not in transitions:
                                transitions.append(transition)

                    # If there are transitions, create a new combined state
                    if transitions:
                        unique_transitions = []
                        for transition in transitions:
                            if "|" in transition:
                                # Split the combined states and add their components
                                for sub_state in transition.split("|"):
                                    if sub_state not in unique_transitions:
                                        unique_transitions.append(sub_state)
                            else:
                                # Add the transition if not already in the list
                                if transition not in unique_transitions:
                                    unique_transitions.append(transition)

                        # Sort and join the unique transitions to form the new state
                        new_state = "|".join(sorted(unique_transitions))


                        # If the new state doesn't exist, add it to the dictionary and process it later
                        if new_state not in self.dict_transitions:
                            self.dict_transitions[new_state] = {}
                            for new_state_symbol in self.list_symbols:
                                self.dict_transitions[new_state][new_state_symbol] = []

                            # Add the new state to the processing queue if it hasn't been processed yet
                            if new_state not in processed_states:
                                states_to_process.append(new_state)

                        # Mark the new state as processed
                        if new_state not in processed_states:
                            processed_states.append(new_state)

                        # Update the current state's transition to the new combined state
                        self.dict_transitions[state][symbol] = [new_state]

        # After processing all new states, clean up the original states
        self.cleanup_original_states()

        # If the old automaton was complete, complete the new one
        if old_fa_was_completed:
            self.completion()

    def split_groups_minimization(self, partition):
        # The value inside the state dictionary would be a list corresponding to the groups their next states belong to
        for group in partition.keys():
            # Look inside all groups of the partition, the next_states each state reach depending on the symbol
            for symbol in self.list_symbols:
                if symbol != "E":
                    for state in partition[group].keys():
                        for next_state in self.dict_transitions[state][symbol]:
                            # For each next state, look for the group it belongs to
                            for group_check in partition.keys():
                                if next_state in partition[group_check]:
                                    # Add to the list of values for the dictionary state the group
                                    partition[group][state].append(group_check)
        # Creation of an intermediary partition, having the same groups as the previous one
        sub_partition = {key: {} for key in partition.keys()}
        # Look inside each group
        for group in partition.keys():
            for state in partition[group].keys():
                # For each state, join together in a string the groups the next states belong to
                t_behaviors = ",".join(partition[group][state])
                # If this pattern doesn't exist, we put it as a new key
                if t_behaviors not in sub_partition[group]:
                    sub_partition[group][t_behaviors] = []
                # The state having that one pattern would then become the value to that key
                sub_partition[group][t_behaviors].append(state)
        # Create new partition for next step
        new_partition = {}
        index = 1
        # Fill the new partition depending on the pattern
        for group in partition.keys():
            for t_behaviors in sub_partition[group].keys():
                # The newly generated groups would be called with letters, starting from A
                new_groups = chr(64 + index)
                index += 1
                # Create keys for each new groups
                if new_groups not in new_partition:
                    new_partition[new_groups] = {}
                # Fill the newly created keys with the states having the same pattern
                for state in sub_partition[group][t_behaviors]:
                    if state not in new_partition[new_groups]:
                        new_partition[new_groups][state] = []
        return new_partition

    def final_partition_minimization(self):
        # 1st Step
        list_non_final_states = []
        for state in self.dict_transitions.keys():
            if state not in self.list_final_states:
                list_non_final_states.append(state)
        partition = {
            "T": {},
            "NT": {},
        }
        for state in self.dict_transitions.keys():
            if state in self.list_final_states:
                partition["T"][state] = []
            else:
                partition["NT"][state] = []
        # Recursion on splitting the states if not same pattern
        new_partition = self.split_groups_minimization(partition)
        while True:
            if new_partition.keys() == partition.keys():
                return new_partition
            partition = new_partition
            new_partition = self.split_groups_minimization(new_partition)

    def minimized_fa(self):
        # Check if the FA is deterministic and complete before minimizing it
        if not self.is_deterministic():
            print("Minimization failed. Your automaton is not deterministic ⚠\n")
            return
        if not self.is_complete():
            print("Minimization failed. Your automaton is not complete ⚠\n")
            return

        # Get the final partition minimization
        minimized_partition = self.final_partition_minimization()

        # Get the new states for the minimized automaton
        state_map = []
        for group, states in minimized_partition.items():
            state_map.append(",".join(states))

        # Initialize the transitions for those new states
        new_transitions = {}
        for new_state in state_map:
            new_transitions[new_state] = {}

        # Loop through each state and its transitions in the original FA
        for state, transitions in self.dict_transitions.items():
            # For each group of states in the minimized FA
            for new_state in state_map:
                # Check if the original state is part of the new group
                if state in new_state.split(","):
                    # For each symbol and its corresponding list of destination states from the original state
                    for symbol, dest_list in transitions.items():
                        if symbol != "E":
                            # Iterate through each destination in the list
                            for dest in dest_list:
                                # Check each group in state_map to see if it contains the destination state
                                for s in state_map:
                                    # If the destination state is part of the group
                                    if dest in s.split(","):
                                        # Update the new transition for this symbol with the new state (group of states)
                                        new_transitions[new_state][symbol] = s

        old_final_state = self.list_final_states
        self.list_final_states =[]
        for state in new_transitions.keys():
            for symbol in self.list_symbols:
                if symbol != "E":
                    for i in range (len(old_final_state)):
                        if old_final_state[i] in state and state not in self.list_final_states:
                            self.list_final_states.append(state)
                    new_transitions[state][symbol] = new_transitions[state][symbol].split(",")

        self.dict_transitions = new_transitions

        # Defining the file path for the new CSV file to store the minimized finite automaton
        new_csv_filepath = self.filepath.split(".txt")[0]+".csv"
        self.get_csv_from_fa(new_csv_filepath)

        print("The minimized automaton has been written in " + new_csv_filepath)

    def standardization(self):
        dict_transition_initial_state = {"i": {}}
        for symbol in self.list_symbols:
            if symbol !="E":
                dict_transition_initial_state["i"][symbol] = []

        for initial_state in self.list_initial_states:
            for symbol in self.list_symbols:
                if symbol != "E":
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
                    if symbol != "E":
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


    def input_word_check(self, state, word, start=0):
        # using count to start the word not specifically at the start, which will be relevant lower in the function, starts at 0 if not specified
        count = start
        # using current_state to "start the automaton" not specifically at the initial state, which is also relevant lower in the function
        current_state = state
        # fails is used when we want to break the following while loop on "soft" problems
        fails = False

        # as long as we don't reach the end of the word and there's no soft problem
        while count < len(word) and not fails:
            print("\n" + str(count+1) + ". Checking letter '" + word[count] + "' (stops after " + str(len(word)) + " iterations) ...")

            # if the current letter figures in the available transitions
            if word[count] in self.dict_transitions[current_state].keys():
                print("Next letter found!")

                print("Current state: [" + current_state + "] -> ", end="")

                print(self.dict_transitions[current_state])

                # if where said transition(s) have no output, There's nothing we can do.
                if len(self.dict_transitions[current_state][word[count]]) == 0:
                    return False

                # if it has one output, we just have to study this one, pretty straightforward
                elif len(self.dict_transitions[current_state][word[count]]) == 1:
                    current_state = self.dict_transitions[current_state][word[count]][0]

                    # we NEED to be at the end of the word in order to be able to return a True
                    if count == len(word) - 1:
                        # initiate the check
                        check = False
                        for final in self.list_final_states:
                            # if the current state is one of the final states, return True. if it's not, return False because we're at the end of the word
                            if current_state == final:
                                check = True
                        return check

                # if there's more than one output to the transition, reiterate this on each of the outputs (this is where the first two variables of the function come in handy)
                else:
                    # named fork because the transition forks into multiple outputs
                    for fork in self.dict_transitions[current_state][word[count]]:
                        if self.input_word_check(fork, word, count + 1):
                            # returns True if even one of the forks lands a True (we only need the word to work through one final state)
                            return True
                    # return False if there's zero final state that works for the word
                    return False

                count += 1

            else:
                # the aforementioned soft problem is when the current letter isn't in the current state transitions. With this, all the possibilities are covered
                fails = True

        # if the loop fails because we reached a transition with no output, return False
        if fails:
            return False
        # if the loop didn't fail but we're not at the end of the word, also return not True (so False)
        elif not fails and count != len(word):
            return False
        # if the loop didn't fail and we're at the end of the word, return True
        else:
            return True

    def word_recognition(self, word: str):
        initial_states = ", ".join(self.list_initial_states)
        final_states = ", ".join(self.list_final_states)
        print("As a reminder, the initial states are " + initial_states + " and the final states are " + final_states + ".")

        # runs input_word_check on every input, returns and notifies a True if the word works with one input, False if it didn't with any
        for state in self.list_initial_states:
            result = self.input_word_check(state, word)

            if result:
                print("\nThe word '" + word + "' worked through one of the inputs!")
                return True

        print("\nWent through all the inputs of this automaton and found nothing")
        return False


    def epsilon_closure(self):
        # Initialize the epsilon closure dictionary
        epsilon_closures = {}

        # Calculate epsilon closure for each state
        for state in self.dict_transitions.keys():
            if state not in epsilon_closures:
                epsilon_closures[state] = []
                stack = [state]

                while stack:
                    current_state = stack.pop()
                    # Add the current state to the epsilon closure if it's not already there
                    if current_state not in epsilon_closures[state]:
                        epsilon_closures[state].append(current_state)

                        # Add all states reachable via epsilon transitions
                        for epsilon_state in self.dict_transition_epsilon.get(current_state, []):
                            if epsilon_state not in epsilon_closures[state]:
                                stack.append(epsilon_state)

        return epsilon_closures

    def display(self):
        # Determine if epsilon transitions exist
        has_epsilon = False
        for state in self.dict_transition_epsilon:
            if self.dict_transition_epsilon[state]:
                has_epsilon = True

        # Prepare the list of symbols to display, excluding 'E' if no epsilon transitions
        display_symbols = []
        for symbol in self.list_symbols:
            if symbol != "E" or has_epsilon:
                display_symbols.append(symbol)

        # Calculate padding for each column
        padding = [4]  # Padding for the initial/final state marker (4 for the arrows)

        # Calculate padding for the state column
        max_state_length = 0
        for state in self.dict_transitions.keys():
            if len(state) > max_state_length:
                max_state_length = len(state)
        padding.append(max_state_length)

        # Calculate padding for each symbol column
        max_transition_lengths = [2] * len(display_symbols)
        for state in self.dict_transitions.keys():
            for i in range(len(display_symbols)):
                symbol = display_symbols[i]
                if symbol == "E":
                    transition = ", ".join(self.dict_transition_epsilon.get(state, []))
                else:
                    transition = ", ".join(self.dict_transitions[state].get(symbol, []))
                if len(transition) > max_transition_lengths[i]:
                    max_transition_lengths[i] = len(transition)
        for length in max_transition_lengths:
            padding.append(length)

        # Draw the top border of the table
        draw_line_str = "+"
        for p in padding:
            draw_line_str += "-" * (p + 2) + "+"
        print(draw_line_str)

        # Print the header row
        header = "|" + " " * (padding[0] + 2) + "|"
        header += " " * (padding[1] + 2) + "|"
        for i in range(len(display_symbols)):
            symbol = display_symbols[i]
            diff = padding[i + 2] - len(symbol)
            left_pad = diff // 2
            right_pad = diff - left_pad
            header += " " * (left_pad + 1) + symbol + " " * (right_pad + 1) + "|"
        print(header)
        print(draw_line_str)

        # Print each state's row
        for state in self.dict_transitions.keys():
            # Determine the initial/final state marker
            if state in self.list_initial_states and state in self.list_final_states:
                marker = "<-->"
            elif state in self.list_initial_states:
                marker = "->"
            elif state in self.list_final_states:
                marker = "<-"
            else:
                marker = ""

            # Print the marker for initial/final state with padding
            line = "|"
            diff = padding[0] - len(marker)
            left_pad = diff // 2
            right_pad = diff - left_pad
            line += " " * (left_pad + 1) + marker + " " * (right_pad + 1) + "|"

            # Print the state with padding
            diff = padding[1] - len(state)
            left_pad = diff // 2
            right_pad = diff - left_pad
            line += " " * (left_pad + 1) + state + " " * (right_pad + 1) + "|"

            # Print the transitions for each symbol
            for i in range(len(display_symbols)):
                symbol = display_symbols[i]
                if symbol == "E":
                    transition = ", ".join(self.dict_transition_epsilon.get(state, []))
                else:
                    transition = ", ".join(self.dict_transitions[state].get(symbol, []))
                if not transition:
                    transition = "--"

                # Calculate padding for the transition string
                diff = padding[i + 2] - len(transition)
                left_pad = diff // 2
                right_pad = diff - left_pad

                # Append the transition string with padding
                line += " " * (left_pad + 1) + transition + " " * (right_pad + 1) + "|"

            print(line)
            print(draw_line_str)