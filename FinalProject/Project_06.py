from graphviz import Digraph
#'dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp', 'patchwork', 'osage',
def drawDFA(DFA):
	allState, alphabet, startingState, dfaTable, acceptedState = DFA;
	sigma = ', '.join(alphabet)

	adj = dict()

	gr = Digraph();
	gr.engine = 'dot'
	gr.format = 'pdf'

	for i, u in enumerate(allState):
		for label in alphabet:
			v = dfaTable[u, label];
			if (u, v) in adj.keys():
				adj[u, v] = adj[u, v] + ', ' + label 
			else:
				adj[u, v] = label

	gr.attr('node', style = 'invis');
	gr.node('myStarting');
	
	gr.attr('node', style = '', shape = 'doublecircle');
	for u in acceptedState:
		gr.node(u);
	
	gr.attr('node', shape = 'circle');
	for u in allState:
		if u not in acceptedState:
			gr.node(u)
	
	gr.edge('myStarting', startingState, 'Start');
	for u, v in adj.keys():
		if adj[u, v] == sigma:
			gr.edge(u, v, 'Sigma')
		else:
			gr.edge(u, v, adj[u, v])


	gr.render('DFA', view = True)
	pass

def drawNFA(NFA):
	pass


