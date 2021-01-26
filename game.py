import random
# Custom imports
from wikiconnector import wiki_get_proverbs
from menus import Difficulty_Levels


class Game:
    """
    Creates game session.
    """
    def __init__(self, player='Gal Anonim', difficulty=1):
        self.player = player
        self.difficulty = difficulty
        self.errors = 0
        self.wikiData = wiki_get_proverbs()
        self.proverb = str()
        self.drawnEntry = str()
        self.hiddenEntry = str()
        self.letterHistory = list()
        self.entryList = list()


    def draw_an_entry(self):
        """
        Build proverbs database by connecting to Wiki API.
        Then draw an entry and create hidden entry.

        Returns:
            drawnEntry (str): Visible entry for the game in uppercase.
            hiddenEntry (str): Hidden entry for the game,
                               hashed with underscores.
            proverb(str): Raw drawn proverb.
        """
        if(self.wikiData is None):
            self.wikiData = wiki_get_proverbs()
        if(self.wikiData is not None):
            self.proverb = random.choice(self.wikiData)
            self.drawnEntry = self.proverb.upper()
            self.hiddenEntry = list(self.drawnEntry)
            i = 0
            while i < len(self.drawnEntry):
                if (self.drawnEntry[i].isalpha()):
                    self.hiddenEntry[i] = '_'
                i += 1
            self.hiddenEntry = ''.join(self.hiddenEntry)
        else:
            self.drawnEntry = None
            self.hiddenEntry = None
        return self.drawnEntry, self.hiddenEntry, self.proverb


    def check_letter(self, letter):
        """
        Check inputted letter against drawnEntry. If it is found in the
        entry, then replace its corresponding underscore in hiddenEntry.
        Breaks on hard difficulties after first occurance.

        Args:
            letter (char): Letter to check against the Entry.
        """
        if(not self.entryList):
            self.entryList = list(self.drawnEntry)
        self.hiddenEntry = list(self.hiddenEntry)
        if(letter not in self.letterHistory):
            self.letterHistory.append(letter)
        i = 0
        isError = True
        if(letter.isalpha()):
            for char in self.entryList:
                if(letter == char):
                    self.hiddenEntry[i] = letter
                    self.entryList[i] = ' '
                    isError = False
                    if(self.difficulty == Difficulty_Levels.Ekstremalny or
                            self.difficulty == Difficulty_Levels.Szaleńczy):
                        break
                i += 1
        if(isError):
            self.errors += 1
        self.hiddenEntry = ''.join(self.hiddenEntry)


    def reset(self, difficulty=1):
        """
        Reset the game with defined difficulty.

        Args:
            difficulty (int, optional): Defaults to 1.

        Returns:
            (str): Sends the 'gameReady' signal to game's cmd.
        """
        self.errors = 0
        self.letterHistory = []
        self.entryList = []
        self.difficulty = difficulty
        cmd = 'gameReady'
        return cmd
