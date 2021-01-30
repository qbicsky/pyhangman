import os
import sys
import operator
import math
import json

from colors import Color

import gallows
from defmenus import DIFFICULTY_MENU


class Ranking:
    """Build ranking based on JSON file."""

    def __init__(self, jsonFile='ranking.json'):
        """
        Load Ranking from JSON file.  If file doesn't exist,
        create one in the same folder, where script resides.

        Args:
            jsonFile (str, optional): Defaults to 'ranking.json'.
        """
        self.jsonFile = os.path.join(sys.path[0], jsonFile)
        try:
            with open(self.jsonFile, "r", encoding="UTF-8") as file:
                try:
                    self.data = json.load(file)
                except json.decoder.JSONDecodeError:
                    self.data = {}
        except FileNotFoundError:
            self.data = {}

        with open(self.jsonFile, "w", encoding="UTF-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4,
                      sort_keys=True)

    def __str__(self):
        """
        Show Ranking data.

        Returns:
            data (dict): Dictionary with Ranking data.
        """
        return self.data

    def reset(self):
        jsonFile = self.jsonFile
        self.data = {}
        with open(jsonFile, "w", encoding="UTF-8") as file:
            json.dump(self.data, file, ensure_ascii=False,
                      indent=4, sort_keys=True)

    def show(self):
        """
        Return Top 5 players.

        Returns:
            list: Prepared list of lines for printing on Canvas
                  with container Canvas method
        """
        containerLen = 44
        ranking = Ranking()
        ranking = {
            item: ranking.data.get(item).get('points')
            for item in ranking.data
        }
        ranking = sorted(ranking.items(), key=operator.itemgetter(1),
                         reverse=True)

        top5rankingTitle = 'Ranking TOP 5'

        evenerLen = math.ceil((containerLen - len(top5rankingTitle)) / 2)
        evener = [' ' for _ in range(evenerLen)]
        evener = ''.join(evener)

        top5ranking = list()
        top5ranking.append(evener + top5rankingTitle)

        evenerLen = containerLen - len('Lp. Gracz' + 'Pkt')
        evener = [' ' for _ in range(evenerLen)]
        evener = ''.join(evener)

        top5ranking.append(Color.DARKGREY + 'Lp. Gracz' + evener + 'Pkt'
                           + Color.END)

        i = 0
        for player in ranking:
            evenerLen = (containerLen
                         - len(str(i + 1)) - len('   ')
                         - len(player[0]) - len(str(player[1]))
                         )
            evener = ['.' for _ in range(evenerLen)]
            evener = ''.join(evener)
            top5ranking.append(str(i + 1) + '   ' + player[0]
                               + Color.DARKGREY + evener + Color.END
                               + str(player[1])
                               )
            i += 1
            if(i == 5):
                break
        return top5ranking


class Rank:
    """
    Create specific player Ranking data and update based on new game.
    Then store this data in Ranking JSON file.
    """

    def __init__(self, player='Gal Anonim', difficulty=1,
                 errors=(gallows.possibleErrors - 1)):
        """
        Add new statistics to player's data in Ranking.

        Args:
            player (str, optional): Name of the player.
                                    Defaults to 'Gal Anonim'.
            difficulty (int, optional): Difficulty level from the Game.
                                        Defaults to 1.
            errors (tuple, optional): Errors made during the gameplay.
                                      Defaults to (gallows.possibleErrors - 1).
        """
        jsonFile = Ranking().jsonFile
        ranking = Ranking().data

        if (ranking.get(player) is None):
            playerRanking = self.new_player(player).get(player)
        else:
            playerRanking = ranking.get(player)

        if(errors < gallows.possibleErrors):
            playerRanking = self.update_stats(playerRanking,
                                              'winnings', difficulty=difficulty)

            self.points = gallows.possibleErrors * difficulty - errors

            pointsSum = playerRanking.get('points')
            pointsSum = pointsSum + self.points
            pointsSum = {'points': pointsSum}

            playerRanking.update(pointsSum)
        else:
            playerRanking = self.update_stats(playerRanking,
                                              'losses', difficulty=difficulty)

        playerRanking = {
            player: playerRanking
        }

        ranking.update(playerRanking)

        with open(jsonFile, "w", encoding="UTF-8") as file:
            json.dump(ranking, file, ensure_ascii=False,
                      indent=4, sort_keys=True)

    @staticmethod
    def new_player(player):
        """
        Create new player in the Ranking, if doesn't exists already.

        Args:
            player (str): Name of the player
        Returns:
            playerRanking [dict]: Dictionary with new player's Ranking\
                                  data.
        """
        difficultyDict = {
            str(difficulty): {
                "winnings": 0,
                "losses": 0
            }
            for difficulty in DIFFICULTY_MENU.getkeys()
        }
        playerRanking = {
            player: {
                "points": 0,
                "difficulty": difficultyDict
            }
        }
        return playerRanking

    @staticmethod
    def update_stats(ranking, statStr, difficulty):
        """
        Adds winnings or losses to respective difficulty levels
        in form of Player's ranking dictionary.

        Args:
            ranking (dict): Dictionary with Player's stats
            statStr (string): 'losses' or 'winnings'
            difficulty (int): Integer representing difficulty

        Returns:
            [type]: [description]
        """
        stat = ranking.get('difficulty').get(str(difficulty)).get(statStr)
        stat = {statStr: stat + 1}
        ranking.get('difficulty').get(str(difficulty)).update(stat)
        return ranking
