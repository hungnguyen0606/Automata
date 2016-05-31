from SDK import EPS
import Project_02
import Project_05
import copy

def makeNFA(ch, alphabet, count):
	allState = [str(count), str(count+1)];
	startingState = allState[0];
	acceptedState = [allState[-1]];
	newAlphabet = list(alphabet);
	#newAlphabet.append(EPS);

	#init transition table
	EpsNFATable = dict();
	for u in allState:
		for label in newAlphabet:
			EpsNFATable[u, label] = [];

	EpsNFATable[startingState, ch].append(allState[-1]);

	return ((allState, newAlphabet, startingState, EpsNFATable, acceptedState), count+2)
	pass

def unionNFA(nfaU, nfaV, count):
	allState = list(nfaU[0]);
	allState.extend(nfaV[0]);
	#create new starting state
	allState.append(str(count));
	newAlphabet = list(nfaU[1]);
	#update transition table
	EpsNFATable = nfaU[-2].copy();
	EpsNFATable.update(nfaV[-2]);
	for label in newAlphabet:
		EpsNFATable[allState[-1], label] = [];
	EpsNFATable[allState[-1], EPS].extend([nfaU[2], nfaV[2]])

	acceptedState = list(nfaU[-1]);
	acceptedState.extend(nfaV[-1]);

	return ((allState, newAlphabet, allState[-1], EpsNFATable, acceptedState), count+1)
	pass

def repeatNFA(nfaU, count):
	allState = list(nfaU[0]);
	#allState.extend(nfaV[0]);
	alphabet = list(nfaU[1]);
	acceptedState = list(nfaU[-1]);
	startingState = nfaU[2];

	EpsNFATable = nfaU[-2].copy();
	for u in acceptedState:
		if startingState not in EpsNFATable[u, EPS]:
			EpsNFATable[u, EPS].append(startingState);
		if u not in EpsNFATable[startingState, EPS]:
			EpsNFATable[startingState, EPS].append(u);

	return ((allState, alphabet, startingState, EpsNFATable, acceptedState), count);
	pass

def concatNFA(nfaU, nfaV, count):
	allState = list(nfaU[0]);
	allState.extend(nfaV[0]);
	alphabet = list(nfaU[1]);
	acceptedState = list(nfaV[-1]);

	EpsNFATable = nfaU[-2].copy();
	EpsNFATable.update(nfaV[-2]);
	for u in nfaU[-1]:
		EpsNFATable[u, EPS].append(nfaV[2]);

	return ((allState, alphabet, nfaU[2], EpsNFATable, acceptedState), count)
	pass

def preprocess(s, alphabet):
	s = s.replace(' ', '');
	ret = s[0];
	anti = set(['*', ')', '+'])
	favor = set([')', '*']).union(set(alphabet));
	for i in range(1, len(s)):
		if s[i] not in anti:
			if s[i-1] in favor:
				ret += '.'
		ret += s[i]
	ret += '~';
	return ret

def ReToDFA(s, alphabet):
	alphabet.add(EPS);
	priority = {
		'~': -1,  #ending character
		'(': 0,
		')': 1,
		'+': 2,   #union
		'.': 3,   #concat
		'*': 4,   #kleene star
	}
	#
	s = preprocess(s, alphabet);
	q = [];
	st = [];
	count = 0;

	lastCh = None;
	for ch in s:
		_nfa = None
		nextOp = None
		if ch in alphabet:
			_nfa, count = makeNFA(ch, alphabet, count);
			q.append(_nfa);
		else:
			nextOp = ch

			#lastCh = ch;
			if ch == '(':
				st.append(ch);
				continue;

			pr = priority[nextOp];
			while len(st) > 0 and pr < priority[st[-1]]:
				oper = st.pop();

				if oper == '+':
					assert len(q) > 1, 'Invalid expression - not have enough operands'
					u = q.pop();
					v = q.pop();
					nfa, count = unionNFA(u, v, count);
					q.append(nfa);

				elif oper == '.':
					assert len(q) > 1, 'Invalid expression - not have enough operands'
					u = q.pop();
					v = q.pop();
					nfa, count = concatNFA(v, u, count);
					q.append(nfa);

				elif oper == '*':
					assert len(q) > 0, 'Invalid expression - not have enough operands'
					u = q.pop();
					nfa, count = repeatNFA(u, count);
					q.append(nfa);

			if nextOp == ')':
				assert len(st) > 0, 'Invalid expression'
				assert st[-1] == '(', 'Invalid bracket matching'
				st.pop();

			if nextOp != ')':
				st.append(nextOp);


	newDFA = Project_02.NfaToDfa(q[0]);
	newDFA = Project_05.reduceDFA(newDFA);
	return newDFA
