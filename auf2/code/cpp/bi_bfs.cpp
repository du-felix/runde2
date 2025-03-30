#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <queue>
#include <tuple>
#include <set>
#include <map>
#include <chrono>
#include <utility>
#include <algorithm>

using namespace std;

class Graph {
    public:
        int breite;
        int hoehe;
        int V;
        vector<vector<int>> adjacency_list;
        unordered_set<int> gruben;

        Graph(int hoehe, int breite): breite(breite), hoehe(hoehe) {
            V = breite * hoehe;
            adjacency_list.resize(V);
        }

        void add_edge(int u, int v) {
            adjacency_list[u].push_back(v);
            adjacency_list[v].push_back(u);
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

vector<tuple<pair<int, int>, char>> cart_prod(Graph &G1, Graph &G2, tuple<int, int> vertex, unordered_set<int> g1_gruben, unordered_set<int> g2_gruben) {
    array<char, 4> directions = {'U', 'D', 'L', 'R'};
    vector<tuple<pair<int, int>, char>> neighbors;
    int n1, n2;
    tie(n1, n2) = vertex;
    for (auto d: directions) {
        int new_n1 = G1.edge_dir(n1, d);
        int new_n2 = G2.edge_dir(n2, d);
        if (n1 != new_n1 || n2 != new_n2) {
            if (g1_gruben.find(new_n1) != g1_gruben.end()) {
                new_n1 = 0;
            }
            if (g2_gruben.find(new_n2) != g2_gruben.end()) {
                new_n2 = 0;
            }
            if (g1_gruben.find(new_n1) != g1_gruben.end() && g2_gruben.find(new_n2) != g2_gruben.end()) {
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

tuple<pair<map<pair<int, int>, tuple<pair<int, int>, char>>, map<pair<int, int>, tuple<pair<int, int>, char>>>, pair<int, int>, float> bi_bfs(Graph &G1, Graph &G2, pair<int, int> source, pair<int, int> dest, int height, int width) {
    auto start = chrono::high_resolution_clock::now();

    queue<pair<int, int>> qs, qd;
    set<pair<int, int>> visiteds, visitedd;
    map<pair<int, int>, tuple<pair<int, int>, char>> parents, parentd;
    bool break_flag = false;
    pair<int, int> meeting_vertex;

    qs.push(source);
    qd.push(dest);
    visiteds.insert(source);
    visitedd.insert(dest);

    while (!qs.empty() && !qd.empty()) {
        if (break_flag) {
            break;
        }
        if (qs.size() < qd.size()) {
            pair<int, int> vertex = qs.front();
            qs.pop();
            for (auto neighbor: cart_prod(G1, G2, vertex, G1.gruben, G2.gruben)) {
                if (visiteds.find(get<0>(neighbor)) == visiteds.end()) {
                    visiteds.insert(get<0>(neighbor));
                    qs.push(get<0>(neighbor));
                    parents[get<0>(neighbor)] = make_tuple(vertex, get<1>(neighbor));
                    if (visitedd.find(get<0>(neighbor)) != visitedd.end()) {
                        meeting_vertex = get<0>(neighbor);
                        break_flag = true;
                        break;
                    }
                }
            }
        } else {
            pair<int, int> vertex = qd.front();
            qd.pop();
            for (auto neighbor: cart_prod(G1, G2, vertex, G1.gruben, G2.gruben)) {
                if (visitedd.find(get<0>(neighbor)) == visitedd.end()) {
                    visitedd.insert(get<0>(neighbor));
                    qd.push(get<0>(neighbor));
                    parentd[get<0>(neighbor)] = make_tuple(vertex, get<1>(neighbor));
                    if (visiteds.find(get<0>(neighbor)) != visiteds.end()) {
                        meeting_vertex = get<0>(neighbor);
                        break_flag = true;
                        break;
                    }
                }
            }
        }
    }
    
    auto end = chrono::high_resolution_clock::now();
    float time = chrono::duration_cast<chrono::milliseconds>(end - start).count();
    return make_tuple(make_pair(parents, parentd), meeting_vertex, time);
}

vector<char> uni_get_seq(map<pair<int, int>, tuple<pair<int, int>, char>> &parent, pair<int, int> dest) {
    vector<char> seq;
    pair<int, int> vertex = dest;
    while (vertex != make_pair(0, 0)) {
        seq.push_back(get<1>(parent[vertex]));
        vertex = get<0>(parent[vertex]);
    }
    reverse(seq.begin(), seq.end());
    return seq;
}

void print_path(vector<char> &seq) {
    for (size_t i = 1; i < seq.size()+1; i++) {
        std::cout << i << ": " << seq[i-1] << ";" << endl;
    }
    std::cout << std::endl;
}

int main(int argc, char const *argv[]) {
    string filebase = "auf2/data/labyrinthe";
    for (size_t i = 0; i < 5; i++) {
        string filename = filebase + to_string(i) + ".txt";
        auto [G1, G2] = create_graph(filename);
    }
    return 0;
}
