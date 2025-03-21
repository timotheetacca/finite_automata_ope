
# [Finite Automata Operations Project](https://github.com/timotheetacca/finite_automata_ope)
> ###### 2025-L2 EFREI TACCA Timothée, TRAN Kim-Lan, LOESCH Thomas, OUDIN Julien, MOINDJIE Daïf

This project is designed to perform various operations on Finite Automata (FA), including reading, displaying, standardizing, determinizing, completing, minimizing, and testing word recognition
## Project Overview

The program is divided into several stages:

1. **Reading a FA**: The program reads a FA from a text file, stores it in memory, and displays it on the screen
2. **Displaying FA Information**: The program checks if the FA is deterministic, deterministic and complete, or standard, and displays the results
3. **Standardization**: If the FA is not standard, the program can standardize it on demand
4. **Determinization and completion**: If the FA is not complete or deterministic, the program can convert it into an equivalent complete deterministic FA
5. **Minimization**: The program can minimize a complete deterministic FA
6. **Word Recognition**: The program can test if a given word is recognized by the FA
7. **Complementary Language**: The program can create a complementary automaton of the given FA

## How to Use the Program

### Prerequisites

- [Python 3.x](https://www.python.org/)
- `csv` and `os` libraries *(included in Python standard library)*

## Download
### Git clone
You have 2 options to install our project. You can install the project using git clone :

```
git clone https://github.com/timotheetacca/finite_automata_ope.git
```

### Install

You can also directly install the latest release of our project from [here](https://github.com/timotheetacca/finite_automata_ope)

![download_img](https://github.com/user-attachments/assets/a29cc643-5616-44cf-aa5c-f30e097818cb)


### Example FA File Format

The text file representing an automaton should have the following structure:
``` 
2       
5       
1 0      
1 4       
6         
0 a 1     
0 a 0
0 b 0
1 b 2
2 a 3
3 a 4
```


- **Line 1**: Number of symbols in the automaton's alphabet
- **Line 2**: Number of states
- **Line 3**: Number of initial states, followed by the initial states separeted by space
- **Line 4**: Number of final states followed by the final states separeted by space
- **Line 5**: Number of transitions
- **Lines 6 and beyond**: Transitions in the form `<source state> <symbol> <target state>`


### Example Usage

If you'd like to use the program's functions, here are a few examples
```python
# Initialize the FA with a file path
fa = finite_automata("fa_example.txt")

# Read and display the FA
fa.get_fa_information()
fa.get_csv_from_fa("fa_output.csv")

# Check if the FA is deterministic
fa.is_deterministic(display=True)

# Standardize the FA if it is not standard
if not fa.is_standard():
    fa.standardization()

# Determinize and complete the FA
fa.determinization_and_completion("determinized_fa.csv")

# Minimize the FA
fa.minimized_fa()

# Create a complementary FA
fa.complementary()
``` 
## Feedback

If you have any feedback, please reach out to us at timothee.tacca@efrei.net, kim-lan.tran@efrei.net,  julien.oudin@efrei.net ,thomas.loesch@efrei.net or daif.moindjie@efrei.net
