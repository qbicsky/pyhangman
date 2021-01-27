import terminal
import menus

from generators import gen_container
from gallows import gallows, possibleErrors
from wikiconnector import wiki_proverb_info

from colors import Color
from canvas import Canvas
from game import Game
from ranking import Rank, Ranking


cmd = str()
game = Game()

while True:
    if(cmd == menus.Main_Menu.Zakończ.value):
        terminal.clear()
        quit()

    elif(cmd == menus.Main_Menu.Rozpocznij_grę.value):
        gc = gen_container(gallows[possibleErrors], [])
        identifyPlayer = Canvas(gc)
        identifyPlayer.statusBar = (
            'Wpisz swoje imię lub pseudonim.'
            + 'Ta nazwa będzie używana do wpisania Twojego wyniku do rankingu.')
        identifyPlayer.cmdListener = 'Przedstaw się:'
        identifyPlayer.print_canvas()
        cmd = identifyPlayer.cmd_listen()

        player = cmd.upper()
        cmd = 'chooseDifficulty'
        terminal.clear()

    elif(cmd == menus.Main_Menu.Ranking_TOP_5.value):
        while True:
            gc = gen_container(gallows[possibleErrors], Ranking().show())
            showRanking = Canvas(gc)
            showRanking.statusBar = '[ ]:Menu  [G]:Graj  [Wpisz "Reset"]:Wyzeruj ranking  [X]:Zakończ'
            showRanking.cmdListener = Canvas().cmdListener
            showRanking.print_canvas()
            cmd = showRanking.cmd_listen()

            if(cmd == menus.Context_Menu.Wróć_do_Menu.value
                    or cmd == menus.Main_Menu.Rozpocznij_grę.value
                    or cmd == menus.Main_Menu.Zakończ.value):
                break
            elif(cmd == menus.Context_Menu.Wyzeruj_ranking.value):
                Ranking().reset()

    elif(cmd == 'chooseDifficulty'):
        while True:
            gc = gen_container(gallows[possibleErrors],
                               menus.gen_menu(menus.difficultyMenu))
            chooseDifficulty = Canvas(gc)
            chooseDifficulty.statusBar = (
                'Wybrany poziom trudności będzie miał wpływ na ilość zdobytych punktów.')
            chooseDifficulty.cmdListener = 'Wybierz poziom trudności:'
            chooseDifficulty.print_canvas()
            cmd = chooseDifficulty.cmd_listen()

            difficulty = cmd
            difficultyAmount = len(menus.difficultyMenu)

            if(difficulty.isdigit()):
                difficulty = int(difficulty)
                if(0 <= difficulty <= difficultyAmount):
                    cmd = 'gameReady'
                    game.reset()
                    game.player = player
                    game.difficulty = difficulty
                    break

    elif(cmd == 'gameReady'):
        # The game
        gc = gen_container(gallows[possibleErrors], [])
        drawingEntry = Canvas(gc)
        drawingEntry.statusBar = (
            'Łączenie do bazy Wiktionary w celu wylosowania przysłowia...')
        drawingEntry.print_canvas()

        game.draw_an_entry()

        if(game.drawnEntry is None):
            drawingEntry.statusBar = (
                "Brak odpowiedzi z Wiktionary. Sprawdź połączenie do Internetu.")
            drawingEntry.cmdListener = (
                "[G]:Spróbuj ponownie  [R]:Ranking  [ ]:Wróć do Menu  [X]:Zakończ")
            drawingEntry.print_canvas()
            cmd = drawingEntry.cmd_listen()

        else:
            while True:
                gc = gen_container(gallows[game.errors], [game.hiddenEntry])

                genericStatusBar = (
                    'Grasz jako ' + game.player + ' w trybie '
                    + menus.difficultyLevels[game.difficulty].lower() + 'm. ')
                endGameStatusBar = (
                    Color.END + '[Z]' + Color.DARKGREY
                    + ':Sprawdź znaczenie przysłowia  ' + Color.END + '[R]'
                    + Color.DARKGREY + ':Ranking  ' + Color.END + '['
                    + terminal.return_key() + ']' + Color.DARKGREY
                    + ':Zagraj ponownie  ' + Color.END + '[G]'
                    + Color.DARKGREY + ':Zmień gracza  ' + Color.END + '[ ]'
                    + Color.DARKGREY + ':Wróć do Menu  ' + Color.END + '[X]'
                    + Color.DARKGREY + ':Zakończ \nlub wybierz inny poziom: '
                    + Color.END + '[1]' + Color.DARKGREY + ':Normalny, '
                    + Color.END + '[2]' + Color.DARKGREY + ':Trudny, '
                    + Color.END + '[3]' + Color.DARKGREY + ':Ekstremalny, '
                    + Color.END + '[4]' + Color.DARKGREY + ':Szaleńczy.')
                gameCanvas = Canvas(gc)
                # Lost game
                if(game.errors == possibleErrors):
                    rank = Rank(game.player, game.difficulty, game.errors)

                    gc = gen_container(gallows[game.errors], [Color.RED
                                       + game.drawnEntry + Color.END])
                    gameCanvas = Canvas(gc)
                    gameCanvas.statusBar = (genericStatusBar
                                            + 'Niestety, przegrywasz!\n'
                                            + endGameStatusBar)
                    gameCanvas.cmdListener = Canvas().cmdListener
                    gameCanvas.print_canvas()
                    cmd = gameCanvas.cmd_listen()
                # Won game
                elif(game.errors < possibleErrors
                        and game.hiddenEntry == game.drawnEntry):

                    rank = Rank(game.player, game.difficulty, game.errors)

                    declinationLastChar = int(str(rank.points)[-1])
                    if(rank.points > 10):
                        declinationSecondLastChar = int(str(rank.points)[-2])
                    else:
                        declinationSecondLastChar = None
                    if(rank.points == 1):
                        pointsStr = ' punkt'
                    elif(1 < declinationLastChar < 5
                            and declinationSecondLastChar != 1):
                        pointsStr = ' punkty'
                    else:
                        pointsStr = ' punktów'

                    gc = gen_container(gallows[game.errors], [Color.GREEN
                                       + game.drawnEntry + Color.END])
                    gameCanvas = Canvas(gc)
                    gameCanvas.statusBar = (
                        genericStatusBar + 'Wygrywasz! W tej grze zdobywasz '
                        + str(rank.points)
                        + pointsStr + '! Gratulacje!!!\n' + endGameStatusBar)
                    gameCanvas.cmdListener = Canvas().cmdListener
                    gameCanvas.print_canvas()
                    cmd = gameCanvas.cmd_listen()

                else:
                    if(game.difficulty == menus.Difficulty_Levels.Normalny
                            or game.difficulty == menus.Difficulty_Levels.Ekstremalny):

                        gameCanvas.statusBar = (
                            genericStatusBar
                            + 'Użyte litery '
                            + str(game.letterHistory))

                    elif(game.difficulty == menus.Difficulty_Levels.Trudny
                            or game.difficulty == menus.Difficulty_Levels.Szaleńczy):

                        gameCanvas.statusBar = (
                            genericStatusBar
                            + 'Wybrany poziom trudności nie ujawnia historii użytych liter...')

                    gameCanvas.cmdListener = 'Wybierz literę:'
                    gameCanvas.print_canvas()
                    cmd = gameCanvas.cmd_listen()

                    game.check_letter(cmd)
                    game.letterHistory.sort()
                    cmd = None
                # Final actions
                if(game.hiddenEntry == game.drawnEntry
                        or game.errors == possibleErrors):
                    if(cmd == menus.Context_Menu.Zagraj_ponownie.value):
                        cmd = game.reset(game.difficulty)
                        break
                    elif(cmd in menus.difficultiesCheck):
                        cmd = game.reset(int(cmd))
                        break
                    elif(cmd == menus.Context_Menu.Sprawdź_znaczenie_przysłowia.value):
                        wiki_proverb_info(game.proverb)
                    elif(cmd):
                        break
    else:
        gc = gen_container(gallows[possibleErrors],
                           menus.gen_menu(menus.mainMenu))
        mainMenu = Canvas(gc)
        mainMenu.print_canvas()
        cmd = mainMenu.cmd_listen()
