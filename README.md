# finite_automata_ope

---

# 1. Displaying FA on screen

![fa_graph](https://github.com/user-attachments/assets/6320d67b-30d6-469d-96b5-f0b670b78137)


this graph corresponds to the following `.txt` file :

```
2  
5  
1 0  
1 4  
6  
0a0  
0b0  
0a1  
1b2  
2a3  
3a4  
```

The first 2 lines give us the number of symbols in the alphabet, 2 symbols :  
A={a,b}  
  
The second, the number of states, 5 states:  
Q={0,1,2,3,4}  

The third, the number of initial states, 1 initial state, , followed by the list of initial states:  
I={0}

The fourth, the number of final states, 1 final state, followed by the list of final states:  
T={4}  

The fifth, the number of transitions, 6 transitions, , followed by the list of all transitions:  
0a1 → corresponds to the transition from 0 to 1 for *a*  
   
     
The goal is to collec all this informations in order to create a `.csv` that looks like this :  


![fa_csv](https://github.com/user-attachments/assets/b346f690-be01-49e5-98f1-4eb811a7daa0)


