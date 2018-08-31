import unittest
from Board import Board, Token, InvalidMoveException
from Player import RandomPlayer


class TestHome(unittest.TestCase):

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = [RandomPlayer(i) for i in range(4)]
        self.board = Board(self.players)

    def test_home_tokens(self):
        """Test if all homes are filled with 4 tokens after creation."""
        for player in self.players:
            with self.subTest(player=player):
                home_t_num = self.board.home_token_number(player.id)
                self.assertEqual(home_t_num, 4)

    def test_throw(self):
        """Test if a thrown token is placed into the corresponding home"""
        for player in self.players:
            with self.subTest(player=player):
                self.board.move_out_of_home(player.id)
                self.board.throw(self.board.get_start_content(player.id))
                self.assertEqual(len(self.board.get_home_tokens(player.id)), 4)
                self.board.get_field_content(self.board.get_start_position(player.id))


class TestStartPosition(unittest.TestCase):

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = [RandomPlayer(i) for i in range(4)]
        self.board = Board(self.players)

    def test_start_positions(self):
        """Test if the correct start positions are returned"""
        expected = (0, 10, 20, 30)
        for e, player in zip(expected, self.players):
            with self.subTest(e=e, player=player):
                s = self.board.get_start_position(player.id)
                self.assertEqual(s, e)

    def test_start_postion_content_empty(self):
        """Test if the start postion content is correctly returned as empty after creation"""
        for player in self.players:
            with self.subTest(player=player):
                s = self.board.get_start_content(player.id)
                self.assertEqual(s, None)

    def test_start_postion_content_full(self):
        """Test if the start postion content is correctly returned as an own token if there is one"""
        for player in self.players:
            with self.subTest(player=player):
                start_pos = self.board.get_start_position(player.id)
                t = Token(start_pos, player.id)
                self.board.board[start_pos] = t
                s = self.board.get_start_content(player.id)
                self.assertEqual(t, s)


class TestMovingFromHome(unittest.TestCase):

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = [RandomPlayer(i) for i in range(4)]
        self.board = Board(self.players)

    def test_move_from_home_unobstructed(self):
        """Test if the token can be moved from home to the start position if it is unobstructed"""
        for player in self.players:
            with self.subTest(player=player):
                prev_home_tokens = self.board.get_home_tokens(player.id)
                prev_home_num = self.board.home_token_number(player.id)
                self.board.move_out_of_home(player.id)
                new_home_num = self.board.home_token_number(player.id)
                self.assertGreater(prev_home_num, new_home_num)
                self.assertEqual(prev_home_num-1, new_home_num)
                moved_token = self.board.get_start_content(player.id)
                self.assertIn(moved_token, prev_home_tokens)

    def test_move_from_home_obstructed_by_other(self):
        """Test other token is thrown and own token is moved when start field is blocked by another players token"""
        for player in self.players:
            with self.subTest(player=player):
                blocking_token = Token(-1, -1)  # create blocking token
                self.board._move(blocking_token, self.board.get_start_position(player.id))  # move blocking token to current players start field
                prev_home_tokens = self.board.get_home_tokens(player.id)
                prev_home_num = self.board.home_token_number(player.id)
                self.board.move_out_of_home(player.id)
                new_home_num = self.board.home_token_number(player.id)
                moved_token = self.board.get_start_content(player.id)
                self.assertGreater(prev_home_num, new_home_num)
                self.assertIn(moved_token, prev_home_tokens)
                self.assertEqual(blocking_token.position, self.board.home_pos)

    def test_move_from_home_obstructed_by_own(self):
        """Test if an InvalidMoveException is raised when trying to move from 
        home to a start field blocked by a players own token"""
        for player in self.players:
            with self.subTest(player=player):
                blocking_token = Token(-1, player.id)  # create ow blocking token
                self.board._move(blocking_token, self.board.get_start_position(player.id))
                prev_home_tokens = self.board.get_home_tokens(player.id)
                prev_home_num = self.board.home_token_number(player.id)
                with self.assertRaises(InvalidMoveException):
                    self.board.move_out_of_home(player.id)
                new_home_num = self.board.home_token_number(player.id)
                self.assertEqual(prev_home_num, new_home_num)
                self.assertEqual(blocking_token, self.board.get_start_content(player.id))


    def test_move_from_home_empty_home(self):
        """Check to see if trying to move a token out of an empty home 
        raises the correct exception"""
        for player in self.players:
            with self.subTest(player=player):
                for i, t in enumerate(self.board.tokens[player.id]):
                    # place all tokens on arbitrary position outside of home
                    self.board._move(t, i)
                with self.assertRaises(InvalidMoveException):
                    self.board.move_out_of_home(player.id)


class TestMoving(unittest.TestCase):
    """Tests related to movement on the board, without throwing"""

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = [RandomPlayer(i) for i in range(4)]
        self.board = Board(self.players)

    def test_move_unobstructed(self):
        """Test moving a token from the start postion to an unabstructed position"""

        def move_unobstructed(places):
            """Test if a player can move his token for places on the board"""
            for player in self.players:
                with self.subTest(player=player):
                    self.board.move_out_of_home(player.id) # move one token from home so there is a movable token on the board
                    t = self.board.get_start_content(player.id)
                    prev_pos = t.position
                    self.board.move_token(t, places)
                    new_pos = t.position
                    self.assertEqual(prev_pos+places, new_pos)  # test if new position and old position fit
                    self.assertEqual(self.board.get_field_content(new_pos), t)  # test if moved token and token on new position are equal
                    self.assertEqual(self.board.get_field_content(prev_pos), None)  # test if old position is filled with None
                    self.board.throw(t) # undo the move so start field is not blocked

        for i in range(1, 7):
            with self.subTest(i=i):
                # move all possible dice rolls from 1...6
                move_unobstructed(i)


class TestThrowing(unittest.TestCase):
    """Tests throwing of tokens"""

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = [RandomPlayer(i) for i in range(4)]
        self.board = Board(self.players)

    def test_throw_token_in_home_exception(self):
        """Tests if trying to throw a token in the home field raises the
        InvalidMoveException"""
        for player in self.players:
            with self.subTest(player=player):
                home_token = self.board.get_home_tokens(player.id)[0]
                with self.assertRaises(InvalidMoveException):
                    self.board.throw(home_token)

    def test_throw_token_on_board(self):
        """Tests if throwing a token on board works"""
        for player in self.players:
            with self.subTest(player=player):
                prev_home_tokens = self.board.get_home_tokens(player.id)
                self.board.move_out_of_home(player.id)
                moved_token = self.board.get_start_content(player.id)
                self.board.throw(moved_token)
                new_home_tokens = self.board.get_home_tokens(player.id)
                self.assertIn(moved_token, new_home_tokens)
                self.assertEqual(moved_token.position, self.board.home_pos)

    def test_throw_from_target_exception(self):
        """Test if throwing a token that is in a players target raises the
        InvalidMoveException"""
        pass


class TestMovingBorder(unittest.TestCase):
    """Tests if moving a token around the border at field 40 works.
    """

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = [RandomPlayer(i) for i in range(4)]
        self.board = Board(self.players)

    def test_move_over_border(self):
        """Test if a token is moved correctly over the boarder. The board ends
        at the field with index 39.
        But player 0 can't move over the border since his target field is there,
        so he is skipped here"""
        for player in self.players:
            with self.subTest(player=player):
                if player.id == 0: return
                token = self.board.get_home_tokens(player.id)[0]
                self.board._move(token, 38)
                self.board.move_token(token, 5)
                self.assertEqual(token.position, 3)
                self.board._move(token, 39)
                self.board.move_token(token, 1)
                self.assertEqual(token.position, 0)


class TestMovingIntoTarget(unittest.TestCase):
    """Tests if moving a token around the border at field 40 works.
    """

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = [RandomPlayer(i) for i in range(4)]
        self.board = Board(self.players)

    def test_moving_into_target_correct(self):
        """Test if a player is automatically moved to the correct position in 
        the target if he moves enough places """
        for places in range(1, 5):
            with self.subTest(places=places):
                for player in self.players:
                    with self.subTest(player=player):
                        token = self.board.get_home_tokens(player.id)[0]
                        self.board._move(token, self.board.get_target_position(player.id))
                        self.board.move_token(token, places)
                        self.assertEqual(token.position, -places * (player.id + 1))

    def test_moving_into_target_fails(self):
        """Test if the correct exception is raised when the player is in front
         of the target but his dice roll would overshoot the last position in 
         the target"""
        for player in self.players:
            with self.subTest(player=player):
                token = self.board.get_home_tokens(player.id)[0]
                self.board._move(token, self.board.get_target_position(player.id))
                with self.assertRaises(InvalidMoveException):
                    self.board.move_token(token, 5)  # 5 will always overshoot home of length 4
                self.assertEqual(token.position, self.board.get_target_position(player.id))
