"""
Class describing the play board.
There are 40 fields on the board. The player starting fields are 10 fields apart
Counting starts on a player starting field with index 0.
Tokens in target have a position attribute of -1...-4.
"""

class Board:

    def __init__(self, player_list):
        self.players = player_list
        self.board = [None] * 56
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

    def __str__(self):
        """
        Return current board configuration as a line. The left most symbol is at
        position 0, the right most symbol is at position 39.
        Dots represent an empty field.
        A number represents a token on that position. The number is the id of 
        player to which the token belongs.
        :return: The current board configuration
        :rtype: str
        """
        string_representation = ["".join(str(field.id)) if field is not None else "." for field in self.board]
        string_representation = " ".join(string_representation)  # add one space between two symbols
        return string_representation

    @property
    def home_pos(self):
        """Get position used to indicate that a token is in the players home"""
        return self._home_pos

    def move_out_of_home(self, player_id):
        """
        Get a token from players home and move it to the start position if free. If start position is blocked by
        another players token, beat that token. If start position is blocked by own token, raise InvalidMoveException.
        :param player_id: Which players token to move
        :type player_id: int
        :raises InvalidMoveException: When the players start field is blocked by one of his own tokens
        """
        home_tokens = self.get_home_tokens(player_id)
        if not home_tokens:
            raise InvalidMoveException("Cant move token from empty home")
        self.move_token(home_tokens[0])

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
        return [t for t in self.tokens[player_id] if t.position == self.home_pos]

    def player_tokens(self, player_id):
        """return a list of all tokens of a player"""
        return self.tokens[player_id]

    def get_player_tokens_on_board(self, player_id):
        """Return a list of all tokens that are currently on the board, meaning
        no home tokens are included."""
        return [t for t in self.tokens[player_id] if t.position != self.home_pos]

    def home_token_number(self, player_id):
        """get number of tokes that are in the players home"""
        return len(self.get_home_tokens(player_id))

    def get_field_content(self, position):
        """get content of the board at position"""
        if 0 <= position <= 39:
            return self.board[position]

    def throw(self, token):
        if token.position == self.home_pos or self.board[token.position] != token:
            raise InvalidMoveException("Trying to throw token that is not on the board")
        self.board[token.position] = None
        token.position = self.home_pos

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
        if token.position == self.home_pos:
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
                start_content.position = self.home_pos
                self._move(token, self.start_fields[token.id])
        elif token.position < 0:
            # token is in target
            raise NotImplementedError
        elif token.position >= 0:
            # token is on normal board
            new_pos = (token.position + places) % 40
            if token.position <= self.get_target_position(id) and token.position+places> self.get_target_position(id):
                # this move would move the token past the home, instead try to move it in the home
                rest_places = self.get_target_position(id) - token.position - places # places the token would move in the target
                rest_places *= id + 1  # the last 16 fields of the board are the target fields
                self._move(token, rest_places)
                return
            target_content = self.get_field_content(new_pos)
            if target_content is not None and target_content.id != token.id:
                # kick other players token
                self.throw(target_content)
            self._move(token, new_pos)

    def _move(self, token, new_pos):
        """
        Change token position attribute and update board
        """
        old_pos = token.position
        token.position = new_pos
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
        self._position = position
        self.id = id

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new):
        self._position = new
