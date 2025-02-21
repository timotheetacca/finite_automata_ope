class finiteAutomaton:
    def __init__(self, arrayLetters: set[str], arrayStates: set[str], arrayInitialStates: set[str], arrayFinalStates: set[str], arrayTransitions: set[str]):
        """
        Constructor of the class finiteAutomate
        :param arrayLetters: set of letters used in the automaton
        :param arrayStates: set of states used in the automaton
        :param arrayInitialStates: set of initial states of the automaton
        :param arrayFinalStates: set of final states of the automaton
        :param arrayTransitions: set of transitions of the automaton
        
        BTW, I (Thomas) used sets instead of arrays because in a set, the elements are unique, and we don't want to have two times the same state, letter, etc.
        """
        
        self.arrayLetters = arrayLetters
        self.arrayStates = arrayStates
        self.arrayInitialStates = arrayInitialStates
        self.arrayFinalStates = arrayFinalStates
        self.arrayTransitions = arrayTransitions # I.e, ["0a0", "0b0", "0a1", "1b2", "a3", "3a4"]
        self.dictTransitions = {} #I.e, {0: {a: set([0, 1]), b: set([0])}, 1: {b: set([2])}, 3: {a: set([4])}} (for the example above)
            

    def fillTransitionDico(self)->None:
        """
        Fill the dicoTransitions attribute with the transitions in the arrayTransitions attribute so that 
        we can easily access the transitions of a state with a letter
        """
        
        for transition in self.arrayTransitions: # transition is in the form "0a0" for example
            if transition[0] not in self.dictTransitions.keys():
                self.dictTransitions[transition[0]] = {transition[1] : set([transition[2]])}
            else:
                if transition[1] not in self.dictTransitions[transition[0]].keys():
                    self.dictTransitions[transition[0]][transition[1]] = set([transition[2]])
                else:
                    self.dictTransitions[transition[0]][transition[1]].add(transition[2])
                
        return
    
    def displayFiniteAutomaton(self)->None:
        
        return
    

def readFiniteAutomataFromFile(file)->finiteAutomaton:

    return