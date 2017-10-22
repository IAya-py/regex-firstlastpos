class Stack:
    def __init__(self):
        self.items = []
        self.length = 0
        
    def push(self, val):
        self.items.append(val)
        self.length += 1
        
    def pop(self):
        if self.empty():
            return None
        self.length -= 1
        return self.items.pop()
        
    def size(self):
        return self.length
    
    def peek(self):
        if self.empty():
            return None
        return self.items[0]
    
    def empty(self):
        return self.length == 0
    
    def __str__(self):
        return str(self.items)

class Node:
    def __init__(self, nullable):
        self.firstpos = {global_naming}
        self.lastpos = {global_naming}
        self.nullable = nullable

    def getNullable(self):
        return self.nullable

    def getFirstPos(self):
        return self.firstpos

    def getLastPos(self):
        return self.lastpos

class ExpressionNode:
    def __init__(self, nullable):
        self.firstpos = set()
        self.lastpos = set()
        self.nullable = nullable

    def getNullable(self):
        return self.nullable

    def getFirstPos(self):
        return self.firstpos

    def getLastPos(self):
        return self.lastpos


    def setNullable(self, nullable):
        self.nullable = nullable

    def setFirstPos(self, firstpos):
        self.firstpos = firstpos

    def setLastPos(self, lastpos):
        self.lastpos = lastpos



ExNode = ExpressionNode(False)

list_of_nodes = []
global global_naming
global_naming = 0


precedence = {}

precedence['+'] = 2
precedence['.'] = 2
precedence['('] = 1

def convert(expression):
    return __convert(expression.split())
    
def __convert(tokens):
    postfix = []
    opstack = Stack()
    
    for token in tokens:
        if token.isidentifier():
            postfix.append(token)
        elif token == '(':
            opstack.push(token)
        elif token == ')':
            while True:
                temp = opstack.pop()
                if temp is None or temp == '(':
                    break
                elif not temp.isidentifier():
                    postfix.append(temp)
            
        else: # must be operator
            if not opstack.empty():
                temp = opstack.peek()
            
                while not opstack.empty() and precedence[temp] >= precedence[token] and token.isidentifier():
                    postfix.append(opstack.pop())
                    temp = opstack.peek()
                
            opstack.push(token)
                
    while not opstack.empty():
        postfix.append(opstack.pop())
            
    return postfix
            
def dfa(postfix):
    counter = 0
    iteration = len(postfix)
    #for x in range(iteration):
    while counter < len(postfix):
        print(postfix)
        if postfix[counter] == '+':
            calculateOR(postfix[counter - 2], postfix[counter - 1], postfix[counter])
            postfix.pop(counter)
            postfix.pop(counter - 1)
            postfix.pop(counter - 2)
            postfix = postfix[:counter-2] + ['d'] + postfix[counter-2:] 
            counter = 0
            continue
                
        
        if postfix[counter] == '.':
            if postfix[len(postfix) - 1] == '+':
                calculateCAT(postfix[1], postfix[2], postfix[counter])
                postfix.pop(1)
                postfix.pop(1)
                postfix.pop(counter - 2)

                postfix = postfix[:1] + ['d'] + postfix[1:] 
                counter = 0
                continue
                
            else:
                calculateCAT(postfix[0], postfix[1], postfix[counter])
                postfix.pop(0)
                postfix.pop(0)
                postfix.pop(counter-2)
                postfix = ['d'] + postfix[0:]
                counter = 0 
                continue

        if postfix[counter] == 'm':
            postfix.pop(counter)
            ExNode.setNullable(True)
            counter = 0

        counter += 1


                
def calculateCAT(op1, op2, oper):

    print(op1, ' ', op2, ' ', oper)
    global global_naming

    if (op1) is 'd':
        
        obj1 = Node(False)
        global_naming += 1


        if(ExNode.getNullable() is True):
            ExNode.setFirstPos(obj1.getFirstPos() | ExNode.getFirstPos())  
        else:
            ExNode.setFirstPos(ExNode.getFirstPos())  

        if(obj1.getNullable() is True):
            ExNode.setLastPos(obj1.getLastPos() | ExNode.getLastPos())
        else:
            ExNode.setLastPos(obj1.getLastPos())

        ExNode.setNullable(obj1.getNullable() & ExNode.getNullable())
        
        list_of_nodes.append(obj1)
        print(ExNode.getFirstPos(), " ", ExNode.getLastPos())
        
    else:
        

        obj1 = Node(False)
        global_naming += 1
        obj2 = Node(False)
        global_naming += 1


        if(ExNode.getNullable() is True):
            ExNode.setFirstPos(obj1.getFirstPos() | obj2.getFirstPos())  
        else:
            ExNode.setFirstPos(obj1.getFirstPos())  

        if(obj2.getNullable() is True):
            ExNode.setLastPos(obj1.getLastPos() | obj2.getLastPos())
        else:
            ExNode.setLastPos(obj2.getLastPos())

        ExNode.setNullable(obj1.getNullable() & obj2.getNullable())
            
        list_of_nodes.append(obj1)
        list_of_nodes.append(obj2)
        print(ExNode.getFirstPos(), " ", ExNode.getLastPos())

def calculateOR(op1, op2, oper):
    print(op1, ' ', op2, ' ', oper)
    global global_naming

    if (op2) is 'd':
        
        obj1 = Node(False)
        global_naming += 1

        ExNode.setNullable(obj1.getNullable() | ExNode.getNullable())
        ExNode.setFirstPos(obj1.getFirstPos() | ExNode.getFirstPos())  
        ExNode.setLastPos(obj1.getLastPos() | ExNode.getLastPos())
        print(ExNode.getFirstPos(), " ", ExNode.getLastPos())        
        list_of_nodes.append(obj1)
        
    else:
        

        obj1 = Node(False)
        global_naming += 1
        obj2 = Node(False)
        global_naming += 1

        ExNode.setNullable(obj1.getNullable() | obj2.getNullable())
        ExNode.setFirstPos(obj1.getFirstPos() | obj2.getFirstPos())  
        ExNode.setLastPos(obj1.getLastPos() | obj2.getLastPos())
        print(ExNode.getFirstPos(), " ", ExNode.getLastPos())
        list_of_nodes.append(obj1)
        list_of_nodes.append(obj2)


    


postfix = convert("( a + b ) m . a . b . b ")
dfa(postfix)
calculateCAT('d', '#', '.')
print("Node  FirstPos  LastPos   Nullable")
for x in list_of_nodes:
    print("Node" , "       " , x.getFirstPos(), "     ", x.getLastPos(), "    ", x.getNullable() )

print("Node" , "       " , ExNode.getFirstPos(), "     ", ExNode.getLastPos(), "    ", ExNode.getNullable() )


