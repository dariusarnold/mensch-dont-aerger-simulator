import Player
import Board
from random import randint
from utils import mprint
from Board import Board

class Game:

    def __init__(self, p1=None, p2=None, p3=None, p4=None):
        self.board = Board()
        self.players = [self.create_player(p) for p in (p1, p2, p3, p4) if p is not None]
        self.game_running = True
        self.p1, self.p2, self.p3, self.p4 = [p for p in self.players]


        mprint("Starting game with {} players.".format(len(self.players)))
        for i, player in enumerate(self.players):
            mprint("Player {index} is a {type}".format(index=i, type=type(player).__name__))

    def create_player(self, player_type):
        """
        Create  a new player of type
        :param player_type: Which type of player to create: first, last random
        :type player_type: str 
        :return: created player
        """
        if player_type == 'first':
            p = Player.FirstPlayer()
        elif player_type == 'last':
            p = Player.LastPlayer()
        elif player_type == 'random':
            p = Player.RandomPlayer()
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


