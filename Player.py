"""abstract class Player, derive from it and implement players with different 
strategies"""

from random import randint, choice
from Board import InvalidMoveException

class Player:

    def __init__(self, id):
        self.id = id
        self.has_won = False

    def turn(self, board, dice_roll):
        raise NotImplementedError


class FirstPlayer(Player):
    """
    This player only moves his furthest figure
    """

    def __init__(self, id):
        super().__init__(id)

    def turn(self, board, dice_roll):
        pass


class LastPlayer(Player):
    """
    This player always moves the figure in the back
    """

    def __init__(self, id):
        super().__init__(id)

    def turn(self, board, dice_roll):
        pass


class RandomPlayer(Player):
    """
    This player selects a figure to move randomly
    """

    def __init__(self, id):
        super().__init__(id)

    def turn(self, board, dice_roll):
        home_tokens = board.get_home_tokens(self.id)
        available_tokens = board.get_player_tokens_on_board(self.id)
        if dice_roll == 6 and home_tokens:
            # need to get out of the home if start field is free
            try:
                board.move_out_of_home(self.id)
            except InvalidMoveException as ive:
                # start field blocked by own token, skip this 6
                pass

        elif available_tokens:
            picked = self.select_random_token(available_tokens)
            board.move_token(picked, dice_roll)

    def select_random_token(self, token_list):
        """Return one random token from token_list"""
        #print(len(token_list))
        return choice(token_list)
        #return token_list[randint(0, len(token_list))]