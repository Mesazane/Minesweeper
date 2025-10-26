# Minesweeper with CP and CSP Solver

# Board Config (Default)
BOARD_SIZE = 15

DEFAULT_BOMB_COUNT = 30

STEP_LIMIT = 20


## Configuration & Testing

To test the solver under different conditions or adjust the game difficulty, you can modify the following constants at the **top** of the `game.py` file:

* `BOARD_SIZE`: Sets the grid size (default is `15` for 15x15).
* `DEFAULT_BOMB_COUNT`: Determines the default number of bombs on the board.
* `STEP_LIMIT`: Sets the maximum number of steps allowed before the game ends (default is `20`).

To change the bomb values from the drop down, navigate to 6 lines below the `Bomb selection dropdown` comment and change the values accordingly.
