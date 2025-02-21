from finite_automata_functions import finite_automata

def main():
    file_path = "fa.txt"
    csv_path = "fa_csv.csv"

    fa = finite_automata(file_path)
    fa.get_fa_information()
    fa.get_csv_from_fa(csv_path)

if __name__ == "__main__":
    main()
