import pygame as pg
import random

class Config:
    game_width = 800
    game_height = 600
    block_size = 40
    grid_size = (400, 440)
    grid_width = grid_size[0] // block_size
    grid_height = grid_size[1] // block_size
    fps = 60
    
class Piece:
    def __init__(self, shape):
        self.__shape = shape
        self.__x = Config.grid_width // 2 
        self.__y = 0 
        
    def set_position(self, x, y):
        self.__x = x
        self.__y = y
        
    def get_position(self):
        return (self.__x, self.__y)
    
    def get_shape(self):
        return self.__shape
    
    def rotate(self):
        self.__shape = [list(row) for row in zip(*self.__shape[::-1])]
    
class Grid:
    def __init__(self):
        self.__board = [['-' for _ in range(Config.grid_width)] for _ in range(Config.grid_height)]
        
    def clean_lines(self):
            unclear_num = [r for r in self.__board if any ([c == '-' for c in r])]
            clear_nums = Config.game_height - len(unclear_num)
            
            for i in range(clear_nums):
                unclear_num.insert(0,['-' for x in range(Config.grid_width)])
            
            self.__board = unclear_num
    def get_grid(self):
        return self.__board
    
    def get_grid_value(self, py, px):
        return self.__board[py][px]   
        
    def check_valid_move(self, p: Piece):
        tmp_shape = p.get_shape()
        tmp_pos = p.get_position()
        for i, r in enumerate(tmp_shape):
            for j, cell in enumerate(r):
                if cell:
                    px = tmp_pos[0] + j
                    py = tmp_pos[1] + i
                    if px < 0 or px >= Config.grid_width or py >= Config.grid_height or (py >= 0 and self.__board[py][px] != '-'):
                        return False
        return True
        
    def place_piece(self, p: Piece):
        tmp_shape = p.get_shape()
        tmp_pos = p.get_position()
        for i, r in enumerate(tmp_shape):
            for j, cell in enumerate(r):
                if cell:
                    px = tmp_pos[0] + j
                    py = tmp_pos[1] + i
                    if 0 <= py < Config.grid_height and 0 <= px < Config.grid_width:
                        self.__board[py][px] = 'W'
        
class PieceManager:
    __SHAPES = [
        [[1, 1, 1],
         [0, 1, 0]],
        
        [[1, 1],
         [1, 1]],
        
        [[0, 1, 1],
         [1, 1, 0]],
        
        [[1, 1, 0],
         [0, 1, 1]],
        
        [[1, 1, 1, 1]],
        
        [[1, 0, 0],
         [1, 1, 1]],
        
        [[0, 0, 1],
         [1, 1, 1]],
    ]
    
    def __init__(self, grid: Grid) -> None:
        self.__current = self.gen_piece()
        self.__next = self.gen_piece()
        self.__grid = grid
        
    @classmethod
    def gen_piece(cls):
        return Piece(random.choice(cls.__SHAPES))
    
    def get_current(self):
        return self.__current
    
    def get_next(self):
        return self.__next
    
    def falling(self):
        can_move = self.move_current(0, 1)
        if not can_move:
            self.__grid.place_piece(self.__current)
            self.__current = self.__next
            self.__next = self.gen_piece()
            return False #stuck
        return True
            
    def force_falling(self) -> bool:
        while True:
            if not self.falling():
                return False
            return True
        
        
    def __copy_current_piece(self):
        x, y = self.__current.get_position()
        tmp = Piece(self.__current.get_shape())
        tmp.set_position(x, y)
        return tmp
    
    def move_current(self, dx, dy):
        tmp = self.__copy_current_piece()
        x, y = self.__current.get_position()
        tmp.set_position(x + dx, y + dy)
        
        if self.__grid.check_valid_move(tmp):
            self.__current.set_position(x + dx, y + dy)
            return True
        return False
    
    def rotate_current(self):
        tmp = self.__copy_current_piece()
        tmp.rotate()
        if self.__grid.check_valid_move(tmp):
            self.__current.rotate()
            return True
        return False
        
class Drawer:
    __COLOR = {'W': (255, 255, 255), 'BL': (0, 0, 0), 'R': (255, 0, 0), 'G': (0, 255, 0), 'B': (0, 0, 255)}
    
    @classmethod
    def curr_time(cls):
        return pg.time.get_ticks()
    
    @classmethod
    def get_color(cls, k):
        return cls.__COLOR[k]
    
    def __init__(self, grid: Grid, piece: PieceManager):
        self.__screen = pg.display.set_mode((Config.game_width, Config.game_height))
        self.__screen.fill(self.get_color('W'))
        self.__clock = pg.time.Clock()
        self.__grid = grid
        self.__piece = piece
    
    def _draw_grid(self):
        tmp = pg.Surface(Config.grid_size)
        tmp.fill(self.get_color('BL'))
        for row in range(Config.grid_height):
            for col in range(Config.grid_width):
                val = self.__grid.get_grid_value(row, col)
                rect = pg.Rect(col * Config.block_size, row * Config.block_size, Config.block_size, Config.block_size)
                if val == '-':
                    pg.draw.rect(tmp, self.get_color('W'), rect, 1)
                else:
                    pg.draw.rect(tmp, self.get_color('R'), rect)
                    pg.draw.rect(tmp, self.get_color('BL'), rect, 1)
        
        curr_piece = self.__piece.get_current()
        tmp_shape = curr_piece.get_shape()
        tmp_pos = curr_piece.get_position()
        for i, r in enumerate(tmp_shape):
            for j, cell in enumerate(r):
                if cell:
                    px = tmp_pos[0] + j
                    py = tmp_pos[1] + i
                    rect = pg.Rect(px * Config.block_size, py * Config.block_size, Config.block_size, Config.block_size)
                    pg.draw.rect(tmp, self.get_color('R'), rect)
                    pg.draw.rect(tmp, self.get_color('BL'), rect, 1)

        offL = (Config.game_width - Config.grid_size[0]) // 2
        offT = (Config.game_height - Config.grid_size[1]) // 2

        self.__screen.blit(tmp, (offL, offT))
        
    def update_all(self):
        self._draw_grid()
        self.__clock.tick(Config.fps)
        pg.display.flip() 
    
class Game:
    def __init__(self) -> None:
        self.__grid = Grid()
        self.__piece = PieceManager(self.__grid)
        self.__draw = Drawer(self.__grid, self.__piece)
        self.__fall_delay = 60 * 4
        self.__last_fall = self.__draw.curr_time()
        
    def game_update(self):
        if (Drawer.curr_time() - self.__last_fall > self.__fall_delay):
            self.__piece.falling()
            self.__last_fall = Drawer.curr_time()
        
        
        self.__grid.clean_lines() 
        
    def run(self):
        running = True
        while running:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    running = False
                if ev.type == pg.KEYDOWN:
                    if ev.key == pg.K_LEFT:
                        self.__piece.move_current(-1, 0)
                    if ev.key == pg.K_RIGHT:
                        self.__piece.move_current(1, 0)
                    if ev.key == pg.K_DOWN:
                        self.__piece.falling()
                    if ev.key == pg.SPACE:
                        self.__piece.force_falling()
                    if ev.key == pg.K_UP:
                        self.__piece.rotate_current()
                        
            self.game_update()
            self.__draw.update_all()
                
        pg.quit()
