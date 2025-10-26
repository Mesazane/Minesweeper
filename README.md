# Minesweeper

# Board Config (Default)
BOARD_SIZE = 15

BOMB_COUNT = 30

STEP_LIMIT = 20


## Configuration & Testing

To test the solver under different conditions or adjust the game difficulty, you can modify the following constants at the **top** of the `game.py` file:

* `BOARD_SIZE`: Sets the grid size (default is `15` for 15x15).
* `BOMB_COUNT`: Determines the number of bombs on the board (default is `30`).
* `STEP_LIMIT`: Sets the maximum number of steps allowed before the game ends (default is `20`).

Feel free to change `BOMB_COUNT` and `STEP_LIMIT` to experiment. For example:

* **Easier Test:** Increase `BOMB_COUNT` (e.g., to `20`).
* **Harder Test:** Increase `BOMB_COUNT` (e.g., to `50`).
