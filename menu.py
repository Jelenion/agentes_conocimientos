# ---------- Librerías ----------
import pygame
import subprocess
import sys
import os
import threading
import json
import random

# ---------- Inicialización de Pygame y configuración de la ventana ----------
pygame.init()

# Dimensiones de la ventana del menú
width, height = 500, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu - Puzzle 8")

# ---------- Definición de colores ----------
background_color = (240, 240, 240)   # Color de fondo
button_color = (180, 180, 180)       # Color de los botones
border_color = (100, 100, 100)       # Color del borde de los botones
text_color = (0, 0, 0)               # Color del texto
apple_green = (140, 220, 100)        # Color decorativo (verde manzana)

# ---------- Fuente para los textos ----------
font = pygame.font.SysFont(None, 24)

# ---------- Definición de los botones ----------
bfs_button_rect = pygame.Rect((width // 2 - 150, height // 2 - 90, 300, 50))
a_star_button_rect = pygame.Rect((width // 2 - 150, height // 2 - 20, 300, 50))
both_button_rect = pygame.Rect((width // 2 - 150, height // 2 + 50, 300, 50))

# ---------- Dibuja un botón con el texto especificado en la pantalla ---------- 
def draw_button(rect, text):
    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

# ---------- Genera un estado aleatorio resoluble para el puzzle 8 ---------- 
def generar_estado_resoluble():
    nums = list(range(9))
    while True:
        random.shuffle(nums)
        state = [nums[i:i + 3] for i in range(0, 9, 3)]
        if is_solvable(state):
            return state

# ---------- Guarda el estado inicial en un archivo JSON para ser usado por ambos agentes ----------
def guardar_estado_inicial(estado):
    with open("estado_inicial.json", "w") as f:
        json.dump(estado, f)

# ---------- Carga el estado inicial desde un archivo JSON ----------
def cargar_estado_inicial():
    try:
        with open("estado_inicial.json", "r") as f:
            estado = json.load(f)
            return estado
    except Exception:
        return None

# ---------- Ejecuta el archivo Agente.py con el agente especificado.
#    Si usar_archivo es True, se pasa el argumento --archivo para que ambos agentes usen el mismo estado inicial ----------
def ejecutar_agente(nombre, usar_archivo=False):
    cmd = [sys.executable, "Agente.py", nombre]
    if usar_archivo:
        cmd.append("--archivo")
    subprocess.run(cmd)

# ---------- Función para seleccionar el estado inicial del juego ----------
def seleccionar_estado():
    import tkinter as tk
    from tkinter import simpledialog, messagebox

    root = tk.Tk()
    root.withdraw()

    opcion = messagebox.askquestion("Seleccionar estado", "¿Quieres ingresar manualmente la matriz inicial?\n(Si eliges 'No', será aleatoria)")

    if opcion == 'yes':
        while True:
            entrada = simpledialog.askstring("Matriz inicial", "Introduce 9 números (0-8) separados por espacios:")
            if entrada is None:
                return None
            try:
                nums = list(map(int, entrada.strip().split()))
                if sorted(nums) != list(range(9)):
                    raise ValueError
                state = [nums[i:i + 3] for i in range(0, 9, 3)]
                if not is_solvable(state):
                    messagebox.showerror("No resoluble", "¡La matriz ingresada NO tiene solución!")
                    continue
                return state
            except Exception:
                messagebox.showerror("Error", "Entrada inválida. Debes ingresar los números del 0 al 8 sin repetir.")
    else:
        return None

# ---------- Función para ingresar la matriz manualmente usando Pygame ----------
def ingresar_matriz_pygame():
    matriz = [[None for _ in range(3)] for _ in range(3)]
    tile_size = 80
    offset_x = (width - tile_size * 3) // 2
    offset_y = (height - tile_size * 3) // 2
    font_big = pygame.font.SysFont(None, 48)
    selected = [0, 0]
    ingresados = set()
    running = True

    while running:
        screen.fill((240, 240, 240))
        # Dibuja el tablero
        for i in range(3):
            for j in range(3):
                rect = pygame.Rect(offset_x + j * tile_size, offset_y + i * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, (255, 255, 255), rect)
                pygame.draw.rect(screen, (100, 100, 100), rect, 2)
                if matriz[i][j] is not None:
                    num_text = font_big.render(str(matriz[i][j]), True, (0, 0, 0))
                    text_rect = num_text.get_rect(center=rect.center)
                    screen.blit(num_text, text_rect)
        # Dibuja el selector
        sel_rect = pygame.Rect(offset_x + selected[1] * tile_size, offset_y + selected[0] * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, (140, 220, 100), sel_rect, 4)

        # Mensaje de instrucciones
        msg = "Haz clic o usa flechas. Escribe 0-8. Enter para aceptar."
        msg_text = font.render(msg, True, (0, 0, 0))
        screen.blit(msg_text, (offset_x, offset_y + tile_size * 3 + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Validar matriz completa y sin repetidos
                    flat = [n for row in matriz for n in row]
                    if None in flat:
                        continue
                    if sorted(flat) != list(range(9)):
                        continue
                    return matriz
                elif event.key in [pygame.K_UP, pygame.K_w]:
                    selected[0] = (selected[0] - 1) % 3
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    selected[0] = (selected[0] + 1) % 3
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    selected[1] = (selected[1] - 1) % 3
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    selected[1] = (selected[1] + 1) % 3
                elif pygame.K_0 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    # Solo permite 0-8 y sin repetir
                    flat = [n for row in matriz for n in row if n is not None]
                    if num in flat:
                        continue
                    if num > 8:
                        continue
                    matriz[selected[0]][selected[1]] = num
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i in range(3):
                    for j in range(3):
                        rect = pygame.Rect(offset_x + j * tile_size, offset_y + i * tile_size, tile_size, tile_size)
                        if rect.collidepoint(mx, my):
                            selected = [i, j]
    return None

# Estado meta del puzzle 8 (debe ser igual al de Agente.py)
goal_state = [[1, 2, 3],
              [8, 0, 4],
              [7, 6, 5]]

def is_solvable(state):
    """
    Verifica si un estado del puzzle 8 es resoluble para la meta personalizada.
    """
    # Encuentra la posición objetivo de cada número
    goal_positions = {}
    for i in range(3):
        for j in range(3):
            goal_positions[goal_state[i][j]] = (i, j)
    # Aplana el estado y la meta
    flat = [num for row in state for num in row]
    flat_goal = [num for row in goal_state for num in row]
    # Calcula las inversiones respecto a la meta personalizada
    inversions = 0
    for i in range(9):
        for j in range(i + 1, 9):
            if flat[i] != 0 and flat[j] != 0:
                # Compara la posición en la meta
                pos_i = flat_goal.index(flat[i])
                pos_j = flat_goal.index(flat[j])
                if pos_i > pos_j:
                    inversions += 1
    return inversions % 2 == 0

# ---------- Función principal del menú. Dibuja la interfaz y gestiona los eventos de los botones ----------
def main():
    running = True
    while running:
        screen.fill(background_color)

        # Dibuja un marco decorativo verde manzana alrededor del menú
        pygame.draw.rect(screen, apple_green, (20, 20, width - 40, height - 40), 8, border_radius=20)

        # Dibuja los botones del menú
        draw_button(bfs_button_rect, "Jugar con agente no informado (BFS)")
        draw_button(a_star_button_rect, "Jugar con agente informado (A*)")
        draw_button(both_button_rect, "Comparar ambos agentes lado a lado")

        pygame.display.flip()

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Ejecuta el agente BFS
                if bfs_button_rect.collidepoint(event.pos):
                    estado = seleccionar_estado()
                    if estado is None:
                        estado = generar_estado_resoluble()
                    guardar_estado_inicial(estado)
                    ejecutar_agente("bfs", True)
                # Ejecuta el agente A*
                elif a_star_button_rect.collidepoint(event.pos):
                    estado = seleccionar_estado()
                    if estado is None:
                        estado = generar_estado_resoluble()
                    guardar_estado_inicial(estado)
                    ejecutar_agente("a*", True)
                # Ejecuta ambos agentes en paralelo con el mismo estado inicial
                elif both_button_rect.collidepoint(event.pos):
                    estado = seleccionar_estado()
                    if estado is None:
                        estado = generar_estado_resoluble()
                    guardar_estado_inicial(estado)
                    threading.Thread(target=ejecutar_agente, args=("bfs", True)).start()
                    threading.Thread(target=ejecutar_agente, args=("a*", True)).start()

    pygame.quit()

if __name__ == "__main__":
    main()
