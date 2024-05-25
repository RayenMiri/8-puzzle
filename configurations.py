import pygame

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

pygame.mixer.init()

laucher_sound= pygame.mixer.Sound('lancher_music.mp3')
move_sound = pygame.mixer.Sound('Swipe Swoosh Transition Sound Effect.mp3')
winning_sound = pygame.mixer.Sound('WIN sound effect no copyright.mp3')
applause_sound = pygame.mixer.Sound('Applause  Sound Effect.mp3')