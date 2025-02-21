class finiteAutomaton:
    def __init__(self, arrayLetters: list[str], arrayStates: list[str], arrayInitialStates: list[str], arrayFinalStates: list[str], arrayTransitions: list[str]):
        """
        Constructor of the class finiteAutomate
        :param arrayLetters: array of letters used in the automaton
        :param arrayStates: array of states used in the automaton
        :param arrayInitialStates: array of initial states of the automaton
        :param arrayFinalStates: array of final states of the automaton
        :param arrayTransitions: array of transitions of the automaton
        """
        
        self.arrayLetters = arrayLetters
        self.arrayStates = arrayStates
        self.arrayInitialStates = arrayInitialStates
        self.arrayFinalStates = arrayFinalStates
        self.arrayTransitions = arrayTransitions # I.e, ["0a0", "0b0", "0a1", "1b2", "a3", "3a4"]
        self.dictTransitions = {} #I.e, {0: {a: [0, 1], b: [0]}, 1: {b: [2]}, 3: {a: [4]}} (for the example above)
            

    def fillTransitionDico(self)->None:
        """
        Fill the dicoTransitions attribute with the transitions in the arrayTransitions attribute so that 
        we can easily access the transitions of a state with a letter
        """
        
        for transition in self.arrayTransitions: # transition is in the form "0a0" for example
            if transition[0] not in self.dictTransitions.keys():
                self.dictTransitions[transition[0]] = {transition[1] : [transition[2]]}
            else:
                if transition[1] not in self.dictTransitions[transition[0]].keys():
                    self.dictTransitions[transition[0]][transition[1]] = [transition[2]]
                else:
                    self.dictTransitions[transition[0]][transition[1]].append(transition[2])
                
        return
    
    def displayFiniteAutomaton(self)->None:
        
        return
    

def readFiniteAutomataFromFile(file)->finiteAutomaton:

    return