"""
Tests for Python Connect Four 3D
This program procedurally generates trivial games whose outcome is known.
This allows easier checking of termination conditions which were
"""


from absl.testing import absltest
from open_spiel.python.games import connect_four_3d
import pyspiel

id = 0

def move(file, rank):
    """Returns the move based on the chosen file and rank"""
    return file * 4 + rank

class ConnectFour3DTest(absltest.TestCase):
    def test_game_from_cc(self):
        """Runs our standard game tests, checking API consistency."""
        game = pyspiel.load_game("python_connect_four_3d")
        pyspiel.random_sim_test(game, num_sims=10, serialize=False, verbose=True)

    def vertical_win(self, file, rank):
        """
        This simple game creates two vertical piles next to each-other.
        Naturally, as the second player is one turn behind, the first
        player wins.
        """
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()

        winning_move = move(file, rank)
        losing_move = move((file + 1) % 4, rank)
        for i in range(3):
            state.apply_action(winning_move)
            state.apply_action(losing_move)

        state.apply_action(winning_move)

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")
    
    def test_vertical_win(self):
        for f in range(4):
            for r in range(4):
                self.vertical_win(f,r)


    def file_win(self, file):
        """
        The two players fill-in a file in parallel. Player 0 (which
        is ahead) wins the game systematically.
        """
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()
        winning_file = file
        losing_file = (file + 1) % 4

        for rank in range(3):
            win_move = winning_file * 4 + rank
            lose_move = losing_file * 4 + rank
            state.apply_action(win_move)
            state.apply_action(lose_move)

        last_winning_move = winning_file * 4 + 3
        state.apply_action(last_winning_move)

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

    def test_file_win(self):
        # Check file victories (on the first row)
        for file in range(4):
            self.file_win(file)

    def rank_win(self,rank):
        """
        The two players fill-in a rank in paralle, Player 0 (which is ahead) wins the game
        """
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()
        winning_rank = rank
        losing_rank = (rank + 1) % 4

        for file in range(3):
            win_move = move(file, winning_rank)
            lose_move = move(file, losing_rank)
            state.apply_action(win_move)
            state.apply_action(lose_move)

        last_winning_move = 3 * 4 + winning_rank
        state.apply_action(last_winning_move)

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

    def test_rank_win(self):
        for i in range(4):
            self.rank_win(i)

    def test_diagonal(self):
        """
        The two players repeat the same moves, allowing Player 0 to complete the diagonal on
        the first row
        """
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()

        for i in range(3):
            m = move(i, i)
            state.apply_action(m) # Player 0 move
            state.apply_action(m) # Player 1 move

        # Last move for Player 0
        i = 3
        m = move(i, i)
        state.apply_action(m)

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

    def test_anti_diagonal(self):
        """
        The two players repeat the same moves, allowing Player 0 to complete the diagonal on
        the first row. This is the anti-diagonal
        """
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()

        for i in range(3):
            m = move(3 - i, i)
            state.apply_action(m) # Player 0 move
            state.apply_action(m) # Player 1 move

        # Last move for Player 0
        i = 3
        m = move(3 - i, i)
        state.apply_action(m)

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

    def rising_file(self, file):
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()
        spare_file = (file + 1) % 4

        # First moves
        state.apply_action(move(file, 0))
        state.apply_action(move(file, 1))
        state.apply_action(move(file, 1))
        state.apply_action(move(file, 2))
        state.apply_action(move(file, 2))
        state.apply_action(move(file, 3))
        state.apply_action(move(file, 2))
        state.apply_action(move(file, 3))
        state.apply_action(move(file, 3))
        state.apply_action(move(spare_file, 0))
        state.apply_action(move(file, 3))

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

    def test_rising_file(self):
        for f in range(4):
            self.rising_file(f)

    def descending_file(self, file):
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()
        spare_file = (file + 1) % 4

        # First moves
        state.apply_action(move(file, 3 - 0))
        state.apply_action(move(file, 3 - 1))

        state.apply_action(move(file, 3 - 1))
        state.apply_action(move(file, 3 - 2))

        state.apply_action(move(file, 3 - 2))
        state.apply_action(move(file, 3 - 3))

        state.apply_action(move(file, 3 - 2))
        state.apply_action(move(file, 3 - 3))

        state.apply_action(move(file, 3 - 3))
        state.apply_action(move(spare_file, 0))

        state.apply_action(move(file, 3 - 3))

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

    def test_descending_file(self):
        for f in range(4):
            self.descending_file(f)

    def rising_rank(self, rank):
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()
        spare_rank = (rank + 1) % 4

        # First moves
        state.apply_action(move(0, rank))

        state.apply_action(move(1, rank))
        state.apply_action(move(1, rank))

        state.apply_action(move(2, rank))
        state.apply_action(move(2, rank))

        state.apply_action(move(3, rank))
        state.apply_action(move(2, rank))

        state.apply_action(move(3, rank))
        state.apply_action(move(3, rank))
        state.apply_action(move(0, spare_rank))
        state.apply_action(move(3, rank))

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

    def test_rising_rank(self):
        for r in range(4):
            self.rising_rank(r)

    def descending_rank(self, rank):
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()
        spare_rank = (rank + 1) % 4

        # First moves
        state.apply_action(move(3 - 0, rank))

        state.apply_action(move(3 - 1, rank))
        state.apply_action(move(3 - 1, rank))
        state.apply_action(move(3 - 2, rank))
        state.apply_action(move(3 - 2, rank))
        state.apply_action(move(3 - 3, rank))
        state.apply_action(move(3 - 2, rank))
        state.apply_action(move(3 - 3, rank))
        state.apply_action(move(3 - 3, rank))
        state.apply_action(move(3 - 0, spare_rank))
        state.apply_action(move(3 - 3, rank))

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

    def test_descending_rank(self):
        for r in range(4):
            self.descending_rank(r)

    def test_rising_diagonal(self):
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()
        # The diagonal moves are 0, 5, 10, and 15
        spare_move = 1 # 1 is outside the diagonal

        # First moves
        state.apply_action(0 * 5)
        state.apply_action(1 * 5)

        state.apply_action(1 * 5)
        state.apply_action(2 * 5)

        state.apply_action(2 * 5)
        state.apply_action(3 * 5)

        state.apply_action(2 * 5)
        state.apply_action(3 * 5)

        state.apply_action(3 * 5)
        state.apply_action(spare_move)
        
        state.apply_action(3 * 5)

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")


    def test_rising_anti_diagonal(self):
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()
        # The anti-diagonal moves are 3, 6, 9, and 12
        spare_move = 1 # 1 is outside the diagonal

        # First moves
        state.apply_action((0 + 1) * 3)
        state.apply_action((1 + 1) * 3)

        state.apply_action((1 + 1) * 3)
        state.apply_action((2 + 1) * 3)

        state.apply_action((2 + 1) * 3)
        state.apply_action((3 + 1) * 3)

        state.apply_action((2 + 1) * 3)
        state.apply_action((3 + 1) * 3)

        state.apply_action((3 + 1) * 3)
        state.apply_action(spare_move)
        
        state.apply_action((3 + 1) * 3)

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

    def test_descending_diagonal(self):
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()

        # The diagonal moves are 0, 5, 10, and 15
        spare_move = 1 # 1 is outside the diagonal

        # First moves
        state.apply_action(3 * 5)
        state.apply_action(2 * 5)

        state.apply_action(2 * 5)
        state.apply_action(1 * 5)

        state.apply_action(1 * 5)
        state.apply_action(0 * 5)

        state.apply_action(1 * 5)
        state.apply_action(0 * 5)

        state.apply_action(0 * 5)
        state.apply_action(spare_move)
        
        state.apply_action(0 * 5)

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

    def test_descending_anti_diagonal(self):
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()
        # The anti-diagonal moves are 3, 6, 9, and 12
        spare_move = 1 # 1 is outside the diagonal

        # First moves
        state.apply_action((3 + 1) * 3)
        state.apply_action((2 + 1) * 3)

        state.apply_action((2 + 1) * 3)
        state.apply_action((1 + 1) * 3)

        state.apply_action((1 + 1) * 3)
        state.apply_action((0 + 1) * 3)

        state.apply_action((1 + 1) * 3)
        state.apply_action((0 + 1) * 3)

        state.apply_action((0 + 1) * 3)
        state.apply_action(spare_move)
        
        state.apply_action((0 + 1) * 3)

        self.assertTrue(state.is_terminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")

if __name__ == "__main__":
    absltest.main()