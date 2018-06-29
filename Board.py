"""
Class describing the play board.
There are 40 fields on the board. The player starting fields are 10 fields apart
Counting starts on a player starting field
"""

class Board:

    def __init__(self, player_list):
        self.players = player_list
        self.board = list()
        self.num_players = len(player_list)
        self.start_fields = [0, 10, 20, 30]     # fields in front of the players home
        self.target_fields = [39, 9, 19, 29]    # fields in front of the players target
        self.homes = [list()] * self.num_players
        self.targets = [list()] * self.num_players
        self.tokens = [list()] * self.num_players

        # initialize homes with player tokens
        for p in self.players:
            t = p.Token('h', p.id)
            self.homes[p.id] = [t]*4           # place 4 tokens into player home at start
            self.tokens[p.id] = t
class Token:
    """
    Token with a player id to which it belongs. Position marks the position on
    the board.
    """
    def __init__(self, position, id):
        """

        :param position: Current position of token. Either a number from 0-39, 
        indicating the position on the board, or 'h' for home or -1,-2,-3,-4
        for the player target
         for the position in target
        :type position: int, str
        :param id: Player id of token, integer from 0...4
        :type id: int
        """
        self.pos = position
        self.id = id
        