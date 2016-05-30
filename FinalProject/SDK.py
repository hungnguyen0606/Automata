EPS = 'E'
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

def readEpsNFAtable(f):
	n, m, k = map(int, f.readline().split());
	alphabet = f.readline().split();
	alphabet.append('eps');
	allState = f.readline().split();
	startingState = f.readline().split()[0];
	acceptedState = f.readline().split();

	EpsNFATable = dict();
	for i in range(n):
		u = f.readline().split()[0];
		for j in range(m+1):
			line = f.readline().split();
			EpsNFATable[u, alphabet[j]] = [];
			for k in range(1, int(line[0])+1):
				EpsNFATable[u, alphabet[j]].append(line[k]);

	return (allState, alphabet, startingState, EpsNFATable, acceptedState);

def writeDFAtable(g, DFA):
	allState, alphabet, startingState, dfaTable, acceptedState = DFA;
	g.write(str(len(allState)) + ' ' + str(len(alphabet)) + ' ' + str(len(acceptedState)) + '\n');
	g.write(' '.join(map(str, alphabet)) + '\n');
	g.write(' '.join(map(str, allState)) + '\n');
	g.write(str(startingState) + '\n');
	g.write(' '.join(map(str, acceptedState)) + '\n');

	for u in allState:
		g.write(str(u) + '\n');
		g.write(' '.join(map(str, [dfaTable[u, label] for label in alphabet])) + '\n');

def writeEpsNFAtable(g, allState, alphabet, startingState, EpsNFAtable, acceptedState):
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
			line = [len(EpsNFAtable[u, label])];
			line.extend([EpsNFATable[u, label]]);
			g.write(' '.join(map(str, line)) + '\n')

