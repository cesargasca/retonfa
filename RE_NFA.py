import sys
class Transition(object):
	"""docstring for Transition"""
	def __init__(self, nodeFrom,nodeTo,symbol):
		self.nodeFrom = nodeFrom
		self.nodeTo = nodeTo
		self.symbol = symbol
	def __str__(self):
		return "node"+str(self.nodeFrom) + " -> " + "node" + str(self.nodeTo) + " [label = \"" + self.symbol + "\"];"
		
class NFA(object):
	"""docstring for NFA"""
	op = ["(","*","+","|","."]

	def __init__(self, initialState,finalState,transitions):
		self.initialState = initialState #estado inicial
		self.finalState = finalState #estado final
		self.transitions = transitions #lista de transiciones
	

	def count_transition(self):
		'''regresa el estado final (total de estados) '''
		return self.finalState

	def printTransitions(self):
		'''imprime cada transicion con la sintaxis para grapghviz'''
		print("nodeI [shape=point];")
		for i in range(self.finalState):
			print("node"+str(i+1)+" [name=\""+str(i+1)+"\"];")
			if (i+1) == self.finalState:
				print("node"+str(i+1)+" [name=\""+str(i+1)+"\" shape = \"doublecircle\"];")
			i+=1
		print("nodeI -> node1 [label = \"I\"];")
		for t in self.transitions:
			print(t)

	
	
	def concatenate(self,s):
		'''aplica concatenacion a 2 automatas'''
		number_of_transitions = self.count_transition() #cuanta cuantos estados tiene r
		new_transitions = [] #inicializa nueva lista de transiciones
		for t in self.transitions:
			new_transitions.append(t) #inserta transiciones de r a nueva lista de transiciones
		for t in s.transitions:
			'''a cada estado de s le suma la cantidad de estados en r menos el estado final de r que se fusiona con el estado
			inicial de s'''
			t.nodeFrom += number_of_transitions -1
			t.nodeTo += number_of_transitions -1
			new_transitions.append(t) #agrega a nueva lista de transiciones
		new_NFA = NFA(self.initialState,s.finalState+number_of_transitions- 1,new_transitions) #nuevo automata
		return new_NFA

	def union(self,s):
		'''aplica union a dos automatas'''
		new_transitions = [] #iniciliza nueva lista de transiciones
		number_of_transitions = self.count_transition() #contamos cuantos estados tiene el automata r
		#print("nos " + str(number_of_transitions))
		finalState = s.finalState + number_of_transitions + 2 #le agregamos dos estados nuevos 
		#print("final state " + str(finalState))
		#print("self state" + str(s.finalState))
		for t in self.transitions:
			'''a cada transicion le suma 1 en from y al to del automata r'''
			t.nodeFrom += 1
			t.nodeTo += 1
			new_transitions.append(t) #agrega a nuevas transiciones
		for t in s.transitions:
			'''a cada transicion le suma la cantidad de estados en r  mas un inicial nuevo'''
			t.nodeFrom += number_of_transitions+1
			t.nodeTo += number_of_transitions+1
			new_transitions.append(t) #agrega a nuevas transiciones
		new_transition1 = Transition(1,2,"epsilon") #transicion de estado inicial nuevo a viejo estado inicial de r
		new_transition2 = Transition(1,s.initialState+number_of_transitions+1,"epsilon") #transicion nuevo estado inicial a viejo estado inicial de s
		new_transition3 = Transition(self.finalState+1,finalState,"epsilon") #transicion de viejo estado final de r a nuevo estado final 
		new_transition4 = Transition(s.finalState+number_of_transitions+1,finalState,"epsilon") #transicion de viejo estado final de s a nuevo estado final 
		'''inserta nuevas transiciones'''
		new_transitions.append(new_transition1)
		new_transitions.append(new_transition2)
		new_transitions.append(new_transition3)
		new_transitions.append(new_transition4)
		new_NFA = NFA(1,finalState,new_transitions) #nuevo automata

		return new_NFA

	def kleene(self):
		'''aplica cerradura de kleene a automata'''
		new_transitions = [] #inicializa nueva lista de transiciones
		for t in self.transitions:
			'''a cada transicion le suma 1 en from y al to'''
			t.nodeFrom += 1
			t.nodeTo += 1
			new_transitions.append(t) #inserta en la nueva lista de transiciones
		new_transition1 = Transition(1,2,"epsilon") #transicion epsilon desde estado inicial nuevo
		new_transition2 = Transition(1,self.finalState+2,"epsilon") #transicion epsilon de nuevo estado inicial al nuevo estado final
		new_transition3 = Transition(self.finalState+1,self.initialState+1, "epsilon") #transicion epsilon de regreso
		new_transition4 = Transition(self.finalState+1,self.finalState+2,"epsilon") #transicion epsilon al estado final nuevo
		'''inserta nuevas transiciones '''
		new_transitions.append(new_transition1)
		new_transitions.append(new_transition2)
		new_transitions.append(new_transition3)
		new_transitions.append(new_transition4)
		new_NFA = NFA(1,self.finalState+2,new_transitions) #nuevo automata
		return new_NFA

	def positive(self):
		'''aplica cerradura positiva a un automata ''' 
		new_transitions = [] #inicializa nueva lista de transiciones
		for t in self.transitions:
			'''a cada transicion le suma 1 en from y al to'''
			t.nodeFrom += 1
			t.nodeTo += 1
			new_transitions.append(t) #inserta en la nueva lista de transiciones
		new_transition1 = Transition(1,2,"epsilon") #transicion epsilon desde estado inicial nuevo
		new_transition3 = Transition(self.finalState+1,self.initialState+1, "epsilon") #transicion epsilon de regreso
		new_transition4 = Transition(self.finalState+1,self.finalState+2,"epsilon") #transicion epsilon al estado final nuevo
		new_transitions.append(new_transition1) #inserta nueva transicion
		new_transitions.append(new_transition3) #inserta nueva transicion
		new_transitions.append(new_transition4) #inserta nueva transicion
		new_NFA = NFA(1,self.finalState+2,new_transitions) #nuevo automata
		return new_NFA

	'''def re_to_nfa(self,regexp):
		convierte expresion regular a AFN mediante construccion de thompson
		operands = []
		operators = []
		for symbol in regexp:
			if symbol not in NFA.op and symbol != ")": #pregunta si un simbolo se encuentra en lista de operadores
				initialTransitions = []
				initialTransitions.append(Transition(1,2,symbol)) #inserta transiciones, sólo de 1 a 2
				new_NFA = NFA(1,2,initialTransitions) #crea automata básico 
				operands.append(new_NFA) #inserta automata en pila de operandos
				#operands.append(symbol)
			elif symbol == "*":
				#kleene
				#s = operands[-1]
				r = operands.pop() #saca el automata de pila de operandos 
				#operands.append("kleene("+s+")")
				operands.append(r.kleene()) #aplica cerradura kleene a automata que esta en top de la pila
			elif symbol == "+":
				#positive
				#s = operands[-1]
				r = operands.pop() #saca el automata de pila de operandos 
				#operands.append("positive("+s+")")
				operands.append(r.positive()) #aplica cerradura kleene a automata que esta en top de la pila
			elif symbol == ".":
				operators.append(".") #inserta . en pila de operadores
			elif symbol == "|":
				operators.append("|") #inserta | en pila de operadores
			elif symbol == "(": 
				operators.append("(") #inserta ( en pila de operadores
			else:
				entra aqui si el simbolo es un parentesis de cierre 
				while operators[-1] != "(": #mientras no se encuentre el parentesis de apertura
					if operators[-1] == ".":
						Si encuentra un . concatena los dos automatas que esten en top op1.op2 
						op2 = operands.pop()
						op1 = operands.pop()
						#operands.append(op1 + "." + op2)
						operands.append(op1.concatenate(op2))
					elif operators[-1] == "|":
						Si encuentra un | une los dos automatas que esten en top op1|op2 
						op2 = operands.pop()
						op1 = operands.pop()
						#operands.append(op1 + "|" + op2)
						operands.append(op1.union(op2))
					operators.pop()
				operators.pop()
		if len(operators) == 0:
			pass
		else:
			while len(operators) != 0:
				Hace lo mismo pero sin que encuentre paréntesis
				if operators[-1] == ".":
					op2 = operands.pop()
					op1 = operands.pop()
					#operands.append(op1 + "." + op2)
					operands.append(op1.concatenate(op2))
				elif operators[-1] == "|":
					op2 = operands.pop()
					op1 = operands.pop()
					#operands.append(op1 + "|" + op2)
					operands.append(op1.union(op2))
					operators.pop()
		return operands
		'''

	def re_to_nfa(self,regexp):
		'''convierte expresion regular a AFN mediante construccion de thompson'''
		stack = []
		postfix = infixToPostfix(regexp)
		#print(postfix)
		for s in postfix:
			#print("------>" + s)
			if s == '*':
				automat = stack.pop() #saca el ultimo dato de la lista 
				stack.append(automat.kleene()) #aplica cerradura de kleene e inserta al final de la lista
			elif s == '+':
				automat = stack.pop() #saca el ultimo dato de la lista
				stack.append(automat.positive()) #aplica cerradura positiva e inserta al final de la lista
			elif s == '|':
				right = stack.pop() #saca ultimo dato de la lista
				left = stack.pop() #saca penultimo dato de la lista
				stack.append(left.union(right)) #aplica union a right y left (left|right) e inserta al final de la lista
			elif s == '.':
				right = stack.pop() #saca ultimo dato de la lista
				left = stack.pop() #saca penultimo dato de la lista
				stack.append(left.concatenate(right)) #aplica concatenacion a right y left (left.right) e inserta al final de la lista
			else:
				initialTransitions = [] #inicializa lista vacia
				initialTransitions.append(Transition(1,2,s)) #inserta transicion, sólo de 1 a 2
				new_NFA = NFA(1,2,initialTransitions) #crea automata básico 
				stack.append(new_NFA) #inserta al final de la lista
		return stack.pop() #regresa el ultimo valor de la lista, que es el automata final 


from pythonds.basic.stack import Stack
def infixToPostfix(infixexpr):
	'''convierte regex en infix a postfix''' 
    prec = {}
    '''Diccionario de jerarquías'''
    prec["*"] = 4
    prec["+"] = 4
    prec["."] = 3
    prec["|"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []

    for token in infixexpr:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "abcdefghijklmnopqrstuvwyz" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return "".join(postfixList)

if __name__ == '__main__':
	transitions1 = [Transition(1,2,"a"),Transition(2,3,"c")]
	transitions2 = [Transition(1,2,"b")]
	r = NFA(1,2,transitions1)
	s = NFA(1,2,transitions2)

	print("digraph AFN{")
	print("rankdir=LR; \n node[shape = circle];")

	#aversicierto = r.re_to_nfa("((((((a.b+)|(c+.b))|(a.b))+).(b.c))|(a+))*")
	#aversicierto = r.re_to_nfa("(((((a.b+).(c))|((c.b).(a*)))|(c.b))+.((c.c)*))|(c.b)")
	regexp = str(sys.argv[1])
	#regexp = "(a|b)*.c"
	#regexp = "(a.b+.c|c.b.a*|c.b)*.(c.c)*|c.b"
	thompson = r.re_to_nfa(regexp)
	thompson.printTransitions()

	
	print("}")
	'''
	c = r.concatenate(s)
	u = r.union(s)
	print(c.initialState)
	print(c.finalState)
	c.printTransitions()
	print("----------")
	u.printTransitions()
	print("----------")
	k = r.kleene()
	k.printTransitions()
	print("----------")
	p = r.positive()
	p.printTransitions()'''