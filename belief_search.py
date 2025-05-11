from collections import deque
from maze import Maze
import pygame
import time 
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1], 
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1], 
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1], 
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1], 
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1], 
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1], 
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], 
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], 
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1], 
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1], 
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1], 
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1], 
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1], 
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1], 
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1], 
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1], 
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1], 
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

step_index = 0
solution = []
# Các trạng thái ban đầu (ẩn danh)
start_states = {(1, 1), (33, 1), (1, 23)} 
goal = (35-2, 25-2)

import pygame
import threading
pygame.init()

tile_size = 20

class Player:
    def __init__(self, maze,x_index,y_index):
        self.maze = maze
        self.x = x_index
        self.y = y_index
        self.start_x = self.x
        self.start_y = self.y
        self.path = [(self.x, self.y)]
        self.move_history = [(self.x, self.y)]
        self.reversing = False
        self.image = pygame.image.load('image/Player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.font = pygame.font.SysFont('arial', 20)
        self.step_count = 0
        self.bomb_hits = 0

    def can_move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        return (0 <= new_x < self.maze.width and
                0 <= new_y < self.maze.height and
                self.maze.grid[new_y][new_x] != 1)

    def move(self, direction):
        dx, dy = 0, 0
        if direction == 'UP':
            dy = -1
        elif direction == 'DOWN':
            dy = 1
        elif direction == 'LEFT':
            dx = -1
        elif direction == 'RIGHT':
            dx = 1

        next_x = self.x + dx
        next_y = self.y + dy
        self.step_count += 1


        # Kiểm tra biên mê cung
        if not (0 <= next_x < self.maze.width and 0 <= next_y < self.maze.height):
            return

        # Nếu ô tiếp theo là ô trống hoặc chứa chướng ngại vật (bomb)
        if self.maze.grid[next_y][next_x] == 0 or (next_x, next_y) in self.maze.bombs:
            if not self.reversing and (next_x, next_y) in self.maze.bombs:
                self.reversing = True  # bật cờ lùi
                self.bomb_hits += 1

                if len(self.move_history) >= 4:
                    for _ in range(3):
                        if self.move_history:
                            x, y = self.move_history.pop()
                            if (x, y) in self.path:
                                self.path.remove((x, y))
                else:
                    # Không đủ bước để lùi → reset
                    self.x = self.start_x
                    self.y = self.start_y
                    self.path = [(self.x, self.y)]
                    self.move_history = [(self.x, self.y)]
                    self.reversing = False
                    threading.Thread(target=self.play_collision_sound).start()
                    return

                # Cập nhật lại tọa độ cuối cùng sau khi lùi
                if self.move_history:
                    self.x, self.y = self.move_history[-1]
                    self.path.append((self.x, self.y))
                    self.move_history.append((self.x, self.y))

                threading.Thread(target=self.play_collision_sound).start()
                return  # dừng sau khi xử lý bom

            # Nếu không phải bom, di chuyển bình thường
            self.x = next_x
            self.y = next_y
            if (self.x, self.y) not in self.path:
                self.path.append((self.x, self.y))
            self.move_history.append((self.x, self.y))
            self.reversing = False
        

    def play_collision_sound(self):
        # Optional: Thêm âm thanh nếu bạn có file
        pass

    def draw(self):
        screen = pygame.display.get_surface()

        for px, py in self.path:
            if (px, py) != (self.x, self.y):
                pygame.draw.rect(screen, (173, 216, 230), (px * tile_size, py * tile_size, tile_size, tile_size))

        screen.blit(self.image, (self.x * tile_size, self.y * tile_size))
        self.draw_status(screen)

    def draw_status(self, screen):
        # Thời gian tính bằng giây
        status_text = f"Steps: {self.step_count}   Bombs: {self.bomb_hits}"
        text_surface = self.font.render(status_text, True, (0, 0, 0))
        screen.blit(text_surface, (screen.get_width() - text_surface.get_width() - 10, 10))

# Kiểm tra ô hợp lệ
def is_valid(x, y, maze):
    return 0 <= y < len(maze) and 0 <= x < len(maze[0]) and maze[y][x] == 0

# Di chuyển một bước
def move_state(pos, action):
    x, y = pos
    moves = {
        "UP": (0, -1),
        "DOWN": (0, 1),
        "LEFT": (-1, 0),
        "RIGHT": (1, 0)
    }
    dx, dy = moves[action]
    return (x + dx, y + dy)

# Kiểm tra tính hợp lệ của start states
def validate_start_states(start_states, maze):
    valid_states = set()
    for state in start_states:
        if is_valid(*state, maze):
            valid_states.add(state)
    return valid_states

# Cải thiện hàm search_no_observation
def search_no_observation(start_states, goal, maze):
    # Kiểm tra tính hợp lệ của goal state
    if not is_valid(*goal, maze):
        return None
        
    # Kiểm tra tính hợp lệ của start states
    valid_start_states = validate_start_states(start_states, maze)
    if not valid_start_states:
        return None
        
    # Tối ưu: Sử dụng set thay vì list cho visited để tìm kiếm nhanh hơn
    visited = set()
    queue = deque([(valid_start_states, [])])
    
    # Tối ưu: Lưu trữ các trạng thái đã thăm dưới dạng frozenset
    visited.add(frozenset(valid_start_states))
    
    # Tối ưu: Định nghĩa moves một lần duy nhất
    moves = {
        "UP": (0, -1),
        "DOWN": (0, 1),
        "LEFT": (-1, 0),
        "RIGHT": (1, 0)
    }
    
    while queue:
        current_states, path = queue.popleft()
        
        # Tối ưu: Kiểm tra goal state trước khi xử lý các hành động
        if all(state == goal for state in current_states):
            return path

        # Tối ưu: Sắp xếp các hành động theo ưu tiên (hướng về goal)
        actions = []
        for action in ["UP", "DOWN", "LEFT", "RIGHT"]:
            dx, dy = moves[action]
            # Tính khoảng cách trung bình đến goal sau khi thực hiện hành động
            avg_distance = sum(abs(state[0] + dx - goal[0]) + abs(state[1] + dy - goal[1]) 
                             for state in current_states) / len(current_states)
            actions.append((action, avg_distance))
        
        # Sắp xếp các hành động theo khoảng cách trung bình đến goal
        actions.sort(key=lambda x: x[1])
        
        for action, _ in actions:
            next_states = set()
            for state in current_states:
                next_state = move_state(state, action)
                if is_valid(*next_state, maze):
                    next_states.add(next_state)
                else:
                    next_states.add(state)
            
            # Tối ưu: Chỉ thêm vào queue nếu trạng thái mới chưa được thăm
            frozen_next = frozenset(next_states)
            if frozen_next not in visited:
                visited.add(frozen_next)
                queue.append((next_states, path + [action]))
    
    return None

def run_algorithm():
    start_time = time.time()
    print(f"Số lượng trạng thái ban đầu: {len(start_states)}")
    print("Các trạng thái ban đầu:", start_states)
    solution = search_no_observation(start_states, goal, maze)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Thời gian tìm đường đi: {execution_time:.2f} giây")
    return solution

# Khởi tạo pygame
WIDTH, HEIGHT = 1200, 800
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()

image_bg = pygame.image.load('image/background.png')
image_bg = pygame.transform.scale(image_bg, (WIDTH, HEIGHT))

maze1 = Maze(35, 25)
maze1.grid = maze 
maze1.bombs = set()
runing = True
# Tạo đối tượng Player
player1 = Player(maze1, 1, 1)

while runing:
    timer.tick(60)
    screen.blit(image_bg, (0, 0))
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                direction = None
                if event.key == pygame.K_UP: direction = "UP"
                elif event.key == pygame.K_DOWN: direction = "DOWN"
                elif event.key == pygame.K_LEFT: direction = "LEFT"
                elif event.key == pygame.K_RIGHT: direction = "RIGHT"

                if direction:
                    player1.move(direction)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("Đang tìm đường đi...")
                    solution = run_algorithm()
                    print("Đường đi tìm được:")
                    print(solution)
            
    if step_index < len(solution) if solution else 0:
        player1.move(solution[step_index])
        step_index += 1
        pygame.time.delay(80)

    maze1.draw_maze(screen)
    player1.draw()

    pygame.display.flip()


# print("Đường đi tìm được:")
# print( search_no_observation(start_states, goal, maze))
