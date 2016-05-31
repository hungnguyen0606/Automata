import networkx as nx
import numpy as np
import SDK
import Project_01
import Project_02
import Project_03
import Project_04
import Project_05
import Project_06

from collections import deque
from SDK import EPS

def prob1(input, output):
	#input
	print 'Start to solve 1:';
	f = open(input, 'r');
	myDFA = SDK.readDFAtable(f);
	str = f.readline();
	f.close();

	g = open(output, 'w');
	if Project_01.isAcceptedString(myDFA):
		g.write('Accepted');
	else:
		g.write('Not accepted');
	g.close();



def prob2(input, output):
	#input
	print 'Start to solve 2:';
	f = open(input, 'r');

	myNFA = SDK.readEpsNFAtable(f);
	f.close();


	g = open(output, 'w');

	#newDfaTable = dict([((id[frozenset(k[0])], k[1]), dfaTable[k]) for k in dfaTable.keys()]);

	DFA = Project_02.NfaToDfa(myNFA);

	SDK.writeDFAtable(g, DFA);

	#for st in dfaState:
		#g.write(str(id[frozenset(st)]) + ': ' + str(st) + '\n');
	g.close();
#------------------------------------------------------------------------------------------
def prob5(input, output):
	#input
	print 'Start to solve 5:';
	f = open(input, 'r');
	#allState, alphabet, startingState, dfaTable, acceptedState
	myDFA = SDK.readDFAtable(f);
	f.close();
	#--------------------------------------------------------------------
	#init

	#newAcceptedState = [u for u in newAcceptedState]
	DFA = Project_05.reduceDFA(myDFA);
	#print output
	g = open(output, 'w');
	SDK.writeDFAtable(g, DFA);
	#g.write('Description\n');
	#for u in newAllState:
		#g.write(str(u) + ': ' + ' '.join(map(str, [v for v in allState if id[v] == u])) + '\n')
	g.close();


#-------------------------------------------------------------------------



def prob4(input, output):
	#def readDFAtable(f):
	#return (allState,  alphabet, startingState, dfaTable, acceptedState)
	#input
	f = open(input, 'r');
	myDFA = SDK.readDFAtable(f);
	f.close();

	s = Project_04.DfaToRE(myDFA);

	g = open(output, 'w');
	g.write(s);
	g.close();

#------------------------------------------------------------------------------
#(allState, alphabet, startingState, EpsNFATable, acceptedState);


def prob3(input, output):
	f = open(input, 'r');
	alphabet = set(f.readline().split());
	s = f.readline();
	f.close();

	DFA = Project_03.ReToDFA(s, alphabet);

	g = open(output, 'w')
	SDK.writeDFAtable(g, DFA);
	g.close();

def prob6(input, output):
	f = open(input, 'r');
	choice = int(f.readline());
	if choice == 0:
		FA = SDK.readDFAtable(f);
		Project_06.drawDFA(FA)
	else:
		FA = SDK.readEpsNFAtable(f);
		Project_06.drawNFA(FA)
	f.close();


#-testing----------------------------------------------
#prob3('input3.txt', 'output3.txt')
prob2('input2.txt', 'output2.txt')
f = open('output2.txt', 'r');
dfa = SDK.readDFAtable(f)
f.close();

mydfa = Project_03.ReToDFA(Project_04.DfaToRE(dfa), set(['a','b']));
Project_06.drawDFA(dfa, 'dfa')

f = open('input2.txt', 'r')
nfa = SDK.readEpsNFAtable(f);
f.close();

Project_06.drawNFA(nfa, 'nfa');

Project_06.drawDFA(mydfa, 'compare')

x = 12
