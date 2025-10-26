import tkinter as tk
from tkinter import messagebox
import random

# Board Config
BOARD_SIZE = 15
BOMB_COUNT = 30
STEP_LIMIT = 20

# Interface Config
COLOR_PANEL_BG = "#2C3E8F"      
COLOR_PANEL_FG = "#FFFFFF"      
COLOR_BTN_HOVER = "#4A69C6"     
COLOR_FLAG = "#7B9AF3"          
COLOR_CELL_HIDDEN = "#DCDCDC"    
COLOR_CELL_OPEN = "#FFFFFF"     
COLOR_GAME_BG = "#BDBDBD"       

FONT_CONTROL_BTN = ("Poppins", 11)        
FONT_STATUS_LABEL = ("Poppins", 12) 
FONT_CELL_NUMBER = ("Poppins", 10)      

NUMBER_COLOR_MAP = {
    1: "#0000FF",
    2: "#008000",
    3: "#FF0000",
    4: "#000080",
    5: "#800000",
    6: "#008080",
    7: "#000000",
    8: "#808080"
}

# Minesweeper Model
class MinesweeperGUI:
    """Main class for the Minesweeper game application."""

    def __init__(self, root):
        """Initializes the main window and frames."""
        self.root = root
        self.root.title("Minesweeper CSP vs CP (15x15)")
        self.root.configure(bg=COLOR_PANEL_BG)

        self.control_frame = tk.Frame(root, bg=COLOR_PANEL_BG)
        self.control_frame.pack(pady=10)

        self.game_frame = tk.Frame(root, bg=COLOR_GAME_BG)
        self.game_frame.pack(padx=10, pady=(0, 10))

        self.pixel_shim = tk.PhotoImage(width=1, height=1)

        self.setup_game()

    def setup_game(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        for widget in self.control_frame.winfo_children():
            widget.destroy()

        self.steps_left = STEP_LIMIT
        self.game_over = False
        self.bombs_flagged = 0
        self.cells_opened = 0
        self.board_logic = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board_status = [['H' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

        bombs_planted_count = 0
        while bombs_planted_count < BOMB_COUNT:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            if self.board_logic[row][col] == 0:
                self.board_logic[row][col] = -1
                bombs_planted_count += 1

        self.calculate_neighbor_numbers()
        self.create_control_widgets()
        self.create_grid_widgets()
        self.update_steps_display(count=0)

    def calculate_neighbor_numbers(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board_logic[r][c] == -1:
                    continue
                
                bomb_neighbors_count = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        neighbor_r, neighbor_c = r + i, c + j
                        if 0 <= neighbor_r < BOARD_SIZE and 0 <= neighbor_c < BOARD_SIZE and \
                           self.board_logic[neighbor_r][neighbor_c] == -1:
                            bomb_neighbors_count += 1
                self.board_logic[r][c] = bomb_neighbors_count

    def create_control_widgets(self):
        self.steps_label = tk.Label(self.control_frame, text=f"Steps Left: {self.steps_left}",
                                     font=FONT_STATUS_LABEL, bg=COLOR_PANEL_BG, fg=COLOR_PANEL_FG)
        self.steps_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.bombs_label = tk.Label(self.control_frame, text=f"Bombs: {self.bombs_flagged}/{BOMB_COUNT}",
                                     font=FONT_STATUS_LABEL, bg=COLOR_PANEL_BG, fg=COLOR_PANEL_FG)
        self.bombs_label.pack(side=tk.LEFT, padx=10, pady=5)

        tk.Label(self.control_frame, text="", bg=COLOR_PANEL_BG, padx=10).pack(side=tk.LEFT)

        button_style = {
            'font': FONT_CONTROL_BTN,
            'bg': COLOR_PANEL_FG,
            'fg': COLOR_PANEL_BG,
            'activebackground': COLOR_BTN_HOVER,
            'activeforeground': COLOR_PANEL_FG,
            'relief': tk.FLAT,
            'bd': 0,
            'padx': 10,
            'pady': 5
        }

        self.cp_button = tk.Button(self.control_frame, text="CP Solver",
                                    command=self.run_cp_solver, **button_style)
        self.cp_button.pack(side=tk.LEFT, padx=4)

        self.csp_button = tk.Button(self.control_frame, text="CSP Solver", state=tk.NORMAL,
                                     command=self.run_csp_solver, **button_style)
        self.csp_button.pack(side=tk.LEFT, padx=4)

        self.reset_button = tk.Button(self.control_frame, text="Reset",
                                      command=self.setup_game, **button_style)
        self.reset_button.pack(side=tk.LEFT, padx=(4, 10))

    def create_grid_widgets(self):
        self.buttons = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                button = tk.Button(self.game_frame, text=" ",
                                   font=FONT_CELL_NUMBER,
                                   bg=COLOR_CELL_HIDDEN,
                                   activebackground="#B0B0B0",
                                   relief=tk.FLAT,
                                   bd=0,
                                   image=self.pixel_shim, 
                                   width=28, 
                                   height=28,
                                   compound='center' 
                                  )

                button.bind("<Button-1>", lambda event, row=r, col=c: self.handle_left_click(row, col))
                button.bind("<Button-3>", lambda event, row=r, col=c: self.handle_right_click(row, col))

                button.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = button

    def update_steps_display(self, count=1):
        if self.game_over:
            return

        if count > 0:
            self.steps_left -= count

        self.steps_label.config(text=f"Steps Left: {self.steps_left}")

        if self.steps_left < (STEP_LIMIT * 0.2):
            self.steps_label.config(fg="#FF4040")
        elif self.steps_left < (STEP_LIMIT * 0.5):
            self.steps_label.config(fg="#FFA500")
        else:
            self.steps_label.config(fg=COLOR_PANEL_FG)

        if self.steps_left <= 0 and count > 0:
            self.game_over = True
            messagebox.showerror("Game Over", "Out of steps! All bombs exploded.")
            self.reveal_board(show_bombs=True)

    def handle_left_click(self, r, c):
        if self.game_over or self.board_status[r][c] != 'H':
            return

        self.update_steps_display()

        if self.board_logic[r][c] == -1:
            self.buttons[r][c].config(text="💣", bg="red", relief=tk.FLAT, state=tk.DISABLED)
            self.game_over = True
            messagebox.showerror("Game Over", "You clicked on a bomb!")
            self.reveal_board(show_bombs=True)
        else:
            self.open_cell_recursive(r, c)
            self.check_win_condition()

    def handle_right_click(self, r, c):
        if self.game_over:
            return

        if self.board_status[r][c] == 'H':
            self.board_status[r][c] = 'F'
            self.buttons[r][c].config(text="🚩", bg=COLOR_FLAG)
            self.bombs_flagged += 1
        elif self.board_status[r][c] == 'F':
            self.board_status[r][c] = 'H'
            self.buttons[r][c].config(text=" ", bg=COLOR_CELL_HIDDEN)
            self.bombs_flagged -= 1
        
        self.bombs_label.config(text=f"Bombs: {self.bombs_flagged}/{BOMB_COUNT}")

    def open_cell_recursive(self, r, c):
        if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
            return
        if self.board_status[r][c] != 'H':
            return

        self.board_status[r][c] = 'O'
        self.cells_opened += 1
        cell_value = self.board_logic[r][c]

        display_text = str(cell_value) if cell_value > 0 else ""
        text_color = NUMBER_COLOR_MAP.get(cell_value, "black")

        self.buttons[r][c].config(text=display_text,
                                  bg=COLOR_CELL_OPEN,
                                  relief=tk.FLAT,
                                  font=FONT_CELL_NUMBER,
                                  state=tk.DISABLED,
                                  disabledforeground=text_color)

        if cell_value == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    self.open_cell_recursive(r + i, c + j)

    def check_win_condition(self):
        if self.game_over:
            return
        
        if self.cells_opened == (BOARD_SIZE * BOARD_SIZE) - BOMB_COUNT:
            self.game_over = True
            messagebox.showinfo("Congratulations!", "You won!")
            self.reveal_board(show_flags=True)

    def reveal_board(self, show_bombs=False, show_flags=False):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board_status[r][c] == 'F':
                    if show_bombs and self.board_logic[r][c] != -1:
                        self.buttons[r][c].config(text="❌", bg="white", state=tk.DISABLED)
                    elif show_flags and self.board_logic[r][c] == -1:
                         self.buttons[r][c].config(text="🚩", bg="lightgreen", state=tk.DISABLED)
                    continue

                cell_value = self.board_logic[r][c]
                if cell_value == -1:
                    if show_bombs:
                        self.buttons[r][c].config(text="💣", bg="red", state=tk.DISABLED)
                    elif show_flags:
                         self.buttons[r][c].config(text="🚩", bg="lightgreen", state=tk.DISABLED)
                else:
                    display_text = str(cell_value) if cell_value > 0 else ""
                    text_color = NUMBER_COLOR_MAP.get(cell_value, "black")
                    self.buttons[r][c].config(text=display_text, bg=COLOR_CELL_OPEN,
                                              relief=tk.FLAT,
                                              font=FONT_CELL_NUMBER,
                                              state=tk.DISABLED,
                                              disabledforeground=text_color)

    # CP Solver

    def run_cp_solver(self):
        """Button handler for the 'CP Solver'."""
        if self.game_over:
            return
            
        if self.cells_opened == 0:
            while True:
                r = random.randint(0, BOARD_SIZE - 1)
                c = random.randint(0, BOARD_SIZE - 1)
                if self.board_logic[r][c] != -1:
                    self.safe_ai_click(r,c) 
                    self.update_steps_display() 
                    break
        
        def solve_loop_cp():
            if self.game_over:
                return

            change_made = self.cp_solver_step()
            self.root.update() 
            self.check_win_condition()
            
            if change_made and not self.game_over:
                self.root.after(500, solve_loop_cp) 
            elif not self.game_over:
                messagebox.showinfo("CP Solver", "CP Solver stuck. No more 100% certain moves found.")

        solve_loop_cp()

    def cp_solver_step(self):
        if self.game_over:
            return False
            
        change_made_in_step = False
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board_status[r][c] == 'O' and self.board_logic[r][c] > 0:
                    cell_value = self.board_logic[r][c]
                    
                    hidden_neighbors = []
                    flagged_neighbors_count = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0: continue
                            nr, nc = r + i, c + j
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                                if self.board_status[nr][nc] == 'H':
                                    hidden_neighbors.append((nr, nc))
                                elif self.board_status[nr][nc] == 'F':
                                    flagged_neighbors_count += 1
                    
                    if cell_value == (flagged_neighbors_count + len(hidden_neighbors)) and len(hidden_neighbors) > 0:
                        for (nr, nc) in hidden_neighbors:
                            self.board_status[nr][nc] = 'F'
                            self.buttons[nr][nc].config(text="🚩", bg=COLOR_FLAG)
                            self.bombs_flagged += 1
                            change_made_in_step = True
                        self.bombs_label.config(text=f"Bombs: {self.bombs_flagged}/{BOMB_COUNT}")

                    if cell_value == flagged_neighbors_count and len(hidden_neighbors) > 0:
                        for (nr, nc) in hidden_neighbors:
                            self.open_cell_recursive(nr, nc)
                            change_made_in_step = True
                            
        if change_made_in_step and not self.game_over:
            self.update_steps_display()
            
        return change_made_in_step

    # CSP Solver

    def run_csp_solver(self):
        """Button handler for the 'CSP Solver'."""
        if self.game_over:
            return
            
        if self.cells_opened == 0:
            while True:
                r = random.randint(0, BOARD_SIZE - 1)
                c = random.randint(0, BOARD_SIZE - 1)
                if self.board_logic[r][c] != -1:
                    self.safe_ai_click(r, c)
                    self.update_steps_display() 
                    break
            self.root.update()

        def solve_loop():
            if self.game_over:
                return

            cp_made_move = self.cp_solver_step()
            
            if cp_made_move:
                self.root.update()
                self.check_win_condition()
                if not self.game_over:
                    self.root.after(500, solve_loop) 
                return

            csp_made_move = self.csp_solver_1ply_step()

            if csp_made_move:
                self.root.update()
                self.check_win_condition()
                if not self.game_over:
                    self.root.after(750, solve_loop)
                return
            
            if not self.game_over:
                messagebox.showinfo("CSP Solver", "CSP Solver also stuck. Deeper search or guessing needed.")

        solve_loop()

    def csp_solver_1ply_step(self):
        frontier_cells = self.get_frontier_cells()
        
        for (r, c) in frontier_cells:
            
            if self.check_immediate_contradiction(r, c, is_assumed_bomb=False):
                self.board_status[r][c] = 'F'
                self.buttons[r][c].config(text="🚩", bg=COLOR_FLAG) 
                self.bombs_flagged += 1
                self.bombs_label.config(text=f"Bombs: {self.bombs_flagged}/{BOMB_COUNT}")
                if not self.game_over:
                    self.update_steps_display() 
                return True 

            if self.check_immediate_contradiction(r, c, is_assumed_bomb=True):
                self.safe_ai_click(r, c)
                if not self.game_over:
                    self.update_steps_display() 
                return True 

        return False

    def get_frontier_cells(self):
        frontier = set()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board_status[r][c] == 'O' and self.board_logic[r][c] > 0:
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0: continue
                            nr, nc = r + i, c + j
                            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and self.board_status[nr][nc] == 'H':
                                frontier.add((nr, nc))
        return list(frontier)

    def check_immediate_contradiction(self, test_r, test_c, is_assumed_bomb):
        for i_n in range(-1, 2):
            for j_n in range(-1, 2):
                if i_n == 0 and j_n == 0: continue
                
                neighbor_r, neighbor_c = test_r + i_n, test_c + j_n
                
                if not (0 <= neighbor_r < BOARD_SIZE and 0 <= neighbor_c < BOARD_SIZE and \
                        self.board_status[neighbor_r][neighbor_c] == 'O' and \
                        self.board_logic[neighbor_r][neighbor_c] > 0):
                    continue
                
                number_cell_value = self.board_logic[neighbor_r][neighbor_c]
                
                hidden_count_around_num = 0
                flag_count_around_num = 0
                for i_nn in range(-1, 2):
                    for j_nn in range(-1, 2):
                        if i_nn == 0 and j_nn == 0: continue
                        
                        nn_r, nn_c = neighbor_r + i_nn, neighbor_c + j_nn
                        
                        if 0 <= nn_r < BOARD_SIZE and 0 <= nn_c < BOARD_SIZE:
                            if self.board_status[nn_r][nn_c] == 'F':
                                flag_count_around_num += 1
                            elif nn_r == test_r and nn_c == test_c: 
                                if is_assumed_bomb:
                                    flag_count_around_num += 1
                                else:
                                    pass 
                            elif self.board_status[nn_r][nn_c] == 'H':
                                hidden_count_around_num += 1
                
                if flag_count_around_num > number_cell_value:
                    return True 

                if (flag_count_around_num + hidden_count_around_num) < number_cell_value:
                    return True 

        return False
        
    def safe_ai_click(self, r, c):
        if self.game_over or self.board_status[r][c] != 'H':
            return 
        
        if self.board_logic[r][c] == -1:
            print(f"CSP ERROR: Attempted to open a bomb at [{r},{c}]")
            return
        else:
            self.open_cell_recursive(r, c)

# Main Program Execution
if __name__ == "__main__":
    """Main entry point for the application."""
    root = tk.Tk()
    app = MinesweeperGUI(root)
    root.mainloop()
