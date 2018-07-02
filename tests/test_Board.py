import unittest
from Board import Board, Token, InvalidMoveException
from Player import RandomPlayer


class TestHome(unittest.TestCase):

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = ("random",) * 4
        self.players = [RandomPlayer(i) for i, p in enumerate(self.players) if p is not None]
        self.p1, self.p2, self.p3, self.p4 = self.players
        self.b = Board(self.players)

    def test_home_tokens(self):
        """Test if all homes are filled with 4 tokens after creation."""
        for p in self.players:
            with self.subTest(p=p):
                home_t_num = self.b.home_token_number(p.id)
                self.assertEqual(home_t_num, 4)

    def test_throw(self):
        """Test if a thrown token is placed into the corresponding home"""
        for p in self.players:
            with self.subTest(p=p):
                self.b.move_out_of_home(p.id)
                self.b.throw(self.b.get_start_content(p.id))
                self.assertEqual(len(self.b.get_home_tokens(p.id)), 4)
                self.b.get_field_content(self.b.get_start_position(p.id))


class TestStartPosition(unittest.TestCase):

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = ("random",) * 4
        self.players = [RandomPlayer(i) for i, p in enumerate(self.players) if p is not None]
        self.p1, self.p2, self.p3, self.p4 = self.players
        self.b = Board(self.players)

    def test_start_positions(self):
        """Test if the correct start positions are returned"""
        expected = (0, 10, 20, 30)
        for e, p in zip(expected, self.players):
            with self.subTest(e=e, p=p):
                s = self.b.get_start_position(p.id)
                self.assertEqual(s, e)

    def test_start_postion_content_empty(self):
        """Test if the start postion content is correctly returned as empty after creation"""
        for p in self.players:
            with self.subTest(p=p):
                s = self.b.get_start_content(p.id)
                self.assertEqual(s, None)

    def test_start_postion_content_full(self):
        """Test if the start postion content is correctly returned as an own token if there is one"""
        for p in self.players:
            with self.subTest(p=p):
                start_pos = self.b.get_start_position(p.id)
                t = Token(start_pos, p.id)
                self.b.board[start_pos] = t
                s = self.b.get_start_content(p.id)
                self.assertEqual(t, s)


class TestMovingFromHome(unittest.TestCase):

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = ("random",) * 4
        self.players = [RandomPlayer(i) for i, p in enumerate(self.players) if p is not None]
        self.p1, self.p2, self.p3, self.p4 = self.players
        self.b = Board(self.players)

    def test_move_from_home_unobstructed(self):
        """Test if the token can be moved from home to the start position if it is unobstructed"""
        for p in self.players:
            with self.subTest(p=p):
                prev_home_tokens = self.b.get_home_tokens(p.id)
                prev_home_num = self.b.home_token_number(p.id)
                self.b.move_out_of_home(p.id)
                new_home_num = self.b.home_token_number(p.id)
                self.assertGreater(prev_home_num, new_home_num)
                self.assertEqual(prev_home_num-1, new_home_num)
                moved_token = self.b.get_start_content(p.id)
                self.assertIn(moved_token, prev_home_tokens)

    def test_move_from_home_obstructed_by_other(self):
        """Test other token is thrown and own token is moved when start field is blocked by another players token"""
        for p in self.players:
            with self.subTest(p=p):
                blocking_token = Token(-1, -1)  # create blocking token
                self.b._move(blocking_token, self.b.get_start_position(p.id))  # move blocking token to current players start field
                prev_home_tokens = self.b.get_home_tokens(p.id)
                prev_home_num = self.b.home_token_number(p.id)
                self.b.move_out_of_home(p.id)
                new_home_num = self.b.home_token_number(p.id)
                moved_token = self.b.get_start_content(p.id)
                self.assertGreater(prev_home_num, new_home_num)
                self.assertIn(moved_token, prev_home_tokens)
                self.assertEqual(blocking_token.pos, 'h')

    def test_move_from_home_obstructed_by_own(self):
        """Test if an InvalidMoveException is raised when trying to move from 
        home to a start field blocked by a players own token"""
        for p in self.players:
            with self.subTest(p=p):
                blocking_token = Token(-1, p.id)  # create ow blocking token
                self.b._move(blocking_token, self.b.get_start_position(p.id))
                prev_home_tokens = self.b.get_home_tokens(p.id)
                prev_home_num = self.b.home_token_number(p.id)
                with self.assertRaises(InvalidMoveException):
                    self.b.move_out_of_home(p.id)
                new_home_num = self.b.home_token_number(p.id)
                self.assertEqual(prev_home_num, new_home_num)
                self.assertEqual(blocking_token, self.b.get_start_content(p.id))


    def test_move_from_home_empty_home(self):
        """Check to see if trying to move a token out of an empty home 
        raises the correct exception"""
        for p in self.players:
            with self.subTest(p=p):
                for i, t in enumerate(self.b.tokens[p.id]):
                    # place all tokens on arbitrary position outside of home
                    self.b._move(t, i)
                with self.assertRaises(InvalidMoveException):
                    self.b.move_out_of_home(p.id)


class TestMoving(unittest.TestCase):
    """Tests related to movement on the board, without throwing"""

    def setUp(self):
        # Create a board with 4 random type players, this is only for testing the board functionality
        self.players = ("random",) * 4
        self.players = [RandomPlayer(i) for i, p in enumerate(self.players) if p is not None]
        self.p1, self.p2, self.p3, self.p4 = self.players
        self.b = Board(self.players)

    def test_move_unobstructed(self):
        """Test moving a token from the start postion to an unabstructed position"""

        def move_unobstructed(places):
            """Test if a player can move his token for places on the board"""
            for p in self.players:
                with self.subTest(p=p):
                    self.b.move_out_of_home(p.id) # move one token from home so there is a movable token on the board
                    t = self.b.get_start_content(p.id)
                    prev_pos = t.pos
                    self.b.move_token(t, places)
                    new_pos = t.pos
                    self.assertEqual(prev_pos+places, new_pos)  # test if new position and old position fit
                    self.assertEqual(self.b.get_field_content(new_pos), t)  # test if moved token and token on new position are equal
                    self.assertEqual(self.b.get_field_content(prev_pos), None)  # test if old position is filled with None
                    self.b.throw(t) # undo the move so start field is not blocked

        for i in range(1, 7):
            with self.subTest(i=i):
                # move all possible dice rolls from 1...6
                move_unobstructed(i)


class TestThrowing(unittest.TestCase):
    """Tests throwing of tokens"""
    pass