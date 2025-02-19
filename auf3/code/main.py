from pyscipopt import Model, quicksum

# -1 entspricht unbekannt bzw. undefiniert.
def create_binary_matrix(filename: str) -> list[list, int, int, list, bool]: # matrix, zeilen_anz, spalten_anz, known_line, bekannt
    matrix = []
    with open(filename, "r") as f:
        zeilen_anz, spalten_anz, bekannt = f.readline().split()
        zeilen_anz, spalten_anz = int(zeilen_anz), int(spalten_anz)
        for lines in range(zeilen_anz):
            new_line = []
            for element in f.readline().split():
                if element == "y":
                    new_line.append(1)
                elif element == "?":
                    new_line.append(-1)
                else:
                    new_line.append(0)
            matrix.append(new_line)
        known_line = f.readline().split()
        for x in range(len(known_line)):
            if known_line[x] == "y":
                known_line[x] = 1
            elif known_line[x] == "n":
                known_line[x] = 0
            else:
                known_line[x] = -1
        if bekannt == "y":
            bekannt = True
        else:
            bekannt = False
    return matrix, zeilen_anz, spalten_anz, known_line, bekannt

def modify_matrix(matrix):
    for x in range(len(matrix)):
        matrix[x].append(0)
        matrix[x].insert(0, 0)
    return matrix

def ilp_model(matrix, r, c, line, line_bool, filename):
    mod_matrix = modify_matrix(matrix)
    model = Model(filename)
    indexset = {}
    for r in range(r):
        for c in range(c+2):
            if mod_matrix[r][c] == -1:
                mod_matrix[r][c] = model.addVar(vtype="B", name=f"mod_matrix_{r}_{c}")

    for i in range(c+2):
        for j in range(c+2):
            indexset[(i, j)] = model.addVar(vtype="B", name=f"permutation_{i}_{j}")
    for n in range(c+2):
        model.addCons(quicksum(indexset[(n, j)] for j in range(c+2)) == 1)
        model.addCons(quicksum(indexset[(i, n)] for i in range(c+2)) == 1)
    model.addCons(indexset[(0, 0)] == 1)
    model.addCons(indexset[(c+1, c+1)] == 1)
    permutation = {}
    for r in range(r):
        for c in range(c+2):
            permutation[(r, c)] = model.addVar(vtype="B", name=f"permutation_{r}_{c}")
            model.addCons(permutation[(r, c)] == quicksum(mod_matrix[r][n]*indexset[(n,c)] for n in range(c+2)))
    if line_bool:
        for c in range(c):
            model.addCons(permutation[(0,c)]==line[c])
    mod_permutation = {}
    bit_change = {}
    for r in range(r):
        for c in range(c+2):
            mod_permutation[(r, c)] = model.addVar(vtype="B", name=f"mod_permutation_{r}_{c}")
            bit_change[(r, c)] = model.addVar(vtype="B", name=f"bit_change_{r}_{c}")
    for r in range(r):
        for n in range(1, c+1):
            model.addCons(bit_change[(r, n)] == permutation[(r, n)] + mod_permutation[(r, n)] - 2 * permutation[(r, n)] * mod_permutation[(r, n)])
    model.setObjective(quicksum(bit_change[(r, c)] for r in range(r) for c in range(c+2)), "minimize")
    for r in range(r):
        model.addCons(quicksum(mod_permutation[(r, n)] + mod_permutation[(r, n+1)] - 2 * mod_permutation[(r, n)] * mod_permutation[(r, n+1)] for n in range(c+1)) == 2)

if __name__ == "__main__":

    filenum = input("Enter the number of the file you want to use (00 - 13): ")
    filename = f"auf3/data/konfetti{filenum}.txt"
    matrix, r, c, zeile, zeile_gegeben = create_binary_matrix(filename)

while False:
        # Quasi inverse Funktion zu create_binary_matrix
    def create_columns(matrix):
        columns = []
        for i in range(len(matrix[0])):
            column = []
            for j in range(len(matrix)):
                column.append(matrix[j][i])
            columns.append(column)
        return columns