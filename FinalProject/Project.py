import networkx as nx
import numpy as np
from collections import deque

def readDFAtable(f):
	n, m, k = map(int, f.readline().split());
	alphabet = f.readline().split();
	acceptedState = map(int, f.readline().split());
	dfaTable = dict();

	for i in range(n):
		line = map(int, f.readline().split());
		for j in range(m):
			dfaTable[i, alphabet[j]] = line[j];

	return (dfaTable, alphabet, acceptedState)

def prob1():
	print 'Start to solve 1:';
	f = open('input1.txt', 'r');
	dfaTable, alphabet, acceptedState = readDFAtable(f);
	str = f.readline();
	f.close();

	currentState = 0;
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
	ret = [start];
	q = deque(start);
	qsize = 1;

	while qsize > 0:
		u = q.pop();
		n = n - 1;
		for v in EpsDfaTable[start, label]:
			if v not in ret:
				q.append(v);
				ret.append(v);
				n = n + 1;

	return ret;

def readEpsDFAtable(f):
	n, m, k = map(int, f.readline().split());
	alphabet = f.readline().split();
	acceptedState = map(int, f.readline().split());
	EpsDfaTable = dict();

	for i in range(n):
		for j in range(m):
			line = map(int, f.readline().split());
			EpsDfaTable[i, alphabet[j]] = [];
			for k in range(1, line[0]+1):
				EpsDfaTable[i, alphabet[j]].append(line[k]);

	return (EpsDfaTable, alphabet, acceptedState)

def prob2():
	f = open('input2.txt', 'r');
	EpsDfaTable, alphabet, acceptedState = readEpsDFAtable(f);
	f.close();

	start = getClosure(0);
	id = dict();
	id[start] = 0;
	dfaState = [start];
	maxId = 1;

	dfaTable = dict();
	q = deque();
	q.append(state[0]);
	n = 1;
	while n > 0:
		u = q.pop();
		n = n - 1;

		for label in alphabet:
			v = [];
			temp = []
			for ne in u:
				temp.extend(EpsDfaTable[ne, label]);
			temp = np.unique(temp).tolist();

			for x in temp:
				temp1 = getClosure(EpsDfaTable, x);
				v.extend(temp1);

			v = np.unique(v).tolist();

			if (v not in id.keys()):
				n = n + 1;
				q.append(v);
				
				dfaState.append(v);

				id[v] = maxId;
				maxId += 1;
			
			dfaTable[id[u], label] = id[v];

	dfaAcceptedState = [];
	for u in dfaState:
		for fin in acceptedState:
			if fin in u:
				dfaAcceptedState.append(id[u]);
				break;

	g = open('output2.txt', 'w');
	g.write(str(len(dfaState)) + ' ' + str(len(alphabet)) + ' ' + str(len(dfaAcceptedState)) + '\n');
	g.write(' '.join(map(str, alphabet)) + '\n');
	g.write(' '.join(map(str, dfaAcceptedState)) + '\n');

	for u in dfaState:
		li = [];
		for label in alphabet:
			li.append(dfaTable[u, label]);
		g.write(' '.join(map(str, li)) + '\n');

	for st in dfaState:
		g.write(str(id[st]) + ': ' + str(st) + '\n');
	g.close();

"""A multi-producer, multi-consumer queue."""

