from pyscipopt import Model, quicksum
from scipy.optimize import newton
import math
import time
import os
from datetime import datetime
from tabulate import tabulate

class Node:
    def __init__(self, code, cost, children=None):
        self.code = code
        self.cost = cost
        self.children = children if children is not None else []

    def add_child(self, child):
        self.children.append(child)

    def __lt__(self, other):
        # For priority queue comparison based on frequency
        return self.frequency < other.frequency

class Queue:
    def __init__(self):
        self.queue = []

    def get(self):
        return self.queue

    def push(self, x):
        self.queue.append(x)

    def pop(self):
        return self.queue.pop(0)
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def length(self):
        return len(self.queue)

def get_data(filename):
    with open(filename, "r") as f:
        n = int(f.readline())
        weight_function = list(map(int, f.readline().split()))
        
        frequency_dict = {}
        text = f.read()
        for char in text:
            if char != "\n":
                if char in frequency_dict:
                    frequency_dict[char] += 1
                else:
                    frequency_dict[char] = 1
    return n, weight_function, frequency_dict, len(text.strip("\n"))

def ip_model(n, costs_dict, probs_dict, text_len):
    model = Model("Word Cost IP")
    alphabet = list(range(n))
    sources = list(range(len(probs_dict)))
    probs = [f/text_len for _, f in probs_dict.items()]
    costs = costs_dict
    u = {}
    def f(r):
        return sum(r ** (-c) for c in costs) - 1
    r = newton(f, 1.5) 
    d_min = min(costs)
    d_max = max(math.ceil(-math.log(p, r)) for p in probs)+5
    D_set = list(range(d_min, d_max))

    for i in sources:
        for d in D_set:
            u[(i, d)] = model.addVar(vtype="B", name=f"u_{i}_{d}")
    
    model.setObjective(quicksum(probs[i] * d * u[(i, d)] for i in sources for d in D_set), "minimize")

    b = {}
    b[0] = model.addVar(vtype="I", lb=1, ub=1, name=f"b_{0}")
    for d in D_set:
        b[d] = model.addVar(vtype="I", name=f"b_{d}")
        lhs = quicksum(u[(i, d)] for i in sources) + b[d]
        rhs = 0
        for k in costs:
            if d-k >= 0:
                rhs += b[d-k]
            else:
                break
        model.addCons(lhs<=rhs)

    for i in sources:
        model.addCons(quicksum(u[(i, d)] for d in D_set) == 1)
    return model, u, d_max

def solve(model, u):
    start = time.time()
    model.optimize()
    end = time.time()
    lengths = []
    for key, _ in u.items():
        if model.getVal(u[key]) == 1:
            lengths.append(key[-1])
    return lengths

def codes(costs, lengths):
    n = round(max(lengths)/min(costs))
    root = Node(None, None)
    codes = []
    codes_dict = {}

    def build(parent, n):
        if n == 0:
            return 0
        for x, i in enumerate(costs):
            node = Node(x, i)
            parent.add_child(node)
            build(node, n-1)
    def get(code, node, cost):
        if not node.children:
            return 0
        else:
            for child in node.children:
                new_code = code
                new_cost = cost
                new_code += str(child.symbol)
                new_cost += child.cost
                if new_cost in lengths:
                    lengths.remove(new_cost)
                    codes.append(new_code)
                else:
                    get(new_code, child, new_cost)
    def weights(lang):
        for code in lang:
            weight = 0
            for symbol in code:
                weight += costs[int(symbol)]
            codes_dict[code] = weight
    
    build(root, n)
    get("", root, 0)
    weights(codes)
    return codes_dict

def implicit_bfs(d_max, lengths, costs):
    n = len(costs)
    language_dict = {}
    q = Queue()
    q.push(Node("", 0, children=None))
    while not q.is_empty():
        node = q.pop()
        if node.cost in lengths:
            lengths.remove(node.cost)
            language_dict[node.code] = node.cost
            if len(lengths) == 0:
                break
        elif node.cost > d_max:
            pass
        else:
            for i in range(n):
                child = Node(node.code + str(i), node.cost + costs[i])
                q.push(child)
    return language_dict

def canonical_huffman():
    pass

def table(alphabet, language, language_dict):
    header = ["Zeichen", "Kosten", "Wort"]
    rows = []
    for i in range(len(alphabet)):
        row = []
        row.append(alphabet[i])
        row.append(language_dict[language[i]])
        row.append(language[i])
        rows.append(row)
    table = tabulate(rows, headers=header, tablefmt="github")
    length = 0
    for x in range(len(alphabet)):
        length += freq[alphabet[x]] * language_dict[language[x]]
    return table, length

if __name__ == "__main__":
    path = "auf1/data/"
    current = os.getcwd() + "/auf1/output/"
    folder_path = os.path.join(current, str(datetime.now().strftime("%m-%d_%H-%M_karp_bfs"))) + "/"
    os.makedirs(folder_path, exist_ok=True)
    input_files = input("Welche Dateien sollen bearbeitet werden?").split()
    for x in input_files:
        file = f"schmuck{x}.txt"
        full_start = time.time()
        n, costs, freq, text_len = get_data(path+file)
        solve_start = time.time()
        model, u, d_max = ip_model(n, costs, freq, text_len)
        lengths = solve(model, u)
        #language_dict = codes(costs, lengths)
        language_dict = implicit_bfs(d_max, lengths, costs)
        solve_end = time.time()
        alphabet = sorted(freq, key=freq.get, reverse=True)
        language = sorted(language_dict, key=language_dict.get)
        table_str, length = table(alphabet, language, language_dict)
        full_end = time.time()
        with open(folder_path + "solution" + x + ".txt", "w") as f:
            f.write(f"Laufzeit zum Lösen des Modells: {round(full_end-full_start, 3)} s\n")
            f.write(f"Gesamtlaufzeit: {round(solve_end-solve_start, 3)} s\n")
            f.write(f"Total Length: {round(length * 0.1, 3)} cm\n\n")
            f.write(table_str)

