import tkinter as tk
from tkinter import messagebox
import random

# Tic-Tac-Toe board and variables
board = [' ' for _ in range(9)]
current_player = 'X'  # Human player starts
scores = {'Player': 0, 'AI': 0}
difficulty = "Medium"  # Default difficulty

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe Game")

# Display the board
buttons = []

def reset_board():
    global board
    board = [' ' for _ in range(9)]
    for button in buttons:
        button.config(text=' ', state=tk.NORMAL)

def show_board():
    for i in range(9):
        buttons[i].config(text=board[i])

def check_winner(b, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    return any(b[i] == b[j] == b[k] == player for i, j, k in win_conditions)

def is_draw(b):
    return ' ' not in b

# AI move based on difficulty
def ai_move():
    global board, current_player

    if difficulty == "Easy":
        move = random.choice([i for i in range(9) if board[i] == ' '])
    elif difficulty == "Medium":
        # Medium strategy: sometimes random, sometimes Minimax
        if random.random() < 0.5:
            move = random.choice([i for i in range(9) if board[i] == ' '])
        else:
            move = best_move()
    else:
        move = best_move()  # Hard difficulty uses Minimax

    board[move] = 'O'
    buttons[move].config(text='O', state=tk.DISABLED)
    current_player = 'X'

    if check_winner(board, 'O'):
        messagebox.showinfo("AI Wins", "AI has won!")
        scores['AI'] += 1
        update_score()
        reset_board()
    elif is_draw(board):
        messagebox.showinfo("Draw", "It's a draw!")
        reset_board()

# Player move
def player_move(i):
    global board, current_player
    if board[i] == ' ':
        board[i] = 'X'
        buttons[i].config(text='X', state=tk.DISABLED)
        current_player = 'O'

        if check_winner(board, 'X'):
            messagebox.showinfo("You Win!", "Congratulations, you won!")
            scores['Player'] += 1
            update_score()
            reset_board()
        elif is_draw(board):
            messagebox.showinfo("Draw", "It's a draw!")
            reset_board()
        else:
            ai_move()

# Minimax algorithm for hard level
def minimax(b, is_ai):
    if check_winner(b, 'O'):
        return 10
    if check_winner(b, 'X'):
        return -10
    if is_draw(b):
        return 0

    if is_ai:
        best_score = -float('inf')
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'O'
                score = minimax(b, False)
                b[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'X'
                score = minimax(b, True)
                b[i] = ' '
                best_score = min(score, best_score)
        return best_score

# Best move for AI using Minimax
def best_move():
    best_score = -float('inf')
    move = 0
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    return move

# Update score on the screen
def update_score():
    score_label.config(text=f"Player: {scores['Player']}  |  AI: {scores['AI']}")

# Start game with chosen difficulty
def start_game(selected_difficulty):
    global difficulty
    difficulty = selected_difficulty
    reset_board()

# GUI layout
for i in range(9):
    button = tk.Button(root, text=' ', font='normal 20', width=5, height=2, command=lambda i=i: player_move(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

score_label = tk.Label(root, text=f"Player: {scores['Player']}  |  AI: {scores['AI']}", font=('normal', 15))
score_label.grid(row=3, column=0, columnspan=3)

# Difficulty level selection
difficulty_label = tk.Label(root, text="Select Difficulty Level:", font=('normal', 12))
difficulty_label.grid(row=4, column=0, columnspan=3)

tk.Button(root, text="Easy", command=lambda: start_game("Easy")).grid(row=5, column=0)
tk.Button(root, text="Medium", command=lambda: start_game("Medium")).grid(row=5, column=1)
tk.Button(root, text="Hard", command=lambda: start_game("Hard")).grid(row=5, column=2)

# New game button
tk.Button(root, text="New Game", command=reset_board).grid(row=6, column=0, columnspan=3)

# Start the GUI loop
root.mainloop()
