import tkinter as tk
import numpy as np
import random
import configurations as cf

mainWindow = tk.Tk()
mainWindow.title("8-Puzzle Game");
mainWindow.geometry("600x600")


def find_empty_tile():
    for row in range(3):
        for col in range(3):
            if tiles[(row, col)]['text'] == "":
                return row, col
          
def swap_tiles(clicked_tile,empty_tile):
    tiles[clicked_tile]['text'],tiles[empty_tile]['text'] = tiles[empty_tile]['text'],tiles[clicked_tile]['text']
    tiles[empty_tile]['background'] = 'white'
    tiles[clicked_tile]['background']=cf._from_rgb((0,255,100))

def on_tile_click(row,col):
    empty_x,empty_y = find_empty_tile()
    if((row == empty_x and abs(col - empty_y) == 1) or (col == empty_y and abs(row - empty_x) == 1)):
        swap_tiles((row,col),(empty_x,empty_y))
        check_winning_state()
        
def is_solvable(puzzle):
    p = puzzle[puzzle != 0]
    inversions = 0
    for i, x in enumerate(p):
        for y in p[i+1:]:
            if x > y:
                inversions += 1
    return inversions % 2==0

def check_winning_state():
    current_state = [tiles[(row,col)]['text'] for row in range(3) for col in range(3)]
    if(current_state == [str(i) for i in range(1,9)]+[""]):
        print('Congratulations , You Won !!')

def generate_puzzle():
    while True:
        puzzle = np.random.permutation(9)
        if is_solvable(puzzle):
            return puzzle
        
def bot_solver():
    return False

def reset_game():
    global puzzle
    puzzle = generate_puzzle()  # Generate a new solvable puzzle
    tiles[find_empty_tile()]["background"]='white'
    for c, i in enumerate(puzzle.flatten()):
        row, col = divmod(c, 3)
        tiles[(row, col)].config(text=str(i) if i != 0 else "", background=cf._from_rgb((0, 255, 100)) if i == 0 else None)

def start_game(p):
    global tiles
    tiles = {}
    for c,i in enumerate(p):
        row, col = divmod(c,3)
        if (i == 0):
            tile  = tk.Button(mainWindow,background=cf._from_rgb((0,255,100)),text="",width=7, height=4,command=lambda x=row,y=col : on_tile_click(x,y))
        else:
            tile  = tk.Button(mainWindow,background='white',text=str(i),width=7, height=4,command=lambda x=row,y=col : on_tile_click(x,y))
        tile.grid(row=row,column = col)
        tiles[(row,col)] = tile
    reset_button = tk.Button(mainWindow, text="Restart", width=7, height=2, command=reset_game)
    reset_button.grid(row=3,column=1)
if __name__ == '__main__':
    puzzle = generate_puzzle()
    start_game(puzzle)
    
   
    mainWindow.mainloop()