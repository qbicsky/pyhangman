import math

import terminal
from colors import Color
from gallows import gallows, possibleErrors


class Canvas:
    """Create Canvas for particular game screen."""
    # Declare attributes, so pylint would not go crazy with dynamicAttributes
    title = str()
    statusBar = str()
    cmdListener = str()
    gameContainer = list(gallows[possibleErrors])
    margin = '  '

    def __init__(self, gameContainer=gameContainer):
        # Set Canvas attributes values in dict, so we can count them later
        self.dynamicAttributes = {
            'title': 'G R A   W   W I S I E L C A  -  P O L S K I E  P R Z Y S Ł O W I A',
            'statusBar': 'Wybierz opcję z menu powyżej.',
            'cmdListener': 'Co chcesz zrobić?'
        }
        self.gameContainer = gameContainer
        # Generate default attributes values based on dictionary
        for attr in self.dynamicAttributes:
            setattr(self, attr, self.dynamicAttributes[attr])
        # Lengths of elements to create proper vertical margins
        self.dynamicAttrLength = len(self.dynamicAttributes)
        self.gameContainerLength = len(self.gameContainer)
        self.canvasLength = self.dynamicAttrLength + self.gameContainerLength

    def print_canvas(self, color=Color.DARKGREY):
        """
        Get all lines of Canvas and print them vertically centered\
        on previously cleared screen.

        Args:
            color (constant, optional): Defaults to Color.DARKGREY.
        """
        terminalHeight = terminal.size('th')
        vMargin = terminalHeight - self.canvasLength
        halfMargin = math.floor(vMargin / 2)
        # Clear terminal
        terminal.clear()
        # Print GUI
        for _ in range(halfMargin):
            print()
        print(self.title)
        self.vertical_separator(halfMargin)
        for line in self.gameContainer:
            print(self.margin + line)
        self.vertical_separator(halfMargin)
        print(color + self.statusBar + Color.END)

    def cmd_listen(self):
        cmd = input(self.cmdListener + ' ').capitalize()
        return cmd

    def session(self, lp: list, rp: list, sb: str):
        pass

    def container(self, leftList, rightList):
        """
        Concatenates container sides (panels) to GUI lines.

        Args:
            leftList (list): left part of container
            rightList (list): right part of container

        Returns:
            (list): List with prepared lines of GUI
        """
        leftListLen = len(leftList)
        rightListLen = len(rightList)
        margin = math.ceil(abs(leftListLen - rightListLen) / 2)
        self.gameContainer = list()
        if(leftListLen >= rightListLen):
            for i in range(margin):
                self.gameContainer.append(leftList[i])
            i = 0
            while i < rightListLen:
                self.gameContainer.append(
                    leftList[margin + i] + '    ' + rightList[i])
                i += 1
            i = rightListLen + margin
            while i < leftListLen:
                self.gameContainer.append(leftList[i])
                i += 1

    @staticmethod
    def vertical_separator(vMargin=0):
        if (vMargin > 0):
            print()
            vMargin = vMargin - 1
