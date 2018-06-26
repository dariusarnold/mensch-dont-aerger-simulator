"""abstract class Player, derive from it and implement players with different 
strategies"""

class Player:

    def __init__(self):
        self.has_won = False

    def turn(self):
        raise NotImplementedError

class FirstPlayer(Player):
    """
    This player only moves his furthest figure
    """

    def __init__(self):
        super().__init__()

    def turn(self, dice_roll):
        pass
        #self.figures_get_furthest().move(dice_roll)