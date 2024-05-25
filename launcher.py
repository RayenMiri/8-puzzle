import tkinter as tk
from Main import PuzzleGame
from configurations import laucher_sound

def launcher():
    launcher_window.destroy()
    mainWindow = tk.Tk()
    game = PuzzleGame(mainWindow)
    mainWindow.mainloop()

def main():
    global launcher_window
    launcher_window = tk.Tk()
    launcher_window.title("8-Puzzle Game Launcher")
    laucher_sound.play()
    
    w_width = 1000
    w_height = 600
    screen_width = launcher_window.winfo_screenwidth()
    screen_height = launcher_window.winfo_screenheight()
    center_x = int(screen_width / 2 - w_width / 2)
    center_y = int(screen_height / 2 - w_height / 2)
    launcher_window.geometry(f'{w_width}x{w_height}+{center_x}+{center_y}')
    launcher_window.configure(bg='#121212')

    welcome_label = tk.Label(
        launcher_window, 
        text="Welcome to 8-Puzzle Game!", 
        font=("Poppins", 24, 'bold'), 
        fg='#FFFFFF', 
        bg='#121212'
    )
    welcome_label.pack(pady=(150, 20))

    play_button = tk.Button(
        launcher_window,
        text="Play",
        height=2,
        width=10,
        font=("Poppins", 16, 'bold'),
        fg='#FFFFFF',
        bg='#1E1E1E',
        activeforeground='#FFFFFF',
        activebackground='#2C2C2C',
        bd=0,
        command=launcher
    )
    play_button.pack(pady=20)

    launcher_window.mainloop()

if __name__ == '__main__':
    main()
   
