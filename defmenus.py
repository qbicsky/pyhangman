import terminal
from menu import Menu, MenuItem

MAIN_MENU = Menu([
    MenuItem('G', 'Rozpocznij grę'),
    MenuItem('R', 'Ranking TOP 5'),
    MenuItem('X', 'Zakończ')
], 'Main Menu')

DIFFICULTY_MENU = Menu([
    MenuItem(1, 'Normalny',
             'Standardowa wersja rozgrywki.'),
    MenuItem(2, 'Trudny',
             'Standardowa wersja rozgrywki, ale bez historii wybieranych liter.'),
    MenuItem(3, 'Ekstremalny',
             'Poprawnie wskazana litera ujawnia tylko jedno jej wystąpienie.'),
    MenuItem(4, 'Szaleńczy',
             'Ekstremalna wersja rozgrywki, dodatkowo bez historii wybieranych liter.')
], 'Difficulty Menu')

RANKING_MENU = Menu([
    MenuItem(' ', 'Wróć do Menu'),
    MenuItem('Reset', 'Wyzeruj ranking'),
    MenuItem('G', 'Rozpocznij grę'),
    MenuItem('X', 'Zakończ')
], 'Ranking Menu')

GAMEOVER_MENU = Menu([
    MenuItem('', 'Zagraj ponownie', alt_key=terminal.return_key()),
    MenuItem('G', 'Zmień gracza'),
    MenuItem('Z', 'Sprawdź znaczenie przysłowia'),
    MenuItem('R', 'Ranking'),
    MenuItem(' ', 'Wróć do Menu'),
    MenuItem('X', 'Zakończ')
], 'Gameover Menu')

OFFLINE_MENU = Menu([
    MenuItem('G', 'Spróbuj ponownie'),
    MenuItem('R', 'Ranking TOP 5'),
    MenuItem(' ', 'Wróć do Menu'),
    MenuItem('X', 'Zakończ')
], 'Offline Menu')
