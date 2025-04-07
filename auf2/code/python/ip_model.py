import time

class Graph:
    def __init__(self, hoehe, breite):
        self.breite = breite
        self.hoehe = hoehe
        self.V = hoehe * breite
        self.graph = {x: [] for x in range(self.V)}
        self.gruben = set([])

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def edge_exists(self, u, v):
        if v in self.graph[u]:
            return True
        return False
    
    def edge_direction(self, u, d):
        if d == "U":
            if self.edge_exists(u, u - self.breite):
                return u - self.breite
            return u
        elif d == "D":
            if self.edge_exists(u, u + self.breite):
                return u + self.breite
            return u
        elif d == "L":
            if self.edge_exists(u, u - 1):
                return u - 1
            return u
        elif d == "R":
            if self.edge_exists(u, u + 1):
                return u + 1
            return u

    def edge_count(self):
        val = 0 - self.gruben
        for keys, values in self.graph.items():
            val += len(values)
        return val // 2
    
    def neighbors(self, u):
        return self.graph[u]
    
    def add_grube(self, x, y):
        vertex = y*self.breite + x
        self.gruben.add(vertex)

    def delete_edges(self, u):
        self.graph[u] = []
    
    def delete_edge(self, u, v):
        if self.edge_exists(u, v):
            self.graph[u].remove(v)
            self.graph[v].remove(u)

def graphen_erstellen(filename) -> list[Graph, Graph, int, int]:
    start = time.time()
    with open(filename, "r") as f:
        #Variablen Initialisieren
        breite, hoehe = map(int, f.readline().split())
        G1 = Graph(hoehe, breite)
        G2 = Graph(hoehe, breite)

        for G in [G1, G2]:
            for x in range(hoehe):
                line = f.readline().strip().split()
                for y in range(breite-1):
                    if line[y] == "0":
                        G.add_edge(x * breite + y, x * breite + y + 1)
            
            for x in range(hoehe-1):
                line = f.readline().strip().split()
                for y in range(breite):
                    if line[y] == "0":
                        G.add_edge(x * breite + y, (x + 1) * breite + y)
            
            for x in range(int(f.readline().strip())):
                line = f.readline().strip().split()
                G.add_grube(int(line[0]), int(line[1]))
    end = time.time()
    return (G1, G2, hoehe, breite, end-start)


def prune(G):
    pass