import random

class Minesweeper(object):
    ''' Minesweeper class - Plays Minesweeper.

        It provides methods that carry out most of the needed functionality. It has the following
          data structures:
        horiz_size/vert_size: Integer. The board is a square horiz_size x vert_size grid. Default value 5.
        mines: Integer. The board contains this many bombs, randomly placed at start of game.
            Default value 3.
        board: A list of vert_size lists, each horiz_size items long. This represents
            the current game state. Possible list contents:
                'M': This cell contains a mine (bomb).
                0-8: An integer, giving the number of mines in this cell's neighborhood.
        hidden_board: A list of lists, the same size as board, containing the
            board as it will be displayed to the player. Possible contents:
                'H': This cell is hidden and can be turned over.
                0-8: This cell has this many mines in its neighborhood.
              'X': Used if the player loses, this shows the location of a mine.
        GameState: Has 3 possible states: "w", "l", "p", 'q'  (These are strings)

    '''

    def __init__(self, horiz_size = 5, vert_size = 5, mines = 3):
        '''
              Initializer. Sets up boards, places mines (via call to method), counts
                 bombs in neighborhod for each bomb (via call to another method).
                 In: Size of one side of grid, number of mines to be placed.
                 Returns: Nothing
                 Interaction with user: None.
                 Modifications to data structures: ActualBoard is set up, mines placed, counts
                    updated. PlayerBoard set to all H. GameState set to "playing"
                 Errors handled: If SideSize <= 2, a value of 2 is used. If SideSize > 15, a value of
                    15 is used. If Mines is greater than the number of cells in the grid, every cell
                    is given a bomb and any excess is ignored. (It's going to be a pretty short game, though.)
                    If Mines < 0, a value of 0 is used.
        '''
        self.horiz_size = horiz_size
        self.vert_size = vert_size
        self.fields = horiz_size * vert_size
        self.mines = mines
        self.uncovered_fields = self.mines

        self.board = list()
        self.hidden_board = list()
        for i in range(self.vert_size):
            self.board.append([0 for num in range(self.horiz_size)])
            self.hidden_board.append(["H" for num in range(self.horiz_size)])

        self.placeMines()

    def placeMines(self):
        '''
              Puts mines onto ActualBoard.
              In: None.
              Returns: None.
              Interaction with user: None.
              Modifications to data structures: Reads self.Size and self.Mines to handle
                setup. Randomly selects location for self.Mines mines to be placed. Calls
                self.get_Counts() to finish setting up ActualBoard.
              Errors handled: None (input was screened in __init__()).  Note that this method
			  must make sure that each mine is placed in a separate cell; that is, if a mine
			  is about to be placed in a cell that already has a mine in it, another cell
			  should be picked instead.
        '''
        self.mine_locs = set()
        while len(self.mine_locs) < self.mines:
            self.mine_locs.add(random.randint(0,self.fields))

        for loc in self.mine_locs:
            row, column = self.__cell_abstract__(loc)
            self.board[row][column] = -1
            self.get_Counts(loc)

        return None

    def get_Counts(self, cell_num):
        '''
              For each cell in grid, counts mines in area, updates ActualBoard.
              In: None.
              Returns: None.
              Interaction with user: None.
              Modifications to data structures: Each cell in ActualBoard that does not have a mine
                is filled with an integer (0 to self.Mines) specifying how many cells in that cell's
                neighborhood are mined. Algorithm:
                  All non-mined cells initialized to 0
                  For each mined cell (r,c):
                    for r-1 to r+1, c-1 to c+1:  Note: need to be sure not running off edge of grid
                       exclude mined cell, otherwise Increment that cell's count by 1
              Errors handled: None.
        '''

        neighbors = self.__find_Neighbors__(cell_num)
        for neighbor in neighbors:
            row, col = self.__cell_abstract__(neighbor)
            if self.val(neighbor) != -1:
                self.board[row][col] += 1

    def get_Input(self):
        '''
              Handles input from user. Prompts user to enter row col of cell to check next.
              In: None.
              Returns: tuple (r, c) of next cell to be uncovered
              Interaction with user: Prompts user for input of row & column. (NOTE: User prompt
                    and input expects 1 to self.Size. Value returned ranges from 0 to self.Size-1 (0-based
                    rather than 1-based indexing).) Gets input from keyboard. Prompts as necessary
                    until valid data is obtained.
              Modifications to data structures: None.
              Errors handled:
                  Input not numeric: Prints error message, tries again.
                  Input is numeric but cell is off grid: Prints error message, tries again.
                  Input is numeric, on grid, already uncovered: Ignored (display board, return to input)
             TODO: Add feature allowing user to enter something showing game should be ended
                early (i.e. a 'Quit' option).
        '''

        cell_num = input("Enter a cell number; 1 - {} or 'q' to quit: ".format(self.fields))

        try:
            cell_num = int(cell_num)
        except ValueError:
            if cell_num in ('q', 'quit', 'exit', 'stop'):
                return 'q'

            print("Please enter a number: '1' not 'one'")
            return 'p'
        else:
            if not (1 <= cell_num <= (self.fields)):
                print("Please enter a number from 1 - {}".format(self.fields))
                return None
            else:
                self.game_state = self.update_Cell(cell_num)

            if self.game_state == 'l':
                print("Kabloom!!")
                print("You've hit a mine...")
                print(self.display_Board("System"))
                return 'l'
            elif self.game_state == 'w':
                print("Yay, you won!")
                print("Next, try it with a bigger board or more mines!")
                print(self.display_Board("System"))
                return 'w'
            else:
                return 'p'


    def update_Cell(self,cell_num):
        '''
          Updates cell on PlayerBoard. If mine is uncovered, sets GameState to "loss".
            In: row & column of cell (assumed to have been checked by getInput() for validity).
            Returns:  None.
            Interaction with user: None.
            Modifications to data structures:
                 If cell in ActualBoard contains a nonzero int, that cell in PlayerBoard is set to that value.
                 If cell is blank (contains 0), calls rippleEffect(r, c). After rippleEffect() returns, if
                   covered cells == number of mines, player has won. (GameState set to "win")
            Errors handled:  None.
        '''

        if cell_num in self.mine_locs:
            return 'l'

        else:
            row, col = self.__cell_abstract__(cell_num)
            cell_val = self.val(cell_num)

            if cell_val == 0:
                self.ripple_Effect(cell_num)
            else:
                self.hidden_board[row][col] = cell_val

            self.uncovered_fields += 1

            if self.uncovered_fields == self.fields:
                return 'w'

    def display_Board(self, display_board):
        '''
          Displays board onscreen. Used with parameter because we may want to display either
            ActualBoard or PlayerBoard, depending on situation.
                In:  Board to be displayed.
                Returns:  None.
                Interaction with user:  Board is printed to screen, with row & column labels (starting at 1, not 0).
                Modifications to data structures:  None.
                Errors handled:  None.
        '''

        text = ""

        if display_board in ("Player", "Both"):
            cell_count = 0
            for row in range(self.vert_size):
                text += "{:>5}: ".format(cell_count)
                for col in range(self.horiz_size):
                    if self.hidden_board[row][col] != -1:
                        text += "{:^3}".format(self.hidden_board[row][col])
                    else:
                        text += " M "
                text += "\n"
                cell_count += self.horiz_size
            text += "\n"

        if display_board in ("System", "Both"):
            cell_count = 0
            for row in range(self.vert_size):
                text += "{:>5}: ".format(cell_count)
                for col in range(self.horiz_size):
                    if self.board[row][col] != -1:
                        text += "{:^3}".format(self.board[row][col])
                    else:
                        text += " M "
                text += "\n"
                cell_count += self.horiz_size
            text += "\n"

        return text

    def ripple_Effect(self, cell_num):
        '''
            Handles clearing adjacent sections of board from empty cell.
                In:  row & column of cell that was cleared.
                Returns: None.
                Interaction with user: None.
                Modifications to data structures:  Verifies that cell is cleared (0 in ActualBoard).
				If so, clears adjacent cells as well. The required version clears all cells in the row and
				column specified; the extra-credit version clears all appropriate neighboring cells.
                Errors handled: None.
        '''
        row, col =  self.__cell_abstract__(cell_num)
        if self.hidden_board[row][col] != "H":
            return None

        self.hidden_board[row][col] = self.val(cell_num)

        ripples = [cell for cell in self.__find_Neighbors__(cell_num) if self.val(cell) != -1]
        for cell in ripples:
            if self.val(cell) > 0:
                t_row, t_col = self.__cell_abstract__(cell)
                self.hidden_board[t_row][t_col] = self.val(cell)
            else:
                self.ripple_Effect(cell)
        return None

    def __find_Neighbors__(self, cell_num):
        '''
        In: Cell to find neighbors of.
        Returns: List of tuples (r,c) that are adjacent to the input cell and not off the grid.
        Interaction with user: None.
        Modifications to data structures: None.
        Errors handled: None. Assumes arguments received are valid coordinates (or are at least integers.)
            If integers but off the grid, then only neighboring cells that would be on the grid are returned
            (e.g. if (-1, -1) were received, (0,0) would be included in returned data. Argument of (-5, -5)
            would return empty list.)
        '''

        row, col = self.__cell_abstract__(cell_num)

        neighbors = list()

        neighbors.append(self.__coord_valid__([row - 1, col - 1]))
        neighbors.append(self.__coord_valid__([row - 1, col]))
        neighbors.append(self.__coord_valid__([row - 1, col + 1]))
        neighbors.append(self.__coord_valid__([row, col - 1]))
        neighbors.append(self.__coord_valid__([row, col + 1]))
        neighbors.append(self.__coord_valid__([row + 1, col - 1]))
        neighbors.append(self.__coord_valid__([row + 1, col]))
        neighbors.append(self.__coord_valid__([row + 1, col + 1]))

        return (((buddy[0] * self.horiz_size) + buddy[1]) + 1 for buddy in neighbors if buddy is not None)

    def __coord_valid__(self, coord):
        return_val = coord
        row, col = coord

        if row < 0 or row > (self.vert_size - 1):
            return_val = None
        elif col < 0 or col > (self.horiz_size - 1):
            return_val = None

        return return_val

    def __str__(self):
        return self.display_Board("Player")

    def __repr__(self):
        print(self.display_Board("Both"))
        return ""

    def __cell_abstract__(self, cell_num):
        ''' Requires 1 >= cell_num <= self.fields '''
        cell_num -= 1
        num_mod = (cell_num % self.horiz_size)

        if cell_num != 0:
            # if num_mod != 0:
            row = cell_num // self.horiz_size
            column = num_mod
        else:
            row = 0
            column = 0


        return (row, column)

    def val(self, cell_num):
        row, col = self.__cell_abstract__(cell_num)
        return self.board[row][col]
