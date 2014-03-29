# Module to play the Game of Life

import random, itertools

class InputError(ValueError):
    pass

class LifeStill(Exception):
    pass

class TooManyLiveCells(Exception):
    pass

class Life(object):
    def __init__(self, mode = "Random", horiz_size = 5, vert_size = 5, num_live_cells = 5):
        try:
            self.mode = "Random" if mode != "StillLife" else "StillLife"
            self.horiz_size = abs(int(horiz_size)) if horiz_size != "" else 5
            self.vert_size = abs(int(vert_size)) if vert_size != "" else 5
            self.fields = self.horiz_size * self.vert_size
    
            self.num_live_cells = abs(int(num_live_cells)) if num_live_cells != "" else 5
            if self.num_live_cells > self.fields:
                print("\nMore live cells ({}) than space on the board ({}).".format(self.num_live_cells, self.fields))
                raise TooManyLiveCells()
        except ValueError:
            print("\nInvalid input.")
            print("Enter a number. For example: '1' instead of 'one'")
            raise InputError()

        if self.mode == "Random":
            self.__create_grid__()
        elif self.mode == "StillLife":
            # Now the main program needs to run Life.still_life()
            pass

    def __calculate_neighbors__(self, orig_cell):
        neighbors = list()

        row = orig_cell // self.horiz_size # (loc // self.horiz_size) gives the row

            # Readability, FTW
            # I technically now only do this calculation once instead of having to do it twice and compare, so yay!
        above_left =  orig_cell - self.horiz_size - 1
        above =       orig_cell - self.horiz_size
        above_right = orig_cell - self.horiz_size + 1
        left =        orig_cell - 1
        right =       orig_cell + 1
        below_left =  orig_cell + self.horiz_size - 1
        below =       orig_cell + self.horiz_size
        below_right = orig_cell + self.horiz_size + 1

            # Basically, if you're on the board and on the correct row you should be, you pass, else die.
            # If you're above*, then your row should be one less than orig_cell's row, same row if left/right
            # and one more if below*.
        neighbors.append(above_left if above_left // self.horiz_size == row - 1 else None) # Above left
        neighbors.append(above if above // self.horiz_size == row - 1 else None) # Above
        neighbors.append(above_right if above_right // self.horiz_size == row - 1 else None) # Above right
        neighbors.append(left if left // self.horiz_size == row else None) # Left
        neighbors.append(right if right // self.horiz_size == row else None) # Right
        neighbors.append(below_left if below_left // self.horiz_size == row + 1 else None) # Below left
        neighbors.append(below if below // self.horiz_size == row + 1 else None) # Below
        neighbors.append(below_right if below_right // self.horiz_size == row + 1 else None) # Below right

        # Whew! Ugly!

            # Count the live neighbors
        num_live_neighbors = 0
        for neighbor in neighbors:
            if neighbor in self.live_cell_locs:
                num_live_neighbors += 1
        return num_live_neighbors

    def __change_cell_state__(self, cell):
        cell_vals = self.grid[cell]
        if (cell_vals[0] == 1 and cell_vals[1] in (2,3)) or (cell_vals == [0,3]): # Living numbers
            self.grid[cell] = [1,0] # Liven, or keep alive; will recount later, so 0 doesn't matter
            self.live_cell_locs.add(cell)
        elif cell_vals[1] < 2 or cell_vals[1] > 3: # Dying numbers
            self.grid[cell] = [0,0] # Kill
            self.live_cell_locs.discard(cell) # Remove from live_cell_locs

    def __create_grid__(self, live_cell_locs = ()):
                #self.grid: dict(); Key: cell number, sequential; Value: list containing status (dead(0)/alive(1)) and number of living neighbors (used for next round)
                # self.grid = dict.fromkeys(range(self.fields),[0,0]) # Fast, but same object for all keys...
            self.grid = {num:[0,0] for num in range(self.fields)} # ~3 times slower than above, but unique copy of list for each key (probably why slower...)
            self.__place_cells__(live_cell_locs)

    def __place_cells__(self, live_cell_locs = ()):
        self.live_cell_locs = set(live_cell_locs)

        if len(live_cell_locs) == 0:
            while len(self.live_cell_locs) < self.num_live_cells:
                loc = random.randint(1,self.fields) - 1
                self.live_cell_locs.add(loc)
                self.grid[loc] = [1,0]
        else:
            for loc in live_cell_locs:
                self.grid[loc] = [1,0]
        self.count_neighbors()

    def __repr__(self):
        self.__str__()
        print("\nGrid:", self.grid)
        print("\nHorizontal Size:", self.horiz_size)
        print("\nVertical Size:", self.vert_size)
        print("\nNumber of fields:", self.fields)
        print("\nLocation of live cells:", self.live_cell_locs)
        print("\nStarting number of live cells:", self.num_live_cells)

        return str()

    def __str__(self):
        print("")
        for line in self.display_grid():
            print(line)
        return str()

    def count_neighbors(self):
        for cell in self.grid:
            num_live_neighbors = self.__calculate_neighbors__(cell)
            self.grid[cell][1] = num_live_neighbors

    def display_grid(self):
        row = 0

        header = "Column:  "
        for i in range(self.horiz_size):
            header += "{:^3} ".format(i+1)
        yield header
        
        for i in range(self.vert_size):
            text = "Row {:>3}: ".format(row+1)
            col = 0
            for i in range(self.horiz_size):
                display_val = "-" if self.grid[row * self.horiz_size + col][0] == 0 else "*"
                text += "{:^3} ".format(display_val)
                col += 1
            row += 1
            yield text

    def next_round(self):
        prev_round_cell_locs = self.live_cell_locs.copy()
        
        for cell in self.grid:
            self.__change_cell_state__(cell)
        self.count_neighbors()

        if prev_round_cell_locs == self.live_cell_locs:
            raise LifeStill("Life has stopped. No more changes will occur.")
        elif len(self.live_cell_locs) == 0:
            return False
        else:
            return True

    def still_life(self):
        if self.mode == "StillLife":
            for combo in itertools.combinations(range(self.fields), self.num_live_cells):
                self.__create_grid__(live_cell_locs=combo)
                try:
                    self.next_round()
                except LifeStill:
                    yield True
                else:
                    yield False
        else:
            return None
