"""abstract class Player, derive from it and implement players with different 
strategies"""


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
        #self.figures_get_furthest().move(dice_roll)


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
        pass