import math



def gen_container(leftList, rightList):
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
    margin = math.ceil(abs(leftListLen - rightListLen)/2)
    gameContainer = list()
    if(leftListLen >= rightListLen):
        for i in range(margin):
            gameContainer.append(leftList[i])
        i = 0
        while i < rightListLen:
            gameContainer.append(leftList[margin + i] + '    ' + rightList[i])
            i += 1
        i = rightListLen + margin
        while i < leftListLen:
            gameContainer.append(leftList[i])
            i += 1
    return gameContainer
