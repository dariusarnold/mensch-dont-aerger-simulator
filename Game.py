import Player
import Board
from random import randint
from utils import mprint
from Board import Board

class Game:

    def __init__(self, p1=None, p2=None, p3=None, p4=None):
        """
        Initialize a game with given player types.
        Possible player types: 
        'first': always moves first token
        'last': always moves last token
        'random': moves random token
        'firstbeat': Beats other player if it can, otherwise moves first token
        'lastbeat': Beats other player if it can, otherwise moves last token
        :param p1: String describing player type
        :type p1: str
        :param p2: String describing player type
        :type p2: str
        :param p3: String describing player type
        :type p3: str
        :param p4: String describing player type
        :type p4: str
        """
        self.players = [self.create_player(p, i) for i, p in enumerate((p1, p2, p3, p4)) if p is not None]
        self.game_running = True
        self.p1, self.p2, self.p3, self.p4 = [p for p in self.players]


        mprint("Starting game with {} players.".format(len(self.players)))
        for player in self.players:
            mprint("Player {index} is a {type}".format(index=player.id, type=type(player).__name__))

    def create_player(self, player_type, player_id):
        """
        Create  a new player of type
        :param player_type: Which type of player to create: first, last random
        :type player_type: str 
        :return: created player
        """
        if player_type == 'first':
            p = Player.FirstPlayer(player_id)
        elif player_type == 'last':
            p = Player.LastPlayer(player_id)
        elif player_type == 'random':
            p = Player.RandomPlayer(player_id)
        else:
            raise TypeError("Player type {} not known".format(player_type))
        return p

    def play(self):
        while self.game_running:
            self.turn()

    def turn(self):
        """play one turn for all players"""
        for player in self.players:
            dice_roll = randint(1, 6)
            player.turn(dice_roll)
            if player.has_won:
                self.game_running = False
                return player


