# agentes_conocimientos

Miniproyecto de Agentes basados en conocimientos

Este proyecto resuelve el puzzle 8 utilizando dos tipos de agentes, uno no informado (BFS) y otro informado (A* con heurística de Manhattan). Permite comparar el desempeño de ambos agentes sobre el mismo estado inicial, que puede ser generado aleatoriamente o ingresado manualmente por el usuario.

# Características

- Resolución automática del puzzle 8 usando BFS y A*.
- Interfaz gráfica con Pygame para visualizar el proceso de resolución.
- Selección del estado inicial: aleatorio o manual (por consola o tablero interactivo).
- Comparación visual y estadística entre ambos agentes.
- Validación de estados resolubles según la meta personalizada.

# Estructura del proyecto

- `Agente.py`: Lógica de los agentes, heurísticas y visualización de la resolución.
- `menu.py`: Menú principal, selección de estado inicial y ejecución de agentes.
- `estado_inicial.json`: Archivo temporal para compartir el estado inicial entre agentes.
- Otros archivos: recursos, módulos auxiliares, etc.

# Requisitos

- Python 3.10 o superior
- pygame
- tkinter (incluido en la mayoría de instalaciones de Python)

Instala pygame con:
```
pip install pygame
```

# Uso

1. Ejecuta `menu.py` para abrir el menú principal.
2. Selecciona el tipo de agente o la comparación.
3. Elige el estado inicial (manual o aleatorio).
4. Observa la resolución y compara estadísticas.

# Créditos

Desarrollado como miniproyecto para la materia de Inteligencia Artificial.

---
