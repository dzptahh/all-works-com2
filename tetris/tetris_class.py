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
    
class Grid:
    def __init__(self):
        self.__board = [[x for x in range(Config.grid_width)] for y in range(Config.grid_height)]    #contain 2D array

    def get_grid(self):
        return self.__board # Encapsulate
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
    
    def __init__(self) -> None:
        self.__current = PieceManager.gen_piece() # Gen at 1st time
        self.__next = PieceManager.gen_piece()
        
    @classmethod
    def gen_piece(cls):
        return Piece(random.choice(cls.__SHAPE))
    
    def get_current(self):
        self.__current
    
    
class Piece:
    def __init__(self, shape):
        self.shape = shape
        self.__x = Config.grid_width // 2 
        self.__y = 0 
        
    def set_position(self,x,y):
        self.__x = x
        self.__y = y
        
        
class Drawer:
    __COLOR = {'W': (255,255,255), 'BL': (0,0,0), 'R': (255,0), 'G': (0,255,0), 'B': (0,0,255)}
    
    @classmethod
    def GetColor(cls, k):
        return cls.__COLOR[k]
    
    def __init__(self, grid: Grid):
        self.__screen = pg.display.set_mode((Config.game_width, Config.game_height))
        self.__screen.fill(self.GetColor('W'))
        self.__gird = grid.get_grid()
        
    def _Draw_grid(self):
        tmp = pg.Surface(Config.grid_size)
        tmp.fill(self.GetColor('BL'))
        for row in range(Config.grid_height):
            for col in range(Config.grid_width):
                rect = pg.Rect(col*Config.block_size, row*Config.block_size, Config.block_size, Config.block_size)
                pg.draw.rect(tmp, self.GetColor('W'), rect, 1)
        
        
        self.__screen.blit(tmp,(10,10))
        
    def UpdateAll(self):
        self._Draw_grid()
        pg.display.flip() 
    
class Game:
    def __init__(self) -> None:
        self.__grid = Grid()
        self.__piece = PieceManager()
        self.__draw = Drawer(self.__grid)
        
    def game_update(self):
        p = self.__piece.get_current()
        p.set_position()
        
    def run(self):
        print("RUN")
        running = True
        while (running):
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    running = False

            
            self.game_update()
            self.__draw.UpdateAll()
                
        print("Exit Run")