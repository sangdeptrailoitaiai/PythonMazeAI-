import pygame 
import random
import image

class Maze:
    """Class đại diện cho mê cung trong game."""
    
    def __init__(self, width, height):
        """
        Khởi tạo mê cung với kích thước cho trước.
        
        Args:
            width (int): Chiều rộng của mê cung
            height (int): Chiều cao của mê cung
        """
        self.width = width
        self.height = height
        self.grid = [[1] * width for _ in range(height)]  
        self.start_x, self.start_y = 1, 1
        self.end_x, self.end_y = width - 2, height - 2
        self.generate_maze()
        self.grid[self.start_y][self.start_x] = 0
        self.grid[self.end_y][self.end_x] = 0
        self.path = []
        self.cell_size = 20
        self.bombs = set()
        self.create_bombs()
        
        # Load images once
        self.wall_image = pygame.image.load('image/cobblestone.png')
        self.wall_image = pygame.transform.scale(self.wall_image, (self.cell_size, self.cell_size))
        self.bomb_image = pygame.image.load('image/bomb.png')
        self.bomb_image = pygame.transform.scale(self.bomb_image, (self.cell_size, self.cell_size))
        
        # Validate maze
        if not self.validate_maze():
            raise ValueError("Generated maze is invalid - no path exists between start and end")

    def validate_maze(self):
        """Kiểm tra xem mê cung có đường đi từ start đến end không."""
        visited = set()
        stack = [(self.start_x, self.start_y)]
        
        while stack:
            x, y = stack.pop()
            if (x, y) == (self.end_x, self.end_y):
                return True
                
            if (x, y) not in visited:
                visited.add((x, y))
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < self.width and 0 <= ny < self.height and 
                        self.grid[ny][nx] == 0 and (nx, ny) not in visited):
                        stack.append((nx, ny))
        return False

    def generate_maze(self):
        """Tạo mê cung ngẫu nhiên sử dụng thuật toán DFS."""
        # Tạo tường bao quanh
        for x in range(self.width):
            self.grid[0][x] = 1
            self.grid[self.height - 1][x] = 1
        for y in range(self.height):
            self.grid[y][0] = 1
            self.grid[y][self.width - 1] = 1
        
        stack = [(1, 1)]
        while stack:
            x, y = stack[-1]
            neighbors = [(x + dx, y + dy) for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)] 
                        if 0 < x + dx < self.width - 1 and 0 < y + dy < self.height - 1]
            unvisited_neighbors = [neighbor for neighbor in neighbors 
                                 if self.grid[neighbor[1]][neighbor[0]] == 1]
            if unvisited_neighbors:
                nx, ny = random.choice(unvisited_neighbors)
                self.grid[ny][nx] = 0
                self.grid[y + (ny - y) // 2][x + (nx - x) // 2] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

    def create_bombs(self, count=20):
        """
        Tạo các chướng ngại vật (bom) trong mê cung.
        
        Args:
            count (int): Số lượng bom cần tạo
        """
        bombs_count = 0
        while bombs_count < count:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if (self.grid[y][x] == 1 and 
                (x, y) != (self.start_x, self.start_y) and 
                (x, y) != (self.end_x, self.end_y) and 
                self.is_far_from_bombs(x, y)):
                self.bombs.add((x, y))
                bombs_count += 1

    def is_far_from_bombs(self, x, y, min_distance=5):
        """
        Kiểm tra xem vị trí có đủ xa các bom khác không.
        
        Args:
            x (int): Tọa độ x
            y (int): Tọa độ y
            min_distance (int): Khoảng cách tối thiểu
            
        Returns:
            bool: True nếu vị trí hợp lệ, False nếu không
        """
        for bomb_x, bomb_y in self.bombs:
            if abs(x - bomb_x) + abs(y - bomb_y) < min_distance:
                return False
        return True

    def draw_maze(self, screen):
        """
        Vẽ mê cung lên màn hình.
        
        Args:
            screen: Surface của pygame để vẽ lên
        """
        # Vẽ tường và đường đi
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    screen.blit(self.wall_image, (x * self.cell_size, y * self.cell_size))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), 
                                   (x * self.cell_size, y * self.cell_size, 
                                    self.cell_size, self.cell_size))
        
        # Vẽ điểm bắt đầu và kết thúc
        pygame.draw.rect(screen, (0, 255, 0), 
                        (self.start_x * self.cell_size, self.start_y * self.cell_size, 
                         self.cell_size, self.cell_size))
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.end_x * self.cell_size, self.end_y * self.cell_size, 
                         self.cell_size, self.cell_size))
        
        # Vẽ đường đi
        for x, y in self.path:
            pygame.draw.rect(screen, (0, 0, 255), 
                           (x * self.cell_size, y * self.cell_size, 
                            self.cell_size, self.cell_size))
        
        # Vẽ bom
        for x, y in self.bombs:
            screen.blit(self.bomb_image, (x * self.cell_size, y * self.cell_size))

        



    

