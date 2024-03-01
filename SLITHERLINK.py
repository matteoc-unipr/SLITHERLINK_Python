'''
@Authors: Costella Matteo, Bigliardi Gianmarco
'''


from boardgame import BoardGame, console_play
from boardgamegui import gui_play
import g2d
def abstract():
    raise NotImplementedError("Abstract method")

class SlitherGame(BoardGame):
    def __init__(self, filename: str, r, c): 
        self._numbers = ['0', '1', '2', '3']
        self._filename = filename
        self._rows = r
        self._cols = c
        self._matrix = []
        self._start = 0
        self._condition1 = None        
        self._condition2 = None
        with open(self._filename, "r") as filename:
            for line in filename:
                for col in line[:-1]:
                    self._matrix.append(col.strip())
        

    def cols(self):
        return self._cols
    def rows(self):
        return self._rows
    
    def value_at(self, x: int, y: int) -> str:               
        '''
        Return a string with the current value of a cell
        '''                         
        b, c = self._matrix, self._cols 
        if x<0 or x>= self._cols or y<0 or y>= self._rows:
            return '.'

        return str(b[y * c + x])


    def play_at(self, x: int, y: int):     
        '''
        Draw a line at the given position if it can
        '''                                      
        if x % 2 == 0 and y % 2 != 0 or  y % 2 == 0 and x % 2 != 0:
            if self._matrix[y * self._cols + x] == "-":
                self._matrix[y * self._cols + x] = ""
            elif self._matrix[y * self._cols + x] == "x":
                self._matrix[y * self._cols + x] = ""        
            else:  
                self._matrix[y * self._cols + x] = "-"
        return x, y 


    def flag_at(self, x: int, y: int): 
        '''
        Draw a flag at the given position if it can
        '''   
        if x % 2 == 0 and y % 2 != 0 or  y % 2 == 0 and x % 2 != 0:                 
            self._matrix[y * self._cols + x] = "x"
        return x, y        
    
    def autofill_plus(self, x:int, y:int):
        '''
        If a plus is selected, it fills automatically the cells around it with lines or flags, if it's possible
        '''
        if x % 2 == 0 and y % 2 == 0:
            count_line = 0
            count_x = 0
            i = y * self._cols + x
            directions = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
            for direction in directions:
                if self.value_at(*direction) == '-':
                    count_line += 1
                if self.value_at(*direction) == 'x':                               #NON RIEMPIE ANGOLI!!!!!!!!!!!!!!!!!!1
                    count_x += 1
                if self.value_at(*direction) == '.':
                    count_line += 1
            if count_line == 2 or count_line == 3:
                if self.value_at(x + 1, y) == '':
                    self.flag_at((i % self._cols ) + 1, (i // self._cols))
                if self.value_at(x - 1, y) == '':
                    self.flag_at((i % self._cols ) - 1, (i // self._cols))
                if self.value_at(x, y - 1) == '':
                    self.flag_at((i % self._cols ), (i // self._cols) - 1)
                if self.value_at(x, y + 1) == '':
                    self.flag_at((i % self._cols ), (i // self._cols) + 1)
                
            if count_x == 2 or count_x == 3:
                if self.value_at(x + 1, y) == '':
                    self.play_at((i % self._cols ) + 1, (i // self._cols))
                if self.value_at(x - 1, y) == '':
                    self.play_at((i % self._cols ) - 1, (i // self._cols))
                if self.value_at(x, y - 1) == '':
                    self.play_at((i % self._cols ), (i // self._cols) - 1)
                if self.value_at(x, y + 1) == '':
                    self.play_at((i % self._cols ), (i // self._cols) + 1)           

    def autofill_numbers(self, x:int, y:int):
        '''
        If a number is selected, it fills automatically the cells around it with lines or flags, if it's possible
        '''
        if x % 2 != 0 and y % 2 != 0:
            count_line = 0
            count_x = 0
            i = y * self._cols + x
            element = self._matrix[i]
            directions = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
            for direction in directions:
                if self.value_at(*direction) == '-':
                    count_line += 1
                if self.value_at(*direction) == 'x':
                    count_x += 1

            if element == '0' and count_line == 0 or element == '1' and count_line == 1 or element == '2' and count_line == 2 or element == '3' and count_line == 3:
                if self.value_at(x + 1, y) == '':
                    self.flag_at((i % self._cols ) + 1, (i // self._cols))
                if self.value_at(x - 1, y) == '':
                    self.flag_at((i % self._cols ) - 1, (i // self._cols))
                if self.value_at(x, y - 1) == '':
                    self.flag_at((i % self._cols ), (i // self._cols) - 1)
                if self.value_at(x, y + 1) == '':
                    self.flag_at((i % self._cols ), (i // self._cols) + 1)         
            if count_x == 2 or count_x == 3:
                if self.value_at(x + 1, y) == '':
                    self.play_at((i % self._cols ) + 1, (i // self._cols))
                if self.value_at(x - 1, y) == '':
                    self.play_at((i % self._cols ) - 1, (i // self._cols))
                if self.value_at(x, y - 1) == '':
                    self.play_at((i % self._cols ), (i // self._cols) - 1)
                if self.value_at(x, y + 1) == '':
                    self.play_at((i % self._cols ), (i // self._cols) + 1) 
    
    def single_loop(self, position, old):
        ''' 
        Check if there is only one loop and if it is closed (rule 2 for finish the game)
        '''
        pos = position
        old_pos = old
        x = pos % self._cols
        y = pos // self._cols
        self._check1 = 0
        for i in range(0, len(self._matrix)):
            if self._matrix[i] == '-':
                self._check1 += 1
        if old_pos == self._start and self._circle_count > 1:
            if self._circle_count == self._check1:
                self._condition2 = True
        else:
            self._condition2 = False 
            if self.value_at(x + 2, y) == '-' and x % 2 != 0 and y % 2 == 0 and ((y) * self._cols + (x + 2)) != self._start:
                if ((y) * self._cols + (x + 2)) != old_pos and self.value_at(x + 1, y + 1) != '-' and self.value_at(x + 1, y - 1) != '-':
                    self._circle_count += 1
                    self.single_loop(((y) * self._cols + (x + 2)), pos)
                 
            if self.value_at(x - 2, y) == '-' and x % 2 != 0 and y % 2 == 0 and ((y) * self._cols + (x - 2)) != self._start:
                if ((y) * self._cols + (x - 2)) != old_pos and self.value_at(x - 1, y + 1) != '-' and self.value_at(x - 1, y - 1) != '-':
                    self._circle_count += 1
                    self.single_loop(((y) * self._cols + (x - 2)), pos)
    
            if self.value_at(x, y + 2) == '-' and x % 2 == 0 and y % 2 != 0 and ((y + 2) * self._cols + (x)) != self._start:
                if ((y + 2) * self._cols + (x)) != old_pos and self.value_at(x + 1, y + 1) != '-' and self.value_at(x - 1, y + 1) != '-':
                    self._circle_count += 1
                    self.single_loop((y + 2) * self._cols + (x), pos)
                 
            if self.value_at(x, y - 2) == '-' and x % 2 == 0 and y % 2 != 0 and ((y - 2) * self._cols + (x)) != self._start:
                if ((y - 2) * self._cols + (x)) != old_pos and self.value_at(x + 1, y - 1) != '-' and self.value_at(x - 1, y - 1) != '-':
                    self._circle_count += 1
                    self.single_loop((y - 2) * self._cols + (x), pos)
    
            if self.value_at(x - 1, y - 1) == '-' and ((y - 1) * self._cols + (x-1)) != self._start:
                if ((y - 1) * self._cols + (x-1)) != old_pos:
                    self._circle_count += 1
                    self.single_loop((y - 1) * self._cols + (x-1), pos)
                    
            if self.value_at(x + 1, y + 1) == '-' and ((y + 1) * self._cols + (x+1)) != self._start: 
                if ((y + 1) * self._cols + (x+1)) != old_pos: 
                    self._circle_count += 1 
                    self.single_loop((y + 1) * self._cols + (x+1), pos)
             
            if self.value_at(x + 1, y - 1) == '-' and ((y - 1) * self._cols + (x+1)) != self._start:
                if ((y - 1) * self._cols + (x+1)) != old_pos:
                    self._circle_count += 1
                    self.single_loop((y - 1) * self._cols + (x+1), pos)
    
            if self.value_at(x - 1, y + 1) == '-' and ((y + 1) * self._cols + (x-1)) != self._start:
                if ((y + 1) * self._cols + (x-1)) != old_pos: 
                    self._circle_count += 1   
                    self.single_loop((y + 1) * self._cols + (x-1), pos)                              

                
    def number_plus_finished(self) -> bool:
        '''
        Check if the number of lines around every number corresponds to his value.
        Check also if there are no more than 2 lines around plus.
        (rule 1 for finishing game)
        '''
        self._victory = [] 
        for i in range(0, len(self._matrix) - self._cols):                 
            element = self._matrix[i]
            count = 0
            x = i % self._cols
            y = i // self._cols                                
            directions = [i + 1, i - 1, (y - 1) * self._cols + x, (y + 1) * self._cols + x]
            for direction in directions:
                if self._matrix[direction] == '-':
                    count += 1
            
            if element == '0' and count == 0:
                self._victory.append(True)
            elif element == '1' and count == 1:
                self._victory.append(True)
            elif element == '2' and count == 2:                            
                self._victory.append(True)
            elif element == '3' and count == 3:    
                self._victory.append(True)
            elif element == '+':
                if count == 0 or count == 2:                                    #controlla che i + siano collegati a 0 o 2 linee
                    self._victory.append(True)                    
            elif element == '' or element == ' ' or element == '-' or element == 'x':
                self._victory.append(True)
            else:
                self._victory.append(False) 
        if len(set(self._victory)) == 1:
            return True
        else:
            return False

    def finished(self) -> bool:
        '''
        If all the conditions are true, the game is finished.
        '''
        self._check = 0
        self._finished_list = []
        self._circle_count_ring = 0
        if self.number_plus_finished() == True:
            self._condition1 = True
        else:
            self._condition1 = False       
        
        for i in range(0, len(self._matrix)):
            if self._matrix[i] == '-':
                self._check += 1
            if self._matrix[i] == '-' and self._check == 1:                
                self._start = i
                self._circle_count = 0
                self.single_loop(i, None)

        if self._condition1 == True and self._condition2 == True:
            return True
        else:
            return False



    def plus(self):
         
         for i in range(0, len(self._matrix) - self._cols):                  
            element = self._matrix[i]
            count_plus = 0
            x = i % self._cols
            y = i // self._cols                                
            directions = [i + 1, i - 1, (y - 1) * self._cols + x, (y + 1) * self._cols + x]
            for direction in directions:
                if self._matrix[direction] == '-':
                    count_plus += 1
            self._count_plus = count_plus
            if element == '+':
                if count_plus == 0 or count_plus == 2: 
                    return True


    def unsolvable(self) -> bool:
        '''
        If the U key is pressed, it reveal if the game is unsolvable(3 condition for unsolvability)
        '''
        parameter1 = True
        parameter2 = True
        parameter3 = True

        for i in range(0, len(self._matrix) - self._cols):   
            self._count_unsolvable = 0 
            self._count_cross = 0              
            element = self._matrix[i]
            x = i % self._cols
            y = i // self._cols                                
            directions = [i + 1, i - 1, (y - 1) * self._cols + x, (y + 1) * self._cols + x]
            for direction in directions:
                if self._matrix[direction] == '-':
                    self._count_unsolvable += 1
                elif self._matrix[direction] == 'x':
                    self._count_cross += 1
                    
            if element == '0' or element == '1' or element == '2' or element == '3':
                if self._count_unsolvable > int(element):
                    parameter1 = False
                            
            if element == '+':
                if self._count_unsolvable > 2:
                    parameter2 = False

            if element == '1' and self._count_cross == 4 or element == '2' and self._count_cross == 3 or element == '3' and self._count_cross == 2:
                parameter3 = False

        if not parameter1 or not parameter2 or not parameter3 or self._condition2:
            return False
        else:
            return True


    #def suggestions(self, x: int, y: int):
    #'''If H key and left mouse button are pressed it give an help drawing a line or a flag in the requested position
    #'''
    #    directions = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
    #    if x % 2 == 0 and y % 2 != 0 or  y % 2 == 0 and x % 2 != 0:
    #        for direction in directions:
    #            if self.value_at(*direction) in self._numbers:
    #                self.play_at(x, y)
    #                self.autofill_numbers((x - 1), y)


def main():
    gamemode = int(g2d.prompt("Game mode? \n 1 - 5x5 \n 2 - 10x10 \n 3 - 18x10 \n 4 - 36x20"))
    if gamemode == 1: game = SlitherGame("game_5x5.txt", 11, 11)
    if gamemode == 2: game = SlitherGame("game_10x10.txt", 21, 21)
    if gamemode == 3: game = SlitherGame("game_18x10.txt", 21, 37)                #GAMEMODE
    if gamemode == 4: game = SlitherGame("game_36x20.txt", 39, 73)        
    gui_play(game)
    console_play(game)
    
main()