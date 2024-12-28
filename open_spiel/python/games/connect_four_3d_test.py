"""
Tests for Python Connect Four 3D
This program procedurally generates trivial games whose outcome is known.
This allows easier checking of termination conditions which were
"""


from absl.testing import absltest
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
        #print(f"{id}_vertical{file},{rank} 7 1.0")
        #id +=1
        game = pyspiel.load_game("python_connect_four_3d")
        state = game.new_initial_state()

        winning_move = move(file, rank)
        losing_move = move((file + 1) % 4, rank)
        for i in range(3):
            state.apply_action(winning_move)
            state.apply_action(losing_move)

        state.apply_action(winning_move)

        self.assertTrue(state.isTerminal(), "The game should be over!")
        self.assertEqual(state.returns(), [1.0, -1.0], "The returns should be 1.0 for P0 and -1.0 for P1")
    
    def test_vertical_win(self):
        for f in range(4):
            for r in range(4):
                self.vertical_win(f,r)



def file_win(file):
    """
    The two players fill-in a file in parallel. Player 0 (which
    is ahead) wins the game systematically.
    """
    global id
    print(f"{id}_file{file} 7 1.0")
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

def rank_win(rank):
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

def diagonal():
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

def anti_diagonal():
    """
    The two players repeat the same moves, allowing Player 0 to complete the diagonal on
    the first row. This is the anti-diagonal
    """
    game = pyspiel.load_game("python_connect_four_3d")
    state = game.new_initial_state()

    for i in range(3):
        m = move(3 - i, i)
        print(m) # Player 0 move
        print(m) # Player 1 move

    # Last move for Player 0
    i = 3
    m = move(3 - i, i)
    print(m)

def rising_file(file):
    game = pyspiel.load_game("python_connect_four_3d")
    state = game.new_initial_state()
    spare_file = (file + 1) % 4

    # First moves
    print(move(file, 0))

    print(move(file, 1))
    print(move(file, 1))

    print(move(file, 2))
    print(move(file, 2))

    print(move(file, 3))
    print(move(file, 2))

    print(move(file, 3))
    print(move(file, 3))
    print(move(spare_file, 0))
    print(move(file, 3))

def descending_file(file):
    game = pyspiel.load_game("python_connect_four_3d")
    state = game.new_initial_state()
    spare_file = (file + 1) % 4

    # First moves
    print(move(file, 3 - 0))
    print(move(file, 3 - 1))

    print(move(file, 3 - 1))
    print(move(file, 3 - 2))

    print(move(file, 3 - 2))
    print(move(file, 3 - 3))

    print(move(file, 3 - 2))
    print(move(file, 3 - 3))

    print(move(file, 3 - 3))
    print(move(spare_file, 0))

    print(move(file, 3 - 3))

def rising_rank(rank):
    game = pyspiel.load_game("python_connect_four_3d")
    state = game.new_initial_state()
    spare_rank = (rank + 1) % 4

    # First moves
    print(move(0, rank))

    print(move(1, rank))
    print(move(1, rank))

    print(move(2, rank))
    print(move(2, rank))

    print(move(3, rank))
    print(move(2, rank))

    print(move(3, rank))
    print(move(3, rank))
    print(move(0, spare_rank))
    print(move(3, rank))

def descending_rank(rank):
    game = pyspiel.load_game("python_connect_four_3d")
    state = game.new_initial_state()
    spare_rank = (rank + 1) % 4

    # First moves
    print(move(3 - 0, rank))

    print(move(3 - 1, rank))
    print(move(3 - 1, rank))
    print(move(3 - 2, rank))
    print(move(3 - 2, rank))
    print(move(3 - 3, rank))
    print(move(3 - 2, rank))
    print(move(3 - 3, rank))
    print(move(3 - 3, rank))
    print(move(3 - 0, spare_rank))
    print(move(3 - 3, rank))

def rising_diagonal():
    game = pyspiel.load_game("python_connect_four_3d")
    state = game.new_initial_state()
    # The diagonal moves are 0, 5, 10, and 15
    spare_move = 1 # 1 is outside the diagonal

    # First moves
    print(0 * 5)
    print(1 * 5)

    print(1 * 5)
    print(2 * 5)

    print(2 * 5)
    print(3 * 5)

    print(2 * 5)
    print(3 * 5)

    print(3 * 5)
    print(spare_move)
    
    print(3 * 5)

def rising_anti_diagonal():
    game = pyspiel.load_game("python_connect_four_3d")
    state = game.new_initial_state()
    # The anti-diagonal moves are 3, 6, 9, and 12
    spare_move = 1 # 1 is outside the diagonal

    # First moves
    print((0 + 1) * 3)
    print((1 + 1) * 3)

    print((1 + 1) * 3)
    print((2 + 1) * 3)

    print((2 + 1) * 3)
    print((3 + 1) * 3)

    print((2 + 1) * 3)
    print((3 + 1) * 3)

    print((3 + 1) * 3)
    print(spare_move)
    
    print((3 + 1) * 3)

def descending_diagonal():
    game = pyspiel.load_game("python_connect_four_3d")
    state = game.new_initial_state()

    # The diagonal moves are 0, 5, 10, and 15
    spare_move = 1 # 1 is outside the diagonal

    # First moves
    print(3 * 5)
    print(2 * 5)

    print(2 * 5)
    print(1 * 5)

    print(1 * 5)
    print(0 * 5)

    print(1 * 5)
    print(0 * 5)

    print(0 * 5)
    print(spare_move)
    
    print(0 * 5)

def descending_anti_diagonal():
    game = pyspiel.load_game("python_connect_four_3d")
    state = game.new_initial_state()
    # The anti-diagonal moves are 3, 6, 9, and 12
    spare_move = 1 # 1 is outside the diagonal

    # First moves
    print((3 + 1) * 3)
    print((2 + 1) * 3)

    print((2 + 1) * 3)
    print((1 + 1) * 3)

    print((1 + 1) * 3)
    print((0 + 1) * 3)

    print((1 + 1) * 3)
    print((0 + 1) * 3)

    print((0 + 1) * 3)
    print(spare_move)
    
    print((0 + 1) * 3)

def main():
    global id
    id = 0
    # Check pile victories
    for file in range(4):
       for rank in range(4):
           vertical_win(file,rank)

    # Check file victories (on the first row)
    for file in range(4):
        file_win(file)

    # Check rank victories (on the first row)
    for rank in range(4):
        rank_win(rank)

    # Check flat diagonals
    diagonal()
    anti_diagonal()

    # Rising files and ranks
    for file in range(4):
        rising_file(file)
        descending_file(file)

    for rank in range(4):
        rising_rank(rank)
        descending_rank(rank)

    # Check rising and descending diagonals
    rising_diagonal()
    rising_anti_diagonal()
    descending_diagonal()
    descending_anti_diagonal()

if __name__ == "__main__":
    absltest.main()