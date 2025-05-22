# Librerias importadas
import pygame
import time
import random
from collections import deque

# ---------- Lógica del Puzzle ----------
goal_state = [[1, 2, 3],
              [4, 0, 5],
              [6, 7, 8]]
# Movimientos disponibles en X - Y
# Arriba (-1, 0)
# Abajo (1, 0)
# Izquierda (0, -1)
# Derecha (0, 1)
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Convertir matriz a tupla
def to_tuple(matrix):
    return tuple(tuple(row) for row in matrix)

# Buscar valor 0
def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Mostrar posibles movimientos de 0
def get_neighbors(state):
    x, y = find_zero(state)
    neighbors = []
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

# Encontrar solucion deseada
def bfs(start_state):
    visited = set() # guarda tuplas vistas
    queue = deque([(start_state, [])]) # cola que estado actual y como llegar al objetivo
    while queue:
        current, path = queue.popleft()
        if current == goal_state:
            return path + [current]
        visited.add(to_tuple(current))
        for neighbor in get_neighbors(current):
            if to_tuple(neighbor) not in visited:
                queue.append((neighbor, path + [current]))
    return None

def is_solvable(state):
    flat_list = [num for row in state for num in row if num != 0]
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    return inversions % 2 == 0

def generar_estado_resoluble():
    nums = list(range(9))
    while True:
        random.shuffle(nums)
        state = [nums[i:i + 3] for i in range(0, 9, 3)]
        if is_solvable(state):
            return state

# ---------- Visualización Pygame ----------
def draw_board(screen, state, font, tile_size, offset_y):
    apple_green = (140, 220, 100)
    border_rect = pygame.Rect(45, offset_y - 5, tile_size * 3 + 10, tile_size * 3 + 10)
    pygame.draw.rect(screen, apple_green, border_rect, border_radius=15)

    for i in range(3):
        for j in range(3):
            value = state[i][j]
            rect = pygame.Rect(j * tile_size + 50, i * tile_size + offset_y, tile_size, tile_size)
            pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=12)  # fondo blanco
            pygame.draw.rect(screen, (200, 200, 200), rect, 2, border_radius=12)  # borde gris claro
            if value != 0:
                color = (200, 0, 0) if value % 2 == 0 else (0, 150, 0)  # rojo para pares, verde para impares
                text = font.render(str(value), True, color)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def draw_button(screen, rect, text, font):
    pygame.draw.rect(screen, (180, 180, 180), rect, border_radius=8)
    pygame.draw.rect(screen, (100, 100, 100), rect, 2, border_radius=8)
    label = font.render(text, True, (0, 0, 0))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def draw_buttons(screen, font):
    pause_btn = pygame.Rect(10, 20, 110, 40)
    resume_btn = pygame.Rect(150, 20, 110, 40)
    reset_btn = pygame.Rect(280, 20, 110, 40)

    draw_button(screen, pause_btn, "Pausar", font)
    draw_button(screen, resume_btn, "Reanudar", font)
    draw_button(screen, reset_btn, "Reiniciar", font)

    return pause_btn, resume_btn, reset_btn

def draw_info(screen, font, tiempo, movimientos, width, height):
    tiempo_text = font.render(f"Tiempo: {int(tiempo)}s", True, (0, 0, 0))
    movs_text = font.render(f"Movimientos: {movimientos}", True, (0, 0, 0))
    screen.blit(tiempo_text, (width - 180, height - 40))
    screen.blit(movs_text, (width - 350, height - 40))

# ---------- Lógica principal ----------
def ejecutar_interactivo():
    pygame.init()
    tile_size = 100
    offset_y = 80
    screen_width = tile_size * 3 + 100
    screen_height = tile_size * 3 + offset_y + 60
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Puzzle 8 - Interactivo")
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 60)

    running = True
    paused = False
    step_index = 0
    start_state = generar_estado_resoluble()
    solution = bfs(start_state)
    start_time = time.time()
    pause_time = 0
    pause_start = None
    movimientos = 0
    completado = False
    tiempo_finalizado = None

    while running:
        current_time = time.time()
        screen.fill((240, 240, 240))

        draw_board(screen, solution[step_index], big_font, tile_size, offset_y)
        pause_btn, resume_btn, reset_btn = draw_buttons(screen, font)

        if completado and tiempo_finalizado is not None:
            tiempo_mostrar = tiempo_finalizado
        elif paused and pause_start:
            tiempo_mostrar = pause_start - start_time - pause_time
        else:
            tiempo_mostrar = current_time - start_time - pause_time

        draw_info(screen, font, tiempo_mostrar, movimientos, screen_width, screen_height)

        if not paused and not completado and step_index < len(solution) - 1:
            if current_time - start_time - pause_time > step_index * 0.5:
                step_index += 1
                movimientos += 1
                if step_index == len(solution) - 1:
                    tiempo_finalizado = current_time - start_time - pause_time
                    completado = True
                    

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_btn.collidepoint(event.pos) and not paused and not completado:
                    paused = True
                    pause_start = time.time()

                elif resume_btn.collidepoint(event.pos) and paused and not completado:
                    paused = False
                    pause_time += time.time() - pause_start
                    pause_start = None

                elif reset_btn.collidepoint(event.pos):
                    start_state = generar_estado_resoluble()
                    solution = bfs(start_state)
                    step_index = 0
                    start_time = time.time()
                    pause_time = 0
                    pause_start = None
                    movimientos = 0
                    paused = False
                    completado = False
                    tiempo_finalizado = None

    pygame.quit()

# ---------- Ejecutar ----------
ejecutar_interactivo()
