#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <queue>
#include <tuple>
#include <set>
#include <map>
#include <bitset>
#include <chrono>
#include <utility>
#include <algorithm>

using namespace std;
using CoPair = pair<int, int>;
using ParentMap =map<CoPair, tuple<CoPair, char>>;
using PqEl = tuple<int, pair<int, int>>;

// Custom comparator for the priority queue.
// It returns true if the first element of a is greater than the first element of b.
// This makes the smallest element (in terms of the comparator value) have the highest priority.
struct Comparator {
    bool operator()(const PqEl& a, const PqEl& b) const {
        return get<0>(a) > get<0>(b);
    }
};

class Graph {
    public:
        int breite;
        int hoehe;
        int V;
        vector<vector<int>> adjacency_list;
        vector<bool> flags;
        unordered_set<int> gruben;


        Graph(int hoehe, int breite): breite(breite), hoehe(hoehe) {
            V = breite * hoehe;
            adjacency_list.resize(V);
            flags.resize(V, false);
        }

        void add_edge(int u, int v) {
            adjacency_list[u].push_back(v);
            adjacency_list[v].push_back(u);
        }

        void delete_edge(int u, int v) {
            adjacency_list[u].erase(remove(adjacency_list[u].begin(), adjacency_list[u].end(), v), adjacency_list[u].end());
            adjacency_list[v].erase(remove(adjacency_list[v].begin(), adjacency_list[v].end(), u), adjacency_list[v].end());
        }

        vector<int> get_neighbors(int u) {
            return adjacency_list[u];
        }

        bool is_neighbor(int u, int v) {
            return find(adjacency_list[u].begin(), adjacency_list[u].end(), v) != adjacency_list[u].end();
        }

        int edge_dir(int u, char direction) {
            if (direction == 'U' && is_neighbor(u, u - breite)) {
                return u - breite;
            } else if (direction == 'D' && is_neighbor(u, u + breite)) {
                return u + breite;
            } else if (direction == 'L' && is_neighbor(u, u - 1)) {
                return u - 1;
            } else if (direction == 'R' && is_neighbor(u, u + 1)) {
                return u + 1;
            } else {
                return u;
            }
        }

        void add_grube(int x, int y) {
            gruben.insert(x + y * breite);
        }

        void delete_neighbors(int u) {
            adjacency_list[u].clear();
            adjacency_list[u].shrink_to_fit();
        }   

        void print_graph() {
            for (size_t i = 0; i < V; i++) {
                cout << i << ": ";
                for (auto neighbor: adjacency_list[i]) {
                    cout << neighbor << " ";
                }
                cout << endl;
            }
        }
};

pair<Graph, Graph> create_graph(string filename) {
    ifstream file(filename);

    if (!file) {
        cerr << "File can't be opened" << endl;
        cerr << "Filename: " << filename << endl;
        exit(1);
    }
    
    string dimensions_line;
    int breite, hoehe;
    if (getline(file, dimensions_line)) {
        istringstream iss(dimensions_line);
        iss >> breite >> hoehe;
    }
    Graph G1(hoehe, breite);
    Graph G2(hoehe, breite);

    // Alle horizontalen Kanten
    for (size_t i = 0; i < hoehe; i++) {
        string line;
        getline(file, line);
        istringstream iss(line);

        size_t j = 0;
        int value;
        while (iss >> value) {
            if(value == 0) {
                G1.add_edge((i * breite + j), (i * breite + j + 1));
            };
            j++;
        }
    }

    // Alle vertikalen Kanten
    for (size_t i = 0; i < (hoehe-1); i++) {
        string line;
        getline(file, line);
        istringstream iss(line);

        size_t j = 0;
        int value;
        while (iss >> value) {
            if (value == 0) {
                G1.add_edge((i * breite + j), ((i + 1) * breite + j));
            };
            j++;
        }
    }

    int range;
    file >> range;
    for (size_t i = 0; i < range; i++) {
        int x, y;
        file >> x >> y;
        G1.add_grube(x, y);
    }
    file.ignore(numeric_limits<streamsize>::max(), '\n');

    for (size_t i = 0; i < hoehe; i++) {
        string line;
        getline(file, line);
        istringstream iss(line);

        size_t j = 0;
        int value;
        while (iss >> value) {
            if(value == 0) {
                G2.add_edge(i * breite + j, i * breite + j + 1);
            };
            j++;
        }
    }

    for (size_t i = 0; i < (hoehe-1); i++) {
        string line;
        getline(file, line);
        istringstream iss(line);

        size_t j = 0;
        int value;
        while (iss >> value) {
            if (value == 0) {
                G2.add_edge(i * breite + j, (i + 1) * breite + j);
            };
            j++;
        }
    }

    file >> range;
    for (size_t i = 0; i < range; i++) {
        int x, y;
        file >> x >> y;
        G2.add_grube(x, y);
    }

    file.close();
    return make_pair(G1, G2);
}

// Let states enter dead end paths but dont generate new States in dead end paths
void prune_graph(Graph &G) {
    vector<CoPair> pruned_vertices;
    for (size_t i = 0; i < G.V; i++) {
        if (G.get_neighbors(i).size() == 1 && i != 0 && i != G.V - 1 && G.gruben.find(i) == G.gruben.end()) {
            auto neighbor = G.get_neighbors(i)[0];
            G.flags[i] = true;
            G.delete_edge(i, neighbor);
            pruned_vertices.push_back(make_pair(i, neighbor));
            i = -1;
        }
    }
    for (auto vertex: pruned_vertices) {
        //G.add_edge(get<0>(vertex), get<1>(vertex));
    }
}

int heuristic(CoPair state, int height, int width) {
    auto x1 = state.first % width;
    auto y1 = state.first / width;
    auto x2 = state.second % width;
    auto y2 = state.second / width;
    return max(x1, x2) + max(y1, y2);
}

vector<tuple<CoPair, char>> cart_prod(Graph &G1, Graph &G2, tuple<int, int> vertex, unordered_set<int> g1_gruben, unordered_set<int> g2_gruben, bool back_traversing) {
    array<char, 4> directions = {'U', 'D', 'L', 'R'};
    vector<tuple<pair<int, int>, char>> neighbors;
    int n1, n2;
    tie(n1, n2) = vertex;
    for (auto d: directions) {
        int new_n1 = G1.edge_dir(n1, d);
        int new_n2 = G2.edge_dir(n2, d);
        
        if (back_traversing == true) {
            if (n1 != new_n1 && !G1.flags[new_n1] || n2 != new_n2 && !G2.flags[new_n2] && (g1_gruben.find(new_n1) == g1_gruben.end() && g2_gruben.find(new_n2) == g2_gruben.end())) {
                    neighbors.push_back(make_tuple(make_pair(new_n1, new_n2), d));
                }           
        } else if (n1 != new_n1 && !G1.flags[new_n1] || n2 != new_n2 && !G2.flags[new_n2]) {
            if (g1_gruben.find(new_n1) != g1_gruben.end()) {
                new_n1 = 0;
            }
            if (g2_gruben.find(new_n2) != g2_gruben.end()) {
                new_n2 = 0;
            }
            if (new_n1 == 0 && new_n2 == 0) {
                continue;
            } else {
                neighbors.push_back(make_tuple(make_pair(new_n1, new_n2), d));
            }
        }
    }
    return neighbors;
}

bool bfs_sp(Graph &G, int dest) {
    queue<int> q;
    unordered_set<int> visited;
    q.push(0);

    while (!q.empty()) {
        auto vertex = q.front();
        q.pop();
        for (auto neighbor: G.get_neighbors(vertex)) {
            if (G.gruben.find(neighbor) != G.gruben.end()) {
                continue;
            } else if (neighbor == dest) {
                return true;
            } else if (visited.find(neighbor) == visited.end()) {
                visited.insert(neighbor);
                q.push(neighbor);
            }    
        }     
    } 
    return false;
}

tuple<ParentMap, float> astar(Graph &G1, Graph &G2, CoPair source, CoPair dest, int height, int width) {
    auto start = chrono::high_resolution_clock::now();

    priority_queue<PqEl, vector<PqEl>, Comparator> pq;
    set<CoPair> visited;
    ParentMap parent;
    
}