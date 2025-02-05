from tetris_config import Config
import pygame as pg
import random

class Piece:
    def __init__(self, shape):
        self.__shape = shape
        self.__x = (Config.grid_width//2) - (len(self.__shape[0])//2)
        self.__y = 0
    
    def set_position(self,x,y):
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
        self.__board = None
        self.reset()
    
    def reset(self):
        self.__board = [self.__emptyrow() for y in range(Config.grid_height)]

    def __emptyrow(self):
        return ['-' for x in range(Config.grid_width)]
        
    def clear_lines(self):
        unclear_nums = [r for r in self.__board if any([c == '-' for c in r])]
        clear_nums = Config.grid_height - len(unclear_nums)
        # print(clear_nums)
        for i in range(clear_nums):
            unclear_nums.insert(0,self.__emptyrow())
        
        self.__board = unclear_nums
        return clear_nums
    
    def get_grid(self):
        return self.__board

    def get_grid_value(self,py,px):
        return self.__board[py][px]
    
    def check_valid_move(self,p:Piece) -> bool:
        tmp_shape = p.get_shape()
        tmp_pos = p.get_position()
        for i, r in enumerate(tmp_shape):
            for j, cell in enumerate(r):
                if cell:
                    px = tmp_pos[0] + j
                    py = tmp_pos[1] + i
                    if px < 0 or px >= Config.grid_width or py < 0 or py >= Config.grid_height or self.__board[py][px] != '-':
                        return False
        return True
        
    def place_piece(self, p:Piece):
        tmp_shape = p.get_shape()
        # print(tmp_shape)
        tmp_pos = p.get_position()
        for i, r in enumerate(tmp_shape):
            for j, cell in enumerate(r):
                if cell == 1:
                    px = tmp_pos[0] + j
                    py = tmp_pos[1] + i
                    self.__board[py][px] = 'LAVENDER'
        
class PieceManager():
    def __init__(self, grid:Grid):
        self.__current = None
        self.__next = None
        self.__grid = grid
        self.reset()
    
    @staticmethod
    def __gen_piece() -> Piece:
        return Piece(random.choice(Config.piece_shape))

    def reset(self):
        self.__current = PieceManager.__gen_piece()
        self.__next = PieceManager.__gen_piece()
        
    def get_current(self) -> Piece:
        return self.__current
    
    def get_next(self) -> Piece:
        return self.__next

    def falling(self) -> bool:
        canmove = self.move_current(0,1)
        if not canmove:
            self.__grid.place_piece(self.__current)
            self.__current = self.__next
            self.__next = PieceManager.__gen_piece()
            return False
        return True

    def force_falling(self) -> bool:
        while True:
            if not self.falling():
                return False
    
    def __copy_current_piece(self) -> Piece:
        x,y = self.__current.get_position()
        tmp = Piece(self.__current.get_shape())
        tmp.set_position(x,y)
        return tmp
        
    def move_current(self, dx: int, dy: int) -> bool:
        tmp = self.__copy_current_piece()
        x,y = self.__current.get_position()
        tmp.set_position(x+dx,y+dy)
        
        checkvalid = self.__grid.check_valid_move(tmp)
        if checkvalid:
            p = self.__current
            p.set_position(x+dx, y+dy)
        return checkvalid
        
    def rotate_current(self) -> bool:
        tmp = self.__copy_current_piece()
        tmp.rotate()
        
        checkvalid = self.__grid.check_valid_move(tmp)
        if checkvalid:
            self.__current.rotate()
        return checkvalid
    
class Drawer:
    def __init__(self, grid: Grid, piece: PieceManager):    
        pg.init()
        self.__screen = pg.display.set_mode((Config.game_width,Config.game_height))        
        self.__clock = pg.time.Clock()
        self.__grid = grid
        self.__piece = piece
        self.reset()

    @staticmethod
    def curr_time():
        return pg.time.get_ticks()

    @staticmethod
    def GetColor(k) -> tuple:
        return Config.game_color[k]
    
    def reset(self):
        self.__screen.fill(self.GetColor('Y'))

    def set_game_information(self,info):
        self.__gameinfo = info
            
    def __draw_grid(self):
        tmp = pg.Surface((Config.grid_size))
        tmp.fill(self.GetColor('MINT'))
        
        for row in range(Config.grid_height):
            for col in range(Config.grid_width):
                val = self.__grid.get_grid_value(row,col)
                rect = pg.Rect(col*Config.block_size, row*Config.block_size, Config.block_size, Config.block_size)
                if val == '-': 
                    pg.draw.rect(tmp, self.GetColor('LAVENDER'),rect,1)
                else:
                    pg.draw.rect(tmp, self.GetColor('LAVENDER'),rect)
                    pg.draw.rect(tmp, self.GetColor('BL'),rect,1)
                            
        curr_piece = self.__piece.get_current()
        tmp_shape = curr_piece.get_shape()
        # print(tmp_shape)
        tmp_pos = curr_piece.get_position()
        for i, r in enumerate(tmp_shape):
            for j, cell in enumerate(r):
                if cell == 1:
                    px = tmp_pos[0] + j
                    py = tmp_pos[1] + i
                    rect = pg.Rect(px*Config.block_size, py*Config.block_size, Config.block_size, Config.block_size)
                    pg.draw.rect(tmp, self.GetColor('LAVENDER'),rect)
                    pg.draw.rect(tmp, self.GetColor('BL'),rect,1)
                    
        
        offL = (Config.game_width - Config.grid_size[0]) // 2
        offT = (Config.game_height - Config.grid_size[1]) // 2
        self.__screen.blit(tmp,(offL,offT))
    
    def __draw_game_state(self):
        tmp = pg.Surface((Config.panel_size), pg.SRCALPHA)
        tmp.fill(self.GetColor('PEACH'))
        
        font = pg.font.Font(None,36)
        score_text = font.render(f"Score: {self.__gameinfo['score']}",True,self.GetColor('BL'))
        level_text = font.render(f"Level: {self.__gameinfo['level']}",True,self.GetColor('BL'))
        speed_text = font.render(f"Speed: {self.__gameinfo['speed']}",True,self.GetColor('BL'))
        tmp.blit(score_text,(20,20))
        tmp.blit(level_text,(20,70))
        tmp.blit(speed_text,(20,120))
        
        offL = 0 #((Config.game_width - Config.panel_size[0]) // 2) + Config.panel_size[0]
        offT = (Config.game_height - Config.panel_size[1]) // 2
        self.__screen.blit(tmp,(offL,offT))
    
    def __draw_gameover(self):
        tmp_opacity = pg.Surface((Config.game_width,Config.game_height), pg.SRCALPHA)
        tmp_opacity.fill(self.GetColor('CORAL'))
        tmp_opacity.set_alpha(200)

        tmp = pg.Surface((Config.game_width,Config.game_height), pg.SRCALPHA)
        # tmp.fill(self.GetColor('LIGHTGRAY'))
        
        font = pg.font.Font(None,48)
        line1_text = font.render(f"Score: {self.__gameinfo['score']}",True,self.GetColor('W'))
        line2_text = font.render(f"GAME OVER !!",True,self.GetColor('W'))
        line3_text = font.render(f"Press Space bar",True,self.GetColor('W'))
        
        rect1 = line1_text.get_rect(center=(Config.game_width//2,(Config.game_height//2)-60))
        rect2 = line2_text.get_rect(center=(Config.game_width//2,Config.game_height//2))
        rect3 = line3_text.get_rect(center=(Config.game_width//2,(Config.game_height//2)+60))
        
        tmp.blit(line1_text,rect1)
        tmp.blit(line2_text,rect2)
        tmp.blit(line3_text,rect3)
        
        self.__screen.blit(tmp_opacity,(0,0))
        self.__screen.blit(tmp,(0,0))
        
    def update_all(self):
        self.__draw_grid()
        self.__draw_game_state()
        if self.__gameinfo['state'] == 'gameover':
            self.__draw_gameover()
            
        self.__clock.tick(Config.fps)
        pg.display.flip()
        
        


class Game:
    def __init__(self):
        self.__grid = Grid()
        self.__piece = PieceManager(self.__grid)
        self.__draw = Drawer(self.__grid, self.__piece)
        self.__score = None
        self.__level = None
        self.__fall_delay = None
        self.__state = None
        self.__last_fall = None
        self.__game_reset()
    
    def __game_reset(self):
        self.__grid.reset()
        self.__piece.reset()
        self.__draw.reset()
        
        self.__score = 0
        self.__level = 1
        self.__fall_delay = self.__adj_falling_speed()
        self.__state = 'playing'
        self.__last_fall = Drawer.curr_time()
        
    def __adj_falling_speed(self):
        return max(600 - (self.__level * 50), 50)
        
    def __gameupdate(self):
        # print(Drawer.curr_time())
        if self.__state == 'playing':
            if (Drawer.curr_time() - self.__last_fall > self.__fall_delay): 
                if not self.__piece.falling():  # current <-- next
                    if not self.__piece.falling(): # current (previous next)
                        self.__state = 'gameover'
                        
                self.__last_fall = Drawer.curr_time() 
        
        self.__score += self.__grid.clear_lines()
        self.__level = (self.__score//10) + 1
        self.__fall_delay = self.__adj_falling_speed()
        tmp_info = {'score':self.__score,'level':self.__level,'speed':self.__fall_delay,'state':self.__state}
        self.__draw.set_game_information(tmp_info)
        
    def run(self):
        print("Run")
        running = True
        while (running):
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    running = False
                if (ev.type == pg.KEYDOWN):
                    if self.__state == 'playing':
                        if ev.key == pg.K_LEFT:
                            self.__piece.move_current(-1,0)
                        if ev.key == pg.K_RIGHT:
                            self.__piece.move_current(1,0)
                        if ev.key == pg.K_DOWN:
                            self.__piece.falling()
                        if ev.key == pg.K_SPACE:
                            self.__piece.force_falling()
                        if ev.key == pg.K_UP:
                            self.__piece.rotate_current()
                    elif self.__state == 'gameover':
                        if ev.key == pg.K_SPACE:
                            self.__game_reset()
                        
            self.__gameupdate()
            self.__draw.update_all()
            
        print("Exit Run")
        
