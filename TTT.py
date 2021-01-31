import random, time

board = [[' ',' ',' '],
         [' ',' ',' '],
         [' ',' ',' ']]
end = False
draw = False

def select_mode(vs, symbol, order):
    # Initialize settings for game
    setup = dict() 
    setup['versus'] = 0

    if symbol == "O":
        setup['symbol'] = "O"
        setup['o_symbol'] = "X"
    else:    
        setup['symbol'] = "X"
        setup['o_symbol'] = "O"

    if order == "y":
        setup["order"] = 1
    else:
        setup["order"] = 0
    
    return setup


def print_board():
    # Prints board to command line
    for i in range(5):
        if i % 2 == 0:
            row = i // 2
            print(f'{board[row][0]} | {board[row][1]} | {board[row][2]}')
        else:
            print("---------")


def check_board(sym):
    # Checks if a win or a draw occurs
    global end, draw
    # Check the rows
    for row in range(3):
        row_count = 0
        for column in range(3):
            if board[row][column] == sym:
                row_count += 1
        # print("Row count:", row_count)
        if row_count == 3:
            end = True
            return True

    # Check columns
    for column in range(3):
        column_count = 0
        for row in range(3):
            if board[row][column] == sym:
                column_count += 1
        # print("Column count:", column_count)
        if column_count == 3:
            end = True
            return True
    
    # Check diagonals
    diagonal_count = [0,0]
    for i in range(3):
        if board[i][i] == sym:
            diagonal_count[0] += 1
        if board[2-i][i] == sym:
            diagonal_count[1] += 1
    print("Diagonal count:", diagonal_count)

    if diagonal_count[0] == 3 or diagonal_count[1] == 3:
        end = True
        return True

    # Check if board is full
    filled_cells = 0
    for row in range(3):
        for column in range(3):
            if board[row][column] != ' ':
                filled_cells += 1

    if filled_cells == 9:
        draw = True
        return True

    return False        
    
def player_move(symbol):
    global end
    while True:
        try:
            position = int(input("Player 1 move: "))
            if is_valid_pos(position, symbol):
                if check_board(symbol):
                    pass
            break
        except:
            pass
        print("Invalid move!")
    print_board()

def opponent_move(symbol, versus):
    global end
    while True:
        if versus:
            print("Thinking....")
            time.sleep(3)
            position = random.randint(1,9)
        else:
            position = input("Player 2 move: ")
        try:
            position = int(position)
            if is_valid_pos(position, symbol):
                if versus:
                print("Opponent move:", position)
                if check_board(symbol):
                    pass
                break
        except:
            pass
        if not versus:
            print("Invalid move!")
    print_board()
    
def is_valid_pos(pos, sym):
    # Checks if move is valid
    
    # Subtract one from position for zero-indexing
    pos -= 1
    row = pos // 3
    col = pos % 3
    
    if board[row][col] == ' ':
        board[row][col] = sym
        return True
    return False

def main():
    print("Welcome to Command Line TicTacToe!\n")
    print("The rules are simple and as follows:")
    print("1. Choose an empty spot on the board")
    print("2. Input the number corresponding to the spot you want to place your number in (check below for reference)\n")
    print("1 | 2 | 3\n"+
          "---------\n"+
          "4 | 5 | 6\n"+
          "---------\n"+
          "7 | 8 | 9")
    print("\n3. The game ends when you or your opponent place an X or O along the same column, row, or diagonal")
    versus = input("Who is your opponent? [0 = player, 1 = computer] ")
    symbol = input("What symbol do you want to use? [Choices: O, X] ")
    order = input("Do you want to go first? [y/n]" )
    FINAL_SETUP = select_mode(versus, symbol, order)
    # print(FINAL_SETUP)
    while not end:
        if FINAL_SETUP["order"]:
            player_move(FINAL_SETUP["symbol"])
            if end:
                if FINAL_SETUP["versus"]:
                    print("You win!")
                else:
                    print("Player 1 wins!")
                break
            elif draw:
                print("Draw!")
                break
            opponent_move(FINAL_SETUP["o_symbol"], FINAL_SETUP["versus"])
            if end:
                if FINAL_SETUP["versus"]:
                    print("You lose.")
                else:
                    print("Player 2 wins!")
                break
            elif draw:
                print("Draw!")
                break
        else:
            opponent_move(FINAL_SETUP["o_symbol"], FINAL_SETUP["versus"])
            if end:
                if FINAL_SETUP["versus"]:
                    print("You lose.")
                else:
                    print("Player 2 wins!")
                break
            elif draw:
                print("Draw!")
                break
            player_move(FINAL_SETUP["symbol"])
            if end:
                if FINAL_SETUP["versus"]:
                    print("You win!")
                else:
                    print("Player 1 wins!")
                break
            elif draw:
                print("Draw!")
                break
    print("Thank you for playing!")

if __name__=="__main__":
    main()
