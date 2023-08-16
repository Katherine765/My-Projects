from random import randint, choice
from tkinter import *

tk = Tk()
canvas = Canvas(tk, width=270, height=340) #height was 340 without bottom messages
canvas.pack()
canvas.create_rectangle(15, 55, 255, 295, fill='#BBAFA0', outline='')
canvas.create_text(50, 30, text='2048', font=('Helvetica', 25, 'bold'), fill='#776E65')
canvas.create_text(135, 15, text='Score', font=('Helvetica', 10, 'bold'), fill='#776E65')
#canvas.create_text(225, 15, text='High Score', font=('Helvetica', 10, 'bold'), fill='#776E65')


# Puts the lighter gray squares on top of the big square
LENGTH = 50
coordinates = []
y = 63
for a in range(4):
    x = 23
    for b in range(4):
        canvas.create_rectangle(x, y, x + LENGTH, y + LENGTH, fill='#CDC1B4', outline='')
        coordinates.append((x, y))
        x += 58
    y += 58

class Game():
    def __init__(self, coordinates):
        self.board = [None for x in range(16)]
        self.coordinates = coordinates
        self.temporary = []
        self.already_combined = []
        self.win = False
        self.score = 0
        self.colors = {2: '#EEE4DA', 4: '#EDE0C8', 8: '#F2B179', 16: '#F59563',\
                       32: '#F67C5F', 64: '#F65E3B', 128: '#EDCF72', 256: '#EDCC61',\
                       512: '#EDC850', 1024: '#EDC53F', 2048: '#EDC22E',\
                       4096: '#F4A63A', 8192: '#F57C5F', 16384: '#F75D5D'}

    def check_if_combined(self,current_block, next_block):
        #so that 2 2 4 or 4 2 2 don't become 8 in one arrow press
        if current_block in self.already_combined or next_block in self.already_combined:
            return True
        return False
        
    
    def new_block(self):
        """Generate a new block in an empty cell."""
        value = 4 if randint(0, 9) == 0 else 2
        self.board[choice(self.block_list('empties'))] = value

        
    def update(self):
        """Update the game board display on the canvas."""
        for ID in self.temporary:
            canvas.delete(ID)
        
        for a in range(16):
            value = self.board[a]
            if not value is None:
                x = self.coordinates[a][0]
                y = self.coordinates[a][1]
                self.temporary.append(canvas.create_rectangle(x, y, x + LENGTH, y + LENGTH, fill=self.colors[value], outline=''))
                self.temporary.append(canvas.create_text(x + 25, y + 25, text=value, \
                                                         font=('Helvetica', 18 if value<1000 else 13, 'bold'), \
                                                         fill='#776E65' if value in (2,4) else '#F9F6F2'))

        #score
        self.temporary.append(canvas.create_text(135, 30, text=self.score, font=('Helvetica', 10, 'bold'), fill='#776E65'))

    def block_list(self, group):
        """Return a list of indices of empty or filled cells."""
        empties = []
        fulls = []
        for index, block in enumerate(self.board):
            if block is None:
                empties.append(index)
            else:
                fulls.append(index)
        return locals()[group]
            
    def arrow(self, order):
        """Handle arrow key input and move blocks accordingly."""
        self.already_combined = []
        #the first four blocks against the target wall don't have anywhere to move to
        for blockID in order[4:16]:
            fulls = self.block_list('fulls')
            if blockID in fulls:
                current_block = blockID
                
                #the next_block will always be 4 IDs closer to the target wall, and therefore backwards within the order
                next_block_index = order.index(blockID) - 4
                next_block = order[next_block_index]

                #the next_block will always be the first to become out of range
                while 16 > next_block_index > -1:
                    #move to empty spot
                    if self.board[next_block] is None:
                        self.board[next_block] = self.board[current_block]
                        self.board[current_block] = None
                    #combine with the same block type
                    elif self.board[next_block] == self.board[current_block] and not self.check_if_combined(current_block, next_block):
                        self.board[next_block] *= 2
                        self.score += self.board[next_block]
                        self.board[current_block] = None

                        try:
                            del self.already_combined[current_block]
                        except:
                            pass
                        self.already_combined.append(next_block)
                        
                        
                    current_block = order[order.index(current_block) - 4]
                    next_block_index = order.index(current_block) - 4
                    next_block = order[next_block_index]
        try:
            self.new_block()
        except:
            #basically the board is full and you pressed an arrow that didn't move anything, so no new blocks freed up
            pass
        
        self.update()
        self.win_lose()

    def win_lose(self):
        if not self.win and 2048 in self.board:
            self.win = True
            canvas.create_text(58, 320, text='YOU WIN', font=('Helvetica', 15, 'bold'), fill='#776E65')
            
        elif not None in self.board:
            for index, value in enumerate(self.board):
                if value in self.get_touching_values(index):
                    break
            else:
                canvas.create_text(194, 320, text='GAME OVER', font=('Helvetica', 15, 'bold'), fill='#776E65')
                canvas.unbind_all("<Left>")
                canvas.unbind_all("<Right>")
                canvas.unbind_all("<Up>")
                canvas.unbind_all("<Down>")
                
                
    
    #chat gpt wrote the first half of this cuz i didn't feel like it
    def get_touching_values(self, blockID):
        row = blockID // 4
        col = blockID % 4
        touching_blocks = []
        if row > 0: touching_blocks.append(blockID - 4)
        if row < 3: touching_blocks.append(blockID + 4)
        if col > 0: touching_blocks.append(blockID - 1)
        if col < 3: touching_blocks.append(blockID + 1)

        touching_values = [self.board[ID] for ID in touching_blocks]
        return touching_values
      
    def up(self, e):
        self.arrow(list(range(16))) 
    
    def down(self, e):
        self.arrow(list(range(15, -1, -1))) 
    
    def left(self, e):
        self.arrow((0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15)) 
    
    def right(self, e):
        self.arrow((3, 7, 11, 15, 2, 6, 10, 14, 1, 5, 9, 13, 0, 4, 8, 12)) 

game = Game(coordinates)
game.new_block()
game.new_block()
game.update()
canvas.bind_all('<Down>', game.down)
canvas.bind_all('<Up>', game.up)
canvas.bind_all('<Left>', game.left)
canvas.bind_all('<Right>', game.right)
