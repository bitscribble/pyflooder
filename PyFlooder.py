#!/usr/bin/env python3

import random, pygame, sys, argparse

class Board():
    def __init__(self, size: int = 14):
        self.size = size
        self.init_cells()
        
    def init_cells(self):
        self.cells = []
        new = []
        for i in range (0, self.size):
            for j in range (0, self.size):
                new.append(random.randint(1,6))
            self.cells.append(new)
            new = []
    
    def flood_fill(self, x: int, y: int, new_color: int, old_color: int):
        
        if (x > (self.size-1)) or (y > (self.size-1)): 
            return
        elif (x < 0) or (y < 0): # python problem with arrays < 0
            return
        
        if self.cells[x][y] == old_color:
            
            # put new cell with new color
            self.cells[x][y] = new_color

            # recursive call for bottom pixel fill
            self.flood_fill(x+1, y, new_color, old_color)

            # recursive call for top pixel fill
            self.flood_fill(x-1, y, new_color, old_color)

            # recursive call for right pixel fill
            self.flood_fill(x, y+1, new_color, old_color)

            # recursive call for left pixel fill
            self.flood_fill(x, y-1, new_color, old_color)

    def check_win(self, color: int):
        for i in range (0, self.size):
            for j in range (0, self.size):
                if self.cells[i][j] != color:
                    return False
        return True


PURPLE = (156,0,181)
BLUE = (0,140,255)
GREEN = (8,181,49)
YELLOW = (255,255,0)
RED = (255,8,8)
PINK = (255,123,173)

color_dict = {
  1: PURPLE,
  2: BLUE,
  3: GREEN,
  4: YELLOW,
  5: RED,
  6: PINK
}

def draw_board(screen: pygame.Surface, board: Board, size: int):
    width, height = screen.get_size()
    for i in range (0, board.size):
        for j in range (0, board.size):
            color = board.cells[i][j]
            pygame.draw.rect(screen, color_dict[color], pygame.Rect(j*(size), i*(size), size, size))

def get_color_from_click(x: int, y: int, c: int, b: Board):
    return board.cells[y//c][x//c]

def print_text(text: str, font_size: int):
    screen.fill((0,0,0))
    font = pygame.font.SysFont("Arial", font_size)
    txtsurf = font.render(text, True, (255,255,255))
    screen.blit(txtsurf, (((BOARD_SIZE*CELL_SIZE) // 2)-(txtsurf.get_width()/2), ((BOARD_SIZE*CELL_SIZE) // 2)-(txtsurf.get_height()/2)))
    pygame.display.update()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scaled', action='store_true')
    args = parser.parse_args()

    BOARD_SIZE = 14
    MAX_TRIES = 24

    if args.scaled:
        CELL_SIZE = 40
    else:
        CELL_SIZE = 20

    if args.scaled:
        FONT_SIZE = 32
    else:
        FONT_SIZE = 16

    board = Board(BOARD_SIZE)

    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE*CELL_SIZE, BOARD_SIZE*CELL_SIZE))
    pygame.display.set_caption('Flooder - Tries: {}'.format(MAX_TRIES))

    draw_board(screen, board, CELL_SIZE)
    pygame.display.flip()

    old_color = board.cells[0][0]
    tries = 0
    finished = False

    while True:
        
        new_color = old_color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if finished == False:
                    pos = pygame.mouse.get_pos()
                    new_color = get_color_from_click(pos[0], pos[1], CELL_SIZE, board)

                    if old_color != new_color:
                        board.flood_fill(0,0,new_color,old_color)
                        old_color = new_color
                        tries += 1
                else:
                    board.init_cells()
                    draw_board(screen, board, CELL_SIZE)
                    pygame.display.flip()
                    old_color = board.cells[0][0]
                    tries = 0
                    finished = False

                draw_board(screen, board, CELL_SIZE)
                pygame.display.flip()

                if board.check_win(new_color):
                    print_text("You win, tries {}".format(tries), FONT_SIZE)
                    finished = True
                elif tries >= MAX_TRIES:
                    print_text("You loose", FONT_SIZE)
                    finished = True

                pygame.display.set_caption('Flooder - Tries: {}'.format(MAX_TRIES-tries))
