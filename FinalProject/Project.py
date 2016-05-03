import networkx as nx
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
		if (start, label) in EpsDfaTable:
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
			if line[0] != 0:
				EpsDfaTable[i, alphabet[j]] = [];
			for k in range(1, line[0]+1):
				EpsDfaTable[i, alphabet[j]].append(line[k]);

	return (EpsDfaTable, alphabet, acceptedState)

def prob2():
	f = open('input2.txt', 'r');
	EpsDfaTable, alphabet, acceptedState = readEpsDFAtable(f);

	q = deque();
	q.append(getClosure(0));
	n = 1;

	

"""A multi-producer, multi-consumer queue."""

