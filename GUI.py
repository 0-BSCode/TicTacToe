import pygame as pg
import random, time

RES = (500,500)
BLACK = (0,0,0)
WHITE = (255,255,255)
L_WIDTH = 6

results = {"PLAYER": False, "COMPUTER": False, "DRAW": False}
board = [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']]


def drawText(display, text, coords, size, color=BLACK, antialias=True, center=True, font='bookmanoldstyle', button=False):
    fontstyle = pg.font.SysFont(font, size)
    Text = fontstyle.render(text, antialias, color)
    if center:
        Textrect = Text.get_rect(center=coords)
    else:
        Textrect = Text.get_rect(topleft=coords)
    display.blit(Text, Textrect)
    if button:
        return (Text, Textrect)

class Menu():
    ''''End screen that shows winner of the game'''
    def __init__(self):
        self.x_coord = RES[0] // 2
        self.y_coord = RES[0] // 3

    def update_screen(self, display):
        display.fill(WHITE)
        # Evaluate what to place on screen
        if results["PLAYER"]:
            drawText(display, "PLAYER WINS", (self.x_coord, self.y_coord), 50, color=(0, 255, 0))
        elif results["COMPUTER"]:
            drawText(display, "COMPUTER WINS", (self.x_coord, self.y_coord), 50, color=(255, 0, 0))
        elif results["DRAW"]:
            drawText(display, "DRAW", (self.x_coord, self.y_coord), 50, color=(255, 100, 0))
        self.text, self.text_btn = drawText(display, "PLAY AGAIN?", (self.x_coord, 2*self.y_coord), 20, button=True)

    def handle_event(self, event, scenes):
        global board, results
        mouse_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.text_btn.x <= mouse_pos[0] <= (self.text_btn.x + self.text_btn.w) and self.text_btn.y <= mouse_pos[1] <= (self.text_btn.y + self.text_btn.h):
                board = [[' ', ' ', ' '],
                         [' ', ' ', ' '],
                         [' ', ' ', ' ']]
                for key in results.keys():
                    results[key] = False
                return scenes["GAME"]
        return scenes["MAIN"]


class Board():
    def __init__(self):
        self.player_turn = True
        self.boxdim = ((RES[0] // 3), RES[1] // 3)

    def drawGrid(self, display):
        for i in range(1, 3):
            pg.draw.line(display, BLACK, (i * RES[0] // 3, 0), (i * RES[0] // 3, RES[1]), L_WIDTH)
            pg.draw.line(display, BLACK, (0, i * RES[1] // 3), (RES[0], i * RES[1] // 3), L_WIDTH)

    def update_screen(self, display):
        display.fill(WHITE)
        self.drawGrid(display)
        for row in range(0, 3):
            for cell in range(0, 3):
                avg_x = int((row*self.boxdim[0]) + (self.boxdim[0] / 2))
                avg_y = int((cell*self.boxdim[1]) + (self.boxdim[1] / 2))
                drawText(display, board[row][cell], (avg_x, avg_y), 100)

    def handle_event(self, event, scenes):
        mouse_pos = pg.mouse.get_pos()
        for value in results.values():
            if value:
                time.sleep(1)
                # Ensure player is first to play next game
                self.player_turn = True
                return scenes["MAIN"]
        
        # Check whose turn it is
        if event.type == pg.MOUSEBUTTONDOWN and self.player_turn:
            self.playerMove(mouse_pos)
        elif not self.player_turn:
            time.sleep(2)
            self.opponentMove()
        return scenes["GAME"]

    def validMove(self, row, cell):
        '''Evaluate if move was valid'''
        if board[row][cell] == ' ':
            return True
        return False
    
    def evaluateBoard(self):
        if self.player_turn:
            sym = "X"
        else:
            sym = "O"
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
            results["DRAW"] = True
            return True

        return False        

    def playerMove(self, coords):
        for row in range(0, 3):
            for cell in range(0, 3):
                if (row * self.boxdim[0]) <= coords[0] <= ((row+1) * self.boxdim[0]) and (cell * self.boxdim[1]) <= coords[1] <= ((cell+1) * self.boxdim[1]):
                    if self.validMove(row, cell):
                        board[row][cell] = "X"
        if self.evaluateBoard() and not results["DRAW"]:
            results["PLAYER"] = True
        else:
            self.player_turn = False

    def opponentMove(self):
        empty_cells = []
        for b_row in range(0, 3):
            for b_cell in range(0, 3):
                if board[b_row][b_cell] == ' ':
                    empty_cells.append((b_row, b_cell))
        move = random.randint(0, len(empty_cells) - 1)
        row = empty_cells[move][0]
        cell = empty_cells[move][1]
        board[row][cell] = "O"
        if self.evaluateBoard() and  not results["DRAW"]:
            results["COMPUTER"] = True
        else:
            self.player_turn = True
        
if __name__ == '__main__':
    pg.init()
    scenes = {"MAIN": Menu(), "GAME": Board()}
    screen = pg.display.set_mode(RES)
    pg.display.set_caption("TicTacToe")
    running = True
    scene = scenes["GAME"]
    # screen.fill(WHITE)
    # drawGrid(screen)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            else:
                scene = scene.handle_event(event, scenes)
                scene.update_screen(screen)
        pg.display.update()