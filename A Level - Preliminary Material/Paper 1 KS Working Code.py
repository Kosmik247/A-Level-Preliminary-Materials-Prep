#Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9.4 programming environment

import random
import os

def Main():
    """
    The main function that runs the puzzle game.

    Parameters
    ----------
    None

    Returns
    -------
    None"""
    Again = "y"
    Score = 0
    while Again == "y":
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        Score = MyPuzzle.AttemptPuzzle()
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()

class Puzzle():
    def __init__(self, *args):
        """
        Initialises the variables for the puzzle instance
        Parameters
        ----------
        Args: Either a text file name (string) or a set of integers to generate puzzle

        Returns
        -------
        None
        """

        if len(args) == 1:
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            Q1Pattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(Q1Pattern)
            Q2Pattern = Pattern("Q", "*QQQ**Q*Q")
            self.__AllowedPatterns.append(Q2Pattern)
            Q3Pattern = Pattern("Q", "Q**QQQ**Q")
            self.__AllowedPatterns.append(Q3Pattern)
            Q4Pattern = Pattern("Q", "**Q**QQQQ")
            self.__AllowedPatterns.append(Q4Pattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            T1Pattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(T1Pattern)
            T2Pattern = Pattern("T", "**TTT**TT")
            self.__AllowedPatterns.append(T2Pattern)
            T3Pattern = Pattern("T", "*T**TTT*T")
            self.__AllowedPatterns.append(T3Pattern)
            T4Pattern = Pattern("T", "T**T**TTT")
            self.__AllowedPatterns.append(T4Pattern)
            self.__AllowedSymbols.append("T")
            L1Pattern = Pattern("L", "L***LLLL*")
            self.__AllowedPatterns.append(L1Pattern)
            L2Pattern = Pattern("L", "LLL***LL*")
            self.__AllowedPatterns.append(L2Pattern)
            L3Pattern = Pattern("L", "LLLLL****")
            self.__AllowedPatterns.append(L3Pattern)
            L4Pattern = Pattern("L", "**LLLLL**")
            self.__AllowedPatterns.append(L4Pattern)
            self.__AllowedSymbols.append("L")
            self.__AllowedSymbols.append("B")
    def __LoadPuzzle(self, Filename):
        """
        Loads a txt puzzle file from saved files
        Parameters
        ----------
        Filename: A string

        Returns
        -------
        None
        """
        #try:
        with open(Filename) as f:
            # First integer value is the number of symbols followed by the symbols
            NoOfSymbols = int(f.readline().rstrip())
            for Count in range (1, NoOfSymbols + 1):
                self.__AllowedSymbols.append(f.readline().rstrip())
            # Second integer value is the number of patterns followed by the patterns
            NoOfPatterns = int(f.readline().rstrip())
            for Count in range(1, NoOfPatterns + 1):
                Items = f.readline().rstrip().split(",")
                P = Pattern(Items[0], Items[1])
                self.__AllowedPatterns.append(P)
            self.__GridSize = int(f.readline().rstrip())
            # Second letter is the blocked letter. Hardcoded it in
            for Count in range (1, self.__GridSize * self.__GridSize + 1):
                Items = f.readline().rstrip().split(",")
                if Items[0] == "@":
                    C = BlockedCell()
                    self.__Grid.append(C)
                else:
                    C = Cell()
                    C.ChangeSymbolInCell(Items[0])
                    for CurrentSymbol in range(1, len(Items)):
                        C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                    self.__Grid.append(C)
            self.__Score = int(f.readline().rstrip())
            self.__SymbolsLeft = int(f.readline().rstrip())
        #except:
            #print("Puzzle not loaded")
    def __SavePuzzle(self):
        with open("current_game.txt","w") as save_game_file:
            save_game_file.write(str(len(self.__AllowedSymbols))+"\n")
            for symbol in self.__AllowedSymbols:
                save_game_file.write(symbol+"\n")
            save_game_file.write(str(len(self.__AllowedPatterns)) + "\n")
            for pattern in self.__AllowedPatterns:
                save_game_file.write(pattern.GetSymbol() + ","+pattern.GetPatternSequence()+"\n")
            save_game_file.write(str(self.__GridSize)+"\n")
            for cell in self.__Grid:
                if cell.GetSymbol() == "-":
                    save_game_file.write("" + "," + ','.join(cell.GetSymbolsNotAllowed()) + "\n")
                else:
                    save_game_file.write(cell.GetSymbol() + "," + ','.join(cell.GetSymbolsNotAllowed()) + "\n")

            save_game_file.write(str(self.__Score) + "\n")
            save_game_file.write(str(self.__SymbolsLeft) + "\n")

    def AttemptPuzzle(self):
        """
        Function run while user is solving puzzle, returns score
        Parameters
        ----------
        None

        Returns
        -------
        Score: A class attribute (integer)
        """
        Finished = False
        while not Finished:
            self.__SavePuzzle()
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
            Row = -1
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass
            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            CurrentCell = self.__GetCell(Row, Column)

            if CurrentCell.CheckSymbolAllowed(Symbol) and Symbol != "B":
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore
            elif Symbol == "B" and type(CurrentCell) == BlockedCell:
                self.__Score -= 2
                Position = self.__GridSize + Column - 1 * (self.__GridSize - Row)
                self.__Grid[Position] = Cell()
            elif Symbol == "B" and type(CurrentCell) == Cell:
                print("That cell is not a blocked cell and does not need to be destroyed.")
            print("Would you like to revert the move just made? Y/N")
            revert = input("WARNING: You will lose 3 points: \n")

            if revert.upper() == "Y":
                self.__Score = 0
                self.__SymbolsLeft = 0
                self.__GridSize = 0
                self.__Grid = []
                self.__AllowedPatterns = []
                self.__AllowedSymbols = []
                self.__LoadPuzzle("current_game.txt")
                self.__Score -= 3
            if self.__SymbolsLeft == 0:
                Finished = True
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
        """
        Loads a txt puzzle file from saved files
        Parameters
        ----------
        Row: Integer coordinate
        Column: Integer coordinate

        Returns
        -------
        Grid: Class attribute -> returns the specific cell at the index grid
        """
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()

    def CheckforMatchWithPattern(self, Row, Column):
        """
        Checks if the letters in grid match any scoring pattern
        Parameters
        ----------
        Row: Integer coordinate
        Column: Integer coordinate

        Returns
        -------
        10 -> If a match
        0 -> Not a match

        """
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except:
                    pass
        return 0

    def __GetSymbolFromUser(self):
        """
        Gets input symbol from user
        Parameters
        ----------
        None

        Returns
        -------
        Symbol: (string) user input
        """
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):
        """
        Creates a horizontal line
        Parameters
        ----------
        None

        Returns
        -------
        Line: The horizontal line (string)
        """
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
        """
        Displays the puzzle to the user

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())

class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        """
        Pattern class init function
        Parameters
        ----------
        SymbolToUse: (string)
        PatternString: (string)

        Returns
        -------
        None
        """
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString
    def GetSymbol(self):
        return self.__Symbol
    def MatchesPattern(self, PatternString, SymbolPlaced):
        """
        Matches the pattern stored to the scoring patterns
        Parameters
        ----------
        SymbolToUse: (string)
        PatternString: (string)

        Returns
        -------
        False: If pattern doesn't match it
        True: If pattern matches
        """
        if SymbolPlaced != self.__Symbol:
            return False
        for Count in range(0, len(self.__PatternSequence)):
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def GetPatternSequence(self):
        """
        A function to access the self.__Pattern sequence
        Parameters
        ----------
        None

        Returns
        -------
        PatternSequence: The pattern sequence
        """
        return self.__PatternSequence

class Cell():
    def __init__(self):
        """
        Init function for cell class
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._Symbol = ""
        self.__SymbolsNotAllowed = []
    def GetSymbolsNotAllowed(self):
        if len(self.__SymbolsNotAllowed) == 0:
            return ""
        else:
            return self.__SymbolsNotAllowed[0]
    def GetSymbol(self):
        """
        Function to get the symbol of the current class instance
        Parameters
        ----------
        None

        Returns
        -------
        Symbol: Current symbol if not empty
        "-": If empty
        """
        if self.IsEmpty():
          return "-"
        else:
          return self._Symbol
    
    def IsEmpty(self):
        """
        Checks if cell is empty
        Parameters
        ----------
        None

        Returns
        -------
        True: If empty
        False: If not empty
        """
        if len(self._Symbol) == 0:
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        """
        Change the symbol stored in the cell
        Parameters
        ----------
        NewSymbol: Input symbol (string)

        Returns
        -------
        None
        """
        if self.IsEmpty():
            self._Symbol = NewSymbol


    def CheckSymbolAllowed(self, SymbolToCheck):
        """
        Checks if symbol is allowed from the list of symbols not allowed
        Parameters
        ----------
        SymbolToCheck: (string) input symbol

        Returns
        -------
        True: If item is not in SymbolsNotAllowed
        False: If item is in SymbolsNotAllowed
        """
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        """
        Adds symbol to not allowed symbols
        Parameters
        ----------
        SymbolToAdd: (string)

        Returns
        -------
        None
        """
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        """
        Updates Cell
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        pass

class BlockedCell(Cell):
    def __init__(self):
        """
        Init function of Blocked Cell
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        """
        Checks if symbal is allowed
        Parameters
        ----------
        SymbolToCheck: (string) Input symbol to check

        Returns
        -------
        False:
        """
        return False

if __name__ == "__main__":
    Main()