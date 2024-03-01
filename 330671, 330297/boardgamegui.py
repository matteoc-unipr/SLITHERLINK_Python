'''
@Authors: Costella Matteo, Bigliardi Gianmarco
'''
'''
!!!BEFORE STARTING THE PROGRAM, CHANGE THE FILE PATH AT LINE 63, 66, 97 WITH YOUR PATH OF pop.mp3, pop3.mp3 AND win.mp3!!!
'''
import g2d
from boardgame import BoardGame
from time import time

W, H = 40, 40
LONG_PRESS = 0.3

class BoardGameGui:
    def __init__(self, g: BoardGame, W: int, H: int):
        self._arena_W = W       
        self._arena_H = H
        self._game = g
        self._mouse_down = 0
        self._time_count = 0
        self._bestscore = 0
        self.update_buttons()
        self._name = g2d.prompt("Player username?")
        
        
        
    def tick(self):
        self._time_count += 1
        with open("BESTSCORE.txt", "r") as bestscore:
            for line in bestscore:
                bestscore = line 
                self._bestscore = int(bestscore)

        name = "ID: " + str(self._name)
        toplay = "Time: " + str(self._time_count // 30)
        best_score = "Best Time: " + str(self._bestscore) + 's'
        
        g2d.set_color((255, 255, 255))                                        
        g2d.fill_rect((0, self._arena_H - 50), (self._arena_W, 100))              #time count and username
        g2d.set_color((0, 0, 0))
        g2d.draw_text(name + " ", (self._arena_W - 150, self._arena_H - 50), 30)
        g2d.draw_text(toplay + " ", (15, self._arena_H - 50), 30)
        g2d.draw_text(best_score + " ", (15, self._arena_H ), 30)
        
        keys = set(g2d.current_keys())
        if 'h' in keys and "LeftButton" in keys and self._mouse_down == 0:
            self._mouse_down = time()
        elif 'h' in keys and "LeftButton" not in keys and self._mouse_down > 0:
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            if time() - self._mouse_down < LONG_PRESS:
                self._game.suggestions(x, y)    
            self.update_buttons()
            self._mouse_down = 0

        if "LeftButton" in g2d.current_keys() and self._mouse_down == 0:
            self._mouse_down = time()
        
        elif "LeftButton" not in g2d.current_keys() and self._mouse_down > 0:
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            if time() - self._mouse_down > LONG_PRESS:
                g2d.play_audio('C:\\Users\\Utente\\Desktop\\UNIVERSITA\\INFORMATICA\\PROGRAMMI\\SLITHERLINK\\pop.mp3')
                self._game.flag_at(x, y)
            else:
                g2d.play_audio('C:\\Users\\Utente\\Desktop\\UNIVERSITA\\INFORMATICA\\PROGRAMMI\\SLITHERLINK\\pop2.mp3')
                self._game.play_at(x, y)
                self._game.autofill_plus(x, y)
                self._game.autofill_numbers(x, y)
            self.update_buttons()
            self._mouse_down = 0

        if g2d.key_pressed('u'):
            if not self._game.unsolvable():
                g2d.alert('unsovable')

    def current_time(self):
        return self._time_count // 30   

    def update_buttons(self):
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        cols, rows = self._game.cols(), self._game.rows()
        for y in range(rows):
            for x in range(cols):
                value = str(self._game.value_at(x, y))
                center = x * W + W//2, y * H + H//2
                if value == '-':
                    if x % 2 == 0 and y % 2 != 0: 
                        g2d.draw_line((x * W + W//2, y * H), (x * W + W//2, y * H + H))
                    if x % 2 != 0 and y % 2 == 0: 
                        g2d.draw_line((x * W , y * H + H//2), (x * W + W, y * H + H//2))
                else:
                    g2d.draw_text_centered(value, center, H)
        g2d.update_canvas()
        if self._game.finished():
            g2d.play_audio('C:\\Users\\Utente\\Desktop\\UNIVERSITA\\INFORMATICA\\PROGRAMMI\\SLITHERLINK\\win.mp3')            #####################################à
            if self.current_time() < self._bestscore:
                with open("BESTSCORE.txt", "w") as new_bestscore:
                    print(self.current_time(), file=new_bestscore)
                g2d.alert(("Game won!" " " "   New Best Score!!! ", self.current_time()))
            else:
                g2d.alert(("Game over!" " " "   Your score is  ", self.current_time()))            
                g2d.close_canvas()


def gui_play(game: BoardGame):
    g2d.init_canvas((game.cols() * W, (game.rows() * H + 100)))
    ui = BoardGameGui(game, (game.cols() * W),  (game.rows() * H + 50))
    g2d.main_loop(ui.tick)
