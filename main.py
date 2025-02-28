from finite_automata_functions import finite_automata

def main():
    filepath = "fa.txt"
    csv_filepath = "fa_csv.csv"

    fa = finite_automata(filepath)
    fa.get_fa_information()
    fa.get_csv_from_fa(csv_filepath)
    print(f"{filepath} has been successfully converted into {csv_filepath} \n")

    fa.is_deterministic(True)
    fa.is_complete(True)
    
    if fa.is_standard(True) == False : 
        wanna = input("Do you want to convert the FA into standard form? (y/n) ")
        if wanna == "y":
            fa.standardization()
            print("FA has been converted into standard form")

    
    fa.get_csv_from_fa(csv_filepath)
    
    fa.completion()

    fa.get_csv_from_fa(csv_filepath)

    fa.determinization()

    fa.get_csv_from_fa(csv_filepath)


if __name__ == "__main__":
    main()
