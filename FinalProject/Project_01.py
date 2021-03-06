import copy

def isAcceptedString(DFA):
	allState, alphabet, startingState, dfaTable, acceptedState = copy.deepcopy(DFA)
	currentState = startingState;
	for ch in str:
		if (currentState, ch) in dfaTable.keys():
			currentState = dfaTable[currentState, ch];
		else:
			currentState = -1;
			break;

	return currentState in acceptedState