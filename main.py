from finite_automata_functions import finite_automata

def main():
    file_path = "fa.txt"
    csv_path = "fa_csv.csv"

    fa = finite_automata(file_path)
    fa.get_fa_information()
    fa.get_csv_from_fa(csv_path)
    print(f"{file_path} has been successfully converted into {csv_path} \n")

    fa.is_deterministic()
    fa.is_complete()

    fa.completion()
    fa.get_csv_from_fa(csv_path)

    fa.determinization_and_completion_automaton()

    fa.get_csv_from_fa(csv_path)


if __name__ == "__main__":
    main()
