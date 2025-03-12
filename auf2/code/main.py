from collections import defaultdict

def graphen_ohne_gruben(filename):
    with open(filename, "r") as f:
        hoehe, breite = map(int, f.readline().split())
        G1 = {x: [] for x in range(hoehe * breite)}
        G2 = {x: [] for x in range(hoehe * breite)}
        for x in range(hoehe):
            line = f.readline().strip()
            for y in range(breite-1):
                if line[y] == "0":
                    G1[x * breite + y].append(x * breite + y + 1)
                    G1[x * breite + y + 1].append(x * breite + y)
        for x in range(hoehe-1):
            line = f.readline().strip()
            for y in range(breite):
                if line[y] == "0":
                    G1[x * breite + y].append((x + 1) * breite + y)
                    G1[(x + 1) * breite + y].append(x * breite + y)
        f.skip(1)
        for x in range(hoehe):
            line = f.readline().strip()
            for y in range(breite-1):
                if line[y] == "0":
                    G2[x * breite + y].append(x * breite + y + 1)
                    G2[x * breite + y + 1].append(x * breite + y)
        for x in range(hoehe-1):
            line = f.readline().strip()
            for y in range(breite):
                if line[y] == "0":
                    G2[x * breite + y].append((x + 1) * breite + y)
                    G2[(x + 1) * breite + y].append(x * breite + y)
    return G1, G2, hoehe, breite

            
def bfs(G1, G2):
    pass

if __name__ == "__main__":
    filename = "./labyrinthe0.txt"

    