import os
from finite_automata_functions import *

def main():
    print("Welcome to the Finite Automata Program!")
    print("You can perform various operations on a finite automaton.\n")

    file_type = int(input("If you want to start from a CSV file (enter '1') or a text file (enter '2'): "))
    while file_type != 1 and file_type != 2:
        print("\nInvalid input. Please enter '1' or '2'")
        file_type = int(input("If you want to start from a CSV file (enter '1') or a text file (enter '2'): "))

    filepath = input("Enter the path to your file: ")
    while not os.path.exists(filepath):
        print(f"File '{filepath}' does not exist. Please enter a valid file path.")
        filepath = input("\nEnter the path to your file: ")

    fa = finite_automata(filepath)

    # Load the automaton information based on the file type
    if file_type == 1:
        fa.get_fa_information_from_csv(filepath)
        print("Finite automaton successfully loaded from CSV file.")
    else:
        fa.get_fa_information()
        print("Finite automaton successfully loaded from text file.")

    running = True
    while running:
        print("\nSelect an action to perform:")
        print("1. Display FA information")
        print("2. Export FA to CSV")
        print("3. Check if FA is deterministic")
        print("4. Check if FA is complete")
        print("5. Check if FA is standard")
        print("6. Complete the FA")
        print("7. Determinize the FA")
        print("8. Standardize the FA")
        print("9. Minimize the FA")
        print("10. Get complementary FA")
        print("11. Exit")

        choice = input("Enter your choice (1-11): ").strip()

        if choice == "1":
            print("\nFA Information:")
            print(f"Number of symbols: {fa.nb_symbols}")
            print(f"Number of initial states: {fa.nb_initial_states}")
            print(f"Initial states: {fa.list_initial_states}")
            print(f"Number of final states: {fa.nb_final_states}")
            print(f"Final states: {fa.list_final_states}")
            print(f"Transitions: {fa.dict_transitions}")

        elif choice == "2":
            csv_filepath = input("Enter the file path to save the CSV: ")
            fa.get_csv_from_fa(csv_filepath)
            print(f"Your automaton has been exported to {csv_filepath}")

        elif choice == "3":
            fa.is_deterministic(display=True)

        elif choice == "4":
            fa.is_complete(display=True)

        elif choice == "5":
            fa.is_standard(display=True)

        elif choice == "6":
            fa.completion()
            print("Your automaton has been completed.")

        elif choice == "7":
            fa.determinization()
            print("Your automaton has been determinized.")

        elif choice == "8":
            fa.standardization()
            print("Your automaton has been standardized.")

        elif choice == "9":
            fa.minimized_fa()
            print("Your automaton has been minimized.")

        elif choice == "10":
            fa.complementary()
            print("The complementary automaton has been created.")

        elif choice == "11":
            print("Exiting the program...")
            running = False

        else:
            print("Invalid choice. Please enter a number between 1 and 11.")


if __name__ == "__main__":
    main()