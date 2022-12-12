from random import randint

"""
Class Casino: Allows to play dices
:list_of_players: list of players who will play dices
:type list_of_players: list of instances of the player class
(by deafult list is empty)
"""


class Casino:
    def __init__(self, list_of_players=None):
        self.set_list_of_players(list_of_players)

    def get_list_of_players(self):
        return self._list_of_players

    def set_list_of_players(self, new_list):
        if not new_list:
            self._list_of_players = []
        self._list_of_players = list(new_list)

    """
    Methods that allows to remove and add players to casino
    """

    def add_player(self, player):
        self._list_of_players.append(player)

    def remove_player(self, player):
        self._list_of_players.remove(player)

    """
    Checks the result of each player
    Prints the information about the throw
    Returns the winner unless there are multiple winners - returns None
    """

    def game(self, list_of_players):
        results = {}
        for each_player in list_of_players:
            numbers = self.throw_dice(each_player)
            score = each_player.player_result()
            name = each_player.get_name()
            if score in results.keys():
                return 0
            results[score] = each_player.get_name()
            print(f'{name} threw {numbers} and scored {score}')
        list_of_results = list(results.keys())
        return results[max(list_of_results)]

    """
    Returns the result of the game
    """
    def play(self):
        players = self.get_list_of_players()
        game = self.game(players)
        if game == 0:
            return 'The game is unresolved.'
        return f'{game} won the game!'

    """
    Method that throws the dice
    Returns random list of 4 numbers from 1 to 6
    """

    def throw_dice(self, player):
        player.set_dice([randint(1, 6) for _ in range(4)])
        return player.get_dice()


class Player:

    """
    Class Player: Each player have name and a dice throw
    :name: name of the player (it must be unique)
    :type name: str (deafult it is an empty str)
    :dice: list of 4 random generated ints
    :type dice: list of positive ints between 1 and 6
    """

    def __init__(self, name=''):
        self.set_name(name)
        self._dice = []

    def get_name(self):
        return self._name

    def get_dice(self):
        return self._dice

    def set_name(self, new_name):
        if not new_name:
            raise ValueError("Name cannot be empty.")
        self._name = str(new_name)

    def set_dice(self, new_dice):
        self._dice = new_dice

    """
    Method that returs the points of player's throw
    """

    def player_result(self):
        numbers = self._dice
        winnings = []
        if self.is_list_even(numbers):
            winnings.append(sum(numbers)+2)
        if self.is_list_odd(numbers):
            winnings.append(sum(numbers)+3)
        for each_number in set(numbers):
            if numbers.count(each_number) == 2:
                winnings.append(each_number*2)
            if numbers.count(each_number) == 3:
                winnings.append(each_number*4)
            if numbers.count(each_number) == 4:
                winnings.append(each_number*6)
        if not winnings:
            return 0
        return max(winnings)

    def is_list_even(self, numbers):
        for each_number in numbers:
            if each_number % 2 == 1:
                return False
        return True

    def is_list_odd(self, numbers):
        for each_number in numbers:
            if each_number % 2 == 0:
                return False
        return True
