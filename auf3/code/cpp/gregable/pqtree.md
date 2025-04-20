# PQ Tree Construction

The PQ Tree is incrementally built by each constraint, susbets S of indices of ones, respectively.

## Constraint Attributes

- Leaf nodes in the subset S are F
- Leaf nodes not in the subset S are E
- Internal nodes with only F children are F
- Internal nodes with only E children are E
- Internal nodes with F and E children are P
- Smallest subtree containing all F nodes is considered the pertinent subtree, the root is  considered the pertinent root.
- Applying a constraint is called **reduction**

## Process of Construction

All phases only apply to the pertinent subtree.

- *Bubble Phase:* applying labels to all children
- *Reduction Phase:* Reconstructing the tree by reordering nodes to new P and Q nodes
  - if reduction fails, there're no valid permutations
