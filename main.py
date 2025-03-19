import os

from finite_automata_functions import *

def load_fa():
    file_type = int(input("If you want to start from a \033[32m CSV file (enter '1') \033[0m or a \033[93mtext file (enter '2')\033[0m : "))
    while file_type != 1 and file_type != 2:
        print("\n\033[91mInvalid input. Please enter '1' or '2'\033[0m")
        file_type = int(input("If you want to start from a \033[32m CSV file (enter '1') \033[0m or a \033[93mtext file (enter '2')\033[0m : "))

    filepath = input("Enter the path to your file: ")
    while not os.path.exists(filepath):
        print(f"\033[91mFile'{filepath}' does not exist. Please enter a valid file path.\033[0m")
        filepath = input("\nEnter the path to your file: ")

    fa = finite_automata(filepath)

    if file_type == "csv":
        fa.get_fa_information_from_csv(filepath)
        print("\033[92mFinite automaton successfully loaded from CSV file.\033[0m")
    else:
        fa.get_fa_information()
        print("\033[92mFinite automaton successfully loaded from text file.\033[0m")
    return fa

def main():
    print("\033[94mWelcome to the Finite Automata  Program!\033[0m")
    print("You can perform various operations on a finite automaton.")

    load_fa()

    running = True
    while running:
        print("\n\033[93mSelect an action to perform:\033[0m")
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
        print("11. Change FA")
        print("12. Exit")

        choice = input("\033[94mEnter your choice (1-12): \033[0m").strip()

        if choice == "1":
            print("\n\033[92mFA Information:\033[0m")
            print(f"Number of symbols: {fa.nb_symbols}")
            print(f"Number of initial states: {fa.nb_initial_states}")
            print(f"Initial states: {fa.list_initial_states}")
            print(f"Number of final states: {fa.nb_final_states}")
            print(f"Final states: {fa.list_final_states}")
            print(f"Transitions: {fa.dict_transitions}")

        elif choice == "2":
            csv_filepath = input("Enter the file path to save the CSV: ")
            fa.get_csv_from_fa(csv_filepath)
            print(f"\033[92mYour automaton has been exported to {csv_filepath}\033[0m")

        elif choice == "3":
            fa.is_deterministic(display=True)

        elif choice == "4":
            fa.is_complete(display=True)

        elif choice == "5":
            fa.is_standard(display=True)

        elif choice == "6":
            fa.completion()
            print("\033[92mYour automaton has been completed.\033[0m")

        elif choice == "7":
            fa.determinization()
            print("\033[92mYour automaton has been determinized.\033[0m")

        elif choice == "8":
            fa.standardization()
            print("\033[92mYour automaton has been standardized.\033[0m")

        elif choice == "9":
            fa.minimized_fa()
            print("\033[92mYour automaton has been minimized.\033[0m")

        elif choice == "10":
            fa.complementary()
            print("\033[92mThe complementary automaton has been created.\033[0m")

        elif choice == "11":
            fa = load_fa()

        elif choice == "12":
            print("\033[91mExiting the program. Goodbye!\033[0m")
            running = False

        else:
            print("\033[91mInvalid choice. Please enter a number between 1 and 12.\033[0m")


if __name__ == "__main__":
    main()