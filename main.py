import pygame
import time
from maze import Maze
from player import Player
from ai import MazeSolver
# Phát nhạc nền
pygame.mixer.init()
pygame.mixer.music.load("image/background_music.mp3")  # Đường dẫn đến file nhạc
pygame.mixer.music.set_volume(0.5)  # Âm lượng: 0.0 đến 1.0
pygame.mixer.music.play(-1)  # Lặp vô hạn

pygame.init()
WIDTH, HEIGHT = 1300, 1000
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
LIGHT_PURPLE = (235, 235, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")
font = pygame.font.SysFont('arial', 36)
small_font = pygame.font.SysFont('arial', 24)
timer = pygame.time.Clock()

image_bg = pygame.image.load('image/background.png')
image_bg = pygame.transform.scale(image_bg, (WIDTH, HEIGHT))

def draw_button(rect, text, base_color, hover=False, glow=False):
    color = tuple(min(255, c + 40) for c in base_color) if hover else base_color
    pygame.draw.rect(screen, color, rect, border_radius=10)

    if glow and hover:
        glow_surface = pygame.Surface((rect.width+10, rect.height+10), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surface, (*color, 100), glow_surface.get_rect())
        screen.blit(glow_surface, (rect.x - 5, rect.y - 5))

    text_surf = font.render(text, True, (0, 0, 0))
    screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2,
                            rect.y + (rect.height - text_surf.get_height()) // 2))


def draw_hud(difficulty, steps, timer):
    hud_text = f"Difficulty: {difficulty} | Steps: {steps} | Time: {timer}s"
    text_surface = font.render(hud_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, HEIGHT - 30))



def show_menu():
    global selected_difficulty
    selected_difficulty = "easy"  # mặc định
    difficulty_open = False
    button_width, button_height = 300, 70
    play_btn = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 60, button_width, button_height)
    ai_btn = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 60, button_width, button_height)
    # Thêm 2 nút mới
    intro_btn = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 180, 300, 60)
    howto_btn = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 260, 300, 60)

    while True:
        screen.blit(image_bg, (0, 0))
        mx, my = pygame.mouse.get_pos()

        # Vẽ combo box độ khó
        diff_rect = pygame.Rect(WIDTH - 280, 30, 160, 40)
        pygame.draw.rect(screen, WHITE, diff_rect)
        pygame.draw.rect(screen, BLACK, diff_rect, 2)
        screen.blit(small_font.render(f"Level: {selected_difficulty.title()}", True, BLACK), (diff_rect.x + 10, diff_rect.y + 10))

        difficulty_options = ["Easy", "Medium", "Hard"]
        difficulty_option_rects = []

        if difficulty_open:
            for i, diff in enumerate(difficulty_options):
                rect = pygame.Rect(diff_rect.x, diff_rect.y + (i + 1) * diff_rect.height, diff_rect.width, diff_rect.height)
                pygame.draw.rect(screen, LIGHT_PURPLE, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
                screen.blit(small_font.render(diff, True, BLACK), (rect.x + 10, rect.y + 10))
                difficulty_option_rects.append((rect, diff.lower()))

        # Vẽ menu chơi với hiệu ứng hover
        draw_button(play_btn, "Player", (200, 255, 200), play_btn.collidepoint(mx, my))
        draw_button(ai_btn, "AI", (200, 200, 255), ai_btn.collidepoint(mx, my))
        draw_button(intro_btn, "Introduction", (255, 255, 180), intro_btn.collidepoint(mx, my))
        draw_button(howto_btn, "How to Play", (180, 255, 255), howto_btn.collidepoint(mx, my))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos() 

                if diff_rect.collidepoint(mx, my):
                    difficulty_open = not difficulty_open
                elif difficulty_open:
                    for rect, diff in difficulty_option_rects:
                        if rect.collidepoint(mx, my):
                            selected_difficulty = diff
                            difficulty_open = False

                elif play_btn.collidepoint(mx, my):
                    return "player"
                elif ai_btn.collidepoint(mx, my):
                    return "ai"
                elif intro_btn.collidepoint(mx, my):
                    show_popup("Introduction",
                               "This is a maze solving game.\nYou can play manually or use AI.\nYour goal is to reach the red square!")

                elif howto_btn.collidepoint(mx, my):
                    show_popup("How to Play", "Use arrow keys to move.\nAvoid bombs.\nReach the red goal to win.")

        pygame.display.update()
        timer.tick(60)
def show_popup(title, message):
    popup_width, popup_height = 600, 300
    popup_x = WIDTH // 2 - popup_width // 2
    popup_y = HEIGHT // 2 - popup_height // 2
    ok_btn = pygame.Rect(popup_x + popup_width//2 - 60, popup_y + 220, 120, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_btn.collidepoint(pygame.mouse.get_pos()):
                    return

        screen.blit(image_bg, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(screen, BLACK, (popup_x, popup_y, popup_width, popup_height), 2)

        title_surface = font.render(title, True, BLACK)
        screen.blit(title_surface, (popup_x + 20, popup_y + 20))

        # Vẽ từng dòng trong message
        lines = message.split("\n")
        for i, line in enumerate(lines):
            line_surface = small_font.render(line, True, BLACK)
            screen.blit(line_surface, (popup_x + 20, popup_y + 80 + i * 30))

        draw_button(ok_btn, "OK", (200, 255, 200), ok_btn.collidepoint(pygame.mouse.get_pos()))
        pygame.display.update()
        timer.tick(60)


def run_game(mode):
    pygame.mixer.music.stop()

    # Phát nhạc riêng cho từng chế độ
    if mode == "player":
        pygame.mixer.music.load("image/player_mode.mp3")
    elif mode == "ai":
        pygame.mixer.music.load("image/ai_mode.mp3")

    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    global selected_difficulty
    if selected_difficulty == "easy":
        maze = Maze(35, 25)
    elif selected_difficulty == "medium":
        maze = Maze(45, 35)
    else:
        maze = Maze(55, 45)

    player = Player(maze)
    solver = MazeSolver(maze)

    solution = []
    step_index = 0
    selected_algorithm = None
    auto_solve = (mode == "ai")
    won = False

    start_ticks = None
    end_ticks = None
    has_started = False
    ai_plan_time = None

    combo_rect = pygame.Rect(WIDTH - 230, 30, 200, 40)
    combo_open = False
    search_algorithms = ["BFS", "A*", "Q-learning", "Backtracking", "Simulated Annealing"]
    reload_btn = pygame.Rect(WIDTH - 190, 300, 180, 60)
    menu_btn = pygame.Rect(WIDTH - 190, 370, 180, 50)
    reload_btn2 = pygame.Rect(WIDTH - 190, 300, 180, 60)
    menu_btn2 = pygame.Rect(WIDTH - 190, 370, 180, 50)
    info_btn = pygame.Rect(WIDTH - 190, 440, 180, 50)  # Thêm nút Info
    info_open = False  # Biến kiểm tra trạng thái mở/đóng của info panel

    running = True
    submenu_open = False
    # Dictionary lưu thông tin của các thuật toán
    algorithm_info = {
        "BFS": {"time": 0, "steps": 0, "used": False},
        "A*": {"time": 0, "steps": 0, "used": False},
        "Q-learning": {"time": 0, "steps": 0, "used": False},
        "Backtracking": {"time": 0, "steps": 0, "used": False},
        "Simulated Annealing": {"time": 0, "steps": 0, "used": False}
    }
    while running:
        timer.tick(60)
        screen.blit(image_bg, (0, 0))
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if mode == "player" and not won:
                if event.type == pygame.KEYDOWN:
                    direction = None
                    if event.key == pygame.K_UP: direction = "UP"
                    elif event.key == pygame.K_DOWN: direction = "DOWN"
                    elif event.key == pygame.K_LEFT: direction = "LEFT"
                    elif event.key == pygame.K_RIGHT: direction = "RIGHT"

                    if direction:
                        player.move(direction)
                        if not has_started:
                            start_ticks = pygame.time.get_ticks()
                            has_started = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if reload_btn.collidepoint(mx, my):
                        if selected_difficulty == "easy":
                            new_maze = Maze(35, 25)
                        elif selected_difficulty == "medium":
                            new_maze = Maze(45, 35)
                        else:
                            new_maze = Maze(55, 45)

                        player = Player(new_maze)
                        solver.set_maze(new_maze)
                        maze = new_maze
                        solution.clear()
                        step_index = 0
                        selected_algorithm = None
                        start_ticks, end_ticks = None, None
                        has_started = False
                        won = False
                        ai_plan_time = None

                    elif menu_btn.collidepoint(mx, my):
                        submenu_open = not submenu_open

                    if submenu_open and 'submenu_rects' in locals():
                        for rect, text in submenu_rects:
                            if rect.collidepoint(mx, my):
                                if text == "Reset":
                                    player = Player(maze)
                                    solution.clear()
                                    step_index = 0
                                    selected_algorithm = None
                                    start_ticks, end_ticks = None, None
                                    has_started = False
                                    won = False
                                    ai_plan_time = None
                                    submenu_open = False

                                elif text == "Continue":
                                    submenu_open = False

                                elif text == "Hint":
                                    hint = solver.solve_bfs((player.x, player.y))
                                    if hint and len(hint) > 0:
                                        direction = hint[0]
                                        hint_bg = pygame.Rect(WIDTH - 200, HEIGHT - 60, 180, 40)
                                        pygame.draw.rect(screen, (255, 255, 255), hint_bg)
                                        pygame.draw.rect(screen, (0, 0, 0), hint_bg, 2)
                                        
                                        hint_text = small_font.render(f"Next: {direction}", True, (0, 128, 0))
                                        screen.blit(hint_text, (hint_bg.x + 10, hint_bg.y + 10))
                                        pygame.time.delay(500)
                                elif text == "Menu":
                                    return

                if (player.x, player.y) == (maze.end_x, maze.end_y):
                    won = True
                    if has_started and not end_ticks:
                        end_ticks = pygame.time.get_ticks()

            elif event.type == pygame.MOUSEBUTTONDOWN and auto_solve and not solution and not won:
                if reload_btn2.collidepoint(mx, my):
                    if selected_difficulty == "easy":
                        maze = Maze(35, 25)
                    elif selected_difficulty == "medium":
                        maze = Maze(45, 35)
                    else:
                        maze = Maze(55, 45)
                    player = Player(maze)
                    solver.set_maze(maze)
                    solution.clear()
                    step_index = 0
                    selected_algorithm = None
                    start_ticks, end_ticks = None, None
                    has_started = False
                    won = False
                    ai_plan_time = None
                    # Reset thông tin các thuật toán
                    for algo in algorithm_info:
                        algorithm_info[algo] = {"time": 0, "steps": 0, "used": False}
                elif menu_btn2.collidepoint(mx, my):
                    return
                elif info_btn.collidepoint(mx, my):
                    info_open = not info_open

                elif combo_rect.collidepoint(mx, my):
                    combo_open = not combo_open
                elif combo_open:
                    for i, name in enumerate(search_algorithms):
                        option_rect = pygame.Rect(combo_rect.x, combo_rect.y + (i + 1) * combo_rect.height, combo_rect.width, combo_rect.height)
                        if option_rect.collidepoint(mx, my):
                            selected_algorithm = name
                            start = time.perf_counter()
                            if name == "BFS":
                                solution = solver.solve_bfs((player.x, player.y))
                            elif name == "A*":
                                solution = solver.solve_a_star((player.x, player.y))
                            elif name == "Q-learning":
                                solution = solver.solve_q_learning((player.x, player.y))
                            elif name == "Backtracking":
                                solution = solver.solve_backtracking((player.x, player.y))
                            elif name == "Simulated Annealing":
                                solution = solver.solve_simulated_annealing((player.x, player.y))
                            ai_plan_time = round(time.perf_counter() - start, 4)
                            # Cập nhật thông tin thuật toán
                            algorithm_info[name]["time"] = ai_plan_time
                            algorithm_info[name]["steps"] = len(solution)
                            algorithm_info[name]["used"] = True
                            step_index = 0
                            combo_open = False
                            break

        if step_index < len(solution) and not won:
            player.move(solution[step_index])
            step_index += 1
            if not has_started:
                start_ticks = pygame.time.get_ticks()
                has_started = True
            pygame.time.delay(80)
            if (player.x, player.y) == (maze.end_x, maze.end_y):
                won = True
                if has_started and not end_ticks:
                    end_ticks = pygame.time.get_ticks()

        maze.draw_maze(screen)
        player.draw()

        if mode == "player" and not won:
            draw_button(reload_btn, "Change Maze", (200, 255, 200))
            draw_button(menu_btn, "Menu", (255, 200, 200))

        if mode == "ai" and not won:
            draw_button(reload_btn2, "Change Maze", (200, 255, 200))
            draw_button(menu_btn2, "Menu", (255, 200, 200))
            draw_button(info_btn, "Info", (200, 200, 255))  # Vẽ nút Info

            # Vẽ combobox chọn thuật toán
            pygame.draw.rect(screen, (255, 255, 255), combo_rect)
            pygame.draw.rect(screen, (0, 0, 0), combo_rect, 2)
            algorithm_text = selected_algorithm if selected_algorithm else "Select Algorithm"
            text_surface = small_font.render(algorithm_text, True, (0, 0, 0))
            screen.blit(text_surface, (combo_rect.x + 10, combo_rect.y + 10))

            # Vẽ các tùy chọn thuật toán khi combobox mở
            if combo_open:
                for i, name in enumerate(search_algorithms):
                    option_rect = pygame.Rect(combo_rect.x, combo_rect.y + (i + 1) * combo_rect.height, 
                                           combo_rect.width, combo_rect.height)
                    pygame.draw.rect(screen, (255, 255, 255), option_rect)
                    pygame.draw.rect(screen, (0, 0, 0), option_rect, 1)
                    text_surface = small_font.render(name, True, (0, 0, 0))
                    screen.blit(text_surface, (option_rect.x + 10, option_rect.y + 10))

            # Vẽ panel thông tin khi info_open = True
            if info_open:
                info_panel = pygame.Rect(WIDTH - 400, 100, 380, 700)
                pygame.draw.rect(screen, (255, 255, 255), info_panel)
                pygame.draw.rect(screen, (0, 0, 0), info_panel, 2)
                
                # Tiêu đề
                title = small_font.render("Algorithm Information", True, (0, 0, 0))
                screen.blit(title, (info_panel.x + 10, info_panel.y + 10))
                
                # Vẽ thông tin từng thuật toán
                y_offset = 50
                for algo in search_algorithms:
                    info = algorithm_info[algo]
                    if info["used"]:
                        algo_text = small_font.render(f"{algo}:", True, (0, 0, 0))
                        time_text = small_font.render(f"Time: {info['time']:.4f}s", True, (0, 0, 0))
                        steps_text = small_font.render(f"Steps: {info['steps']}", True, (0, 0, 0))
                        
                        screen.blit(algo_text, (info_panel.x + 20, info_panel.y + y_offset))
                        screen.blit(time_text, (info_panel.x + 40, info_panel.y + y_offset + 25))
                        screen.blit(steps_text, (info_panel.x + 40, info_panel.y + y_offset + 50))
                        y_offset += 90
                    else:
                        algo_text = small_font.render(f"{algo}: Not used yet", True, (128, 128, 128))
                        screen.blit(algo_text, (info_panel.x + 20, info_panel.y + y_offset))
                        y_offset += 40

        if ai_plan_time is not None:
            ai_time_text = small_font.render(f"AI Plan Time: {ai_plan_time:.4f}s", True, BLACK)
            screen.blit(ai_time_text, (WIDTH - 200, 100))

        if has_started and start_ticks:
            if won and end_ticks:
                seconds = (end_ticks - start_ticks) // 1000
            else:
                seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            time_text = small_font.render(f"Time: {seconds}s", True, BLACK)
            screen.blit(time_text, (WIDTH - 170, 70))

        if submenu_open:
            submenu_rects = []
            submenu_texts = ["Reset", "Continue", "Hint", "Menu"]

            for i, text in enumerate(submenu_texts):
                rect = pygame.Rect(menu_btn.x, menu_btn.y + (i + 1) * 50, 180, 40)
                submenu_rects.append((rect, text))
                draw_button(rect, text, (255, 255, 255), rect.collidepoint(mx, my))

        if won:
            box_width, box_height = 280, 200
            box_x = WIDTH - box_width - 10
            box_y = HEIGHT // 2 - box_height // 2
            pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, BLACK, (box_x, box_y, box_width, box_height), 2)

            congrats_text = small_font.render("Congratulations,", True, (0, 128, 0))
            reward_text = small_font.render("you have found a scholarship", True, (0, 128, 0))
            screen.blit(congrats_text, (box_x + 20, box_y + 30))
            screen.blit(reward_text, (box_x + 20, box_y + 50))

            next_btn = pygame.Rect(box_x + 20, box_y + 90, 240, 40)
            back_btn = pygame.Rect(box_x + 20, box_y + 140, 240, 40)
            draw_button(next_btn, "Play Again", (200, 255, 200), next_btn.collidepoint(mx, my))
            draw_button(back_btn, "Return to Menu", (255, 200, 200), back_btn.collidepoint(mx, my))

            # Xử lý sự kiện click cho các nút
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if next_btn.collidepoint(mx, my):
                        # Reset game state
                        player = Player(maze)  # Tạo người chơi mới với mê cung hiện tại
                        solution.clear()
                        step_index = 0
                        selected_algorithm = None
                        start_ticks, end_ticks = None, None
                        has_started = False
                        won = False
                        ai_plan_time = None
                    elif back_btn.collidepoint(mx, my):
                        return  # Return to menu

        pygame.display.update()

while True:
    mode = show_menu()
    run_game(mode)