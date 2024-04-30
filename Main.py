import tkinter as tk
import numpy as np
import heapq
import time
import configurations as cf

class PuzzleSolver:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        
    @staticmethod    
    def manhattan_distance(state):
        distance = 0
        for i in range(1, 9):
            current_position = state.index(str(i))
            goal_position = i - 1
            current_row, current_col = divmod(current_position, 3)
            goal_row, goal_col = divmod(goal_position, 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        return distance
    
    @staticmethod
    def get_neighbors(state):
        neighbors = []
        zero_index = state.index("")
        zero_row, zero_col = divmod(zero_index, 3)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dr, dc in directions:
            new_row, new_col = zero_row + dr, zero_col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_index = new_row * 3 + new_col
                new_state = state[:]
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
                neighbors.append(new_state)
        return neighbors

    def a_star_search(self):
        initial_state = tuple(self.initial_state)
        goal_state = tuple(self.goal_state)
        open_set = []
        heapq.heappush(open_set, (0, initial_state))
        came_from = {initial_state: None}
        g_score = {initial_state: 0}
        f_score = {initial_state: self.manhattan_distance(initial_state)}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal_state:
                return self.reconstruct_path(came_from, current)

            for next_state in self.get_neighbors(list(current)):
                next_state = tuple(next_state)
                tentative_g_score = g_score[current] + 1
                if next_state not in g_score or tentative_g_score < g_score[next_state]:
                    came_from[next_state] = current
                    g_score[next_state] = tentative_g_score
                    f_score[next_state] = tentative_g_score + self.manhattan_distance(next_state)
                    heapq.heappush(open_set, (f_score[next_state], next_state))

        return None
    
    @staticmethod
    def reconstruct_path(came_from, current):
        path = []
        while current:
            path.append(list(current))
            current = came_from.get(current)
        return path[::-1]
    
    
class PuzzleGame:
    def __init__(self, master):
        self.master = master
        self.master.title("8-Puzzle Game")
        self.master.geometry("600x600")
        self.tiles = {}
        self.moves = 0
        self.status_bar = tk.Label(self.master, text="Shuffling...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.puzzle = self.generate_puzzle()
        self.winning_pos = [str(i) for i in range(1, 9)] + [""]
        self.start_game(self.puzzle)
        
    def solve_puzzle(self):
        initial_state = [self.tiles[(row, col)]['text'] for row in range(3) for col in range(3)]
        solver = PuzzleSolver(initial_state, self.winning_pos)
        solution_path = solver.a_star_search()
        if solution_path:
            self.show_solution(solution_path)
        else:
            self.update_status_bar("No solution found.")

    def show_solution(self, solution_path):
        for delay, state in enumerate(solution_path, 1):
            self.master.after(delay * 500, self.update_puzzle, state)
            if delay % 10 == 0:
                self.master.update()

    def show_solution(self, solution_path, index=0):
        if index < len(solution_path):
            state = solution_path[index]
            self.update_puzzle(state)
            self.master.after(500, self.show_solution, solution_path, index + 1)
        else:
            self.update_status_bar("Solved.")
        
    def find_empty_tile(self):
        for row in range(3):
            for col in range(3):
                if self.tiles[(row, col)]['text'] == "":
                    return row, col

    def swap_tiles(self, clicked_tile, empty_tile):
        self.tiles[clicked_tile]['text'], self.tiles[empty_tile]['text'] = self.tiles[empty_tile]['text'], self.tiles[clicked_tile]['text']
        self.tiles[empty_tile]['background'] = 'white'
        self.tiles[clicked_tile]['background'] = cf._from_rgb((0, 255, 100))
        self.moves += 1
        self.update_status_bar(f"Moves: {self.moves}")
        
    def on_tile_click(self, row, col):
        empty_x, empty_y = self.find_empty_tile()
        if ((row == empty_x and abs(col - empty_y) == 1) or (col == empty_y and abs(row - empty_x) == 1)):
            self.swap_tiles((row, col), (empty_x, empty_y))
            self.check_winning_state()

    def is_solvable(self, puzzle):
        p = puzzle[puzzle != 0]
        inversions = 0
        for i, x in enumerate(p):
            for y in p[i + 1:]:
                if x > y:
                    inversions += 1
        return inversions % 2 == 0

    def check_winning_state(self):
        current_state = [self.tiles[(row, col)]['text'] for row in range(3) for col in range(3)]
        if current_state == self.winning_pos :
            self.update_status_bar("Congratulations, You Won!!")
            
    def update_status_bar(self, message):
        self.status_bar.config(text=message)        

    def generate_puzzle(self):
        while True:
            puzzle = np.random.permutation(9)
            if self.is_solvable(puzzle):
                return puzzle

    def reset_game(self):
        self.moves = 0
        self.update_status_bar("Shuffling...")
        self.puzzle = self.generate_puzzle()
        self.tiles[self.find_empty_tile()]["background"] = 'white'
        for c, i in enumerate(self.puzzle.flatten()):
            row, col = divmod(c, 3)
            self.tiles[(row, col)].config(text=str(i) if i != 0 else "", background=cf._from_rgb((0, 255, 100)) if i == 0 else None)

    def start_game(self, p):
        self.tiles_frame = tk.Frame(self.master)
        self.tiles_frame.pack()
        for c, i in enumerate(p):
            row, col = divmod(c, 3)
            if i == 0:
                tile = tk.Button(self.tiles_frame, background=cf._from_rgb((0, 255, 100)), text="", width=7, height=4,
                                command=lambda x=row, y=col: self.on_tile_click(x, y))
            else:
                tile = tk.Button(self.tiles_frame, background='white', text=str(i), width=7, height=4,
                                command=lambda x=row, y=col: self.on_tile_click(x, y))
            tile.grid(row=row, column=col)
            self.tiles[(row, col)] = tile
        reset_button = tk.Button(self.master, text="Restart", width=7, height=2, command=self.reset_game)
        reset_button.pack()
        self.update_status_bar("Ready to play!")
        solve_button = tk.Button(self.master, text="Solve", width=7, height=2, command=self.solve_puzzle)
        solve_button.pack()
        
    def update_puzzle(self, state):
        for index, tile_value in enumerate(state):
            row, col = divmod(index, 3)
            if tile_value == "":
                self.tiles[(row, col)]['background'] = cf._from_rgb((0, 255, 100))
            else:
                self.tiles[(row, col)]['background'] = 'white'
            self.tiles[(row, col)]['text'] = tile_value
        self.moves += 1
        self.update_status_bar(f"Moves: {self.moves}")
        
    def show_solution(self, solution_path):
        for state in solution_path:
            self.update_puzzle(state)
            self.master.update_idletasks()
            time.sleep(0.2)  
        

if __name__ == '__main__':
    mainWindow = tk.Tk()
    game = PuzzleGame(mainWindow)
    mainWindow.mainloop()