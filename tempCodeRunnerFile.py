import pygame
import time
from maze import Maze
from player import Player
from ai import MazeSolver
# Phát nhạc nền
pygame.mixer.init()
pygame.mixer.music.load("image/background_music.mp3")  # Đường dẫn đến file nhạc
pygame.mixer.music.set_volume(0.5)  # Âm lượng: 0.0 đến 1.0