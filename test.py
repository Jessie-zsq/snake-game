import os
os.environ["SDL_IME_SHOW_UI"] = "0"

import pygame
import random
import sys

pygame.init()
pygame.key.stop_text_input()

# 常量
CELL_SIZE = 20
GRID_W = 30
GRID_H = 20
WIDTH = CELL_SIZE * GRID_W
HEIGHT = CELL_SIZE * GRID_H

# 速度档位
SPEEDS = {"slow": ("Slow", 6), "medium": ("Medium", 10), "fast": ("Fast", 16)}

# 颜色
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (220, 50, 50)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
YELLOW = (255, 220, 0)

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.body = [(GRID_W // 2, GRID_H // 2)]
        self.direction = RIGHT

    @property
    def head(self):
        return self.body[0]

    def move(self, grow=False):
        x = self.head[0] + self.direction[0]
        y = self.head[1] + self.direction[1]
        self.body.insert(0, (x, y))
        if not grow:
            self.body.pop()

    def collides_with_self(self):
        return self.head in self.body[1:]

    def collides_with_wall(self):
        x, y = self.head
        return x < 0 or x >= GRID_W or y < 0 or y >= GRID_H

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn([])

    def spawn(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
            if pos not in snake_body:
                self.position = pos
                break

    def draw(self, surface):
        x, y = self.position
        center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(surface, RED, center, CELL_SIZE // 2 - 1)


def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))


def show_game_over(screen, score):
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 18)
    texts = [
        (font, "GAME OVER", WHITE, (0, -40)),
        (small_font, f"Score: {score}", WHITE, (0, 10)),
        (small_font, "Press R to return to menu or Q to quit", WHITE, (0, 50)),
    ]
    for f, text, color, offset in texts:
        surf = f.render(text, True, color)
        rect = surf.get_rect(center=(WIDTH // 2 + offset[0], HEIGHT // 2 + offset[1]))
        screen.blit(surf, rect)


def show_start_screen(screen):
    """速度选择界面，返回选中的 fps 和速度名称。"""
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 18)
    tiny_font = pygame.font.Font(None, 14)
    speed_keys = list(SPEEDS.keys())
    selected = 1  # 默认选中速

    # "START" 按钮
    btn_w, btn_h = 180, 44
    btn_x = WIDTH // 2 - btn_w // 2
    btn_y = HEIGHT // 2 + 110
    btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

    while True:
        mx, my = pygame.mouse.get_pos()
        mouse_on_btn = btn_rect.collidepoint(mx, my)

        screen.fill(BLACK)

        title = font.render("SNAKE", True, GREEN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))

        # 速度选择
        prompt = small_font.render("Select speed:", True, WHITE)
        screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))

        for i, key in enumerate(speed_keys):
            label, _ = SPEEDS[key]
            text = f"[{'*' if i == selected else ' '}] {label}"
            color = YELLOW if i == selected else WHITE
            surf = small_font.render(text, True, color)
            screen.blit(surf, surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 28)))

        # START 按钮
        btn_color = YELLOW if mouse_on_btn else GRAY
        pygame.draw.rect(screen, btn_color, btn_rect, border_radius=6)
        pygame.draw.rect(screen, WHITE, btn_rect, 2, border_radius=6)
        btn_text = font.render("START", True, BLACK)
        screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

        hint = tiny_font.render("Click START or press ENTER / SPACE to begin   Q: quit", True, GRAY)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 20)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.TEXTEDITING:
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(speed_keys)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(speed_keys)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    key = speed_keys[selected]
                    return SPEEDS[key][0], SPEEDS[key][1]
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_rect.collidepoint(event.pos):
                    key = speed_keys[selected]
                    return SPEEDS[key][0], SPEEDS[key][1]


def run_game(screen, clock, speed_name, fps):
    snake = Snake()
    food = Food()
    food.spawn(snake.body)
    score = 0
    game_over = False
    last_direction = snake.direction

    while True:
        direction_changed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not direction_changed:
                if game_over:
                    if event.key in (pygame.K_r, pygame.K_q):
                        return
                else:
                    if event.key == pygame.K_UP and last_direction != DOWN:
                        snake.direction = UP
                        direction_changed = True
                    elif event.key == pygame.K_DOWN and last_direction != UP:
                        snake.direction = DOWN
                        direction_changed = True
                    elif event.key == pygame.K_LEFT and last_direction != RIGHT:
                        snake.direction = LEFT
                        direction_changed = True
                    elif event.key == pygame.K_RIGHT and last_direction != LEFT:
                        snake.direction = RIGHT
                        direction_changed = True

        if not game_over:
            next_head = (snake.head[0] + snake.direction[0],
                         snake.head[1] + snake.direction[1])
            growing = next_head == food.position
            snake.move(grow=growing)
            last_direction = snake.direction

            if growing:
                food.spawn(snake.body)
                score += 1

            if snake.collides_with_wall() or snake.collides_with_self():
                game_over = True

        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)

        # 分数和速度显示
        font = pygame.font.Font(None, 16)
        score_text = font.render(f"Score: {score}", True, WHITE)
        speed_text = font.render(f"Speed: {speed_name}", True, YELLOW)
        screen.blit(score_text, (10, 10))
        screen.blit(speed_text, (WIDTH - 130, 10))

        if game_over:
            show_game_over(screen, score)

        pygame.display.flip()
        clock.tick(fps)


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    while True:
        speed_name, fps = show_start_screen(screen)
        run_game(screen, clock, speed_name, fps)


if __name__ == "__main__":
    main()
