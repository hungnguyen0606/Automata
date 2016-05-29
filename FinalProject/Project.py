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

	return (allState,  alphabet, startingState, dfaTable, acceptedState)

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

def writeDFAtable(g, allState, alphabet, startingState, dfaTable, acceptedState):

	g.write(str(len(allState)) + ' ' + str(len(alphabet)) + ' ' + str(len(acceptedState)) + '\n');
	g.write(' '.join(map(str, alphabet)) + '\n');
	g.write(' '.join(map(str, allState)) + '\n');
	g.write(str(startingState) + '\n');
	g.write(' '.join(map(str, acceptedState)) + '\n');

	for u in allState:
		g.write(str(u) + '\n');
		g.write(' '.join(map(str, [dfaTable[u, label] for label in alphabet])) + '\n');

def writeEpsDFAtable(g, allState, alphabet, startingState, epsDFAtable, acceptedState):
	g.write(str(len(allState)) + ' ' + str(len(alphabet)) + ' ' + str(len(acceptedState)) + '\n');
	g.write(' '.join(map(str, alphabet)) + '\n');
	g.write(' '.join(map(str, allState)) + '\n');
	g.write(str(startingState) + '\n');
	g.write(' '.join(map(str, acceptedState)) + '\n');

	newAlpha = alphabet;
	newAlpha.append('eps')

	for u in allState:
		g.write(str(u) + '\n');
		for label in newAlpha:
			line = [len(epsDFAtable[u, label])];
			line.extend([EpsDfaTable[u, label]]);
			g.write(' '.join(map(str, line)) + '\n')


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

	g = open('output2.txt', 'w');
	alphabet.pop();
	newAllState = [id[frozenset(u)] for u in dfaState];
	newStartingState = id[frozenset(start)];
	#newDfaTable = dict([((id[frozenset(k[0])], k[1]), dfaTable[k]) for k in dfaTable.keys()]);


	writeDFAtable(g, newAllState, alphabet, newStartingState, dfaTable, dfaAcceptedState);

	for st in dfaState:
		g.write(str(id[frozenset(st)]) + ': ' + str(st) + '\n');
	g.close();
#------------------------------------------------------------------------------------------
def prob5():
	#input
	print 'Start to solve 5:';
	f = open('input5.txt', 'r');
	allState, alphabet, startingState, dfaTable, acceptedState = readDFAtable(f);
	f.close();
	#--------------------------------------------------------------------
	#init
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
	#newAcceptedState = [u for u in newAcceptedState]

	#print output
	g = open('output5.txt', 'w');
	writeDFAtable(g, newAllState, newAlphabet, newStartingState, newDfaTable, newAcceptedState);
	g.write('Description\n');
	for u in newAllState:
		g.write(str(u) + ': ' + ' '.join(map(str, [v for v in allState if id[v] == u])) + '\n')
	g.close();


#-------------------------------------------------------------------------

def _concat(u, v, opU, opV, op):
	if op == 'multiplication':
		newOP = 'empty'
		if u == '' or v == '':
			return ('', 'empty');
		newOP = 'multiplication'
		if u == 'eps':
			return (v, opV);
		if v == 'eps':
			return (u, opU);
		if opU == 'addition' and opV == 'addition':
			return ('(' + u + ')' + '(' + v + ')', 'multiplication');
		if opU == 'addition' and opV != 'addition':
			return ('(' + u + ')' + v, 'multiplication') ;
		if opU != 'addition' and opV == 'addition':
			return (u + '(' + v + ')', 'multiplication');
		return (u + v, 'multiplication')
	else:
		if u == '' and v == '':
			return ('', 'empty');
		if u == '':
			return (v, opV)
		if v == '':
			return (u, opU)

		return (u + '+' + v, 'addition')

def prob4_new_28_05_2016__08_02PM():
	#def readDFAtable(f):
	#return (allState,  alphabet, startingState, dfaTable, acceptedState)
	#input
	f = open('input4.txt', 'r');
	allState,  alphabet, startingState, dfaTable, acceptedState = readDFAtable(f);
	f.close();
	#-------------------------------------------------------------------
	#convert to graph
	adj = dict();
	lastOperation = dict();
	for u in allState:
		for label in alphabet:
			v = dfaTable[u, label];
			if (u, v) in adj.keys():
				adj[u, v] = adj[u, v] + '+' + str(label);
				lastOperation[u, v] = 'addition'
			else:
				adj[u, v] = str(label);
				lastOperation[u, v] = 'element'

	newStartingState = 'new Starting';
	newEndingState = 'new Ending';

	for u in acceptedState:
		adj[u, newEndingState] = 'eps';
		lastOperation[u, newEndingState] = 'element'

	adj[newStartingState, startingState] = 'eps';
	lastOperation[newStartingState, startingState] = 'element'

	#adj[newStartingState, newEndingState] = ''
	#-------------------------------------------------------------------
	#removing node
	allState.append(newStartingState);
	allState.append(newEndingState);

	for u in allState:
		for v in allState:
			if (u, v) not in adj.keys():
				adj[u, v] = '';
				lastOperation[u, v] = 'empty'

	for i in range(len(allState) - 2):
		mid = allState[i];

		for j in range(i+1, len(allState) - 1):
			u = allState[j];
			if adj[u, mid] == '':
				continue

			for k in range(i+1, len(allState)):
				v = allState[k];
				if adj[mid, v] == '':
					continue
				if u == '6' and v == '5':
					x = 1
					y = 2
					z = x + y
				if v != newStartingState:
					tt = '';
					if adj[mid, mid] == '' or adj[mid, mid] == 'eps':
						tt = 'eps';
					else:
						if lastOperation[mid, mid] == 'element':
							tt = adj[mid, mid] + '*';
						else:
							tt = '(' + adj[mid, mid] + ')*';

					
					temp, newOP1 = _concat(adj[u, mid], tt, lastOperation[u, mid], 'multiplication', 'multiplication');
					temp, newOP2 = _concat(temp, adj[mid, v], newOP1, lastOperation[mid, v], 'multiplication');

					lastOP = ''
					if tt.find('(0+11*01+00*1)*') != -1 or adj[u,v].find('(0+11*01+00*1)') != -1:
						x = 123
						y = 3;
						z = x+y
					adj[u, v], lastOperation[u, v] = _concat(adj[u, v], temp, lastOperation[u, v], newOP2, 'addition');

					#adj[u, v] = adj[u, v] + '+' + temp

	g = open('output4.txt', 'w');
	g.write(adj[newStartingState, newEndingState]);
	g.close();

#prob2();
prob5()
#prob4_new_28_05_2016__08_02PM();