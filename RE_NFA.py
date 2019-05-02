import sys
import os
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
		f= open("NFA.gv","w+")
		f.write("digraph AFN{\n")
		f.write("rankdir=LR; \n node[shape = circle];\n")
		f.write("nodeI [shape=point];\n")
		for i in range(self.finalState):
			f.write("node"+str(i+1)+" [name=\""+str(i+1)+"\"];\n")
			if (i+1) == self.finalState:
				f.write("node"+str(i+1)+" [name=\""+str(i+1)+"\" shape = \"doublecircle\"];\n")
			i+=1
		f.write("nodeI -> node1 [label = \"I\"];\n")
		for t in self.transitions:
			f.write(str(t) + "\n")
		f.write("}\n")

	
	
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

class RegularExpresion(object):
	"""docstring for RegularExpresion"""
	def __init__(self, regexp):
		self.infix = ponPuntos(regexp)
		self.postfix = infixToPostfix(regexp)

	def re_to_nfa(self):
		'''convierte expresion regular a AFN mediante construccion de thompson'''
		stack = []
		postfix = infixToPostfix(self.infix)
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
    prec = {}
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

def ponPuntos(re):
	op = ["(","|",".",")"]
	aux = ""
	i = 0
	n = 0
	#print(len(re))
	while (i + 1) < len(re):
		
		if re[i] in op:
			if re[i] == ")" and re[i+1] == "+" or re[i+1] == "*":
				aux += re[i]
				aux += re[i+1]
			elif re[i] == ")" and re[i+1] not in op and re[i+1] != "+" and re[i+1] != "*":
				aux += re[i]
				aux+= "."
				#aux += re[i+1]
			else:
				aux += re[i]

		elif re[i] == "+" or re[i] == "*":
			if(re[i+1] not in op) or re[i+1] == "(":
				aux+= "."
			
			
		elif re[i] not in op and re[i + 1] not in op and re[i + 1] != "*" and re[i + 1] != "+":
			aux += re[i]
			aux += "."
					
		elif re[i] not in op and re[i + 1] == "*" or re[i + 1] == "+":
			aux += re[i]
			aux += re[i+1]
				
		elif (re[i] not in op and re[i+1] in op):
			aux += re[i]
		else:
			print("NO C")
			print(aux)
			break
		i+=1
		n = i
		if re[i] not in op and re[i] != "*" and re[i] != "+" and n + 1 == len(re):
			#print("entra")
			aux += re[i]
		
		
	#print(i)
	#aux += re[len(re)-1]	
	return aux


if __name__ == '__main__':
	print("digraph AFN{")
	print("rankdir=LR; \n node[shape = circle];")

	#aversicierto = r.re_to_nfa("((((((a.b+)|(c+.b))|(a.b))+).(b.c))|(a+))*")
	#aversicierto = r.re_to_nfa("(((((a.b+).(c))|((c.b).(a*)))|(c.b))+.((c.c)*))|(c.b)")
	regexp = str(sys.argv[1])
	re = RegularExpresion(regexp)
	#regexp = "(a|b)*.c"
	#regexp = "(a.b+.c|c.b.a*|c.b)*.(c.c)*|c.b"
	thompson = re.re_to_nfa()
	thompson.printTransitions()

	
	print("}")
	os.system("dot -Tgif NFA.gv > NFA.gif")
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