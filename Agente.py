import pygame
import time
import random
from collections import deque
import heapq
import sys
import json
import threading
import subprocess

# ---------- Lógica del Puzzle ----------
# Estado meta del puzzle 8
goal_state = [[1, 2, 3],
              [8, 0, 4],
              [7, 6, 5]]

# Movimientos posibles: arriba, abajo, izquierda, derecha
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Convierte una matriz (lista de listas) en una tupla de tuplas. Útil para usar como clave en sets o diccionarios.
def to_tuple(matrix):
    return tuple(tuple(row) for row in matrix)

# Busca la posición (i, j) del cero (espacio vacío) en el estado del puzzle
def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Genera todos los estados vecinos posibles moviendo el cero en las 4 direcciones
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

# ---------- Agente No Informado: BFS ----------
# Algoritmo de búsqueda en anchura (BFS) para resolver el puzzle 8
# Retorna la solución (lista de estados), nodos expandidos y tiempo de ejecución
def bfs(start_state):
    visited = set()
    queue = deque([(start_state, [])])
    visited.add(to_tuple(start_state))
    nodos_expandidos = 0
    start = time.time()
    while queue:
        current, path = queue.popleft()
        nodos_expandidos += 1
        if current == goal_state:
            end = time.time()
            return path + [current], nodos_expandidos, end - start
        for neighbor in get_neighbors(current):
            neighbor_tuple = to_tuple(neighbor)
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)
                queue.append((neighbor, path + [current]))
    end = time.time()
    return None, nodos_expandidos, end - start

# ---------- Agente Informado: A* ----------
# Calcula la suma de las distancias de Manhattan de cada ficha a su posición objetivo
# Heurística para el algoritmo A*
def manhattan_distance(state):
    # Crea un diccionario con la posición objetivo de cada valor
    goal_positions = {}
    for i in range(3):
        for j in range(3):
            goal_positions[goal_state[i][j]] = (i, j)
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_i, goal_j = goal_positions[value]
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

# Algoritmo A* para resolver el puzzle 8 usando la heurística de Manhattan
# Retorna la solución (lista de estados), nodos expandidos y tiempo de ejecución
def a_star(start_state):
    visited = {}
    heap = []
    start_tuple = to_tuple(start_state)
    h = manhattan_distance(start_state)
    heapq.heappush(heap, (h, 0, start_state, []))
    visited[start_tuple] = 0
    nodos_expandidos = 0
    start = time.time()
    while heap:
        f, g, current, path = heapq.heappop(heap)
        nodos_expandidos += 1
        current_tuple = to_tuple(current)
        if current == goal_state:
            end = time.time()
            return path + [current], nodos_expandidos, end - start
        for neighbor in get_neighbors(current):
            neighbor_tuple = to_tuple(neighbor)
            new_g = g + 1
            if neighbor_tuple not in visited or new_g < visited[neighbor_tuple]:
                visited[neighbor_tuple] = new_g
                h = manhattan_distance(neighbor)
                heapq.heappush(heap, (new_g + h, new_g, neighbor, path + [current]))
    end = time.time()
    return None, nodos_expandidos, end - start

# Verifica si un estado del puzzle es resoluble contando las inversiones
def is_solvable(state):
    """
    Verifica si un estado del puzzle 8 es resoluble.
    Retorna True si es resoluble, False si no lo es.
    Lanza ValueError si la matriz no es válida.
    """
    # Validación básica de la matriz
    flat_list = [num for row in state for num in row]
    if sorted(flat_list) != list(range(9)):
        raise ValueError("La matriz debe contener todos los números del 0 al 8 sin repetir.")

    # Calcula las inversiones (sin contar el 0)
    flat_list_no_zero = [num for num in flat_list if num != 0]
    inversions = 0
    for i in range(len(flat_list_no_zero)):
        for j in range(i + 1, len(flat_list_no_zero)):
            if flat_list_no_zero[i] > flat_list_no_zero[j]:
                inversions += 1
    return inversions % 2 == 0

# mostrar estado sin resolucion
def mostrar_estado_no_resoluble(state):
    import pygame
    pygame.init()
    tile_size = 100
    offset_y = 60
    screen_width = tile_size * 3 + 60
    screen_height = tile_size * 3 + offset_y + 60
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("¡Estado sin solución!")
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)
    running = True
    while running:
        screen.fill((250, 220, 220))
        # Dibuja la matriz
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                rect = pygame.Rect(j * tile_size + 30, i * tile_size + offset_y, tile_size, tile_size)
                pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=10)
                pygame.draw.rect(screen, (200, 100, 100), rect, 2, border_radius=10)
                if value != 0:
                    text = font.render(str(value), True, (180, 0, 0))
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
        # Mensaje
        msg = small_font.render("¡Este estado NO tiene solución!", True, (180, 0, 0))
        screen.blit(msg, (30, 20))
        msg2 = small_font.render("Cierra esta ventana para continuar...", True, (80, 0, 0))
        screen.blit(msg2, (30, screen_height - 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

# Genera un estado aleatorio resoluble para el puzzle 8
def generar_estado_resoluble():
    nums = list(range(9))
    while True:
        random.shuffle(nums)
        state = [nums[i:i + 3] for i in range(0, 9, 3)]
        if is_solvable(state):
            return state
        else:
            mostrar_estado_no_resoluble(state)

# ---------- Visualización Pygame ----------
# Dibuja el tablero del puzzle 8 en la pantalla usando Pygame
def draw_board(screen, state, font, tile_size, offset_y):
    apple_green = (140, 220, 100)
    border_rect = pygame.Rect(45, offset_y - 5, tile_size * 3 + 10, tile_size * 3 + 10)
    pygame.draw.rect(screen, apple_green, border_rect, border_radius=15)
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            rect = pygame.Rect(j * tile_size + 50, i * tile_size + offset_y, tile_size, tile_size)
            pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=12)
            pygame.draw.rect(screen, (200, 200, 200), rect, 2, border_radius=12)
            if value != 0:
                color = (200, 0, 0) if value % 2 == 0 else (0, 150, 0)
                text = font.render(str(value), True, color)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

# Dibuja un botón con texto en la pantalla
def draw_button(screen, rect, text, font):
    pygame.draw.rect(screen, (180, 180, 180), rect, border_radius=8)
    pygame.draw.rect(screen, (100, 100, 100), rect, 2, border_radius=8)
    label = font.render(text, True, (0, 0, 0))
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

# Dibuja los botones de Pausar, Reanudar y Reiniciar
# Retorna los rectángulos de los botones para detección de clics
def draw_buttons(screen, font):
    pause_btn = pygame.Rect(10, 20, 110, 40)
    resume_btn = pygame.Rect(150, 20, 110, 40)
    reset_btn = pygame.Rect(280, 20, 110, 40)
    draw_button(screen, pause_btn, "Pausar", font)
    draw_button(screen, resume_btn, "Reanudar", font)
    draw_button(screen, reset_btn, "Reiniciar", font)
    return pause_btn, resume_btn, reset_btn

# Dibuja la información de tiempo transcurrido y movimientos realizados
def draw_info(screen, font, tiempo, movimientos, width, height):
    tiempo_text = font.render(f"Tiempo: {int(tiempo)}s", True, (0, 0, 0))
    movs_text = font.render(f"Movimientos: {movimientos}", True, (0, 0, 0))
    screen.blit(tiempo_text, (width - 180, height - 40))
    screen.blit(movs_text, (width - 350, height - 40))

# Dibuja las estadísticas del agente: nodos expandidos y tiempo de ejecución
def draw_stats(screen, font, nodos_expandidos, tiempo, height):
    stats_text = [
        f"Nodos expandidos: {nodos_expandidos}",
        f"Tiempo de ejecución: {tiempo:.4f} s"
    ]
    for idx, txt in enumerate(stats_text):
        text = font.render(txt, True, (0, 0, 0))
        screen.blit(text, (50, height - 110 + idx * 25))

# Guarda el estado inicial en un archivo JSON
def guardar_estado_inicial(estado):
    with open("estado_inicial.json", "w") as f:
        json.dump(estado, f)

def cargar_estado_inicial():
    with open("estado_inicial.json", "r") as f:
        return json.load(f)

def ejecutar_agente(nombre, usar_archivo=False):
    cmd = [sys.executable, "Agente.py", nombre]
    if usar_archivo:
        cmd.append("--archivo")
    subprocess.Popen(cmd)

# ---------- Ejecución del juego ----------
# Lógica principal de la interfaz interactiva del juego
# Permite pausar, reanudar y reiniciar la partida, y muestra estadísticas al finalizar
def ejecutar_interactivo(algoritmo='bfs', start_state=None):
    pygame.init()
    tile_size = 100
    offset_y = 80
    screen_width = tile_size * 3 + 100
    # Aumenta el alto para dejar espacio a las estadísticas
    screen_height = tile_size * 3 + offset_y + 160  # antes era +60
    screen = pygame.display.set_mode((screen_width, screen_height))
    titulo = "Puzzle 8 - Agente BFS"
    if(algoritmo!='bfs'):
        titulo = "Puzzle 8 - Agente A*"
    pygame.display.set_caption(titulo)
    font = pygame.font.SysFont(None, 28)
    big_font = pygame.font.SysFont(None, 60)

    running = True
    paused = False
    step_index = 0
    if algoritmo == 'bfs':
        solution, nodos_expandidos, tiempo_ejecucion = bfs(start_state)
    else:
        solution, nodos_expandidos, tiempo_ejecucion = a_star(start_state)
    # --- FIN VERIFICACIÓN ---

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

        # Ahora las estadísticas se dibujan más abajo
        if completado:
            draw_stats(screen, font, nodos_expandidos, tiempo_ejecucion, screen_height)

        # Avanza los pasos de la solución automáticamente
        if not paused and not completado and step_index < len(solution) - 1:
            if current_time - start_time - pause_time > step_index * 0.5:
                step_index += 1
                movimientos += 1
                if step_index == len(solution) - 1:
                    tiempo_finalizado = current_time - start_time - pause_time
                    completado = True

        pygame.display.flip()

        # Manejo de eventos de la ventana y botones
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
                    if algoritmo == 'bfs':
                        solution, nodos_expandidos, tiempo_ejecucion = bfs(start_state)
                    else:
                        solution, nodos_expandidos, tiempo_ejecucion = a_star(start_state)
                    step_index = 0
                    start_time = time.time()
                    pause_time = 0
                    pause_start = None
                    movimientos = 0
                    paused = False
                    completado = False
                    tiempo_finalizado = None

    pygame.quit()

# ---------- Punto de entrada ----------
if __name__ == '__main__':
    algoritmo = 'bfs'
    usar_archivo = False
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'a*':
            algoritmo = 'a*'
        if len(sys.argv) > 2 and sys.argv[2] == '--archivo':
            usar_archivo = True

    if usar_archivo:
        start_state = cargar_estado_inicial()
    else:
        start_state = generar_estado_resoluble()
    ejecutar_interactivo(algoritmo, start_state)
