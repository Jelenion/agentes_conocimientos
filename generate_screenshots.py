import pygame
import os
import sys

# Asegurar que se puedan importar los módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Agente import bfs, a_star, goal_state, draw_board, draw_buttons, draw_info, draw_stats
import menu

# Inicializar Pygame y fuentes
pygame.init()
pygame.font.init()

# Colores del menú
background_color = (240, 240, 240)
button_color = (180, 180, 180)
border_color = (100, 100, 100)
text_color = (0, 0, 0)
apple_green = (140, 220, 100)

font_menu = pygame.font.SysFont(None, 24)
font_agent = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 60)

# Un estado inicial simple que se resuelve en pocos pasos:
# 0 está en (1,0). Movimientos: 8 abajo -> 1 izquierda -> 2 arriba.
start_state = [
    [8, 1, 3],
    [0, 2, 4],
    [7, 6, 5]
]

# Directorio de salida para las capturas
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
os.makedirs(output_dir, exist_ok=True)

def capture_menu():
    print("Generando captura de pantalla del Menú Principal...")
    width, height = 500, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Menu - Puzzle 8")
    
    screen.fill(background_color)
    # Dibujar marco decorativo
    pygame.draw.rect(screen, apple_green, (20, 20, width - 40, height - 40), 8, border_radius=20)
    
    # Dibujar botones
    bfs_btn = pygame.Rect((width // 2 - 150, height // 2 - 90, 300, 50))
    astar_btn = pygame.Rect((width // 2 - 150, height // 2 - 20, 300, 50))
    both_btn = pygame.Rect((width // 2 - 150, height // 2 + 50, 300, 50))
    
    # Función de dibujado de botones adaptada para recibir la pantalla y fuente
    def draw_btn_local(rect, text):
        pygame.draw.rect(screen, button_color, rect, border_radius=10)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)
        label = font_menu.render(text, True, text_color)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)
        
    draw_btn_local(bfs_btn, "Jugar con agente no informado (BFS)")
    draw_btn_local(astar_btn, "Jugar con agente informado (A*)")
    draw_btn_local(both_btn, "Comparar ambos agentes lado a lado")
    
    pygame.display.flip()
    pygame.image.save(screen, os.path.join(output_dir, "menu_principal.png"))
    print("Menú Principal guardado.")

def capture_manual_input():
    print("Generando captura de pantalla de Ingreso Manual...")
    width, height = 500, 400
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Menu - Puzzle 8")
    
    screen.fill(background_color)
    # Dibujar marco decorativo
    pygame.draw.rect(screen, apple_green, (20, 20, width - 40, height - 40), 8, border_radius=20)
    
    # Mockear un tablero de entrada parcial
    matriz = [
        [1, 2, 3],
        [8, None, None],
        [None, None, None]
    ]
    tile_size = 80
    offset_x = (width - tile_size * 3) // 2
    offset_y = (height - tile_size * 3) // 2
    font_big = pygame.font.SysFont(None, 48)
    selected = [1, 1] # Selección en el centro
    
    for i in range(3):
        for j in range(3):
            rect = pygame.Rect(offset_x + j * tile_size, offset_y + i * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, (255, 255, 255), rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            if matriz[i][j] is not None:
                num_text = font_big.render(str(matriz[i][j]), True, (0, 0, 0))
                text_rect = num_text.get_rect(center=rect.center)
                screen.blit(num_text, text_rect)
                
    # Dibujar el selector verde
    sel_rect = pygame.Rect(offset_x + selected[1] * tile_size, offset_y + selected[0] * tile_size, tile_size, tile_size)
    pygame.draw.rect(screen, apple_green, sel_rect, 4)
    
    msg = "Haz clic o usa flechas. Escribe 0-8. Enter para aceptar."
    msg_text = font_menu.render(msg, True, (0, 0, 0))
    screen.blit(msg_text, (offset_x - 30, offset_y + tile_size * 3 + 10))
    
    pygame.display.flip()
    pygame.image.save(screen, os.path.join(output_dir, "ingreso_manual.png"))
    print("Ingreso Manual guardado.")

def capture_bfs_solving():
    print("Generando captura de pantalla de BFS Resolviendo...")
    solution, nodos, tiempo = bfs(start_state)
    
    tile_size = 100
    offset_y = 80
    screen_width = tile_size * 3 + 100
    screen_height = tile_size * 3 + offset_y + 160
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Puzzle 8 - Agente BFS")
    
    screen.fill((240, 240, 240))
    
    # Dibujar el primer paso intermedio (index = 1)
    draw_board(screen, solution[1], big_font, tile_size, offset_y)
    draw_buttons(screen, font_agent)
    
    # Simular información en progreso
    draw_info(screen, font_agent, 1.0, 1, screen_width, screen_height)
    
    pygame.display.flip()
    pygame.image.save(screen, os.path.join(output_dir, "resolucion_bfs.png"))
    print("BFS Resolviendo guardado.")

def capture_bfs_result():
    print("Generando captura de pantalla de Resultado BFS...")
    solution, nodos, tiempo = bfs(start_state)
    
    tile_size = 100
    offset_y = 80
    screen_width = tile_size * 3 + 100
    screen_height = tile_size * 3 + offset_y + 160
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Puzzle 8 - Agente BFS")
    
    screen.fill((240, 240, 240))
    
    # Dibujar estado final (completado)
    draw_board(screen, solution[-1], big_font, tile_size, offset_y)
    draw_buttons(screen, font_agent)
    
    # Dibujar información final
    draw_info(screen, font_agent, tiempo, len(solution) - 1, screen_width, screen_height)
    draw_stats(screen, font_agent, nodos, tiempo, screen_height)
    
    pygame.display.flip()
    pygame.image.save(screen, os.path.join(output_dir, "resultado_bfs.png"))
    print("Resultado BFS guardado.")

def capture_astar_result():
    print("Generando captura de pantalla de Resultado A*...")
    solution, nodos, tiempo = a_star(start_state)
    
    tile_size = 100
    offset_y = 80
    screen_width = tile_size * 3 + 100
    screen_height = tile_size * 3 + offset_y + 160
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Puzzle 8 - Agente A*")
    
    screen.fill((240, 240, 240))
    
    # Dibujar estado final (completado)
    draw_board(screen, solution[-1], big_font, tile_size, offset_y)
    draw_buttons(screen, font_agent)
    
    # Dibujar información final
    draw_info(screen, font_agent, tiempo, len(solution) - 1, screen_width, screen_height)
    draw_stats(screen, font_agent, nodos, tiempo, screen_height)
    
    pygame.display.flip()
    pygame.image.save(screen, os.path.join(output_dir, "resultado_astar.png"))
    print("Resultado A* guardado.")

if __name__ == "__main__":
    try:
        capture_menu()
        capture_manual_input()
        capture_bfs_solving()
        capture_bfs_result()
        capture_astar_result()
        print("\nTodas las capturas de pantalla se generaron correctamente en la carpeta 'screenshots'.")
    except Exception as e:
        print(f"Error al generar capturas: {e}")
    finally:
        pygame.quit()
