import pygame
import threading
import os

tile_size = 20

class Player:
    """Class đại diện cho người chơi trong game."""
    
    def __init__(self, maze):
        """
        Khởi tạo người chơi.
        
        Args:
            maze: Đối tượng Maze
        """
        self.maze = maze
        self.x = maze.start_x
        self.y = maze.start_y
        self.start_x = self.x
        self.start_y = self.y
        self.path = [(self.x, self.y)]
        self.move_history = [(self.x, self.y)]
        self.reversing = False
        
        # Load player image
        self.image = pygame.image.load('image/Player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        
        # Load sounds
        self.move_sound = pygame.mixer.Sound('image/move.wav') if os.path.exists('image/move.wav') else None
        self.bomb_sound = pygame.mixer.Sound('image/bomb.wav') if os.path.exists('image/bomb.wav') else None
        
        self.font = pygame.font.SysFont('arial', 20)
        self.step_count = 0
        self.bomb_hits = 0

    def can_move(self, dx, dy):
        """
        Kiểm tra xem có thể di chuyển theo hướng cho trước không.
        
        Args:
            dx (int): Độ dịch theo trục x
            dy (int): Độ dịch theo trục y
            
        Returns:
            bool: True nếu có thể di chuyển, False nếu không
        """
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Chỉ kiểm tra biên mê cung và tường
        return (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] != 1)

    def handle_bomb_collision(self):
        """Xử lý va chạm với bom."""
        self.reversing = True
        self.bomb_hits += 1

        if len(self.move_history) >= 4:
            for _ in range(3):
                if self.move_history:
                    x, y = self.move_history.pop()
                    if (x, y) in self.path:
                        self.path.remove((x, y))
        else:
            # Không đủ bước để lùi → reset
            self.reset_position()
            return

        # Cập nhật lại tọa độ cuối cùng sau khi lùi
        if self.move_history:
            self.x, self.y = self.move_history[-1]
            self.path.append((self.x, self.y))
            self.move_history.append((self.x, self.y))

        if self.bomb_sound:
            threading.Thread(target=self.play_sound, args=(self.bomb_sound,)).start()

    def reset_position(self):
        """Reset vị trí người chơi về điểm bắt đầu."""
        self.x = self.start_x
        self.y = self.start_y
        self.path = [(self.x, self.y)]
        self.move_history = [(self.x, self.y)]
        self.reversing = False
        if self.bomb_sound:
            threading.Thread(target=self.play_sound, args=(self.bomb_sound,)).start()

    def play_sound(self, sound):
        """Phát âm thanh."""
        sound.play()

    def move(self, direction):
        """
        Di chuyển người chơi theo hướng cho trước.
        
        Args:
            direction (str): Hướng di chuyển ('UP', 'DOWN', 'LEFT', 'RIGHT')
        """
        dx, dy = 0, 0
        if direction == 'UP':
            dy = -1
        elif direction == 'DOWN':
            dy = 1
        elif direction == 'LEFT':
            dx = -1
        elif direction == 'RIGHT':
            dx = 1

        # Kiểm tra có thể di chuyển không
        if not self.can_move(dx, dy):
            return

        next_x = self.x + dx
        next_y = self.y + dy
        self.step_count += 1

        # Nếu ô tiếp theo là ô trống hoặc chứa bom
        if self.maze.grid[next_y][next_x] == 0 or (next_x, next_y) in self.maze.bombs:
            if not self.reversing and (next_x, next_y) in self.maze.bombs:
                self.handle_bomb_collision()
                return

            # Di chuyển bình thường
            self.x = next_x
            self.y = next_y
            if (self.x, self.y) not in self.path:
                self.path.append((self.x, self.y))
            self.move_history.append((self.x, self.y))
            self.reversing = False
            
            if self.move_sound:
                threading.Thread(target=self.play_sound, args=(self.move_sound,)).start()

    def draw(self):
        """Vẽ người chơi và đường đi lên màn hình."""
        screen = pygame.display.get_surface()

        # Vẽ đường đi
        for px, py in self.path:
            if (px, py) != (self.x, self.y):
                pygame.draw.rect(screen, (173, 216, 230), 
                               (px * tile_size, py * tile_size, tile_size, tile_size))

        # Vẽ người chơi
        screen.blit(self.image, (self.x * tile_size, self.y * tile_size))
        self.draw_status(screen)

    def draw_status(self, screen):
        """Vẽ thông tin trạng thái người chơi."""
        status_text = f"Steps: {self.step_count}   Bombs: {self.bomb_hits}"
        text_surface = self.font.render(status_text, True, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width() - text_surface.get_width() - 10, 10))


