from pyscipopt import Model, quicksum

def create_matrix(filename: str) -> list[list, int, int, list]:
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

original_matrix, zeilen_anz, spalten_anz, known_line, bekannt = create_matrix("auf3/data/konfetti01.txt")

#add two columns of 0s to begin and end of matrix
z_col = [0 for i in range(zeilen_anz)]
extended_matrix = original_matrix.copy()
for line in extended_matrix:
    line.insert(0, 0)
    line.append(0)

model = Model("Feasibility Model MVP")

# 1 if column i is used in position j
x = {}
for i in range(spalten_anz+2):
    x[i] = {}
    for j in range(spalten_anz+2):
        x[i][j] = model.addVar(vtype="B", name=f"x_{i}_{j}")


# Exclusivity assignments for dimensions constraints
for i in range(spalten_anz):
    model.addCons(quicksum(x[i][j] for j in range(spalten_anz)) == 1, name="exclusivity for cols")
for j in range(spalten_anz):
    model.addCons(quicksum(x[i][j] for i in range(zeilen_anz)) == 1, name="exclusivity for rows")
model.addCons()
# 1 if the permutation has the value 1 in row r and column/position j
y = {}
for r in range(zeilen_anz):
    y[r] = {}
    for j in range(spalten_anz+2):
        y[r][j] = model.addVar(vtype="B", name=f"y_{r}_{j}")
        model.addCons(y[r][j] == quicksum(extended_matrix[r][i] * x[i][j] for i in range(spalten_anz+2)))

# C1P constraints
for n in range(zeilen_anz):
    model.addCons(quicksum((y[r][n] + y[r][n+1] - 2 * y[r][n] * y[r][n+1]) for n in range(spalten_anz+1)) == 2)

model.optimize()