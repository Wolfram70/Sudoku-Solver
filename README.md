# Sudoku Solving using Graph Coloring

This is the repository for Lab Assignment 5 of the IT251 course.<br>
Based on the blog found <a href="https://medium.com/code-science/sudoku-solver-graph-coloring-8f1b4df47072">here</a> and the code is adapted from
<a href="https://github.com/Ishaan97/Sudoku-Solver-Graph-Coloring/tree/master">this</a> repository.

## Added features
1. Randomizing solving by picking one of all possible safe colors at each step ensuring a random solution to a problem with multiple solutions.
2. Problem generation by solving a sudoku with no filled cells (due to randomized solution, this gives a random solved sudoku out of all possiblities) and then randomly masking a fraction of it (given by the user).
3. Support for both 9x9 and 16x16 boards.
4. Support for user inputting of problems.
5. Problem verifying for user input problems to ensure that the board is valid and solvable.
