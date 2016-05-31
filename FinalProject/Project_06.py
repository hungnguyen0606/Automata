from graphviz import Digraph
from SDK import EPS
import copy
#'dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp', 'patchwork', 'osage',
def drawDFA(DFA, output):
	allState, alphabet, startingState, dfaTable, acceptedState = copy.deepcopy(DFA);
	sigma = ', '.join(alphabet)

	adj = dict()

	# gr = Digraph();
	# gr.engine = 'dot'
	# gr.format = 'pdf'

	for i, u in enumerate(allState):
		for label in alphabet:
			v = dfaTable[u, label];
			if (u, v) in adj.keys():
				adj[u, v] = adj[u, v] + ', ' + label 
			else:
				adj[u, v] = label

	draw(DFA, adj, output);
	# gr.attr('node', style = 'invis');
	# gr.node('myStarting');
	
	# gr.attr('node', style = '', shape = 'doublecircle');
	# for u in acceptedState:
	# 	gr.node(u);
	
	# gr.attr('node', shape = 'circle');
	# for u in allState:
	# 	if u not in acceptedState:
	# 		gr.node(u)
	
	# gr.edge('myStarting', startingState, 'Start');
	# for u, v in adj.keys():
	# 	if adj[u, v] == sigma:
	# 		gr.edge(u, v, 'Sigma')
	# 	else:
	# 		gr.edge(u, v, adj[u, v])


	# gr.render('DFA', view = True)
	pass

def drawNFA(NFA, output):
	allState, alphabet, startingState, nfaTable, acceptedState = copy.deepcopy(NFA);
	adj = dict();
	for u in allState:
		for label in alphabet:
			for v in nfaTable[u, label]:
				if label == EPS:
					label = 'epsilon'
				if (u, v) in adj.keys():
					adj[u, v] = adj[u, v] + ', ' + label;
				else:
					adj[u, v] = label;

	draw(NFA, adj, output);
	pass

#allState, alphabet, startingState, faTable, acceptedState
def draw(FA, adj, output):
	newAlpha = list(FA[1])
	if newAlpha[-1] == EPS:
		newAlpha.pop();
	sigma = ', '.join(newAlpha)
	gr = Digraph();
	gr.engine = 'dot'
	gr.format = 'pdf'

	gr.attr('node', style = 'invis');
	gr.node('myStarting');
	
	gr.attr('node', style = '', shape = 'doublecircle');
	for u in FA[-1]:
		gr.node(str(u));
	
	gr.attr('node', shape = 'circle');
	for u in FA[0]:
		if u not in FA[-1]:
			gr.node(str(u))
	
	gr.edge('myStarting', str(FA[2]), 'Start');
	for u, v in adj.keys():
		if adj[u, v] == sigma:
			gr.edge(str(u), str(v), 'Sigma')
		else:
			gr.edge(str(u), str(v), adj[u, v])

	gr.render(output, view = True);

