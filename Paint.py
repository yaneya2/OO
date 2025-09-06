import pygame
import sys

from My_cells import Cells

# Инициализация pygame
pygame.init()

# Параметры сетки
GRID_SIZE = 20
CELL_SIZE = 40
LINE_WIDTH = 1
TOTAL_SIZE = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * LINE_WIDTH

# Создание окна
screen = pygame.display.set_mode((TOTAL_SIZE, TOTAL_SIZE + 50))  # +50 для панели кнопок
pygame.display.set_caption("Сетка 20x20 с рисованием линий")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BACKGROUND = (240, 240, 240)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER = (180, 180, 180)
BACKGROUND_BUTTON = (220, 220, 220)

#режимы рисования
DRAWING_MODE = {"cell" : "Клетки", "line" : "Линии", "brush" : "Заливка"}

# Состояние программы
filled_cells = Cells()
drawing_mode = "cell"  # "cell" или "line"
start_point = None
current_color = RED
previous_color = None

# Кнопки
buttons = {
    "cell": pygame.Rect(10, TOTAL_SIZE + 10, 120, 30),
    "line": pygame.Rect(140, TOTAL_SIZE + 10, 120, 30),
    "clear": pygame.Rect(270, TOTAL_SIZE + 10, 120, 30),
    "brush": pygame.Rect(400, TOTAL_SIZE + 10, 120, 30),
    "color_red": pygame.Rect(530, TOTAL_SIZE + 10, 30, 30),
    "color_green": pygame.Rect(570, TOTAL_SIZE + 10, 30, 30),
    "color_blue": pygame.Rect(610, TOTAL_SIZE + 10, 30, 30),
}


def fill_cell(row, col, color=None):
    """
    Закрашивает указанную клетку
    """
    if color is None:
        color = current_color
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        filled_cells.set_color(row, col, color)
        return True
    return False

def brush(row, col, prev_color, color):
    """заливка"""

    if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
        return
    if filled_cells.get_color(row, col) != prev_color:
        return
    fill_cell(row, col, color)
    brush(row + 1, col, prev_color, color)
    brush(row - 1, col, prev_color, color)
    brush(row, col  + 1, prev_color ,color)
    brush(row, col  - 1, prev_color ,color)

def draw_line(x0, y0, x1, y1, color=None):
    """
    Рисует линию используя алгоритм Брезенхема
    """
    if color is None:
        color = current_color
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    if dx == 0:
        for i in range(min(y0, y1), max(y0, y1) + 1):
            fill_cell(i, x0, color)
        return

    if dy == 0:
        for i in range(min(x0, x1), max(x0, x1) + 1):
            fill_cell(y0, i, color)
        return

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy

    while x0 != x1 and y0 != y1:
        fill_cell(y0, x0, color)

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x0 += sx

        if e2 < dx:
            err += dx
            y0 += sy
    fill_cell(y0, x0, color)

def draw_grid():
    """Рисует сетку и закрашенные сетки"""
    # Заливка фона
    screen.fill(BACKGROUND)

    # Рисование белых ячеек
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = LINE_WIDTH + col * (CELL_SIZE + LINE_WIDTH)
            y = LINE_WIDTH + row * (CELL_SIZE + LINE_WIDTH)
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))

    for row in range(20):
        for col in range(20):
            if filled_cells.get_color(row , col) != WHITE:
                x = LINE_WIDTH + col * (CELL_SIZE + LINE_WIDTH)
                y = LINE_WIDTH + row * (CELL_SIZE + LINE_WIDTH)
                pygame.draw.rect(screen, filled_cells.get_color(row, col), (x, y, CELL_SIZE, CELL_SIZE))

    # Рисование линий сетки
    for i in range(GRID_SIZE + 1):
        # Вертикальные линии
        x = i * (CELL_SIZE + LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (x, 0), (x, TOTAL_SIZE), LINE_WIDTH)

        # Горизонтальные линии
        y = i * (CELL_SIZE + LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, y), (TOTAL_SIZE, y), LINE_WIDTH)


def get_cell_from_mouse_pos(mouse_x, mouse_y):
    """
    Определяет клетку по координатам мыши
    """
    if mouse_x < LINE_WIDTH or mouse_y < LINE_WIDTH or mouse_y >= TOTAL_SIZE:
        return None

    col = (mouse_x - LINE_WIDTH) // (CELL_SIZE + LINE_WIDTH)
    row = (mouse_y - LINE_WIDTH) // (CELL_SIZE + LINE_WIDTH)

    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        return (row, col)
    return None


def clear_all_cells():
    """Очищает все закрашенные клетки"""
    filled_cells.clear()
    global start_point
    start_point = None


def draw_buttons():
    """Рисует кнопки интерфейса"""
    # Фон панели
    pygame.draw.rect(screen, BACKGROUND_BUTTON, (0, TOTAL_SIZE, TOTAL_SIZE, 50))

    # Кнопка рисования клеток
    color = BUTTON_HOVER if drawing_mode == "cell" else BUTTON_COLOR
    pygame.draw.rect(screen, color, buttons["cell"])
    font = pygame.font.Font(None, 20)
    text = font.render("Клетки", True, BLACK)
    screen.blit(text, (buttons["cell"].x + 10, buttons["cell"].y + 8))

    # Кнопка рисования линий
    color = BUTTON_HOVER if drawing_mode == "line" else BUTTON_COLOR
    pygame.draw.rect(screen, color, buttons["line"])
    text = font.render("Линии", True, BLACK)
    screen.blit(text, (buttons["line"].x + 10, buttons["line"].y + 8))

    # Кнопка очистки
    pygame.draw.rect(screen, BUTTON_COLOR, buttons["clear"])
    text = font.render("Очистить", True, BLACK)
    screen.blit(text, (buttons["clear"].x + 10, buttons["clear"].y + 8))

    #кнопка заливки
    color = BUTTON_HOVER if drawing_mode == "brush" else BUTTON_COLOR
    pygame.draw.rect(screen, color, buttons["brush"])
    text = font.render("Заливка", True, BLACK)
    screen.blit(text, (buttons["brush"].x + 10, buttons["brush"].y + 8))


    # Кнопки выбора цвета
    pygame.draw.rect(screen, RED, buttons["color_red"])
    pygame.draw.rect(screen, GREEN, buttons["color_green"])
    pygame.draw.rect(screen, BLUE, buttons["color_blue"])

    # Текущий режим

    mode_text = font.render(f"Режим: {DRAWING_MODE[drawing_mode]}", True, BLACK)
    screen.blit(mode_text, (650, TOTAL_SIZE + 15))


def check_button_click(pos):
    """Проверяет клик по кнопкам"""
    global drawing_mode, current_color, start_point

    if buttons["cell"].collidepoint(pos):
        drawing_mode = "cell"
        start_point = None
    elif buttons["line"].collidepoint(pos):
        drawing_mode = "line"
        start_point = None
    elif buttons["clear"].collidepoint(pos):
        clear_all_cells()
    elif buttons["brush"].collidepoint(pos):
        drawing_mode = "brush"
        start_point = None
    elif buttons["color_red"].collidepoint(pos):
        previous_color = current_color
        current_color = RED
    elif buttons["color_green"].collidepoint(pos):
        previous_color = current_color
        current_color = GREEN
    elif buttons["color_blue"].collidepoint(pos):
        previous_color = current_color
        current_color = BLUE


# Основной цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                # Проверяем клик по кнопкам
                if event.pos[1] > TOTAL_SIZE:
                    check_button_click(event.pos)
                else:
                    cell = get_cell_from_mouse_pos(*event.pos)
                    if cell:
                        row, col = cell
                        if drawing_mode == "cell":
                            fill_cell(row, col)
                        elif drawing_mode == "line":
                            if start_point is None:
                                start_point = (col, row)  # (x, y)
                                #fill_cell(row, col, YELLOW)  # Помечаем начальную точку
                            else:
                                # Рисуем линию от start_point до текущей точки
                                x0, y0 = start_point
                                x1, y1 = col, row
                                draw_line(x0, y0, x1, y1)
                                start_point = None
                        elif drawing_mode == "brush":
                            prev_color = filled_cells.get_color(row, col)
                            brush(row, col, prev_color, current_color)




            elif event.button == 3:  # Правая кнопка мыши - сброс линии
                if drawing_mode == "line":
                    start_point = None

    # Отрисовка
    draw_grid()
    draw_buttons()

    # Отображение информации
    font = pygame.font.Font(None, 20)
    if drawing_mode == "line" and start_point:
        info_text = font.render("Выберите конечную точку для линии", True, BLACK)
        screen.blit(info_text, (10, TOTAL_SIZE - 30))

    # Отображение координат мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_y < TOTAL_SIZE:
        cell_info = get_cell_from_mouse_pos(mouse_x, mouse_y)
        if cell_info:
            row, col = cell_info
            coord_text = font.render(f"Клетка: [{row}, {col}]", True, BLACK)
            screen.blit(coord_text, (10, TOTAL_SIZE - 50))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

# Завершение работы
pygame.quit()
sys.exit()