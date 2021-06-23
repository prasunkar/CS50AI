import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly throughout the field
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # No mines are found at the beginning
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """
        # Keep count of all nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself, we're focusing on nearby mines
                if (i, j) == cell:
                    continue

                # Update the count if a cell is a mine and is inbound
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells if self.count == len(self.cells) else set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

    def infer_from(self, other):
        """
        Returns an inferred sentence from this and another given sentence.
        If it can't make any inferences, it returns None.
        """
        if other.cells.issubset(self.cells):
            return Sentence(self.cells - other.cells, self.count - other.count)
        
        elif self.cells.issubset(other.cells):
            return Sentence(other.cells - self.cells, other.count - self.count)
        
        else:
            return None


class MinesweeperAI():
    """
    Minesweeper game player
    """
    
    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Steps 1 and 2
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Step 3
        new_sentence = Sentence(self.get_neighbours(cell), count)

        for mine in self.mines:
            new_sentence.mark_mine(mine)
        for safe in self.safes:
            new_sentence.mark_safe(safe)

        # Add this new sentence to the knowledge base
        self.knowledge.append(new_sentence)

        # Step 4
        mines, safes = set(), set()

        for sentence in self.knowledge:
            for cell in sentence.known_mines():
                mines.add(cell)
            for cell in sentence.known_safes():
                safes.add(cell)

        for cell in mines:
            self.mark_mine(cell)
        for cell in safes:
            self.mark_safe(cell)

        # Step 5
        additional_sentences = []

        for a, b in itertools.combinations(self.knowledge, 2):
            infer = a.infer_from(b)
            
            if infer is not None and infer not in self.knowledge:
                additional_sentences.append(infer)

        self.knowledge.extend(additional_sentences)

        # Clean up the knowledge base of empty sentences
        for sentence in self.knowledge:
            if sentence == Sentence(set(), 0):
                self.knowledge.remove(sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        remaining_moves = self.safes - self.moves_made
        return random.choice(tuple(remaining_moves)) if remaining_moves else None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        remaining_moves = set(itertools.product(range(0, self.height), range(0, self.width)))
        remaining_moves = remaining_moves - self.mines - self.moves_made

        return random.choice(tuple(remaining_moves)) if remaining_moves else None

    def get_neighbours(self, cell):
        """
        Returns a set containing all neighbours of a given cell.
        """
        neighbours = set()

        # Loop over all surrounding cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself, as we're looking for its neighbours
                if (i, j) == cell:
                    continue

                # Add the cell as a neighbour if it's inbound
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours.add((i, j))

        return neighbours