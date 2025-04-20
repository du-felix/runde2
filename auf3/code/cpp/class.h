#include <vector>

using namespace std;
using Children = vector<PQNode*>;

enum Mark {
    unmarked,
    blocked,
    unblocked,
    queued
};

enum Type {
    p_node,
    q_node,
    leaf
};

class PQTree {
    public:
        PQTree(Children universe) {
            PQNode root(p_node, universe);
        }
};

class PQNode {
    public:
        Children children;
        PQNode* parent;
        Type type;
        Mark mark;
        PQNode(Type t, Children c) {
            type = t;
            children = c;
        }
};
