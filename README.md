# Finite Automata Library

## 1. **Class Attributes**
- `file_path`: *(str)* Path to the automaton .txt
- `nb_symbols`: *(int)* Number of symbols in the automaton
- `nb_states`: *(int)* Number of states in the automaton
- `nb_initial_states`: *(int)* Number of initial states
- `list_initial_states`: *(list of str)* List of initial states
- `nb_final_states`: *(int)* Number of final states
- `list_final_states`: *(list of str)* List of final states
- `nb_transitions`: *(int)* Total number of transitions
- `list_symbols`: *(list of str)* List of symbols in the automaton
- `dict_transitions`: *(dict)* Mapping of states to their transitions. Each state is a key, and its value is also adictionary where each symbol is a list of destination states

  ```python
  "0": {"a": ["1", "0"],  "b": ["0"]},
  "1": { "a": ["1"],"b": []}
 
  ```


- `dict_sink`: *(dict)* Transitions for the sink state *(je l'ai séparé car si on veut ajouter des états, il faudrait supprimer le sink state puis la re-rajouter etc..)*
  Structure:  
  ```python
  "P": "a": ["P"],"b": ["P"]
  ```

---

## **Functions**

###  **`get_fa_information()`**
Reads the automaton file, extracts  information to create an object from the class

---

###  **`get_csv_from_fa(output_filepath)`**
Generates a CSV file of the automaton

---

###  **`is_deterministic()`**
Checks if the automaton is deterministic. 

- **Output**:
  - Returns `False` with a message if the automaton is non-deterministic
  - Returns `True` if deterministic

---

### **`is_complete()`**
Checks if the automaton is complete
- **Output**:
  - Returns `False` with a message if the automaton is incomplete
  - Returns `True` if complete

---

### **`completion()`**
Completes the automaton by filling `dict_transitions` and replacing all the empty transitions with P

---

### 6. **`determinization_and_completion_automaton(states_to_process=None)`**
Determinizes and completes the automaton
- **How it works**:
  - Combines  transitions into new "combined states" if there are more than 1 transition
  - Recursively processes the new combined states until no more can be created
- **Input**: 
  - `states_to_process`: *(list of str)* Specific states to determinize (optional, espacially for start)

---

## **How to make it work**

1. **Initialization**:  
   Create an object of the `finite_automata` 
   ```python
   fa = finite_automata("fa.txt")
   ```

2. **Read automaton data**:  
    Get all the informations from the .txt
   ```python
   fa.get_fa_information()
   ```

3. **Check if deterministic or complete**:  
   ```python
   fa.is_deterministic():
   fa.is_complete():
   ```

4. **Completion**:
   ```python
   fa.completion()
   ```

5. **eterminization**:
   ```python
   fa.determinization_and_completion_automaton()
   ```

6. **Generate a CSV**:  
    If there is no csv in the folder, it will create it
   ```python
   fa.get_csv_from_fa(fa_csv.csv)
   ```
