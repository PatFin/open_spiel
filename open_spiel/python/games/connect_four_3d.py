
import numpy as np

from open_spiel.python.observation import IIGObserverForPublicInfoGame
import pyspiel

_NUM_PLAYERS = 2
_BOARD_FILES = 4
_BOARD_HEIGHT = 4
_BOARD_RANKS = 4
_MAX_GAME_LENGTH = _BOARD_FILES * _BOARD_RANKS * _BOARD_HEIGHT
_NB_POSSIBLE_ACTIONS = _BOARD_FILES * _BOARD_RANKS

_GAME_TYPE = pyspiel.GameType(
    short_name="python_connect_four_3d",
    long_name="Python Connect Four 3D",
    dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
    chance_mode=pyspiel.GameType.ChanceMode.DETERMINISTIC,
    information=pyspiel.GameType.Information.PERFECT_INFORMATION,
    utility=pyspiel.GameType.Utility.ZERO_SUM,
    reward_model=pyspiel.GameType.RewardModel.TERMINAL,
    max_num_players=_NUM_PLAYERS,
    min_num_players=_NUM_PLAYERS,
    provides_information_state_string=True,
    provides_information_state_tensor=True,
    provides_observation_string=True,
    provides_observation_tensor=True,
    provides_factored_observation_string=True)

_GAME_INFO = pyspiel.GameInfo(
    num_distinct_actions=_NB_POSSIBLE_ACTIONS,
    max_chance_outcomes=0,
    num_players=_NUM_PLAYERS,
    min_utility=-1.0,
    max_utility=1.0,
    utility_sum=0.0,
    max_game_length= _MAX_GAME_LENGTH) # If all the pieces are placed and a draw is reached


class Connect4_3D_Game(pyspiel.Game):
    """A Python version of 3D connect 4."""

    def __init__(self, params=None):
        super().__init__(_GAME_TYPE,_GAME_INFO, params or dict())

    def new_initial_state(self):
        """Returns a state corresponding to the start of a game."""
        return Connect4_3D_State(self)
    
    def make_py_observer(self, iig_obs_type=None, params=None):
        """Returns an object used for observing game state."""
        if ((iig_obs_type is None) or \
             (iig_obs_type.public_info and not iig_obs_type.perfect_recall)):
            return Connect4_3D_Observer(params)
        else:
            return IIGObserverForPublicInfoGame(iig_obs_type, params)
    
class Connect4_3D_State(pyspiel.State):
    "A python version of the 3D connect 4 state."

    def __init__(self, game):
        super().__init__(game)
        self.board = np.full((_BOARD_HEIGHT, _BOARD_RANKS, _BOARD_FILES), ".")
        self._is_terminal = False
        self._cur_player = 0
        self._player0_score = 0
    
    def current_player(self):
        """Returns id of the next player to move, or TERMINAL if game is over."""
        return pyspiel.PlayerId.TERMINAL if self._is_terminal else self._cur_player

    def _legal_actions(self, player):
        """Return a list of legal actions, sorted in ascending order."""
        # Move is allowed if the last row at the specified file and rank is still empty
        return [a for a in range(_NB_POSSIBLE_ACTIONS) if self.board[_BOARD_HEIGHT-1, a//4, a%4] == "."]

    def next_row(self, file, rank):
        """Utility function to detect which row the piece should be placed"""
        for row in range(_BOARD_HEIGHT):
            if np.char.equal(self.board[row, file, rank],"."):
                return row
        self.print_board()
        raise ValueError(f"Could not find empty row for file/rank {file}/{rank}")
        

    def _line_exists(self, row, file, rank):
        """
        Checks if the last play resulted in a line being created.
        row: the row (height on the board) on which the last play was made
        file: file the file on which the last play was made
        rank: rank on which the last play was made
        """
        # Check for file / rank / row victories
        b = self.board
        s = str(b[row, file, rank])
        #print(f"Play {s} in {row}, {file}, {rank}")
        
        def checkPile(pile):
            for e in pile:
                if not np.char.equal(e, s):
                    return False
            return True

        #print(f"Board shape is {board.shape}")
        # Check if piling on this pole results in a win
        if checkPile([b[i, file, rank] for i in range(_BOARD_HEIGHT)]) or \
            checkPile([b[row, j, rank] for j in range(_BOARD_FILES)]) or \
            checkPile([b[row, file, k] for k in range(_BOARD_RANKS)]):
            return True
        
        # Check with rising rows
        if row == file and checkPile([b[i,i,rank] for i in range(_BOARD_RANKS)]):
            return True

        # Check with decreasing rows
        if row == 3 - file and checkPile([b[_BOARD_HEIGHT-1-i,i,rank] for i in range(_BOARD_RANKS)]):
            return True

        # Check with rising rows
        if row == rank and checkPile([b[i,file,i] for i in range(_BOARD_FILES)]):
            return True

        # Check with decreasing rows
        if row == 3 - rank and checkPile([b[_BOARD_HEIGHT-1-i, file, i] for i in range(_BOARD_RANKS)]):
            return True

        # Now, on to the diagonals through the middle of the board
        if rank == file:
            # Need to check the diagonal at constant row
            if checkPile([b[row, i, i] for i in range(_BOARD_RANKS)]):
                return True
            # Check for rising diagonal
            if (rank == row) and checkPile([b[i, i, i] for i in range(_BOARD_RANKS)]):
                return True
            # Check for descending diagonal
            if (rank == 3-row) and checkPile(b[_BOARD_HEIGHT-1-i, i, i] for i in range(_BOARD_HEIGHT)):
                return True

        if rank + file == 3:
            # Check the diagonal at constant row
            if checkPile([b[row, i, _BOARD_RANKS - 1 - i] for i in range(_BOARD_FILES)]):
                return True

            # Check for rising anti diagonal
            if (file == row) and checkPile([b[i,i,_BOARD_RANKS - 1 - i] for i in range(_BOARD_FILES)]):
                return True

            # Check for descending anti diagonal
            if (rank == row) and checkPile([b[_BOARD_HEIGHT-1-i, i, _BOARD_RANKS-1-i] for i in range(_BOARD_FILES)]):
                return True

        return False

    def _apply_action(self, action):
        """Applies the specified action to the state"""
        file, rank = action//4, action%4
        row = self.next_row(file, rank)

        self.board[row, file, rank] = "o" if self._cur_player == 0 else "x"

        if self._line_exists(row, file, rank):
            self._is_terminal = True
            self._player0_score = 1.0 if self._cur_player == 0 else -1.0
        elif all(self.board.ravel() != "."):
            # There are no more empty cells
            self._is_terminal = True
            self._player0_score = 0.0
        else:
            self._cur_player = 1 - self._cur_player

    def __str__(self):
        return _board_to_string(self.board)
    
    def is_terminal(self):
        return self._is_terminal
    
    def returns(self):
        """Total reward for each player over the course of the game so far."""
        return [self._player0_score, -self._player0_score]
    
    def _action_to_string(self, player, action):
        """Action -> string."""
        file, rank = action // _BOARD_FILES, action % _BOARD_RANKS
        row = self.next_row(file, rank)
        return f"{action}({row},{file},{rank})"

class Connect4_3D_Observer:
    """An observer that conforms to the PyObserver interface (observation.py)."""

    def __init__(self, params):
        """Initializes an empty observation tensor."""
        if params:
            raise ValueError(f"Observation parameters not supported; passed {params}")
        # The observation should contain a 1-D tensor in `self.tensor` and a 
        # dictionary of views onto the tensor, which may be of any shape.
        # Here the observation is indexed `(cell state, row, column)`.
        shape = (1+ _NUM_PLAYERS, _BOARD_RANKS, _BOARD_FILES, _BOARD_HEIGHT)
        self.tensor = np.zeros(np.prod(shape), np.float32)
        self.dict = {"observation": np.reshape(self.tensor, shape)}
        # TODO not certain the shape of the tensor is appropriate (why 3 times the board cells ?)

    def set_from(self, state, player):
        """Updates the `tensor` and `dict` to reflect the `state` from the PoV of `player`."""
        del player # Why? I guess the player is not needed in the implementation

        obs = self.dict["observation"]
        obs.fill(0)
        for row in range(_BOARD_HEIGHT):
            for file in range(_BOARD_FILES):
                for rank in range(_BOARD_RANKS):
                    cell_state = ".ox".index(state.board[row, file, rank]) # pick the corresponding character
                    obs[cell_state, row, file, rank] = 1 # this I don't understand
    
    def string_from(self, state, player):
        """Observation of `state` from the point of view of `player`, as a string."""
        del player
        return _board_to_string(state.board)

def _board_to_string(board):
    """Returns a string representation of the board."""
    slices = []
    b = np.flip(board,0)
    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            for k in range(b.shape[2]):
                slices.append(f"{b[i, j, k]}")
            slices.append("\n")
        slices.append("\n")
    return "".join(slices)

def main():
    # Initialize the board
    game = Connect4_3D_Game()
    board = Connect4_3D_State(game)

    print(board)

    while not board.is_terminal():
        player = board.current_player
        legal_actions = board._legal_actions(player)
        action = int(input(f"Player {board._cur_player} next move among {legal_actions}:"))

        if action not in legal_actions:
            continue # ignore this pick and ask for another in the next iteration

        board._apply_action(action)

        file = action%4
        rank = action//4

        print(board)

    # Print the result of the game
    if 0.0 < board._player0_score:
        print("Player 0 wins!")
    elif 0.0 > board._player0_score:
        print("Player 1 wins!")
    else:
        print("It's a draw!")

pyspiel.register_game(_GAME_TYPE, Connect4_3D_Game)

if __name__ == "__main__":
    main()
