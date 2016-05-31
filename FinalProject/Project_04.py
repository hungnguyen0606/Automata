from SDK import EPS
import copy
def _concat(u, v, opU, opV, op):
	if op == 'multiplication':
		newOP = 'empty'
		if u == '' or v == '':
			return ('', 'empty');
		newOP = 'multiplication'
		if u == EPS:
			return (v, opV);
		if v == EPS:
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

def DfaToRE(DFA):
	allState,  alphabet, startingState, dfaTable, acceptedState = copy.deepcopy(DFA);
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
		adj[u, newEndingState] = EPS;
		lastOperation[u, newEndingState] = 'element'

	adj[newStartingState, startingState] = EPS;
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
					if adj[mid, mid] == '' or adj[mid, mid] == EPS:
						tt = EPS;
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
	return adj[newStartingState, newEndingState];