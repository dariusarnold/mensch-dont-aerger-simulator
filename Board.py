"""
Class describing the play board.
There are 40 fields on the board. The player starting fields are 10 fields apart
Counting starts on a player starting field
"""

class Board:

    def __init__(self, player_list):
        self.players = player_list
        self.board = [None] * 40
        self.num_players = len(player_list)
        self.start_fields = [0, 10, 20, 30]     # fields in front of the players home
        self.target_fields = [39, 9, 19, 29]    # fields in front of the players target
        self.tokens = [list() for _ in range(self.num_players)]

        # initialize homes with 4 player tokens each
        for p in self.players:
            for i in range(4):
                t = Token('h', p.id)
                self.tokens[p.id].append(t)

class InvalidMoveException(Exception):
    """
    Raised when the attempted move is invalid and wont be performed.
    """
    pass

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
        self._pos = position
        self.id = id

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, new):
        self._pos = new
