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

    def get_start_position(self, player_id):
        """
        Return start position for the given player id. The start position is
        the first field in front of a players home.
        :type player_id: int
        :return: start position of player
        :rtype: int
        """
        return self.start_fields[player_id]

    def get_start_content(self, player_id):
        """
        Get content (either token or empty) for the start position.
        :param player_id: id of player
        :type player_id: int
        :return: Token on start position or None if players start position is empty
        :rtype: Token or None
        """
        return self.board[self.get_start_position(player_id)]

    def throw(self, token):
        if self.board[token.pos] != token:
            raise InvalidMoveException("Trying to throw token that is not on the board")
        self.board[token.pos] = None
        token.pos = 'h'
    def _move(self, token, new_pos):
        """
        Change token pos attribute and update board
        """
        old_pos = token.pos
        token.pos = new_pos
        self.board[new_pos] = token
        if old_pos != 'h': self.board[old_pos] = None


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
