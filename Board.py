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
        self._home_pos = 'h'

        # initialize homes with 4 player tokens each
        for p in self.players:
            for i in range(4):
                t = Token(self.home_pos, p.id)
                self.tokens[p.id].append(t)

    @property
    def home_pos(self):
        """Get pos used to indicate that a token is in the players home"""
        return self._home_pos

    def move_out_of_home(self, player_id):
        """
        Get a token from players home and move it to the start position if free. If start position is blocked by
        another players token, beat that token. If start position is blocked by own token, raise InvalidMoveException.
        :param player_id: Which players token to move
        :type player_id: int
        :raises InvalidMoveException: When the players start field is blocked by one of his own tokens
        """
        t = self.get_home_tokens(player_id)
        if not t:
            raise InvalidMoveException("Cant move token from empty home")
        self.move_token(t[0])

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

    def get_target_position(self, player_id):
        """return target position for the given player id. The target position
        is the field directly in front of a players target."""
        return self.target_fields[player_id]

    def get_home_tokens(self, player_id):
        """return list of tokens that are in a players home. List is empty if
        there are no tokens in the players home"""
        return [t for t in self.tokens[player_id] if t.pos == self.home_pos]

    def player_tokens(self, player_id):
        """return a list of all tokens of a player"""
        return self.tokens[player_id]

    def get_player_tokens_on_board(self, player_id):
        """Return a list of all tokens that are currently on the board, meaning
        no home tokens are included."""
        return [t for t in self.tokens[player_id] if t.pos != self.home_pos]

    def home_token_number(self, player_id):
        """get number of tokes that are in the players home"""
        return len(self.get_home_tokens(player_id))

    def get_field_content(self, position):
        """get content of the board at position"""
        if position >= 0 and position <= 39:
            return self.board[position]

    def throw(self, token):
        if token.pos == self.home_pos or self.board[token.pos] != token:
            raise InvalidMoveException("Trying to throw token that is not on the board")
        self.board[token.pos] = None
        print("Token of player {} on position {} was thrown".format(token.id, token.pos))
        token.pos = self.home_pos

    def move_token(self, token, places=None):
        """
        Move given token by places
        :param token: Which token to move_token
        :type token: Token
        :param places: how many spaces to move_token token. Not required for token in
        home.
        :type places: int
        :rtype: None
        """
        id = token.id # token id is equal to id of the player to which the token belongs
        if token.pos == self.home_pos:
            # is the players start field free?
            start_content = self.get_start_content(id)
            if start_content is None:
                # start is empty
                self._move(token, self.start_fields[token.id])
            elif start_content.id is id:
                # own token blocking start
                raise InvalidMoveException("Start field blocked by own token")
            else:
                # other players token blocks start, throw him
                start_content.pos = self.home_pos
                self._move(token, self.start_fields[token.id])
        elif token.pos < 0:
            # token is in target
            raise NotImplementedError
        elif token.pos >= 0:
            # token is on normal board
            new_pos = (token.pos + places) % 39
            target_content = self.get_field_content(new_pos)
            if target_content is not None and target_content.id != token.id:
                # kick other players token
                self.throw(target_content)
                self._move(token, new_pos)
            else:
                # target field is free, move there
                self._move(token, new_pos)
    def _move(self, token, new_pos):
        """
        Change token pos attribute and update board
        """
        old_pos = token.pos
        token.pos = new_pos
        self.board[new_pos] = token
        if old_pos != self.home_pos: self.board[old_pos] = None


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
