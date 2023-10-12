"""
This code explores machine learning algorithms to solve sudoku puzzles. 
The sudoku is taken as a constraint satisfaction problem and AC3 
(Arc Consistency Algorithm #3) is applied to solve it.
"""

import copy
import pandas as pd
import random

class Sudoku():
    """
    Sudoku representation
    """

    def __init__(self, numbers=9):
        # Set size of sudoku field
        self.height = numbers
        self.width = numbers
        # use argument unpacking operator * to generate list with numbers from 1 to numbers
        self.numbers = [*range(1, numbers + 1)]

        # Initialize empty field and save set of field coordinates
        self.field_coordinates = set()
        self.field = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(" ")
                self.field_coordinates.add((i,j))
            self.field.append(row)

    def print(self):
        """
        Print text based representation of Sudoku field.
        """
        for i in range(self.height):
            print("")
            if i % 3 == 0:
                print("----" * 9)

            for j in range(0, self.width, 3):
                print(f"| {self.field[j][i]} | {self.field[j+1][i]} | {self.field[j+2][i]} |", end="")
        print("")
        print("----" * 9)

    def write_number(self, position, number):
        """
        updates the sudoku field by writing number into field position.
        Removes coordinate pair from available coordinate set.
        """
        i, j = position
        self.field[i][j] = number
        # self.field_coordinates.remove((i,j))



class SudokuSolver():
    """
    SudokuSolver represents a Sudoku puzzle solver using constraint satisfaction techniques.
    
    This class utilizes constraint propagation methods, including enforcing node consistency 
    and AC3 (Arc-Consistency 3) algorithm, to solve Sudoku puzzles. It operates on a Sudoku 
    puzzle instance, updating the puzzle's field and domains of empty cells to find a solution.
    
    Attributes:
        sudoku (Sudoku): The Sudoku puzzle instance to be solved.
        domains (dict): A dictionary mapping cell coordinates (i, j) to sets of possible 
                        numbers that can be placed in the corresponding cell.

    Methods:
        __init__(self, sudoku):
            Initializes the SudokuSolver object with a Sudoku puzzle instance.
        
        solve(self):
            Solves the Sudoku puzzle using constraint propagation techniques.
        
        enforce_node_consistency(self):
            Updates self.domains, ensuring each cell is node-consistent.
        
        update_domains(self, cell, number):
            Fills a cell with a number and updates domains of neighboring cells.
        
        print_domains(self):
            Prints the remaining possible values for empty cells.
        
        get_neighbors(self, cell):
            Returns a set of coordinate pairs representing the 3x3 grid, horizontal, 
            and vertical neighbors of a given cell.
        
        ac3(self, arcs=None):
            Enforces arc consistency on the Sudoku puzzle to solve it.
        
        read_from_file(self, file: str):
            Reads a Sudoku puzzle from a CSV file and updates the Sudoku field and 
            empty cell domains.
    """

    def __init__(self, sudoku):
        """
        Initializes the SudokuSolver object with a Sudoku puzzle instance.
        
        Args:
        sudoku (Sudoku): The Sudoku puzzle instance to be solved.
        """
        self.sudoku = sudoku
        self.domains = {
            coordinates: self.sudoku.numbers.copy()
            for coordinates in self.sudoku.field_coordinates
        }


    def solve(self):
        """ Employ solving algorithms"""
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack()

    def enforce_node_consistency(self):
        """
        update self.domains such that each cell is node-consistent
        (if number is set, remove other numbers from domains)
        """
        for cell in self.sudoku.field_coordinates:
            #print(cell)
            #print(f"is {self.sudoku.field[cell[0]][cell[1]]} in {self.sudoku.numbers}?")
            if self.sudoku.field[cell[0]][cell[1]] in self.sudoku.numbers:
                self.domains[cell] = self.sudoku.field[cell[0]][cell[1]]
                self.update_domains(cell, self.sudoku.field[cell[0]][cell[1]])

    def update_domains(self,cell, number):
        """
        Fill field (i,j) with number and then update domains of neighboring cells.
        Args:
        cell (tuple): Coordinates (i, j) of the cell to be updated.
        number (int): Number to be placed in the cell.
        """
        print("updating domains")
        self.sudoku.field[cell[0]][cell[1]] = number
        self.domains.pop(cell)
        ########### PRINT sudoku field after each update step
        self.sudoku.print()
        ##########
        # neighbors of 3x3 grid in which cell is, vertical and horizontal neighbors
        for coordinates in self.get_neighbors(cell):
            #print(f"checking coordinates {coordinates} for cell {cell}")
            if (coordinates[0], coordinates[1]) in self.domains:
                if number in self.domains[(coordinates[0], coordinates[1])]:
                    self.domains[coordinates].remove(number)

    def print_domains(self):
        """
        Prints the fields that have not been filled yet and prints their possible values.
        """
        print("Domains for missing values:")
        for cell in sorted(self.domains):
            print(f"{cell}: {self.domains[cell]}")

    def get_neighbors(self, cell):
        """ 
        Returns a set of coordinate pairs that represent the 3x3 grid a given cell is located in, 
        and the horizontal and vertical neighbors.
        """
        vertical = self.get_neighbors_vertical(cell)
        horizontal = self.get_neighbors_horizontal(cell)
        grid = self.get_neighbors_grid(cell).union(horizontal).union(vertical)
        return grid

    def get_neighbors_grid(self, cell):
        """ Returns the 3x3 grid of neighbors in which cell is"""
        if cell[0] in [0,1,2]:
            col_range = [0,1,2]
        elif cell[0] in [3,4,5]:
            col_range = [3,4,5]
        elif cell[0] in [6,7,8]:
            col_range = [6,7,8]

        if cell[1] in [0,1,2]:
            row_range = [0,1,2]
        elif cell[1] in [3,4,5]:
            row_range = [3,4,5]
        elif cell[1] in [6,7,8]:
            row_range = [6,7,8]

        grid = set()
        for col in col_range:
            for row in row_range:
                if (col,row) != cell:
                    grid.add((col,row))
        # print(grid)
        return grid

    def get_neighbors_horizontal(self, cell):
        """ Returns the horizontal line of neighbors of 'cell' that don't have a value assigned"""
        grid = set()
        # horizontal line
        for i in range(0, self.sudoku.height):
            if (i, cell[1]) == cell:
                continue
            #print(f"cell: {(i,cell[1])}, domain: {self.domains[(i,cell[1])]}")
            if (i, cell[1]) in self.domains:
                grid.add((i, cell[1]))
        return grid

    def get_neighbors_vertical(self, cell):
        """ Returns the vertical line of neighbors of 'cell' that don't have a value assigned"""
        grid = set()
        # vertical line
        for i in range(0, self.sudoku.width):
            if (cell[0], i) == cell:
                continue
            if (cell[0], i) in self.domains:
                grid.add((cell[0],i))
        return grid


    def revise(self, cell):
        """
        Make cell arc consistent with the other cells in it's 3x3 grid and horizontal
        and vertical neighbors. To do so, remove values from self.domains[cell] for which
        there is no possible corresponding value in its neighbors' self.domains.

        Return True if a revision was made to the domain of the cell, return False if no 
        revision was made.

        Revision is split into several steps: 
        1. Check if the domain of the cell already only consists one number, in which case
            the domains should be updated immediately.
        2.-4. Make cell arc consistent with vertical, horizontal and grid neighbors.
        5.+6. Make cell arc consistent by combining either row or column knowledge with
            grid knowledge.        
        """
        revised = False
        # check if number is already known, i.e. domain is of length 1
        if len(self.domains[cell]) == 1:
            self.update_domains(cell, self.domains[(cell[0],cell[1])][0])
            revised = True
            return revised

        # revise each set of neighbors separately
        if self.revise_neighbors(cell, self.get_neighbors_vertical(cell)):
            revised = True
            return revised
        if self.revise_neighbors(cell, self.get_neighbors_horizontal(cell)):
            revised = True
            return revised
        if self.revise_neighbors(cell, self.get_neighbors_grid(cell)):
            revised = True
            return revised

        # combine knowledge of 3x3 grid with row/column knowledge
        if self.combine_row_grid_knowledge(cell,
                self.get_neighbors_grid(cell),
                self.get_neighbors_horizontal(cell)
                ):
            revised = True
            return revised
        if self.combine_row_grid_knowledge(cell,
                self.get_neighbors_grid(cell),
                self.get_neighbors_vertical(cell)
                ):
            revised = True
            return revised

        return revised

    def revise_neighbors(self, cell, get_neighbors):
        """
        Make cell arc consistent with the other cells in it's 3x3 grid, horizontal
        or vertical neighbors. To do so, remove values from self.domains[cell] for which
        there is no possible corresponding value in its neighbors' self.domains.

        Return True if a revision was made to the domain of the cell, return False if no 
        revision was made.
        """
        revised = False
        if cell not in self.domains:
            return revised
        # check if there is corresponding values for cell's possible numbers
        for possible_number in self.domains[cell]:
            # deepcopy domains to explore possible changes
            possible_domains = copy.deepcopy(self.domains)
            possible_domains.pop(cell)
            # store if the number remains a possible number
            impossible = False
            neighbors = set()
            for neighbor in get_neighbors:
                if neighbor in possible_domains:
                    neighbors.add(neighbor)

            # check if cell is the only one among its neighbors that can take possible value
            only_cell_w_value = True
            for neighbor in neighbors:
                if possible_number in possible_domains[neighbor]:
                    only_cell_w_value = False
            if only_cell_w_value:
                self.update_domains(cell, possible_number)
                revised = True
                return revised

            for neighbor in neighbors:
                # only look at neighbors that don't have a value assigned yet
                # and remove possible_number from their domain
                if neighbor in possible_domains:
                    try:
                        possible_domains[neighbor].remove(possible_number)
                    except ValueError:
                        continue

            # check if values for other cells can be inferred
            # as long as a cell has just one value in the domains check for
            # additional knowledge and alter possible_domains
            while any(len(possible_domains[neighbor]) == 1 for neighbor in neighbors):
                if impossible:
                    break
                for neighbor in neighbors:
                    # check if any cell doesn't have any possible values 
                    if any(len(possible_domains[neighbor]) == 0 for neighbor in neighbors):
                        impossible = True
                        break
                    if len(possible_domains[neighbor]) == 1:
                        # remove number from other neighbors domain
                        for neighbor_2 in neighbors:
                            if neighbor != neighbor_2:
                                try:
                                    possible_domains[neighbor_2].remove(possible_domains[neighbor][0])
                                except ValueError:
                                    continue
                        # remove neighbor from domain
                        possible_domains[neighbor].append("removed")

            if impossible:
                print("impossible number")
                self.domains[cell].remove(possible_number)
                revised = True

        return revised

    def combine_row_grid_knowledge(self, cell, grid, row_neighbors):
        """
        Infer knowledge from the combination of grid information coupled with
        row or column information. 
        If a number is missing in a grid and from current knowledge it can only 
        be placed in cells in the same row or column, this function infers that 
        cells in the other parts of the row or column cannot take that number. 
        Thus, it is removed from their domains.
        To be clear, if row or column neighbors are used depends on the input
        'row_neighbors' and either row or column neighbors are used.
        """
        revised = False
        # only take grid neighbors into account that dont have a value assigned yet
        grid_neighbors = set()
        for grid_neighbor in grid:
            if grid_neighbor in self.domains:
                grid_neighbors.add(grid_neighbor)
        # Find neighbors in grid of cell that are in the same row / column
        cells = set()
        cells.add(cell)
        for neighbor in grid_neighbors:
            if neighbor in grid_neighbors and neighbor in row_neighbors:
                cells.add(neighbor)
        # check if there is a number that is in all cells that are free and in one line in
        # the same grid
        for possible_number in self.domains[cell]:
            for other_cell in cells:
                if not possible_number in self.domains[other_cell]:
                    break
                # check if number is in domain of other cells in grid,
                # if not remove number from cells that are in row but not in grid
                is_in_grid = False
                for grid_cell in grid_neighbors:
                    if grid_cell in cells:
                        continue
                    if possible_number in self.domains[grid_cell]:
                        is_in_grid = True

                if not is_in_grid:
                    for row_cell in row_neighbors:
                        if row_cell in cells:
                            continue
                        try:
                            self.domains[row_cell].remove(possible_number)
                            revised = True
                        except KeyError:
                            continue
                        except ValueError:
                            continue
        return revised


    def ac3(self, arcs=None):
        """
        Update self.domains such that each cell is arc consistent. 
        If arcs is None, beginn with initial list of all arcs in the problem.

        Return True if arc consistency is enforced and no domains are empty; 
        Return False if one or more domains end up empty.
        """
        # load queue
        if arcs is None:
            arcs = set()
            for cell in self.domains:
                arcs.add(cell)
        queue = arcs

        while queue:
            # print(f"queue elements (sorted): {sorted(queue)}")
            # print current sudoku field and possibilities for empty cells
            self.sudoku.print()
            self.print_domains()
            # pick random cell from queue and revise
            cell = queue.pop()
            if cell in self.domains:
                if self.revise(cell):
                    # check if cell is still in self.domains
                    if cell in self.domains:
                        # check if domain is empty
                        for neighbor in self.get_neighbors(cell):
                            if neighbor in self.domains:
                                if len(self.domains[neighbor]) == 0:
                                    return False

                    # add neighbors of cell to queue
                    for neighbor in self.get_neighbors(cell):
                        if neighbor in self.domains:
                            queue.add(neighbor)
        return True

    def assignment_complete(self, assignment):
        """
        Return True if 'assignment' is complete, i.e., all cells of the Sudoku field
        are assigned a number; return False otherwise.
        """
        # check if all fields contain a number
        for i in range(self.sudoku.height):
            for j in range(self.sudoku.width):
                if not str(assignment[i][j]).isnumeric():
                    return False
        return True

    def consistent(self, assignment):
        """
        Return True if 'assignment' is consistent, i.e., no conflicts of numbers
        is apparent and no self.domains[cell] is empty
        """
        for i in range(self.sudoku.height):
            for j in range(self.sudoku.width):
                if str(assignment[i][j]).isnumeric():
                    print(i, j)
                    print(assignment)
                    for neighbor in self.get_neighbors((i, j)):
                        if assignment[i][j] == assignment[neighbor[0]][neighbor[1]]:
                            return False

        for cell in self.domains:
            if len(self.domains[cell]) == 0:
                return False
        return True

    def select_unassigned_cell(self):
        """
        Return an unassigned cell. The cell with the least possible numbers 
        available will be chosen. If there is a tie, a random cell from the 
        tied cells is returned instead. 
        """
        fewest = []
        mark = 10000
        for cell in self.domains:
            # check for lowest number of possible numbers for cell
            if len(self.domains[cell]) < mark:
                fewest = []
                fewest.append(cell)
                mark = len(self.domains[cell])
            elif len(self.domains[cell]) == mark:
                fewest.append(cell)

        # check if successful
        if len(fewest) == 0:
            print("Error in select_unassigned_cell")
            return 1

        # return random cell with fewest possibilites
        return random.choice(fewest)

    def backtrack(self):
        """
        Using Backtracking Seach, take as input a partial assignment for the 
        Sudoku and return a complete assignment if possible to do so. 

        `assignment` is a mapping from cell positions (keys) to numbers (values).

        If no assignment is possible, return None.


        function Backtrack(assignment, csp):
            if assignment complete:
                return assignment
            var = Select-Unassigned-Var(assignment, csp)
            for value in Domain-Values(var, assignment, csp):
                if value consistent with assignment:
                    add {var = value} to assignment
                    # ac3
                   # inferences = Inference(assignment, csp)
                   # if inferences ≠ failure:
                   #     add inferences to assignment
                    result = Backtrack(assignment, csp)
                    if result ≠ failure:
                        return result
                    remove {var = value} and inferences from assignment
            return failure
        """
        # create backups
        domains_backup = copy.deepcopy(self.domains)
        field_backup = copy.deepcopy(self.sudoku.field)

        # fill assignment with known values
        #for cell in self.domains:
        #    if len(self.domains[cell]) == 1:
        #        self.update_domains(cell, self.domains[cell])
        #assignment = self.sudoku.field

        # check if assignment complete
        if self.assignment_complete(self.sudoku.field):
            return self.sudoku.field

        cell = self.select_unassigned_cell()
        for pos_value in self.domains[cell]:
            self.update_domains(cell, pos_value)

            if self.consistent(self.sudoku.field):
                arcs = self.get_neighbors(cell)
                consistency_enforced = self.ac3(arcs)
                # add inferences
                if consistency_enforced:
                    for other_cell in self.domains:
                        if len(self.domains[other_cell]) == 1:
                            self.update_domains(cell, self.domains[cell])
                result = self.backtrack()
                if result is not None:
                    return result

                self.domains = domains_backup
                self.sudoku.field = field_backup
                self.domains[cell].remove(pos_value)
        return None



    def read_from_file(self, file: str):
        """
        Reads a Sudoku game from a CSV file and 
        updates the Sudoku field and the domains of empty fields.

        Args:
        file (str): Path to the CSV file containing the Sudoku puzzle.

        At the moment sudoku must be initialized first and then has preset size, 
        consider changes to allow the size to be read from the file too.
        """
        read_sudoku = pd.read_csv(file, header=None)
        if read_sudoku.size == self.sudoku.height * self.sudoku.width:
            for i in range(self.sudoku.height):
                for j in range(self.sudoku.width):
                    if read_sudoku[i][j] in self.sudoku.numbers:
                        self.sudoku.write_number((i,j), int(read_sudoku[i][j]))
                        self.update_domains((i,j), int(read_sudoku[i][j]))

def main():
    sudoku = Sudoku()
    solver = SudokuSolver(sudoku)
    solver.read_from_file("sudokufield_hellish2.csv")
    sudoku.print()
    solver.solve()
    print(solver.domains)
    sudoku.print()


if __name__ == "__main__":
    main()
