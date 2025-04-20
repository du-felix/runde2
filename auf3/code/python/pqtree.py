from . import templates as t

class Queue:
    def __init__(self):
        self.queue = []

    def get(self):
        return self.queue

    def push(self, x):
        self.queue.append(x)

    def pop(self):
        return self.queue.pop(0)
    
    def empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)
    
class Node:
    def __init__(self, type, children=None):
        self.type = type # "P", "Q" or "L"
        self.children = children if children is not None else []
        self.siblings = []
        self.parent = None
        self.mark = None #"unmarked", "queued", "unblocked", "blocked"
        self.label = None
        self.pertinent_child_count = 0
        self.pertinent_leaf_count = 0

    def __repr__(self):
        if self.is_leaf():
            return f"Leaf({self.label})"
        return f"{self.type}-Node({self.children})"
    
class Tree:
    def __init__(self, cols):
        self.leaves = {x: Node("L") for x in cols}
        self.root = Node("P", list(self.leaves.values()))
        for col, leaf in self.leaves.items():
            leaf.label = col

def bubble(T, S):
    q = Queue()
    block_count = 0
    blocked_nodes = 0
    off_the_top = 0

    for x in S:
        q.push(x)
    while q.size() + block_count + off_the_top:
        if q.size == 0:
            return Tree(0)
        current = q.pop()
        current.mark = "blocked"
        blocked_siblings = [x for x in current.siblings if x.mark == "blocked"]
        unblocked_siblings = [x for x in current.siblings if x.mark == "unblocked"]
        if len(unblocked_siblings):
            sibling = unblocked_siblings[0]
            current.parent = sibling.parent
            current.mark = "unblocked"
        elif len(current.siblings) < 2:
            current.mark = "unblocked"
        if current.mark == "unblocked":
            parent = current.parent
            if len(blocked_siblings):
                block = [] #not computed yet
                for z in block:
                    z.mark = "unblocked"
                    z.parent = parent
                    parent.pertinent_child_count += 1
            if parent == None:
                off_the_top = 1
            else:
                parent.pertinent_child_count += 1
                if parent.mark == "unmarked":
                    q.push(parent)
                    parent.mark = "queued"
            block_count -= len(blocked_siblings)
            blocked_nodes -= len(block)
        else:
            block_count += (1 - len(blocked_siblings))
            blocked_nodes += 1
    return T

def reduce(T, S):
    q = Queue()
    for current in S:
        q.push(current)
        current.pertinent_leaf_count = 1
    while not q.empty:
        current = q.pop()
        if current.pertinent_leaf_count < len(S):
            parent = current.parent
            parent.pertinent_leaf_count += current.pertinent_leaf_count
            parent.pertinent_child_count -= 1
            if parent.pertinent_child_count == 0:
                q.push(parent)
            
            if not t.L1(current):
                if not t.P1(current):
                    if not t.P3(current):
                        if not t.P5(current):
                            if not t.Q1(current):
                                if not t.Q2(current):
                                    return Tree(0)
        else:
            if not t.L1(current):
                if not t.P1(current):
                    if not t.P2(current):
                        if not t.P4(current):
                            if not t.P6(current):
                                if not t.Q1(current):
                                    if not t.Q2(current):
                                        if not t.Q3(current):
                                            return Tree(0) 
    return T



def c1p(Tree, M):
    cols = M
    T = Tree
    sets = [set(i for i, val in enumerate(row) if val == 1) for row in M]
    for s in sets:
        T = bubble(T, s)
        T = reduce(T, s)
        if T.root.children == []:
            return False
    return True

        
