# Tic-Tac-Toe board
board = [' ' for _ in range(9)]

# Display the board
def print_board():
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

# Check for a winner
def check_winner(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    return any(board[i] == board[j] == board[k] == player for i, j, k in win_conditions)

# Check for draw
def is_draw(board):
    return ' ' not in board

# Minimax function for AI
def minimax(board, is_ai):
    if check_winner(board, 'O'):
        return 10
    if check_winner(board, 'X'):
        return -10
    if is_draw(board):
        return 0
    
    if is_ai:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# AI move
def ai_move():
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
    board[move] = 'O'

# Player move
def player_move():
    move = int(input("Enter your move (1-9): ")) - 1
    if board[move] == ' ':
        board[move] = 'X'
    else:
        print("Invalid move, try again.")
        player_move()

# Game loop
def play_game():
    while True:
        print_board()
        player_move()
        if check_winner(board, 'X'):
            print_board()
            print("You win!")
            break
        if is_draw(board):
            print_board()
            print("It's a draw!")
            break
        
        ai_move()
        if check_winner(board, 'O'):
            print_board()
            print("AI wins!")
            break
        if is_draw(board):
            print_board()
            print("It's a draw!")
            break

play_game()
