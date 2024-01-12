#
# LEFT = "<"
# RIGHT = ">"
# TOP = "^"
# BOTTOM = "!^"

from dataclasses import dataclass
from typing import Literal, List

@dataclass
class CellREPR:
    """
    Represents a cell in the Futoshiki game matrix.

    Attributes:
        value (int): The numerical value of the cell (default is None).
        LEFT (Literal[True, None]): A flag indicating a constraint on the left side (default is None).
        RIGHT (Literal[True, None]): A flag indicating a constraint on the right side (default is None).
        TOP (Literal[True, None]): A flag indicating a constraint on the top side (default is None).
        BOTTOM (Literal[True, None]): A flag indicating a constraint on the bottom side (default is None).
    """
    value: int = None
    LEFT: Literal[True, None] = None
    RIGHT: Literal[True, None] = None
    TOP: Literal[True, None] = None
    BOTTOM: Literal[True, None] = None

    @property
    def get_row_constraints_if(self):
        """
        Get a list of row constraints associated with the cell.

        Returns:
            List[Literal[True]]: A list containing row constraints (LEFT, RIGHT) that are not None.
        """
        constraints = [constraint for constraint in [self.LEFT, self.RIGHT] if constraint is not None]
        return constraints

    @property
    def get_col_constraints_if(self):
        """
        Get a list of column constraints associated with the cell.

        Returns:
            List[Literal[True]]: A list containing column constraints (TOP, BOTTOM) that are not None.
        """
        constraints = [constraint for constraint in [self.TOP, self.BOTTOM] if constraint is not None]
        return constraints

    def check_constraints_between_cells(self, u_cell, c_cell, c_type): # u_cell-> update cell, c_cell-> constraint_cell, c_type-> check_type

        if c_type == "LEFT":
            pass



class Futoshiki:
    """
    Represents the Futoshiki game.

    Attributes:
        SAMPLE_GAME_MATRIX (List[List[CellREPR]]): A sample game matrix to illustrate the Futoshiki game.
    """
    SAMPLE_GAME_MATRIX = [
        [CellREPR(BOTTOM=True), CellREPR(value=1), CellREPR(), CellREPR()],
        [CellREPR(RIGHT=True), CellREPR(), CellREPR(), CellREPR()],
        [CellREPR(), CellREPR(value=4), CellREPR(RIGHT=True), CellREPR()],
        [CellREPR(TOP=True), CellREPR(), CellREPR(value=4), CellREPR()],
    ]


    game_matrix = SAMPLE_GAME_MATRIX
    
    """
    ▢ 1 ▢ ▢
    ▾ 
    ▢▸▢ ▢ ▢
    
    ▢ 4 ▢▸▢
    ▴ 
    ▢ ▢ 4 ▢ 
    
    """

    def __init__(self, game_matrix=None):
        if game_matrix is not None:
            self.game_matrix = game_matrix
            
        
    def valid_matrix_basic(self):
        """
        Check the basic validity of the Futoshiki game matrix.

        This method verifies basic conditions such as:
        - Each row and column should contain unique numbers.
        - The constraints (LEFT, RIGHT, TOP, BOTTOM) between adjacent cells are satisfied.

        Returns:
            bool: True if the game matrix is valid based on basic conditions, False otherwise.
        """
        pass

    def valid_matrix_deep(self):
        """
        Check the deep validity of the Futoshiki game matrix.

        This method performs a more thorough validation, checking additional conditions such as:
        - Each row and column should contain unique numbers.
        - The constraints (LEFT, RIGHT, TOP, BOTTOM) between adjacent cells are satisfied.
        - Additional game-specific rules are enforced.

        Returns:
            bool: True if the game matrix is valid based on deep conditions, False otherwise.
        """
        pass

    def update_cell_value(self, position, value):
        row, col = position
        # getting nearby cell values
        # left_cell: CellREPR = self.game_matrix[row][col-1] if col-1 >= 0  else None
        # right_cell: CellREPR = self.game_matrix[row][col+1] if col+1 < len(self.game_matrix[row])  else None
        # top_cell: CellREPR = self.game_matrix[row-1][col] if row-1 >= 0  else None
        # bottom_cell: CellREPR = self.game_matrix[row+1][col] if row+1 < len(self.game_matrix)  else None

        """
        Update the game matrix with the provided value, checking for duplicates in the specified row and column.

        Args:
            row (int): The index of the row in the game matrix.
            col (int): The index of the column in the game matrix.
            value: The value to be placed in the specified cell.

        Raises:
            ValueError: If the provided value already exists in the specified row or column.
        """
        # Check if the value already exists in the specified row or column
        # check left cells

        left_cells: List[CellREPR] = self.game_matrix[row][0:col]
        right_cells: List[CellREPR] = self.game_matrix[row][col+1:]
        top_cells: List[CellREPR] = [self.game_matrix[row_no][col] for row_no in range(0, row)]
        bottom_cells: List[CellREPR] = [self.game_matrix[row_no][col] for row_no in range(row+1, len(self.game_matrix))]

        # check left_cells

        curr_cell: CellREPR = self.game_matrix[row][col]

        validation, validation_right,  validation_top = False, False, False

        validation_left = all([ (cell.value!=value) for cell in left_cells] + [(left_cells[-1].value or 4) > value if left_cells[-1].RIGHT else True] if left_cells!=[] else left_cells)

        if validation_left:
            validation_right = all([ (cell.value!=value) for cell in right_cells] + [(right_cells[0].value or 4) > value if right_cells[0].LEFT else True] if right_cells!=[] else right_cells)

        if validation_right:
            validation_top = all([ (cell.value!=value)  for cell in top_cells] + [(top_cells[-1].value or 4) > value if top_cells[-1].BOTTOM else True]if top_cells!=[] else top_cells)

        if validation_top:
            validation = all([ (cell.value!=value) for cell in bottom_cells] + [(bottom_cells[0].value or 4) > value if bottom_cells[0].TOP else True]if bottom_cells!=[] else bottom_cells)


        if validation is not True:
            raise ValueError(f"This number already exists in the specified row or column else constraints problem. {row}{col} and {value}")

        else:
            # If no duplicate is found, update the game matrix with the provided value
            self.game_matrix[row][col].value = value

    def check_is_game_over(self):
        """
        Check if the game is over by examining the values in the game matrix.

        Returns:
            bool: True if the game is over (all cells are filled), False otherwise.
        """
        for row in self.game_matrix:
            for cell_repr in row:
                if cell_repr.value is None:
                    # If any cell has a value of None, the game is not over
                    return False
        # If all cells have values (not None), the game is over
        return True


if __name__ == "__main__":
    
    # my_futoshiki = [
    #         [CellREPR(value=None), CellREPR(value=3, RIGHT=True), CellREPR(value=None), CellREPR(value=1),],
    #         [CellREPR(value=1), CellREPR(value=1), CellREPR(value=1), CellREPR(value=1),],
    #         [CellREPR(value=1), CellREPR(value=1), CellREPR(value=1), CellREPR(value=1),],
    #         [CellREPR(value=1), CellREPR(value=1), CellREPR(value=1), CellREPR(value=1),],
    #     ]

    futoshiki_game = Futoshiki(game_matrix=None)
    # futoshiki_game.update_cell_value(position=[0, 2], value=2)
    futoshiki_game.update_cell_value(position=[0, 0], value=4)
    futoshiki_game.update_cell_value(position=[2, 0], value=1)
    futoshiki_game.update_cell_value(position=[1, 0], value=3)
    futoshiki_game.update_cell_value(position=[3, 0], value=2)
    futoshiki_game.update_cell_value(position=[1, 1], value=2)
    futoshiki_game.update_cell_value(position=[3, 1], value=3)
    futoshiki_game.update_cell_value(position=[3, 3], value=1)
    futoshiki_game.update_cell_value(position=[2, 2], value=3)
    futoshiki_game.update_cell_value(position=[2, 3], value=2)
    futoshiki_game.update_cell_value(position=[1, 2], value=1)
    futoshiki_game.update_cell_value(position=[1, 3], value=4)
    futoshiki_game.update_cell_value(position=[0, 2], value=2)
    futoshiki_game.update_cell_value(position=[0, 3], value=3)

    # futoshiki_game.update_cell_value(position=[row, col], value=value)
    while not futoshiki_game.check_is_game_over():
        cell_update_inputs = input("Please enter cell value and its position in the format-> row, col, value")
        row, col, value = [int(item) for item in cell_update_inputs.split(",")]
        try:
            futoshiki_game.update_cell_value(position=[row, col], value=value)
        except Exception as e:
            print(f"Error: {str(e)}")
            # raise
    assert  futoshiki_game.check_is_game_over()


# Please enter cell value and its position in the format-> row, col, value0, 0, 4
# Please enter cell value and its position in the format-> row, col, value2, 0, 1
# Please enter cell value and its position in the format-> row, col, value1, 0, 3
# Please enter cell value and its position in the format-> row, col, value3, 0, 2
# Please enter cell value and its position in the format-> row, col, value1, 1, 2
# Please enter cell value and its position in the format-> row, col, value3, 1, 3
# Please enter cell value and its position in the format-> row, col, value3, 3, 1
# Please enter cell value and its position in the format-> row, col, value2, 2, 3
# Please enter cell value and its position in the format-> row, col, value2, 3, 2
# Please enter cell value and its position in the format-> row, col, value1, 2, 1
# Please enter cell value and its position in the format-> row, col, value1, 3, 4










