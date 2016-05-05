import networkx as nx
import numpy as np
from collections import deque

def readDFAtable(f):
	n, m, k = map(int, f.readline().split());
	alphabet = f.readline().split();
	allState = f.readline().split();
	startingState = f.readline().split()[0];
	acceptedState = f.readline().split();

	dfaTable = dict();
	for i in range(n):
		u = f.readline().split()[0];
		line = f.readline().split();
		for j in range(m):
			dfaTable[u, alphabet[j]] = line[j];

	return (allState,  alphabet, startingState, EpsDfaTable, acceptedState)

def prob1():
	#input
	print 'Start to solve 1:';
	f = open('input1.txt', 'r');
	allState, alphabet, startingState, dfaTable, acceptedState = readDFAtable(f);
	str = f.readline();
	f.close();

	currentState = startingState;
	for ch in str:
		if (currentState, ch) in dfaTable.keys():
			currentState = dfaTable[currentState, ch];
		else:
			currentState = -1;
			break;

	g = open('output1.txt', 'w');
	if currentState in acceptedState:
		g.write('Accepted');
	else:
		g.write('Not accepted');
	g.close();

def getClosure(EpsDfaTable, start, label):
	ret = set([start]);
	q = deque([start]);

	while len(q) > 0:
		u = q.pop();

		for v in EpsDfaTable[u, label]:
			if v not in ret:
				q.append(v);
				ret.add(v);


	return ret;

def readEpsDFAtable(f):
	n, m, k = map(int, f.readline().split());
	alphabet = f.readline().split();
	alphabet.append('eps');
	allState = f.readline().split();
	startingState = f.readline().split()[0];
	acceptedState = f.readline().split();

	EpsDfaTable = dict();
	for i in range(n):
		u = f.readline().split()[0];
		for j in range(m+1):
			line = f.readline().split();
			EpsDfaTable[u, alphabet[j]] = [];
			for k in range(1, int(line[0])+1):
				EpsDfaTable[u, alphabet[j]].append(line[k]);

	return (allState, alphabet, startingState, EpsDfaTable, acceptedState);

def prob2():
	#input
	print 'Start to solve 2:';
	f = open('input2.txt', 'r');
	allState,  alphabet, startingState, EpsDfaTable, acceptedState = readEpsDFAtable(f);
	f.close();

	start = getClosure(EpsDfaTable, startingState, 'eps');
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
			if (label == 'eps'):
				break

			v = set();
			temp = set()
			for ne in u:
				temp = temp.union(set(EpsDfaTable[ne, label]));
			#temp = np.unique(temp).tolist();

			for x in temp:
				temp1 = getClosure(EpsDfaTable, x, 'eps');
				v = v.union(temp1);

			#v = np.unique(v).tolist();

			if (len(v) > 0 and frozenset(v) not in id.keys()):
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

	g = open('output2.txt', 'w');
	alphabet.pop();
	g.write(str(len(dfaState)) + ' ' + str(len(alphabet)) + ' ' + str(len(dfaAcceptedState)) + '\n');
	g.write(' '.join(map(str, alphabet)) + '\n');
	g.write(str(id[frozenset(start)]) + '\n');
	g.write(' '.join(map(str, dfaAcceptedState)) + '\n');

	for u in dfaState:
		li = [];
		idu = id[frozenset(u)];
		for label in alphabet:
			if label != 'eps':
				li.append(dfaTable[idu, label]);
		g.write(' '.join(map(str, li)) + '\n');

	for st in dfaState:
		g.write(str(id[frozenset(st)]) + ': ' + str(st) + '\n');
	g.close();

def prob5():
	#input
	print 'Start to solve 5:';
	f = open('input5.txt', 'r');
	allState, alphabet, startingState, dfaTable, acceptedState = readDFAtable(f);
	f.close();

	#init
	newAllState = [];
	newAlphabet = [];
	newDfaTable = [];
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
			if EpsDfaTable[u, label] not in isReach == 0:
				q.append(dfaTable[u, label]);
				isReach.add(dfaTable[u, label])
	allState = [u for u in isReach];
	acceptedState = [u for u in acceptedState if u in isReach]
	#

	tabFil = dict(((u, v), 0) for u in allState for v in allState);
	for u in allState:
		if u not in acceptedState:
			for v in acceptedState:
				tabFil[u, v] = 1
	#---------------------------
	while True:
		ok = False;
		for u in allState:
			for v in allState:
				if u != v:
					for label in alphabet:
						if tabFil[dfaTable[u, label], dfaTable[v, label]] == 1:
							tabFil[u, v] = 1;
							ok = True;
							break;
		if (ok == False):
			break;

	id = dict();
	for i in range(len(allState)):
		if allState[i] not in id.keys():
			id[allState[i]] = len(id);
			for j in range(i+1, allState):
				if tabFil[allState[i], allState[j]] == 0:
					id[allState[j]] = id[allState[i]];
	for u in allState:
		for label in alphabet:
			newDfaTable[id[u], label] = id[dfaTable[u, label]];
	
	newStartingState = id[startingState];
	newAlphabet = alphabet
	newAcceptedState = np.unique([id[u] for u in acceptedState]).tolist();
	newAllState = np.unique([id[u] for u in allState]).tolist();
	#newAcceptedState = [u for u in newAcceptedState]

prob1();