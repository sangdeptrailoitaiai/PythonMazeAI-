from collections import deque
from queue import PriorityQueue
from maze import Maze
import random
import math

class MazeSolver:
    """Class giải quyết mê cung sử dụng các thuật toán tìm kiếm khác nhau."""
    
    def __init__(self, maze):
        """
        Khởi tạo solver với mê cung cho trước.
        
        Args:
            maze: Đối tượng Maze cần giải
        """
        self.visited_positions = set()  # Khởi tạo tập các vị trí đã thăm trước
        self.set_maze(maze)  # Sau đó mới gọi set_maze
        # Thêm các biến cho Q-learning
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1

    def set_maze(self, maze):
        """
        Cập nhật mê cung cần giải.
        
        Args:
            maze: Đối tượng Maze mới
        """
        self.maze = maze
        self.grid = maze.grid
        self.goal = (maze.end_x, maze.end_y)
        self.visited_positions.clear()  # Xóa các vị trí đã thăm khi cập nhật mê cung mới
        
    def heuristic(self, pos):
        """
        Tính hàm heuristic cho vị trí hiện tại.
        
        Args:
            pos (tuple): Vị trí cần tính heuristic
            
        Returns:
            float: Giá trị heuristic (khoảng cách Manhattan đến đích + phạt cho các ô gần bom)
        """
        # Khoảng cách Manhattan đến đích
        manhattan_dist = abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])
        #Ước lượng khoảng cách từ pos đến goal bằng tổng khoảng cách ngang + dọc.
        
        # Phạt cho các ô gần bom
        bomb_penalty = 0
        for bomb in self.maze.bombs:
            bomb_dist = abs(pos[0] - bomb[0]) + abs(pos[1] - bomb[1])
            if bomb_dist < 3:  # Nếu gần bom
                bomb_penalty += (3 - bomb_dist) * 1.5  # Giảm hệ số phạt
        
        # Thêm phạt cho các ô đã thăm
        visited_penalty = 0
        if pos in self.visited_positions:
            visited_penalty = 2
            
        return manhattan_dist + bomb_penalty + visited_penalty 
    # Trả về tổng khoảng cách Manhattan đến đích + phạt cho các ô gần bom + phạt cho các ô đã thăm.

    def get_neighbors(self, node, visited):
        """
        Lấy danh sách các ô lân cận có thể đi được.
        
        Args:
            node (tuple): Vị trí hiện tại
            visited (set): Tập các vị trí đã thăm
            
        Returns:
            list: Danh sách các vị trí lân cận hợp lệ
        """
        neighbors = []
        x, y = node #Tách node thành tọa độ x, y.
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if self.is_valid(nx, ny) and neighbor not in visited:
                neighbors.append(neighbor)
        return neighbors

    def solve_bfs(self, start):
        """
        Giải mê cung bằng thuật toán BFS.
        
        Args:
            start (tuple): Vị trí bắt đầu
            
        Returns:
            list: Danh sách các bước đi đến đích
        """
        if self.goal is None:
            return []

        queue = deque() # hàng đợi
        visited = set() # Lưu các ô đã đi qua để không duyệt lại.
        parent = {} # Lưu đường đi để truy ngược từ goal về start.

        queue.append(start) # thêm vị trí bắt đầu vào hàng đợi
        visited.add(start) # đánh dấu đã đi qua.

        while queue: # duyệt hàng đợi
            current = queue.popleft() #Lấy ô đầu hàng đợi (current)
            if current == self.goal: # nếu đạt đích thì dừng
                break

            for neighbor in self.get_neighbors(current, visited): # duyệt các ô lân cận
                queue.append(neighbor) # thêm vào hàng đợi
                visited.add(neighbor) # đánh dấu đã đi qua
                parent[neighbor] = current # lưu đường đi

        path = self.reconstruct_path(parent, start) # tái tạo đường đi
        return path # trả về đường đi

    def solve_a_star(self, start):
        """
        Giải mê cung bằng thuật toán A*.
        
        Args:
            start (tuple): Vị trí bắt đầu
            
        Returns:
            list: Danh sách các bước đi đến đích
        """
        #f(n) = g(n) + h(n)
        #g(n) là chi phí đi từ start đến n.
        #h(n) là ước lượng khoảng cách từ n đến goal.
        if start == self.goal:
            return []

        # Khởi tạo các cấu trúc dữ liệu
        open_set = PriorityQueue()  # Hàng đợi ưu tiên cho các node cần xét
        open_set.put((0, start))  # (f_score, node)
        came_from = {}  # Lưu node cha để tái tạo đường đi
        g_score = {start: 0}  # Chi phí từ start đến node hiện tại
        f_score = {start: self.heuristic(start)}  # Tổng chi phí dự kiến
        closed_set = set()  # Tập các node đã xét
        self.visited_positions.clear()  # Xóa các vị trí đã thăm trước khi bắt đầu tìm kiếm mới

        while not open_set.empty(): # duyệt hàng đợi
            current = open_set.get()[1]  # Lấy node có f_score nhỏ nhất
            self.visited_positions.add(current)  # Thêm vào tập các vị trí đã thăm

            if current == self.goal:
                # Tìm thấy đường đi, tái tạo đường đi
                return self.reconstruct_path(came_from, start)

            closed_set.add(current) #Nếu chưa đến đích, thêm current vào closed_set để không xét lại sau này.

            # Xét các node lân cận
            for neighbor in self.get_neighbors(current, closed_set):
                tentative_g_score = g_score[current] + 1 #Tính thử chi phí đi đến neighbor qua current

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # Tìm thấy đường đi tốt hơn
                    came_from[neighbor] = current  # lưu đường đi để tái tạo
                    g_score[neighbor] = tentative_g_score #Cập nhật chi phí thực tế đã đi
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor) #Tính tổng chi phí dự kiến
                    if neighbor not in closed_set: #Nếu neighbor chưa được xét
                        open_set.put((f_score[neighbor], neighbor)) #Thêm vào hàng đợi ưu tiên

        return []

    def solve_q_learning(self, start):
        """
        Giải mê cung bằng thuật toán Q-learning.
        
        Args:
            start (tuple): Vị trí bắt đầu
            
        Returns:
            list: Danh sách các bước đi đến đích
        """
        if start == self.goal:
            return []

        # Khởi tạo Q-table nếu chưa có
        if not self.q_table:
            for y in range(self.maze.height):
                for x in range(self.maze.width):
                    if self.is_valid(x, y):  # Chỉ khởi tạo cho các ô có thể đi được
                        state = (x, y) #Tạo một trạng thái (state) dạng tọa độ: (x, y).
                        self.q_table[state] = { #Khởi tạo Q-table cho trạng thái state với 4 hành động: UP, DOWN, LEFT, RIGHT.
                            "UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0 #Giá trị ban đầu của Q-table là 0.
                        }

        # Huấn luyện Q-learning
        for episode in range(1000):  # Lặp qua trình học 1000 lần, Mỗi lần gọi là một episode – tức là một lần chạy từ đầu (start) đến goal (hoặc bị kẹt).
            state = start #Bắt đầu từ vị trí start.
            while state != self.goal: #Duyệt tới khi đạt đích.
                # Chọn hành động theo epsilon-greedy
                if random.random() < self.epsilon:
                    action = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
                else:
                    action = max(self.q_table[state].items(), key=lambda x: x[1])[0]

                # Thực hiện hành động
                next_state = self.move_state(state, action)
                
                # Đảm bảo next_state có trong Q-table
                if next_state not in self.q_table:
                    self.q_table[next_state] = {
                        "UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0
                    }

                # Tính toán reward
                reward = -1  # Phạt cho mỗi bước đi
                if next_state == self.goal:
                    reward = 100  # Thưởng khi đến đích
                elif next_state in self.maze.bombs:
                    reward = -100  # Phạt khi gặp bom

                # Cập nhật Q-value
                old_value = self.q_table[state][action]
                next_max = max(self.q_table[next_state].values())
                new_value = (1 - self.learning_rate) * old_value + \
                           self.learning_rate * (reward + self.discount_factor * next_max)
                self.q_table[state][action] = new_value

                state = next_state

        # Tìm đường đi tốt nhất
        parent = {}
        state = start
        visited = set()

        while state != self.goal and state not in visited:
            visited.add(state)
            if state not in self.q_table:
                self.q_table[state] = {
                    "UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0
                }
            action = max(self.q_table[state].items(), key=lambda x: x[1])[0]
            next_state = self.move_state(state, action)
            if not self.is_valid(*next_state):
                break
            parent[next_state] = state
            state = next_state

        return self.reconstruct_path(parent, start) if state == self.goal else []

    def solve_backtracking(self, start):
        """
        Giải mê cung bằng thuật toán Backtracking.
        
        Args:
            start (tuple): Vị trí bắt đầu
            
        Returns:
            list: Danh sách các bước đi đến đích
        """
        if start == self.goal:
            return []

        parent = {}
        visited = set()

        def backtrack(current):
            if current == self.goal:
                return True

            visited.add(current)
            x, y = current

            # Thử các hướng đi có thể
            directions = [
                ("UP", (x, y-1)),
                ("DOWN", (x, y+1)),
                ("LEFT", (x-1, y)),
                ("RIGHT", (x+1, y))
            ]
            random.shuffle(directions)  # Thêm tính ngẫu nhiên

            for _, (nx, ny) in directions: #_ đại diện cho phần bạn không cần dùng (tên hướng "UP", "DOWN"...)
                if self.is_valid(nx, ny) and (nx, ny) not in visited:
                    parent[(nx, ny)] = current
                    if backtrack((nx, ny)):
                        return True

            visited.remove(current)
            return False

        # Bắt đầu backtracking
        if backtrack(start):
            return self.reconstruct_path(parent, start)
        return []

    def reconstruct_path(self, parent, start):
        """
        Tái tạo đường đi từ bảng parent.
        
        Args:
            parent (dict): Bảng lưu thông tin cha của mỗi node
            start (tuple): Vị trí bắt đầu
            
        Returns:
            list: Danh sách các bước đi
        """
        path = []
        current = self.goal
        while current != start:
            prev = parent.get(current)
            if not prev:
                return []
            dx = current[0] - prev[0]
            dy = current[1] - prev[1]
            if dx == 1:
                path.append("RIGHT")
            elif dx == -1:
                path.append("LEFT")
            elif dy == 1:
                path.append("DOWN")
            elif dy == -1:
                path.append("UP")
            current = prev
        path.reverse()
        return path

    def is_valid(self, x, y):
        """
        Kiểm tra vị trí có hợp lệ không.
        
        Args:
            x (int): Tọa độ x
            y (int): Tọa độ y
            
        Returns:
            bool: True nếu vị trí hợp lệ
        """
        return (0 <= x < self.maze.width and 
                0 <= y < self.maze.height and 
                self.maze.grid[y][x] == 0)

    def move_state(self, state, action):
        """
        Tính toán vị trí mới sau khi thực hiện hành động.
        
        Args:
            state (tuple): Vị trí hiện tại (x, y)
            action (str): Hành động cần thực hiện ("UP", "DOWN", "LEFT", "RIGHT")
            
        Returns:
            tuple: Vị trí mới (x, y)
        """
        x, y = state
        if action == "UP":
            new_y = y - 1
            if self.is_valid(x, new_y):
                return (x, new_y)
        elif action == "DOWN":
            new_y = y + 1
            if self.is_valid(x, new_y):
                return (x, new_y)
        elif action == "LEFT":
            new_x = x - 1
            if self.is_valid(new_x, y):
                return (new_x, y)
        elif action == "RIGHT":
            new_x = x + 1
            if self.is_valid(new_x, y):
                return (new_x, y)
        return state  # Nếu không thể di chuyển, giữ nguyên vị trí

    def solve_simulated_annealing(self, start):
        """
        Giải mê cung bằng thuật toán Simulated Annealing (đảm bảo đường đi hợp lệ và đến đích).
        """
        if start == self.goal:
            return []

        def random_valid_path():
            # Sinh một đường đi hợp lệ ngẫu nhiên từ start đến goal
            from collections import deque
            visited = set()
            queue = deque()
            parent = {}
            queue.append(start)
            visited.add(start)
            
            while queue:
                pos = queue.popleft()
                if pos == self.goal:
                    return self.reconstruct_path(parent, start)
                
                neighbors = []
                for dx, dy, direction in [(-1, 0, "LEFT"), (1, 0, "RIGHT"), (0, -1, "UP"), (0, 1, "DOWN")]:
                    nx, ny = pos[0] + dx, pos[1] + dy
                    if self.is_valid(nx, ny) and (nx, ny) not in visited:
                        neighbors.append((nx, ny))
                random.shuffle(neighbors)
                for next_pos in neighbors:
                    queue.append(next_pos)
                    visited.add(next_pos)
                    parent[next_pos] = pos
            return []

        def follow_path(pos, path):
            # Trả về vị trí cuối cùng sau khi đi theo path
            for direction in path:
                if direction == "UP":
                    pos = (pos[0], pos[1] - 1)
                elif direction == "DOWN":
                    pos = (pos[0], pos[1] + 1)
                elif direction == "LEFT":
                    pos = (pos[0] - 1, pos[1])
                elif direction == "RIGHT":
                    pos = (pos[0] + 1, pos[1])
            return pos

        def calculate_energy(path):
            # Độ dài đường đi + phạt nếu đi qua gần bom
            pos = start
            bomb_penalty = 0
            for direction in path:
                if direction == "UP":
                    pos = (pos[0], pos[1] - 1)
                elif direction == "DOWN":
                    pos = (pos[0], pos[1] + 1)
                elif direction == "LEFT":
                    pos = (pos[0] - 1, pos[1])
                elif direction == "RIGHT":
                    pos = (pos[0] + 1, pos[1])
                for bomb in self.maze.bombs:
                    bomb_dist = abs(pos[0] - bomb[0]) + abs(pos[1] - bomb[1])
                    if bomb_dist < 3:
                        bomb_penalty += (3 - bomb_dist) * 2
            return len(path) + bomb_penalty

        # Khởi tạo đường đi hợp lệ ban đầu
        current_path = random_valid_path()
        if not current_path:
            return []
        current_energy = calculate_energy(current_path)
        best_path = current_path.copy()
        best_energy = current_energy

        # Tham số Simulated Annealing
        initial_temp = 100.0
        final_temp = 0.1
        alpha = 0.95
        iterations_per_temp = 100
        current_temp = initial_temp

        while current_temp > final_temp:
            for _ in range(iterations_per_temp):
                # Tạo đường đi mới bằng cách thay đổi một đoạn nhỏ trong path
                if len(current_path) < 2:
                    continue
                cut = random.randint(1, len(current_path) - 1)
                pos = follow_path(start, current_path[:cut])
                # Sinh lại phần còn lại từ vị trí cut đến goal
                self_for_sa = self  # for closure
                def random_path_from(pos):
                    from collections import deque
                    visited = set()
                    queue = deque()
                    parent = {}
                    queue.append(pos)
                    visited.add(pos)
                    
                    while queue:
                        p = queue.popleft()
                        if p == self_for_sa.goal:
                            return self_for_sa.reconstruct_path(parent, pos)
                        
                        neighbors = []
                        for dx, dy, direction in [(-1, 0, "LEFT"), (1, 0, "RIGHT"), (0, -1, "UP"), (0, 1, "DOWN")]:
                            nx, ny = p[0] + dx, p[1] + dy
                            if self_for_sa.is_valid(nx, ny) and (nx, ny) not in visited:
                                neighbors.append((nx, ny))
                        random.shuffle(neighbors)
                        for next_pos in neighbors:
                            queue.append(next_pos)
                            visited.add(next_pos)
                            parent[next_pos] = p
                    return []
                new_tail = random_path_from(pos)
                if not new_tail:
                    continue
                new_path = current_path[:cut] + new_tail
                new_energy = calculate_energy(new_path)
                delta_energy = new_energy - current_energy
                if delta_energy < 0 or random.random() < math.exp(-delta_energy / current_temp):
                    current_path = new_path
                    current_energy = new_energy
                    if current_energy < best_energy:
                        best_path = current_path.copy()
                        best_energy = current_energy
            current_temp *= alpha
        return best_path if follow_path(start, best_path) == self.goal else []




