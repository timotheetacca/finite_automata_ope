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
        self.list_transitions = []
        self.list_symbols = []
        self.list_states = []

    def get_fa_information(self):
        with open(self.file_path, "r") as fa:
            # Read the automata file and split it into lines
            lines = []
            for line in fa.readlines():
                lines.append(line.strip())

            # Read the lines and gather information for the automata
            self.nb_symbols = lines[0]
            self.nb_states = lines[1]
            self.nb_initial_states = (lines[2]).split(' ')[0]
            self.list_initial_states = (lines[2]).split(' ')[1:]
            self.nb_final_states = (lines[3]).split(' ')[0]
            self.list_final_states = (lines[3]).split(' ')[1:]
            self.nb_transitions = lines[4]
            self.list_transitions = lines[5:]
            self.list_symbols = []
            self.list_states = []
            for i in range(len(self.list_transitions)):
                # Navigate through the  transitions, then add each state and symbol found if not already in the list
                if self.list_transitions[i][0] not in self.list_states:
                    self.list_states.append(self.list_transitions[i][0])
                if self.list_transitions[i][2] not in self.list_states:
                    self.list_states.append(self.list_transitions[i][2])

                if self.list_transitions[i][1] not in self.list_symbols:
                    self.list_symbols.append(self.list_transitions[i][1])

    def get_csv_from_fa(self, output_filepath):
        with open(output_filepath, "w", newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            # Create the header and leave the 2 first boxes empty
            writer.writerow(["", ""] + self.list_symbols)

            for state in self.list_states:
                # Create a row for the .csv with the arrows for initial and final states
                if state in self.list_initial_states:
                    row = [">", state]
                elif state in self.list_final_states:
                    row = ["<", state]
                else:
                    row = ["", state]

                for symbol in self.list_symbols:
                    # Create the list with all the transitions for the current state
                    transitions = []

                    for transition in self.list_transitions:
                        # Check if the current transition starts with the correct state and symbol
                        if transition[0] == state and transition[1] == symbol:
                            transitions.append(transition[2])

                    if len(transitions) > 0:
                        # If the transition is more than 1 state, separate them by a coma
                        row.append(",".join(transitions))

                    else:
                        # If the transition is empty then write '--'
                        row.append("--")

                # Add the row on the .csv
                writer.writerow(row)
