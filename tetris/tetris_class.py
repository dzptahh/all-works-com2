import pygame as pg
import random

class Config:
    game_width = 800
    game_height = 600
    block_size = 20
    grid_size = (400, 500)
    grid_width = grid_size[0] // block_size
    grid_height = grid_size[1] // block_size
    fps = 60
    
class Piece:
    def __init__(self, shape):
        self.__shape = shape
        self.__x = Config.grid_width // 2 
        self.__y = 0 
        
    def set_position(self,x,y):
        self.__x = x
        self.__y = y
        print(self.__x, self.__y)
        
    def get_position(self):
        return (self.__x,self.__y)
    
    def get_shape(self):
        return self.__shape
    
class Grid:
    def __init__(self):
        self.__board = [[x for x in range(Config.grid_width)] for y in range(Config.grid_height)]    #contain 2D array

    def get_grid(self):
        return self.__board # Encapsulate
    
    def check_valid_move(self, p:Piece):
        x,y  = p.get_position()
        tmp_shape = p.get_shape()
        tmp_pos = p.get_position()
        for  i,r in enumerate(tmp_shape):
            for j,cell in enumerate(r):
                if cell:
                    px = tmp_pos[0] + j
                    py = tmp_pos[1] + i
                    if px < 0 or px >= Config.grid_width or py < 0 or py >= Config.grid_height:
                        return False
        return True
        
        
        
        
class PieceManager:
    __SHAPE = [
        [[1,1,1],
         [0,1,0]],
        
        [[1,1],
         [1,1]],
        
        [[0,1,1],
         [1,1,0]],
        
        [[1,1,0],
         [0,1,1]],
        
        [[1,1,1,1]],
        
        [[1,0,0], # L shape
         [1,1,1]],
        
        [[0,0,1],
         [1,1,1]],
    ]
    
    def __init__(self, grid:Grid) -> None:
        self.__current = PieceManager.gen_piece() # Gen at 1st time
        self.__next = PieceManager.gen_piece()
        self.__grid =  grid
        
        
    @classmethod
    def gen_piece(cls):
        return Piece(random.choice(cls.__SHAPE))
    
    def get_current(self):
        return self.__current
    
    def get_next(self):
        return self.__next
    
    def falling(self):
        self.move_current(0,1)
    
    
    def move_current(self,dx,dy,):
        x,y = self.__current.get_position()

        tmp = Piece(self.__current.get_shape())
        tmp.set_position(x+dx,y+dy)
        
        if self.__grid.check_valid_move(tmp):
            self.__current.set_position(x+dx, y+dy)  # Move down by 1 block
            
        
        

        

        
        
                
class Drawer:
    __COLOR = {'W': (255,255,255), 'BL': (0,0,0), 'R': (255,0), 'G': (0,255,0), 'B': (0,0,255)}
    @classmethod
    def curr_time(cls):
        return pg.time.get_ticks()
    
    
    
    @classmethod
    def GetColor(cls, k):
        return cls.__COLOR[k]
    
    def __init__(self, grid: Grid, piece: PieceManager):
        self.__screen = pg.display.set_mode((Config.game_width, Config.game_height))
        self.__screen.fill(self.GetColor('W'))
        self.__clock = pg.time.Clock()
        self.__gird = grid.get_grid()
        self.__piece = piece
    
    def _Draw_grid(self):
        tmp = pg.Surface(Config.grid_size)
        tmp.fill(self.GetColor('BL'))
        for row in range(Config.grid_height):
            for col in range(Config.grid_width):
                rect = pg.Rect(col*Config.block_size, row*Config.block_size, Config.block_size, Config.block_size)
                pg.draw.rect(tmp, self.GetColor('W'), rect, 1)
                
                
        curr_piece = self.__piece.get_current()
        tmp_shape = curr_piece.get_shape()
        tmp_pos = curr_piece.get_position()
        for  i,r in enumerate(tmp_shape):
            for j,cell in enumerate(r):
                if cell == 1:
                    px = tmp_pos[0] + j
                    py = tmp_pos[1]+ i
                    
                    rect = pg.Rect(px*Config.block_size, py*Config.block_size, Config.block_size, Config.block_size)
                    pg.draw.rect(tmp, self.GetColor('W'), rect, 1)
                    
                    
                    rect = pg.Rect(px*Config.block_size, py*Config.block_size, Config.block_size, Config.block_size)
                    pg.draw.rect(tmp, self.GetColor('BL'), rect, 1)

        offL = (Config.game_width - Config.grid_size[0]) // 2
        offT = (Config.game_height - Config.grid_size[1]) // 2

        self.__screen.blit(tmp,(offL,offT))
        
    def UpdateAll(self):
        self._Draw_grid()
        self.__clock.tick(Config.fps)
        pg.display.flip() 
    
class Game:
    def __init__(self) -> None:
        self.__grid = Grid()
        self.__piece = PieceManager(self.__grid)
        self.__draw = Drawer(self.__grid, self.__piece)
        self.__fall_delay = 60*4
        self.__last_fall = self.__draw.curr_time()
        
    def game_update(self):
        print(Drawer.curr_time())
        if (Drawer.curr_time() - self.__last_fall > self.__fall_delay):
            self.__piece.falling()
            self.__last_fall = Drawer.curr_time()
            
        
    def run(self):
        print("RUN")
        running = True
        while (running):
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    running = False
                if (ev.type == pg.KEYDOWN):
                    if ev.key == pg.K_LEFT:
                        self.__piece.move_current(-1, 0)
                    if ev.key == pg.K_RIGHT:
                        self.__piece.move_current(1, 0)
                    if ev.key == pg.K_DOWN:
                        self.__piece.move_current(0, 1)
                    if ev.key == pg.K_UP:
                        # Rotate
                        # self.__piece.move_current(-1, 0)
                        pass
                    
            self.game_update()
            self.__draw.UpdateAll()
                
        print("Exit Run")
