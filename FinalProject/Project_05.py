from collections import deque
import numpy as np
import copy

def reduceDFA(DFA):
	allState, alphabet, startingState, dfaTable, acceptedState = copy.deepcopy(DFA);

	newAllState = [];
	newAlphabet = [];
	newDfaTable = dict();
	newAcceptedState = [];

	#remove unreachable node
	isReach = dict();
	for u in allState:
		isReach[u] = 0;
	isReach = set([startingState]);
	q = deque([startingState]);
	while len(q) > 0:
		u = q.pop();
		for label in alphabet:
			if dfaTable[u, label] not in isReach:
				q.append(dfaTable[u, label]);
				isReach.add(dfaTable[u, label])
	allState = [u for u in isReach];
	acceptedState = [u for u in acceptedState if u in isReach]
	#

	tabFil = dict(((u, v), 0) for u in allState for v in allState);
	for u in allState:
		if u not in acceptedState:
			for v in acceptedState:
				tabFil[u, v] = tabFil[v, u] = 1;
	#---------------------------
	#filling table
	while True:
		ok = False;
		for u in allState:
			for v in allState:
				if u != v:
					for label in alphabet:
						if tabFil[u, v] == 0 and tabFil[dfaTable[u, label], dfaTable[v, label]] == 1:
							tabFil[u, v] = 1;
							ok = True;
							break;
		if (ok == False):
			break;

	#grouping states that can't be distinguished
	id = dict();
	maxID = 0;
	for i in range(len(allState)):
		if allState[i] not in id.keys():
			id[allState[i]] = maxID;
			maxID += 1;
			for j in range(i+1, len(allState)):
				if tabFil[allState[i], allState[j]] == 0:
					id[allState[j]] = id[allState[i]];
	#------------------------------------------------
	#create new dfa
	for u in allState:
		for label in alphabet:
			newDfaTable[id[u], label] = id[dfaTable[u, label]];

	newStartingState = id[startingState];
	newAlphabet = alphabet
	newAcceptedState = np.unique([id[u] for u in acceptedState]).tolist();
	newAllState = np.unique([id[u] for u in allState]).tolist();

	return (newAllState, newAlphabet, newStartingState, newDfaTable, newAcceptedState);