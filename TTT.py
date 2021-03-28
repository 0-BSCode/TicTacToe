import random, time

# For integration with Arduino
# import pyfirmata
# AR_BOARD = pyfirmata.Arduino('COM4')

board = [[' ',' ',' '],
         [' ',' ',' '],
         [' ',' ',' ']]
         
end_results = {"P1W": False, "P2W": False, "CPU": False, "Draw": False}
draw = False

class gameFinished(Exception):
    pass

def select_mode(vs, symbol, order):
    # Initialize settings for game
    setup = dict() 
    if vs:
        setup['versus'] = 1
    else:
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
    print('')


def check_board(sym):
    # Checks if a win or a draw occurs

    # Check the rows
    global draw
    for row in range(3):
        row_count = 0
        for column in range(3):
            if board[row][column] == sym:
                row_count += 1
        if row_count == 3:
            return True

    # Check columns
    for column in range(3):
        column_count = 0
        for row in range(3):
            if board[row][column] == sym:
                column_count += 1
        if column_count == 3:
            return True
    
    # Check diagonals
    diagonal_count = [0,0]
    for i in range(3):
        if board[i][i] == sym:
            diagonal_count[0] += 1
        if board[2-i][i] == sym:
            diagonal_count[1] += 1

    if diagonal_count[0] == 3 or diagonal_count[1] == 3:
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
    global end_results
    while True:
        try:
            position = int(input("Player 1 move: "))
            if is_valid_pos(position, symbol):
                # AR_BOARD.digital[position+2].write(1)
                if check_board(symbol):
                    if draw:
                        end_results['Draw'] = True
                    else:
                        end_results['P1W'] = True
                    raise Exception
                break
        except:
            # If result has been decided, print board one last time then end the game
            print_board()
            raise gameFinished
        print("Invalid move!")
    print_board()

def opponent_move(symbol, versus):
    global end_results
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
                # AR_BOARD.digital[position+2].write(1)
                if versus:
                    print("Opponent move:", position)
                if check_board(symbol):
                    if draw:
                        end_results['Draw'] = True
                    else:
                        if versus:
                            end_results['CPU'] = True
                        else:
                            end_results['P2W'] = True
                    raise Exception
                break
        except:
            # If a result has been decided, print board one last time then end the game
            print_board()
            raise gameFinished
        if not versus:
            print("Invalid move!")
    print_board()
    
def is_valid_pos(pos, sym):
    # Checks if move is valid
    
    # Get rid of 0 case early
    if pos == 0:
        return False

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
    versus = int(input("Who is your opponent? [0 = player, 1 = computer] "))
    symbol = input("What symbol do you want to use? [Choices: O, X] ")
    order = input("Do you want to go first? [y/n] ")
    FINAL_SETUP = select_mode(versus, symbol, order)
    try:
        while True:
            if FINAL_SETUP["order"]:
                player_move(FINAL_SETUP["symbol"])
                opponent_move(FINAL_SETUP["o_symbol"], FINAL_SETUP["versus"])
            else:
                opponent_move(FINAL_SETUP["o_symbol"], FINAL_SETUP["versus"])
                player_move(FINAL_SETUP["symbol"])
    except gameFinished:
        if end_results["P1W"]:
            print("Player 1 wins!")
        elif end_results["P2W"]:
            print("Player 2 wins!")
        elif end_results["CPU"]:
            print("You lose.")
        else:
            print("Draw!")
    print("Thank you for playing!")
    # for i in range(3, 12):
    #     time.sleep(0.2)
    #     AR_BOARD.digital[i].write(0)

if __name__=="__main__":
    main()