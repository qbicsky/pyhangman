from enum import Enum, IntEnum



mainMenu = {
    'G' : 'Rozpocznij grę',
    'R' : 'Ranking TOP 5',
    'X' : 'Zakończ'
}

Main_Menu = Enum('Main_Menu',
    {mainMenu[key].replace(' ', '_') : key for key in mainMenu})

contextMenu = {
    ' ' : 'Wróć do Menu',
    '' : 'Zagraj ponownie',
    'Z' : 'Sprawdź znaczenie przysłowia',
    'Reset' : 'Wyzeruj ranking'
}

Context_Menu = Enum('Context_Menu',
    {contextMenu[key].replace(' ', '_') : key for key in contextMenu})

difficultyLevels = {
    1 : 'Normalny',
    2 : 'Trudny',
    3 : 'Ekstremalny',
    4 : 'Szaleńczy'
}

Difficulty_Levels = IntEnum('Difficulty_Levels',
    {difficultyLevels[key].replace(' ', '_') : key for key in difficultyLevels})

difficultyDesc = {
    1 : 'Standardowa wersja rozgrywki.',
    2 : 'Standardowa wersja rozgrywki, ale bez historii wybieranych liter.',
    3 : 'Poprawnie wskazana litera ujawnia tylko jedno jej wystąpienie.',
    4 : 'Ekstremalna wersja rozgrywki, dodatkowo bez historii wybieranych liter.'
}
difficultyMenu = {
    key : difficultyLevels[key] + '. ' + difficultyDesc[key]
    for key in difficultyLevels
}
difficultiesCheck = {
    str(key)
    for key in difficultyLevels
}

def gen_menu(menuDictionary):
    menu = [
        '[' + str(key) + ']:' + menuDictionary[key]
        for key in menuDictionary
    ]
    return menu
