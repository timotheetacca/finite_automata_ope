import csv


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
        self.list_symbols = []

    def get_fa_information(self):
        with open(self.file_path, "r") as fa:
            # Read the automata file and split it into lines
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
            # Transforms the str lists into int lists
            for i in range(self.nb_initial_states):
                self.list_initial_states[i] = int(self.list_initial_states[i])
            for i in range(self.nb_initial_states):
                self.list_final_states[i] = int(self.list_final_states[i])

            # Navigate through the  transitions, then add each symbol found if not already in the list
            for i in range(self.nb_transitions):
                if lines[i + 5][1] not in self.list_symbols:
                    self.list_symbols.append(lines[i + 5][1])

            # Get the dictionary for all the transitions
            for transition in lines[5:]:
                # Check if transition[0] and transition[2] are in the dict, if not add them with empty symbols list
                for j in range(0, 3, 2):
                    if self.dict_transitions.get(int(transition[j])) == None:
                        # Add the state
                        self.dict_transitions[int(transition[j])] = {}
                        for i in range(self.nb_symbols):
                            # Add the symbol
                            self.dict_transitions[int(transition[j])][self.list_symbols[i]] = []

                # Add every corresponding states to their symbol
                self.dict_transitions[int(transition[0])][transition[1]].append(int(transition[2]))

    def get_csv_from_fa(self, output_filepath):
        with open(output_filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")

            # Create the header and leave the 2 first boxes empty
            writer.writerow(["", ""] + self.list_symbols)

            # Create a row for the .csv with the arrows for initial and final states
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
                        # If the transition isn't empty, convert each item to a string
                        for i in range(len(transition)):
                            transition[i] = str(transition[i])
                        # Join the list into a single string separated by commas if there is more than 1 element
                        row.append(",".join(transition))

                    else:
                        row.append("--")

                writer.writerow(row)
