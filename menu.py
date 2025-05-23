import pygame
import subprocess
import sys
import os
import threading
import json
import random

# Inicializar Pygame
pygame.init()

# Configurar pantalla
width, height = 500, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Menu - Puzzle 8")

# Colores
background_color = (240, 240, 240)
button_color = (180, 180, 180)
border_color = (100, 100, 100)
text_color = (0, 0, 0)
apple_green = (140, 220, 100)

# Fuentes
font = pygame.font.SysFont(None, 24)

# Botones
bfs_button_rect = pygame.Rect((width // 2 - 150, height // 2 - 90, 300, 50))
a_star_button_rect = pygame.Rect((width // 2 - 150, height // 2 - 20, 300, 50))
both_button_rect = pygame.Rect((width // 2 - 150, height // 2 + 50, 300, 50))

def draw_button(rect, text):
    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def generar_estado_resoluble():
    def is_solvable(state):
        flat_list = [num for row in state for num in row if num != 0]
        inversions = 0
        for i in range(len(flat_list)):
            for j in range(i + 1, len(flat_list)):
                if flat_list[i] > flat_list[j]:
                    inversions += 1
        return inversions % 2 == 0

    nums = list(range(9))
    while True:
        random.shuffle(nums)
        state = [nums[i:i + 3] for i in range(0, 9, 3)]
        if is_solvable(state):
            return state

def guardar_estado_inicial(estado):
    with open("estado_inicial.json", "w") as f:
        json.dump(estado, f)

def ejecutar_agente(nombre, usar_archivo=False):
    cmd = [sys.executable, "Agente.py", nombre]
    if usar_archivo:
        cmd.append("--archivo")
    subprocess.run(cmd)

def main():
    running = True
    while running:
        screen.fill(background_color)

        # Dibujar marco decorativo verde manzana
        pygame.draw.rect(screen, apple_green, (20, 20, width - 40, height - 40), 8, border_radius=20)

        draw_button(bfs_button_rect, "Jugar con agente no informado (BFS)")
        draw_button(a_star_button_rect, "Jugar con agente informado (A*)")
        draw_button(both_button_rect, "Comparar ambos agentes lado a lado")

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bfs_button_rect.collidepoint(event.pos):
                    ejecutar_agente("bfs")
                elif a_star_button_rect.collidepoint(event.pos):
                    ejecutar_agente("a*")
                elif both_button_rect.collidepoint(event.pos):
                    estado = generar_estado_resoluble()
                    guardar_estado_inicial(estado)
                    threading.Thread(target=ejecutar_agente, args=("bfs", True)).start()
                    threading.Thread(target=ejecutar_agente, args=("a*", True)).start()

    pygame.quit()

if __name__ == "__main__":
    main()
