def pre1(u):

	if u == 'eps' or u == '':
		return u;
	return '(' + u + ')';

def pre2(u):
	if u == 'eps':
		return '';
	return '(' + u + ')';
def concat(u, v):
	if u == '' or v == '':
		return '';
	if u == 'eps':
		return v;
	if v == 'eps':
		return u;
	return '(' + u + ')' + '(' + v + ')';

def prob4():
	#def readDFAtable(f):
	#return (allState,  alphabet, startingState, dfaTable, acceptedState)
	#input
	f = open('input4.txt', 'r');
	allState,  alphabet, startingState, dfaTable, acceptedState = readDFAtable(f);
	f.close();
	#-------------------------------------------------------------------
	#convert to graph
	adj = dict();
	for u in allState:
		for label in alphabet:
			v = dfaTable[u, label];
			if (u, v) in adj.keys():
				adj[u, v] = adj[u, v] + '+' + str(label);
			else:
				adj[u, v] = str(label);

	for u in allState:
		for v in allState:
			if (u, v) not in adj.keys():
				adj[u, v] = '';

	newStartingState = 'new Starting';
	newEndingState = 'new Ending';

	for u in allState:
		adj[newStartingState, u] = '';
		adj[u, newEndingState] = '';

	for u in acceptedState:
		adj[u, newEndingState] = 'eps';

	adj[newStartingState, startingState] = 'eps';
	adj[newStartingState, newEndingState] = ''
	#-------------------------------------------------------------------
	#removing node
	allState.append(newStartingState);
	allState.append(newEndingState);

	for i in range(len(allState) - 2):
		mid = allState[i];

		for j in range(i+1, len(allState) - 1):
			u = allState[j];
			for k in range(i+1, len(allState)):
				v = allState[k];
				if (u == '5' and v == '6'):
					x = 12;
				if v != newStartingState:
					tt = '';
					if adj[mid, mid] == '' or adj[mid, mid] == 'eps':
						tt = 'eps';
					else:
						tt = '(' + adj[mid, mid] + ')*';
					temp = concat(concat(adj[u, mid], tt), adj[mid, v]);


					if adj[u, v] == 'eps' and temp == 'eps':
						adj[u, v] = 'eps';
					elif adj[u, v] == '' and temp == '':
						adj[u, v] = '';
					elif adj[u, v] == '' or temp == '':
						adj[u, v] = adj[u, v] + temp;
					else:
						adj[u, v] = pre1(adj[u, v]) + '+' + pre1(temp);
					#adj[u, v] = adj[u, v] + '+' + temp

	g = open('output4.txt', 'w');
	g.write(adj[newStartingState, newEndingState]);
	g.close();
def probX():
	#def readDFAtable(f):
	#return (allState,  alphabet, startingState, dfaTable, acceptedState)
	#input
	f = open('input4.txt', 'r');
	allState,  alphabet, startingState, dfaTable, acceptedState = readDFAtable(f);
	f.close();
	#-------------------------------------------------------------------
	#convert to graph
	adj = dict();
	for u in allState:
		for label in alphabet:
			v = dfaTable[u, label];
			if (u, v) in adj.keys():
				adj[u, v] = adj[u, v] + '+' + str(label);
			else:
				adj[u, v] = str(label);


	for u in allState:
		if (u, u) not in adj.keys():
			adj[u, u] = 'eps';

	newStartingState = 'new Starting';
	newEndingState = 'new Ending';


	for u in acceptedState:
		adj[u, newEndingState] = 'eps';

	adj[newStartingState, startingState] = 'eps';

	#-------------------------------------------------------------------
	#removing node
	allState.append(newStartingState);
	allState.append(newEndingState);

	for i in range(len(allState) - 2):
		mid = allState[i];

		for j in range(i+1, len(allState) - 1):
			u = allState[j];
			if (u, mid) not in adj.keys():
				continue;
			for k in range(i+1, len(allState)):
				v = allState[k];
				if (mid, v) not in adj.keys():
					continue;

				if v != newStartingState:
					tt = 'eps';
					if adj[mid, mid] != 'eps':
						tt = '(' + adj[mid, mid] + ')*';
					temp = concat(concat(adj[u, mid], tt), adj[mid, v]);

					if (u, v) not in adj.keys():
						adj[u, v] = temp;
					elif adj[u, v] == 'eps' and temp == 'eps':
						adj[u, v] = 'eps';
					elif adj[u, v] == 'eps':
						adj[u, v] = temp;
					elif temp == 'eps':
						pass;
					else:
						adj[u, v] = pre1(adj[u, v]) + '+' + pre1(temp);
					#adj[u, v] = adj[u, v] + '+' + temp

	g = open('output4.txt', 'w');
	g.write(adj[newStartingState, newEndingState]);
	g.close();
