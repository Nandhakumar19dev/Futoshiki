

from PyQt5 import QtWidgets, uic, QtGui

import sys
from functools import partial
from typing import List

#
RIGHT   =  "〉" #"▷"
BOTTOM  =  "﹀" #"▼" #"▽"
LEFT    =  "〈" #"◁"
TOP     =  "︿" #"△"

class CellREPR:

    def __init__(self, *args, **kwargs):

        self.line_edit: QtWidgets.QLineEdit = kwargs.get("line_edit")
        self.LEFT: QtWidgets.QLabel         = kwargs.get("LEFT")
        self.RIGHT: QtWidgets.QLabel        = kwargs.get("RIGHT")
        self.TOP: QtWidgets.QLabel          = kwargs.get("TOP")
        self.BOTTOM: QtWidgets.QLabel       = kwargs.get("BOTTOM")
        func  = kwargs.get("func")


        self.line_edit.cell_repr = self
        self.line_edit.value = None
        self.line_edit.textEdited.connect(partial(func, self.line_edit))
        self.line_edit.setStyleSheet("background-color: #EAF0F3; color: blue;")


    def cell_init_attrs(self, attr_tuples):
        for attr_tpl in attr_tuples:
            obj_str, value = attr_tpl
            obj = getattr(self, obj_str)

            obj.setText(str(value))

            if isinstance(obj, QtWidgets.QLineEdit):
                obj.value = value
            else:
                obj.value = True
            obj.setEnabled(False)
            obj.setStyleSheet("color: blue;")

    def add_row_n_col_repr(self, row, col):
        self.row = row
        self.col = col

class Ui(QtWidgets.QMainWindow):
    def __init__(self, board_repr, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi("futoshili-board.ui", self)

        func = self.update_cell_value
        self.line_edits = {
            # Row 1
            (0, 0):CellREPR(line_edit=self.lineEdit_02, RIGHT=self.label, BOTTOM=self.label_13, TOP=None, LEFT=None, func=self.update_cell_value),
            (0, 2):CellREPR(line_edit=self.lineEdit_03, RIGHT=self.label_2, BOTTOM=self.label_14, TOP=None, LEFT=self.label, func=func),
            (0, 4):CellREPR(line_edit=self.lineEdit_04, RIGHT=self.label_3, BOTTOM=self.label_15, TOP=None, LEFT=self.label_2, func=func),
            (0, 6):CellREPR(line_edit=self.lineEdit_05, RIGHT=None, BOTTOM=self.label_16, TOP=None, LEFT=self.label_3, func=func),

            # Row 2
            (2, 0):CellREPR(line_edit=self.lineEdit_06, RIGHT=self.label_4, BOTTOM=self.label_17, TOP=self.label_13, LEFT=None, func=func),
            (2, 2):CellREPR(line_edit=self.lineEdit_07, RIGHT=self.label_5, BOTTOM=self.label_18, TOP=self.label_14, LEFT=self.label_4, func=func),
            (2, 4):CellREPR(line_edit=self.lineEdit_08, RIGHT=self.label_6, BOTTOM=self.label_19, TOP=self.label_15, LEFT=self.label_5, func=func),
            (2, 6):CellREPR(line_edit=self.lineEdit_09, RIGHT=None, BOTTOM=self.label_20, TOP=self.label_16, LEFT=self.label_6, func=func),

            # Row 3
            (4, 0):CellREPR(line_edit=self.lineEdit_10, RIGHT=self.label_7, BOTTOM=self.label_21, TOP=self.label_17, LEFT=None, func=func),
            (4, 2):CellREPR(line_edit=self.lineEdit_11, RIGHT=self.label_8, BOTTOM=self.label_22, TOP=self.label_18, LEFT=self.label_7, func=func),
            (4, 4):CellREPR(line_edit=self.lineEdit_12, RIGHT=self.label_9, BOTTOM=self.label_23, TOP=self.label_19, LEFT=self.label_8, func=func),
            (4, 6):CellREPR(line_edit=self.lineEdit_13, RIGHT=None, BOTTOM=self.label_24, TOP=self.label_20, LEFT=self.label_9, func=func),

            # Row 4
            (6, 0):CellREPR(line_edit=self.lineEdit_14, RIGHT=self.label_10, BOTTOM=None, TOP=self.label_21, LEFT=None, func=func),
            (6, 2):CellREPR(line_edit=self.lineEdit_15, RIGHT=self.label_11, BOTTOM=None, TOP=self.label_22, LEFT=self.label_10, func=func),
            (6, 4):CellREPR(line_edit=self.lineEdit_16, RIGHT=self.label_12, BOTTOM=None, TOP=self.label_23, LEFT=self.label_11, func=func),
            (6, 6):CellREPR(line_edit=self.lineEdit_17, RIGHT=None, BOTTOM=None, TOP=self.label_24, LEFT=self.label_12, func=func),

        }

        for key, value in self.line_edits.items():
            row, col = key
            value.add_row_n_col_repr(row, col)

        for key ,value in board_repr.items():
            self.line_edits[key].cell_init_attrs(value)

        # cell_11 = CellREPR(line_edit=self.)

        self.show()


    def update_cell_value(self, lineEdit):
        row, col = lineEdit.cell_repr.row, lineEdit.cell_repr.col
        if lineEdit.text() == '':
            lineEdit.setStyleSheet("background-color: #EAF0F3;")
            return

        value = int(lineEdit.text())


        left_cells: List[CellREPR] = [self.line_edits[(row,_col)] for _col in range(0, col, 2)]#self.game_matrix[row][0:col]
        right_cells: List[CellREPR] = [self.line_edits[(row,_col)] for _col in range(col+2, 7, 2)] #self.game_matrix[row][col + 1:]
        top_cells: List[CellREPR] = [self.line_edits[(_row, col)] for _row in range(0, row, 2)]
        bottom_cells: List[CellREPR] = [self.line_edits[(_row,col)] for _row in range(row+2, 7, 2)]


        curr_cell: CellREPR = self.line_edits[(row, col)]

        validation, validation_right, validation_top = False, False, False

        validation_left = all([(cell.line_edit.value != value) for cell in left_cells] + [
            (left_cells[-1].line_edit.value or 4) > value if left_cells[
                -1].RIGHT.text()==RIGHT else True] if left_cells != [] else left_cells)

        if validation_left:
            validation_right = all([(cell.line_edit.value != value) for cell in right_cells] + [
                (right_cells[0].line_edit.value or 4) > value if right_cells[
                    0].LEFT.text() == LEFT else True] if right_cells != [] else right_cells)

        if validation_right:
            validation_top = all([(cell.line_edit.value != value) for cell in top_cells] + [
                (top_cells[-1].line_edit.value or 4) > value if top_cells[
                    -1].BOTTOM.text() == BOTTOM else True] if top_cells != [] else top_cells)

        if validation_top:
            validation = all([(cell.line_edit.value != value) for cell in bottom_cells] + [
                (bottom_cells[0].line_edit.value or 4) > value if bottom_cells[
                    0].TOP.text() == TOP else True] if bottom_cells != [] else bottom_cells)

        curr_cell.line_edit.value = value
        curr_cell.line_edit.setText(str(value))
        curr_cell.line_edit.setStyleSheet("background-color: #EAF0F3;")

        if validation is not True:
            curr_cell.line_edit.setStyleSheet("background-color: red;")

        else:
            self.check_is_game_over()


    def check_is_game_over(self):
        """

        Check if the game is over by examining the values in the game matrix.

        Returns:
            bool: True if the game is over (all cells are filled), False otherwise.
        """
        for key, cell_repr in self.line_edits.items():

            if cell_repr.line_edit.value is None:
                # If any cell has a value of None, the game is not over
                return False
        # If all cells have values (not None), the game is over

        self.show_info_messagebox()

    def show_info_messagebox(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        # setting message for Message Box
        msg.setText(f"Yes, you completed the game. Play next one...")

        # setting Message box window title
        msg.setWindowTitle("Game Over")

        # declaring buttons on Message Box
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        # start the app
        retval = msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    """
    ▢ 1 ▢ ▢
    ▾ 
    ▢▸▢ ▢ ▢

    ▢ 4 ▢▸▢
    ▴ 
    ▢ ▢ 4 ▢ 

    """

    board_repr = {
        (0, 0):[("BOTTOM", BOTTOM)],
        (0, 2):[("line_edit", 1)],
        (2, 0):[("RIGHT", RIGHT)],
        (4, 2):[("line_edit", 4)],
        (4, 4):[("RIGHT", RIGHT)],
        (6, 0):[("TOP", TOP)],
        (6, 4):[("line_edit", 4)] }
    
    window = Ui(board_repr=board_repr)
    app.exec_()
    


