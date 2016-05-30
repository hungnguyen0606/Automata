from collections import deque
from SDK import EPS
def getClosure(EpsNFATable, start, label):
	ret = set([start]);
	q = deque([start]);

	while len(q) > 0:
		u = q.pop();

		for v in EpsNFATable[u, label]:
			if v not in ret:
				q.append(v);
				ret.add(v);


	return ret;

def NfaToDfa(myNFA):
	allState,  alphabet, startingState, EpsNFATable, acceptedState = myNFA;
	start = getClosure(EpsNFATable, startingState, EPS);
	id = dict();
	id[frozenset(start)] = 0;
	dfaState = [start];
	maxId = 1;

	dfaTable = dict();
	q = deque();
	q.append(start);
	while len(q) > 0:
		u = q.pop();
		for label in alphabet:
			if (label == EPS):
				break

			v = set();
			temp = set()
			for ne in u:
				temp = temp.union(set(EpsNFATable[ne, label]));
			#temp = np.unique(temp).tolist();

			for x in temp:
				temp1 = getClosure(EpsNFATable, x, EPS);
				v = v.union(temp1);

			#v = np.unique(v).tolist();

			if (frozenset(v) not in id.keys()):
				id[frozenset(v)] = len(dfaState);
				q.append(v);
				dfaState.append(v);

			dfaTable[id[frozenset(u)], label] = id[frozenset(v)];

	dfaAcceptedState = [];
	for u in dfaState:
		for fin in acceptedState:
			if fin in u:
				dfaAcceptedState.append(id[frozenset(u)]);
				break;
	
	alphabet.pop();
	newAllState = [id[frozenset(u)] for u in dfaState];
	newStartingState = id[frozenset(start)];

	return (newAllState, alphabet, newStartingState, dfaTable, dfaAcceptedState);
