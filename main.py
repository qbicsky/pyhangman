import terminal
from defmenus import (MAIN_MENU,
                      DIFFICULTY_MENU,
                      RANKING_MENU,
                      OFFLINE_MENU,
                      GAMEOVER_MENU)

from gallows import gallows, possibleErrors
from wikiconnector import wiki_proverb_info

from colors import Color
from canvas import Canvas
from game import Game
from ranking import Rank, Ranking

cmd = str()
player = str()
game = Game()

while True:
    if(cmd == MAIN_MENU.key_by_label('Zakończ')):
        terminal.clear()
        quit()

    elif(cmd == MAIN_MENU.key_by_label('Rozpocznij grę')):
        identifyPlayer = Canvas()
        identifyPlayer.container(gallows[possibleErrors], [])
        identifyPlayer.statusBar = (
            'Wpisz swoje imię lub pseudonim.'
            + 'Ta nazwa będzie używana do wpisania Twojego wyniku do rankingu.')
        identifyPlayer.cmdListener = 'Przedstaw się:'
        identifyPlayer.print_canvas()
        cmd = identifyPlayer.cmd_listen()

        player = cmd.upper()
        cmd = 'chooseDifficulty'
        terminal.clear()

    elif(cmd == MAIN_MENU.key_by_label('Ranking TOP 5')):
        while True:
            showRanking = Canvas()
            showRanking.container(gallows[possibleErrors], Ranking().show())
            showRanking.statusBar = str(RANKING_MENU.build_list('horizontal'))
            showRanking.cmdListener = Canvas().cmdListener
            showRanking.print_canvas()
            cmd = showRanking.cmd_listen()

            if(cmd == RANKING_MENU.key_by_label('Wróć do Menu')
                    or cmd == RANKING_MENU.key_by_label('Rozpocznij grę')
                    or cmd == RANKING_MENU.key_by_label('Zakończ')):
                break
            elif(cmd == RANKING_MENU.key_by_label('Wyzeruj ranking')):
                Ranking().reset()

    elif(cmd == 'chooseDifficulty'):
        while True:
            chooseDifficulty = Canvas()
            chooseDifficulty.container(gallows[possibleErrors],
                                       DIFFICULTY_MENU.build_list(descr=True))
            chooseDifficulty.statusBar = (
                'Wybrany poziom trudności będzie miał wpływ na ilość zdobytych punktów.')
            chooseDifficulty.cmdListener = 'Wybierz poziom trudności:'
            chooseDifficulty.print_canvas()
            cmd = chooseDifficulty.cmd_listen()

            difficulty = cmd
            difficultyAmount = len(DIFFICULTY_MENU)

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
        drawingEntry = Canvas()
        drawingEntry.container(gallows[possibleErrors], [])
        drawingEntry.statusBar = (
            'Łączenie do bazy Wiktionary w celu wylosowania przysłowia...')
        drawingEntry.print_canvas()

        game.draw_an_entry()

        if(game.drawnEntry == str()):
            drawingEntry.statusBar = (
                "Brak odpowiedzi z Wiktionary. Sprawdź połączenie do Internetu.")
            drawingEntry.cmdListener = str(
                OFFLINE_MENU.build_list('horizontal'))
            drawingEntry.print_canvas()
            cmd = drawingEntry.cmd_listen()
        else:
            while True:
                genericStatusBar = (
                    'Grasz jako ' + game.player + ' w trybie '
                    + DIFFICULTY_MENU.label_by_key(game.difficulty).lower() + 'm. ')
                endGameStatusBar = (
                    str(GAMEOVER_MENU.build_list('horizontal', alt=True))
                    + '\n' + Color.DARKGREY + 'lub wybierz inny poziom trudności: '
                    + str(DIFFICULTY_MENU.build_list('horizontal'))
                )
                gameCanvas = Canvas()
                gameCanvas.container(gallows[game.errors], [game.hiddenEntry])
                # Lost game
                if(game.errors == possibleErrors):
                    rank = Rank(game.player, game.difficulty, game.errors)

                    gameCanvas = Canvas()
                    gameCanvas.container(gallows[game.errors],
                                         [Color.RED + game.drawnEntry + Color.END])
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

                    gameCanvas = Canvas()
                    gameCanvas.container(gallows[game.errors],
                                         [Color.GREEN + game.drawnEntry + Color.END])
                    gameCanvas.statusBar = (
                        genericStatusBar + 'Wygrywasz! W tej grze zdobywasz '
                        + str(rank.points)
                        + pointsStr + '! Gratulacje!!!\n' + endGameStatusBar)
                    gameCanvas.cmdListener = Canvas().cmdListener
                    gameCanvas.print_canvas()
                    cmd = gameCanvas.cmd_listen()

                else:
                    if(game.difficulty == DIFFICULTY_MENU.key_by_label('Normalny')
                            or game.difficulty == DIFFICULTY_MENU.key_by_label('Ekstremalny')):

                        gameCanvas.statusBar = (
                            genericStatusBar
                            + 'Użyte litery '
                            + str(game.letterHistory))

                    elif(game.difficulty == DIFFICULTY_MENU.key_by_label('Trudny')
                            or game.difficulty == DIFFICULTY_MENU.key_by_label('Szaleńczy')):

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
                    if(cmd == GAMEOVER_MENU.key_by_label('Zagraj ponownie')):
                        cmd = game.reset(game.difficulty)
                        break
                    elif(cmd in DIFFICULTY_MENU.getkeys('str')):
                        cmd = game.reset(int(cmd))  # type: ignore
                        break
                    elif(cmd == GAMEOVER_MENU.key_by_label('Sprawdź znaczenie przysłowia')):
                        wiki_proverb_info(game.proverb)
                    elif(cmd):
                        break
    else:
        mainMenu = Canvas()
        mainMenu.container(gallows[possibleErrors], MAIN_MENU.build_list())
        mainMenu.print_canvas()
        cmd = mainMenu.cmd_listen()
