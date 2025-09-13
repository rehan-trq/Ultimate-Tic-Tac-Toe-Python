import tkinter as tk
import random
import copy
import time
from tkinter import messagebox, font

class UltimateTicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ultimate Tic-Tac-Toe")
        self.root.configure(bg="#2d2d30")
        
        # Game state initialization
        self.board = [[[[' ' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.small_board_status = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.next_board = None  # (row, col) of next small board, None if any is valid
        self.game_over = False
        self.winner = None
        
        # AI configuration
        self.player_mode = "Human vs AI"  # Starting game mode
        self.ai_difficulty = "Medium"     # Starting difficulty
        
        # Custom color scheme
        self.bg_color = "#1e1e2e"         # Dark background
        self.board_color = "#282a36"      # Slightly lighter board
        self.x_color = "#5fb878"          # Green for X
        self.o_color = "#608cba"          # Blue for O
        self.highlight_color = "#6272a4"  # Yellow highlight
        self.won_board_colors = {
            'X': "#5fb878",
            'O': "#608cba",
            'D': "#7a7a7a",  # Gray for draws
            ' ': "#4a4a4a"   # Darker gray for empty
        }
        
        # Create main frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Create control panel
        self.control_frame = tk.Frame(self.main_frame, bg=self.bg_color, pady=10)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Game mode selection
        self.mode_label = tk.Label(self.control_frame, text="Mode:", bg=self.bg_color, fg="white")
        self.mode_label.pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value=self.player_mode)
        self.mode_menu = tk.OptionMenu(self.control_frame, self.mode_var, 
                                      "Human vs Human", "Human vs AI", "AI vs AI",
                                      command=self.change_mode)
        self.mode_menu.config(bg="#444", fg="white", activebackground="#555", activeforeground="white")
        self.mode_menu["menu"].config(bg="#444", fg="white", activebackground="#555", activeforeground="white")
        self.mode_menu.pack(side=tk.LEFT, padx=5)
        
        # AI difficulty settings
        self.difficulty_label = tk.Label(self.control_frame, text="AI Level:", bg=self.bg_color, fg="white")
        self.difficulty_label.pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value=self.ai_difficulty)
        self.difficulty_menu = tk.OptionMenu(self.control_frame, self.difficulty_var, 
                                           "Easy", "Medium", "Hard", "CSP",
                                           command=self.change_difficulty)
        self.difficulty_menu.config(bg="#444", fg="white", activebackground="#555", activeforeground="white")
        self.difficulty_menu["menu"].config(bg="#444", fg="white", activebackground="#555", activeforeground="white")
        self.difficulty_menu.pack(side=tk.LEFT, padx=5)
        
        # New game button
        self.reset_button = tk.Button(self.control_frame, text="New Game", command=self.reset_game,
                                    bg="#608cba", fg="white", activebackground="#4a6e94", padx=10)
        self.reset_button.pack(side=tk.RIGHT, padx=5)
        
        # Status display
        self.status_frame = tk.Frame(self.main_frame, bg=self.bg_color, pady=10)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status message
        self.status_var = tk.StringVar(value="Player X's turn")
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                                  bg=self.bg_color, fg="white", font=("Arial", 14))
        self.status_label.pack(expand=True)
        
        # Game board container
        self.game_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.game_frame.pack(expand=True, pady=10)
        
        # Create the game board UI
        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                # Frame for each 3x3 small board
                board_frame = tk.Frame(self.game_frame, bg=self.board_color, padx=5, pady=5,
                                     highlightbackground="#666", highlightthickness=1)
                board_frame.grid(row=i, column=j, padx=5, pady=5)
                
                small_board_buttons = []
                for m in range(3):
                    row_small_buttons = []
                    for n in range(3):
                        btn = tk.Button(board_frame, text=' ', width=3, height=1, font=('Arial', 14),
                                       bg="#f0f0f0", command=lambda i=i, j=j, m=m, n=n: self.make_move(i, j, m, n))
                        btn.grid(row=m, column=n, padx=1, pady=1)
                        row_small_buttons.append(btn)
                    small_board_buttons.append(row_small_buttons)
                row_buttons.append(small_board_buttons)
            self.buttons.append(row_buttons)
        
        # Initialize board highlighting
        self.update_board_highlighting()
    
    def change_mode(self, mode):
        """Change the game mode between human and AI players"""
        self.player_mode = mode
        self.reset_game()
    
    def change_difficulty(self, difficulty):
        """Update the AI difficulty level"""
        self.ai_difficulty = difficulty
    
    def reset_game(self):
        """Start a new game with fresh state"""
        # Reset all game state variables
        self.board = [[[[' ' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.small_board_status = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.next_board = None
        self.game_over = False
        self.winner = None
        
        # Reset all UI buttons
        for i in range(3):
            for j in range(3):
                for m in range(3):
                    for n in range(3):
                        self.buttons[i][j][m][n].config(text=' ', bg="#f0f0f0", state=tk.NORMAL)
                
                # Reset small board background colors
                self.buttons[i][j][0][0].master.config(bg=self.board_color)
        
        # Update status message
        self.status_var.set("Player X's turn")
        
        # Update board highlighting
        self.update_board_highlighting()
        
        # Start AI if needed
        if self.player_mode != "Human vs Human" and self.current_player == 'O':
            self.root.after(500, self.make_ai_move)
        elif self.player_mode == "AI vs AI":
            self.root.after(500, self.make_ai_move)
    
    def update_board_highlighting(self):
        """Update the visual highlighting of boards based on game state"""
        # Reset all board highlights
        for i in range(3):
            for j in range(3):
                board_frame = self.buttons[i][j][0][0].master
                
                if self.small_board_status[i][j] != ' ':
                    # Board is won or drawn
                    board_frame.config(bg=self.won_board_colors[self.small_board_status[i][j]])
                elif self.next_board is None or (self.next_board[0] == i and self.next_board[1] == j):
                    # Board is active for next move
                    board_frame.config(bg=self.highlight_color)
                else:
                    # Board is inactive
                    board_frame.config(bg=self.board_color)
    
    def check_small_board_win(self, i, j):
        """Check if a small board has been won or drawn"""
        board = self.board[i][j]
        
        # Check rows for win
        for row in range(3):
            if board[row][0] != ' ' and board[row][0] == board[row][1] == board[row][2]:
                return board[row][0]
        
        # Check columns for win
        for col in range(3):
            if board[0][col] != ' ' and board[0][col] == board[1][col] == board[2][col]:
                return board[0][col]
        
        # Check diagonals for win
        if board[0][0] != ' ' and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] != ' ' and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
        
        # Check if board is full (draw)
        is_full = True
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    is_full = False
                    break
            if not is_full:
                break
        
        if is_full:
            return 'D'  # Draw
        
        return ' '  # Game continues
    
    def check_big_board_win(self):
        """Check if the overall game has been won or drawn"""
        # Check rows
        for row in range(3):
            if self.small_board_status[row][0] != ' ' and self.small_board_status[row][0] != 'D' and \
               self.small_board_status[row][0] == self.small_board_status[row][1] == self.small_board_status[row][2]:
                return self.small_board_status[row][0]
        
        # Check columns
        for col in range(3):
            if self.small_board_status[0][col] != ' ' and self.small_board_status[0][col] != 'D' and \
               self.small_board_status[0][col] == self.small_board_status[1][col] == self.small_board_status[2][col]:
                return self.small_board_status[0][col]
        
        # Check diagonals
        if self.small_board_status[0][0] != ' ' and self.small_board_status[0][0] != 'D' and \
           self.small_board_status[0][0] == self.small_board_status[1][1] == self.small_board_status[2][2]:
            return self.small_board_status[0][0]
        if self.small_board_status[0][2] != ' ' and self.small_board_status[0][2] != 'D' and \
           self.small_board_status[0][2] == self.small_board_status[1][1] == self.small_board_status[2][0]:
            return self.small_board_status[0][2]
        
        # Check if big board is full (draw)
        is_full = True
        for row in range(3):
            for col in range(3):
                if self.small_board_status[row][col] == ' ':
                    is_full = False
                    break
            if not is_full:
                break
        
        if is_full:
            return 'D'  # Draw
        
        return None  # Game continues
    
    def is_valid_move(self, i, j, m, n):
        """Check if a move is valid according to game rules"""
        # Game over check
        if self.game_over:
            return False
        
        # Cell must be empty
        if self.board[i][j][m][n] != ' ':
            return False
        
        # Must play in the correct small board if specified
        if self.next_board is not None and (i, j) != self.next_board:
            return False
        
        # Can't play in a completed board
        if self.small_board_status[i][j] != ' ':
            return False
        
        return True
    
    def make_move(self, i, j, m, n):
        """Handle a player's move attempt"""
        if not self.is_valid_move(i, j, m, n):
            return False
        
        # Check if it's a human player's turn
        if ((self.current_player == 'X' and self.player_mode in ["Human vs Human", "Human vs AI"]) or
            (self.current_player == 'O' and self.player_mode == "Human vs Human")):
            pass  # Allow human move
        else:
            return False  # Not human's turn
        
        # Execute the move
        self.execute_move(i, j, m, n)
        
        # Trigger AI's turn if needed
        if not self.game_over and ((self.current_player == 'O' and self.player_mode == "Human vs AI") or 
                                  self.player_mode == "AI vs AI"):
            self.root.after(500, self.make_ai_move)
        
        return True
    
    def execute_move(self, i, j, m, n):
        """Execute a move and update game state"""
        # Update the board state
        self.board[i][j][m][n] = self.current_player
        
        # Update the button display
        button = self.buttons[i][j][m][n]
        button.config(text=self.current_player, 
                     bg=self.x_color if self.current_player == 'X' else self.o_color,
                     state=tk.DISABLED)
        
        # Check if this move won a small board
        small_win = self.check_small_board_win(i, j)
        if small_win != ' ':
            self.small_board_status[i][j] = small_win
            
            # Update small board visuals
            if small_win != 'D':
                board_frame = self.buttons[i][j][0][0].master
                board_frame.config(bg=self.won_board_colors[small_win])
        
        # Determine which board is playable next
        if self.small_board_status[m][n] == ' ':
            self.next_board = (m, n)
        else:
            self.next_board = None  # Can play anywhere
        
        # Check for overall win
        big_win = self.check_big_board_win()
        if big_win:
            self.game_over = True
            self.winner = big_win
            if big_win == 'D':
                self.status_var.set("Game Over: It's a Draw!")
            else:
                self.status_var.set(f"Game Over: Player {big_win} Wins!")
            return
        
        # Switch to next player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        # Update status message
        if self.next_board:
            self.status_var.set(f"Player {self.current_player}'s turn in board ({self.next_board[0]+1}, {self.next_board[1]+1})")
        else:
            self.status_var.set(f"Player {self.current_player}'s turn (any board)")
        
        # Update board highlighting
        self.update_board_highlighting()
    
    def get_legal_moves(self):
        """Get all valid moves in the current game state"""
        legal_moves = []
        
        if self.next_board:
            # Must play in the specified board
            i, j = self.next_board
            for m in range(3):
                for n in range(3):
                    if self.board[i][j][m][n] == ' ':
                        legal_moves.append((i, j, m, n))
        else:
            # Can play in any active board
            for i in range(3):
                for j in range(3):
                    if self.small_board_status[i][j] == ' ':
                        for m in range(3):
                            for n in range(3):
                                if self.board[i][j][m][n] == ' ':
                                    legal_moves.append((i, j, m, n))
        
        return legal_moves
    
    def make_ai_move(self):
        """Execute AI's turn based on selected difficulty"""
        if self.game_over:
            return
        
        # Select AI algorithm based on difficulty
        if self.ai_difficulty == "Easy":
            move = self.ai_easy_move()
        elif self.ai_difficulty == "Medium":
            move = self.ai_medium_move()
        elif self.ai_difficulty == "Hard":
            move = self.ai_smart_move()
        else:
            solver = UltimateTicTacToeCSP(self)
            solver.ac3()
            # 2) do full backtracking search
            assignment = solver.backtracking_search()
            # 3) pick the very first variable assigned (MRV order) as your move
            if assignment:
                move = next(iter(assignment.keys()))
            else:
                move = None
        
        if move:
            i, j, m, n = move
            self.execute_move(i, j, m, n)
            
            # If AI vs AI mode, schedule next AI move
            if self.player_mode == "AI vs AI" and not self.game_over:
                self.root.after(500, self.make_ai_move)
    
    def ai_easy_move(self):
        """Easy AI: Random valid move selection"""
        legal_moves = self.get_legal_moves()
        if legal_moves:
            return random.choice(legal_moves)
        return None
    
    def ai_medium_move(self):
        """Medium AI: Basic strategic decision making"""
        legal_moves = self.get_legal_moves()
        if not legal_moves:
            return None
        
        # First priority: Check if AI can win any small board
        for move in legal_moves:
            i, j, m, n = move
            # Try the move
            self.board[i][j][m][n] = self.current_player
            win = self.check_small_board_win(i, j)
            # Undo the move
            self.board[i][j][m][n] = ' '
            
            if win == self.current_player:
                return move
        
        # Second priority: Block opponent from winning a small board
        opponent = 'X' if self.current_player == 'O' else 'O'
        for move in legal_moves:
            i, j, m, n = move
            # Check if opponent would win here
            self.board[i][j][m][n] = opponent
            win = self.check_small_board_win(i, j)
            # Undo the test move
            self.board[i][j][m][n] = ' '
            
            if win == opponent:
                return move
        
        # Third priority: Play in the center when possible
        center_moves = [move for move in legal_moves if move[2] == 1 and move[3] == 1]
        if center_moves:
            return random.choice(center_moves)
        
        # Fourth priority: Play in corners
        corner_moves = [move for move in legal_moves if 
                       (move[2] == 0 and move[3] == 0) or 
                       (move[2] == 0 and move[3] == 2) or 
                       (move[2] == 2 and move[3] == 0) or 
                       (move[2] == 2 and move[3] == 2)]
        if corner_moves:
            return random.choice(corner_moves)
        
        # Final fallback: random move
        return random.choice(legal_moves)
    
    def ai_smart_move(self):
        """Advanced AI using minimax with constraints and pruning"""
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        depth = 3  # Search depth - higher is smarter but slower
        
        legal_moves = self.get_legal_moves()
        # Optimize move ordering for better pruning
        legal_moves = self.order_moves(legal_moves)
        
        for move in legal_moves:
            i, j, m, n = move
            # Save current state
            board_copy = copy.deepcopy(self.board)
            status_copy = copy.deepcopy(self.small_board_status)
            next_board_copy = self.next_board
            player_copy = self.current_player
            
            # Try this move
            self.board[i][j][m][n] = self.current_player
            
            # Update game state
            small_win = self.check_small_board_win(i, j)
            if small_win != ' ':
                self.small_board_status[i][j] = small_win
            
            # Update next board
            if self.small_board_status[m][n] == ' ':
                self.next_board = (m, n)
            else:
                self.next_board = None
            
            # Switch player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            # Evaluate this move with minimax
            score = self.minimax(depth - 1, alpha, beta, False)
            
            # Restore original state
            self.board = board_copy
            self.small_board_status = status_copy
            self.next_board = next_board_copy
            self.current_player = player_copy
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break  # Alpha-beta pruning
        
        return best_move
    
    def order_moves(self, moves):
        """Sort moves for better alpha-beta pruning efficiency"""
        # Group moves by strategic value
        center_moves = []
        corner_moves = []
        edge_moves = []
        
        for move in moves:
            i, j, m, n = move
            # Centers are highest priority
            if m == 1 and n == 1:
                center_moves.append(move)
            # Corners are second priority
            elif (m == 0 and n == 0) or (m == 0 and n == 2) or (m == 2 and n == 0) or (m == 2 and n == 2):
                corner_moves.append(move)
            # Edges are lowest priority
            else:
                edge_moves.append(move)
        
        # Further sort moves by how constrained the resulting board would be
        def constraint_key(move):
            _, _, m, n = move
            # More filled cells means more constrained (better for pruning)
            filled_count = 0
            if self.small_board_status[m][n] == ' ':
                for r in range(3):
                    for c in range(3):
                        if self.board[m][n][r][c] != ' ':
                            filled_count += 1
                return -filled_count  # Negative so more filled = higher priority
            return 0
            
        # Sort each group by constraints
        center_moves.sort(key=constraint_key)
        corner_moves.sort(key=constraint_key)
        edge_moves.sort(key=constraint_key)
        
        # Return ordered list with best moves first
        return center_moves + corner_moves + edge_moves
    
    def minimax(self, depth, alpha, beta, is_maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        # Terminal condition check
        big_win = self.check_big_board_win()
        if big_win:
            if big_win == 'X':
                return 100 + depth  # X wins (depth bonus for quicker wins)
            elif big_win == 'O':
                return -100 - depth  # O wins (depth penalty for later losses)
            else:
                return 0  # Draw
        
        # Depth limit reached - evaluate board
        if depth == 0:
            return self.evaluate_board()
        
        legal_moves = self.get_legal_moves()
        
        # Optimize move ordering for deeper levels
        if len(legal_moves) > 5:
            legal_moves = self.filter_promising_moves(legal_moves)
        
        # Order remaining moves for efficiency
        legal_moves = self.order_moves(legal_moves)
        
        if is_maximizing:
            # Maximizing player's turn
            max_eval = float('-inf')
            for move in legal_moves:
                i, j, m, n = move
                # Save state
                board_copy = copy.deepcopy(self.board)
                status_copy = copy.deepcopy(self.small_board_status)
                next_board_copy = self.next_board
                player_copy = self.current_player
                
                # Make move
                self.board[i][j][m][n] = self.current_player
                
                # Update small board status
                small_win = self.check_small_board_win(i, j)
                if small_win != ' ':
                    self.small_board_status[i][j] = small_win
                
                # Update next board
                if self.small_board_status[m][n] == ' ':
                    self.next_board = (m, n)
                else:
                    self.next_board = None
                
                # Switch player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                
                # Recursive evaluation
                eval_score = self.minimax(depth - 1, alpha, beta, False)
                
                # Restore state
                self.board = board_copy
                self.small_board_status = status_copy
                self.next_board = next_board_copy
                self.current_player = player_copy
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, max_eval)
                if alpha >= beta:
                    break  # Beta cutoff
            
            return max_eval
        else:
            # Minimizing player's turn
            min_eval = float('inf')
            for move in legal_moves:
                i, j, m, n = move
                # Save state
                board_copy = copy.deepcopy(self.board)
                status_copy = copy.deepcopy(self.small_board_status)
                next_board_copy = self.next_board
                player_copy = self.current_player
                
                # Make move
                self.board[i][j][m][n] = self.current_player
                
                # Update small board status
                small_win = self.check_small_board_win(i, j)
                if small_win != ' ':
                    self.small_board_status[i][j] = small_win
                
                # Update next board
                if self.small_board_status[m][n] == ' ':
                    self.next_board = (m, n)
                else:
                    self.next_board = None
                
                # Switch player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                
                # Recursive evaluation
                eval_score = self.minimax(depth - 1, alpha, beta, True)
                
                # Restore state
                self.board = board_copy
                self.small_board_status = status_copy
                self.next_board = next_board_copy
                self.current_player = player_copy
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def filter_promising_moves(self, moves):
        """Filter moves to consider only the most promising ones"""
        promising_moves = []
        for move in moves:
            i, j, m, n = move
            # Include moves that send to completed boards
            if self.small_board_status[m][n] != ' ':
                promising_moves.append(move)
                continue
            
            # Count opponent's options in the next board
            open_cells = 0
            for r in range(3):
                for c in range(3):
                    if self.board[m][n][r][c] == ' ':
                        open_cells += 1
            
            # Moves that constrain opponent are promising
            if open_cells <= 3:
                promising_moves.append(move)
            
            # Moves that create alignment opportunities are promising
            self.board[i][j][m][n] = self.current_player
            if self.check_potential_win(i, j, self.current_player):
                promising_moves.append(move)
            self.board[i][j][m][n] = ' '
        
        # If filtering was too aggressive, keep original moves
        return promising_moves if promising_moves else moves
    
    def check_potential_win(self, i, j, player):
        """Check if a move creates a two-in-a-row with empty cell"""
        board = self.board[i][j]
        
        # Check rows
        for row in range(3):
            if (board[row].count(player) == 2 and board[row].count(' ') == 1):
                return True
        
        # Check columns
        for col in range(3):
            column = [board[0][col], board[1][col], board[2][col]]
            if column.count(player) == 2 and column.count(' ') == 1:
                return True
        
        # Check diagonals
        diag1 = [board[0][0], board[1][1], board[2][2]]
        diag2 = [board[0][2], board[1][1], board[2][0]]
        
        if diag1.count(player) == 2 and diag1.count(' ') == 1:
            return True
        if diag2.count(player) == 2 and diag2.count(' ') == 1:
            return True
        
        return False
    
    def evaluate_board(self):
        """Evaluates the current board state and returns a score."""
        # Check if game is already won
        big_win = self.check_big_board_win()
        if big_win == 'X':
            return 100
        elif big_win == 'O':
            return -100
        elif big_win == 'D':
            return 0
            
        score = 0
        
        # Evaluate small boards
        for i in range(3):
            for j in range(3):
                if self.small_board_status[i][j] == 'X':
                    score += 10
                elif self.small_board_status[i][j] == 'O':
                    score -= 10
                else:
                    # Evaluate potential small board wins if not already won
                    small_score = self.evaluate_small_board(i, j)
                    score += small_score
        
        # Strategic positions on the big board
        # Center board is valuable
        if self.small_board_status[1][1] == 'X':
            score += 3
        elif self.small_board_status[1][1] == 'O':
            score -= 3
        
        # Corner boards are valuable
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for i, j in corners:
            if self.small_board_status[i][j] == 'X':
                score += 2
            elif self.small_board_status[i][j] == 'O':
                score -= 2
        
        # Check for potential two-in-a-row on big board
        # Rows
        for i in range(3):
            row = [self.small_board_status[i][0], self.small_board_status[i][1], self.small_board_status[i][2]]
            if row.count('X') == 2 and row.count(' ') == 1:
                score += 5
            if row.count('O') == 2 and row.count(' ') == 1:
                score -= 5
        
        # Columns
        for j in range(3):
            col = [self.small_board_status[0][j], self.small_board_status[1][j], self.small_board_status[2][j]]
            if col.count('X') == 2 and col.count(' ') == 1:
                score += 5
            if col.count('O') == 2 and col.count(' ') == 1:
                score -= 5
        
        # Diagonals
        diag1 = [self.small_board_status[0][0], self.small_board_status[1][1], self.small_board_status[2][2]]
        if diag1.count('X') == 2 and diag1.count(' ') == 1:
            score += 5
        if diag1.count('O') == 2 and diag1.count(' ') == 1:
            score -= 5
        
        diag2 = [self.small_board_status[0][2], self.small_board_status[1][1], self.small_board_status[2][0]]
        if diag2.count('X') == 2 and diag2.count(' ') == 1:
            score += 5
        if diag2.count('O') == 2 and diag2.count(' ') == 1:
            score -= 5
        
        # Consider the number of legal moves available (mobility)
        available_moves = len(self.get_legal_moves())
        if self.current_player == 'X':
            score += available_moves * 0.1
        else:
            score -= available_moves * 0.1
        
        return score

    def evaluate_small_board(self, i, j):
        """Evaluates a single small board at position (i,j)."""
        board = self.board[i][j]
        score = 0
        
        # Check for potential wins in rows
        for row in range(3):
            line = [board[row][0], board[row][1], board[row][2]]
            if line.count('X') == 2 and line.count(' ') == 1:
                score += 1
            if line.count('O') == 2 and line.count(' ') == 1:
                score -= 1
        
        # Check for potential wins in columns
        for col in range(3):
            column = [board[0][col], board[1][col], board[2][col]]
            if column.count('X') == 2 and column.count(' ') == 1:
                score += 1
            if column.count('O') == 2 and column.count(' ') == 1:
                score -= 1
        
        # Check for potential wins in diagonals
        diag1 = [board[0][0], board[1][1], board[2][2]]
        if diag1.count('X') == 2 and diag1.count(' ') == 1:
            score += 1
        if diag1.count('O') == 2 and diag1.count(' ') == 1:
            score -= 1
        
        diag2 = [board[0][2], board[1][1], board[2][0]]
        if diag2.count('X') == 2 and diag2.count(' ') == 1:
            score += 1
        if diag2.count('O') == 2 and diag2.count(' ') == 1:
            score -= 1
        
        # Center position is valuable in small boards too
        if board[1][1] == 'X':
            score += 0.5
        elif board[1][1] == 'O':
            score -= 0.5
        
        return score

    def run(self):
        """Run the game's main loop."""
        self.root.mainloop()


class UltimateTicTacToeCSP:
    """Class implementing the Constraint Satisfaction Problem formulation for Ultimate Tic-Tac-Toe."""
    
    def __init__(self, game):
        """Initialize the CSP solver with a game instance."""
        self.game = game
        # Store the current player when CSP is created
        self.player = self.game.current_player
        # Initialize our variable and domain mapping
        self.variables = self.get_legal_moves()
        self.domains = {var: [self.player] for var in self.variables}
        # Track the result of AC-3 for valid domains
        self.constraints = self.create_constraints()
    
    def get_legal_moves(self):
        """Get all valid moves in the current game state as CSP variables"""
        return self.game.get_legal_moves()
    
    def create_constraints(self):
        """Create binary constraints between variables"""
        constraints = {}
        
        # For each pair of variables, create constraints based on game rules
        for var1 in self.variables:
            constraints[var1] = []
            for var2 in self.variables:
                if var1 != var2:
                    i1, j1, m1, n1 = var1
                    i2, j2, m2, n2 = var2
                    
                    # Variables in same small board have binary constraints
                    if i1 == i2 and j1 == j2:
                        constraints[var1].append(var2)
                    
                    # Variables that affect next board selection have constraints
                    if m1 == i2 and n1 == j2:
                        constraints[var1].append(var2)
                    
                    # Variables that would lead to win conditions have constraints
                    if self.would_create_win_constraint(var1, var2):
                        constraints[var1].append(var2)
        
        return constraints
    
    def would_create_win_constraint(self, var1, var2):
        """Check if var1 and var2 form part of potential win pattern"""
        i1, j1, m1, n1 = var1
        i2, j2, m2, n2 = var2
        
        # Check if in same row, column or diagonal of small board
        if i1 == i2 and j1 == j2:
            # Same row in small board
            if m1 == m2:
                return True
            # Same column in small board
            if n1 == n2:
                return True
            # Main diagonal
            if (m1 == n1 and m2 == n2) or (m1 + n1 == 2 and m2 + n2 == 2):
                return True
        
        # Check if in same row, column or diagonal of big board
        if m1 == m2 and n1 == n2:
            # Same position in different small boards
            # Same row in big board
            if i1 == i2:
                return True
            # Same column in big board
            if j1 == j2:
                return True
            # Main diagonal in big board
            if (i1 == j1 and i2 == j2) or (i1 + j1 == 2 and i2 + j2 == 2):
                return True
        
        return False
    
    def forwardchecking(self, var1, var2):
        """
        Revise the domain of var1 with respect to var2.
        Returns True if the domain of var1 was changed.
        """
        revised = False
        
        # Since we're only looking for the next best move,
        # and domain is just the current player's symbol,
        # we check if making this move would be inconsistent
        # due to constraints with var2
        
        # Check move consistency
        if var1 in self.domains and self.domains[var1]:
            i1, j1, m1, n1 = var1
            i2, j2, m2, n2 = var2
            
            # Simulate the move
            original_state = self.game.board[i1][j1][m1][n1]
            self.game.board[i1][j1][m1][n1] = self.player
            
            # Check if this would lead to an invalid state for the next player
            # For example, sending to a full or won board with no valid moves
            if m1 == i2 and n1 == j2:
                if self.game.small_board_status[m1][n1] != ' ':
                    # Sending to a won board - need to check if there are other options
                    has_valid_board = False
                    for i in range(3):
                        for j in range(3):
                            if self.game.small_board_status[i][j] == ' ':
                                has_valid_board = True
                                break
                        if has_valid_board:
                            break
                    
                    if not has_valid_board:
                        # No valid board to play in next turn
                        self.domains[var1] = []
                        revised = True
            
            # Restore the board state
            self.game.board[i1][j1][m1][n1] = original_state
            
        return revised
    
    def ac3(self):
        """
        Apply AC-3 algorithm to enforce arc consistency.
        Returns False if an inconsistency is found, True otherwise.
        """
        # Queue of arcs to process - start with all binary constraints
        queue = []
        for var1 in self.variables:
            for var2 in self.constraints[var1]:
                queue.append((var1, var2))
        
        while queue:
            var1, var2 = queue.pop(0)
            
            if self.forwardchecking(var1, var2):
                # If domain becomes empty, this is inconsistent
                if var1 in self.domains and not self.domains[var1]:
                    return False
                
                # Add neighbors for rechecking
                for var3 in self.constraints[var1]:
                    if var3 != var2:
                        queue.append((var3, var1))
        
        return True
    
    def select_unassigned_variable(self, assignment):
        """
        Select an unassigned variable using MRV (Minimum Remaining Values)
        and degree heuristic as a tie-breaker.
        """
        unassigned = [v for v in self.variables if v not in assignment and v in self.domains]
        
        if not unassigned:
            return None
        
        # First, filter by MRV
        min_remaining = min(len(self.domains.get(var, [])) for var in unassigned)
        min_vars = [var for var in unassigned if len(self.domains.get(var, [])) == min_remaining]
        
        if len(min_vars) == 1:
            return min_vars[0]
        
        # Tie-breaker: degree heuristic (most constraints)
        return max(min_vars, key=lambda var: len(self.constraints[var]))
    
    def backtracking_search(self):
        """Perform backtracking search to find a solution."""
        # If AC-3 pre-processing eliminates all options, fail early
        if not self.ac3():
            return None
        
        # Get moves with non-empty domains after AC-3
        valid_moves = [var for var in self.variables if var in self.domains and self.domains[var]]
        
        if not valid_moves:
            return None
        
        # For Ultimate Tic-Tac-Toe, we're looking for the best next move,
        # so we can just use the first variable after MRV and degree heuristics
        best_move = self.select_unassigned_variable({})
        
        # Use a strategic move selection if available
        if best_move:
            best_vals = []
            # Strategic weights based on cell position
            strategic_weights = {
                # Center is best
                (1, 1): 3,
                # Corners are good
                (0, 0): 2, (0, 2): 2, (2, 0): 2, (2, 2): 2,
                # Edges are okay
                (0, 1): 1, (1, 0): 1, (1, 2): 1, (2, 1): 1
            }
            
            # First, check if any move leads to winning a small board
            for move in valid_moves:
                i, j, m, n = move
                # Temporarily make the move
                self.game.board[i][j][m][n] = self.player
                win_status = self.game.check_small_board_win(i, j)
                self.game.board[i][j][m][n] = ' '
                
                if win_status == self.player:
                    # Found a winning move
                    return {move: self.player}
            
            # Next, consider strategic positions within small boards
            for move in valid_moves:
                i, j, m, n = move
                # For each move, calculate a strategic score based on position
                position_weight = strategic_weights.get((m, n), 0)
                best_vals.append((move, position_weight))
            
            if best_vals:
                # Sort by strategic value (higher is better)
                best_vals.sort(key=lambda x: x[1], reverse=True)
                best_move = best_vals[0][0]
                return {best_move: self.player}
            
        # Fallback to first available move
        if valid_moves:
            return {valid_moves[0]: self.player}
            
        return None
    
    def consistent(self, var, value, assignment):
        """
        Check if assignment is consistent with all constraints.
        Returns True if assignment is consistent.
        """
        # Check if value conflicts with any assignment
        for assigned_var, assigned_val in assignment.items():
            if var == assigned_var:
                continue
            
            # Check basic constraint: same cell can't have two values
            if var == assigned_var and value != assigned_val:
                return False
            
            # Check if this assignment would create inconsistent board state
            i, j, m, n = var
            self.game.board[i][j][m][n] = value
            consistent = self.check_board_consistency()
            self.game.board[i][j][m][n] = ' '
            
            if not consistent:
                return False
        
        return True


def main():
    """Main function to run the game."""
    game = UltimateTicTacToe()
    game.run()


if __name__ == "__main__":
    main()