# Sudoku Solver

This Python code provides a Sudoku puzzle solver using constraint satisfaction techniques. Sudoku is treated as a constraint satisfaction problem, and the AC3 (Arc Consistency Algorithm #3) is applied to solve it.
When AC3 is not enough to solve the Sudoku, as is the case for the difficulty 'hellish', this algorithm utilizes Backtrack Search to find the missing numbers.

## Sudoku Class

The `Sudoku` class represents a Sudoku puzzle. It initializes an empty Sudoku grid and provides methods to print the Sudoku field and update the numbers in the grid.

### Methods:

- `__init__(self, numbers=9)`: Initializes the Sudoku grid with the specified size (default is 9x9).
- `print(self)`: Prints the current state of the Sudoku grid.
- `write_number(self, position, number)`: Updates the Sudoku grid by writing a number into the specified position.

## SudokuSolver Class

The `SudokuSolver` class utilizes constraint propagation methods, including enforcing node consistency, the AC3 algorithm and Backtrack Search, to solve Sudoku puzzles. It operates on a Sudoku puzzle instance, updating the puzzle's field and domains of empty cells to find a solution. 

### Methods:

- `__init__(self, sudoku)`: Initializes the SudokuSolver object with a Sudoku puzzle instance.
- `solve(self)`: Solves the Sudoku puzzle using constraint propagation techniques.
- `enforce_node_consistency(self)`: Updates self.domains to ensure each cell is node-consistent.
- `update_domains(self, cell, number)`: Fills a cell with a number and updates domains of neighboring cells.
- `print_domains(self)`: Prints the remaining possible values for empty cells.
- `get_neighbors(self, cell)`: Returns a set of coordinate pairs representing the 3x3 grid, horizontal, and vertical neighbors of a given cell.
- `ac3(self, arcs=None)`: Enforces arc consistency on the Sudoku puzzle to solve it.
- `backtrack(self)`: Using Backtrack Search, takes a partial assignment for the Sudoku and returns a complete assignment if possible.
- `read_from_file(self, file: str)`: Reads a Sudoku puzzle from a CSV file and updates the Sudoku field and empty cell domains.

## Usage

To solve a Sudoku puzzle, create a Sudoku object, initialize it with the initial puzzle configuration using the `read_from_file` method, and then create a SudokuSolver object with the Sudoku instance. Finally, call the `solve` method to find the solution.

Example:

```python
sudoku = Sudoku()
solver = SudokuSolver(sudoku)
solver.read_from_file("sudokufield_hellish2.csv")
solver.solve()
print(solver.domains)
sudoku.print()
