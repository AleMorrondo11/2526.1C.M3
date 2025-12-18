# Memory M3 - Juego de Memoria

Un juego interactivo de memoria clásico desarrollado en Python con interfaz gráfica usando Pygame. El objetivo es encontrar todas las parejas de cartas ocultas en el menor número de movimientos posible.

---

## Descripción General

**Memory M3** es una implementación del clásico juego de memoria donde:
- Las cartas se encuentran inicialmente ocultas en un tablero
- Haces clic en dos cartas para revelarlas
- Si las cartas coinciden (parejas), permanecen visibles y se marcan como encontradas
- Si no coinciden, se vuelven a ocultar y debes intentar recordar dónde estaban
- El juego termina cuando encuentras todas las parejas

---

## Requisitos

- **Python 3.10+**
- **Pygame** (para la interfaz gráfica)

---

## Cómo Ejecutar el Juego

### Opción 1: Ejecución por defecto (4x4)
```bash
python game.py
```

### Opción 2: Personalizar dimensiones del tablero
```bash
# Tablero de 6x6 (36 casillas = 18 parejas)
python game.py --rows 6 --cols 6

# Tablero de 3x4 (12 casillas = 6 parejas)
python game.py --rows 3 --cols 4

# Tablero de 8x8 (64 casillas = 32 parejas)
python game.py --rows 8 --cols 8
```

### Argumentos disponibles
- `--rows`: Número de filas del tablero (por defecto: 4)
- `--cols`: Número de columnas del tablero (por defecto: 4)

---

## Cómo Jugar

1. **Inicia el juego** ejecutando el comando anterior
2. **Haz clic en las cartas** para revelarlas
3. **Encuentra las parejas** haciendo clic en dos cartas que coincidan
4. **Memoriza la posición** de las cartas para obtener mejor puntuación
5. **Gana el juego** cuando encuentres todas las parejas
6. **Presiona ESC** para salir del juego en cualquier momento

### Información en pantalla
- **Movimientos**: Número total de clics realizados
- **Parejas encontradas**: Contador de parejas coincidentes
- **Estados de las cartas**:
  - **Oculta** (gris oscuro)
  - **Visible** (azul claro) - se muestra brevemente
  - **Encontrada** (verde)

---


## 🔧 Descripción de los Módulos

### `game.py`
- **Punto de entrada** del programa
- Parsea argumentos de línea de comandos (`--rows`, `--cols`)
- Inicializa la interfaz gráfica
- Lanza el bucle principal del juego

**Funciones principales:**
- `parse_args()`: Procesa los argumentos de la línea de comandos
- `main()`: Inicializa y ejecuta el juego

### `logic.py`
Contiene toda la lógica del juego:

- **`build_symbol_pool(filas, columnas)`**: Genera una lista de símbolos donde cada uno aparece exactamente dos veces para formar parejas. Retorna la lista mezclada aleatoriamente.

- **`create_game(filas, columnas)`**: Inicializa el estado del juego con un tablero válido. Retorna un diccionario con todo lo necesario para gestionar la partida.

- **`reveal_card(juego, posicion)`**: Revela una carta en la posición indicada. Valida las coordenadas y gestiona el estado pendiente.

- **`resolve_pending(juego)`**: Verifica si las cartas pendientes forman una pareja. Si coinciden, las marca como encontradas; si no, las oculta nuevamente.

- **`has_won(juego)`**: Comprueba si se ha ganado el juego (todas las parejas encontradas).

**Estados de las cartas:**
- `STATE_HIDDEN`: Carta oculta (no visible)
- `STATE_VISIBLE`: Carta visible (mostrada temporalmente)
- `STATE_FOUND`: Carta encontrada (pareja completa)

### `memory_engine.py`
Motor gráfico que **NO se modifica**:
- Renderiza el tablero usando Pygame
- Maneja eventos del ratón y teclado
- Delega toda la lógica al módulo `logic`
- Muestra animaciones y estados visuales
- Implementa la clase `MemoryUI` que controla la interfaz

---

## Estados del Juego

El estado del juego se mantiene en un diccionario con:
```python
{
    "board": [lista 2D de cartas],      # Tablero de cartas
    "pending": [lista de posiciones],   # Cartas en espera de validación
    "moves": int,                       # Contador de movimientos
    "matches": int,                     # Parejas encontradas
    "total_pairs": int,                 # Total de parejas a encontrar
    "rows": int,                        # Número de filas
    "cols": int                         # Número de columnas
}
```

### Estructura de una Carta
```python
{
    "symbol": str,      # Símbolo de la carta (ej: "0", "1", "2", etc.)
    "state": str        # Estado: STATE_HIDDEN, STATE_VISIBLE o STATE_FOUND
}
```

---

## 🎨 Paleta de Colores

| Elemento | Color RGB | Uso |
|----------|-----------|-----|
| Fondo | (12, 17, 29) | Fondo del tablero |
| Grilla | (18, 98, 151) | Líneas divisorias |
| Carta Oculta | (55, 71, 79) | Cartas no reveladas |
| Carta Visible | (197, 202, 233) | Cartas reveladas |
| Carta Encontrada | (67, 160, 71) | Parejas completadas |
| Texto | (235, 239, 243) | Información en pantalla |

---

## ⌨️ Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| **ESC** | Salir del juego |
| **Click izquierdo** | Seleccionar carta |

---


## Cómo Funciona la Mecánica del Juego

### Flujo de Juego

1. **Inicialización**:
   - Se genera un pool de símbolos con pares
   - Se crea el tablero y se distribuyen los símbolos
   - Todas las cartas comienzan ocultas

2. **Turno del Jugador**:
   - El jugador hace clic en una carta → se revela
   - El jugador hace clic en otra carta → se revela
   - Se valida si forman pareja

3. **Resolución**:
   - **Pareja correcta**: Las cartas se marcan como encontradas (permanecen visibles)
   - **Pareja incorrecta**: Las cartas se ocultan nuevamente
   - Se incrementa el contador de movimientos

4. **Final del Juego**:
   - Se verifica si todas las parejas han sido encontradas
   - Se muestra el número de movimientos realizados

---

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'pygame'"
**Solución**: Instala pygame
```bash
pip install pygame
```

### Error: "El tablero debe tener un número par de casillas"
**Solución**: Asegúrate de que filas × columnas sea un número par
```bash
# Incorrecto (3x3 = 9, impar)
python game.py --rows 3 --cols 3

# Correcto (3x4 = 12, par)
python game.py --rows 3 --cols 4
```

## Información de Desarrollo

### Requisitos previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Ambiente de desarrollo recomendado
```bash
# Instalar dependencias
pip install pygame
```

## Soporte

Si encuentras problemas:
1. Verifica que Python 3.10+ esté correctamente instalado
2. Instala las dependencias: `pip install pygame`
3. Asegúrate de ejecutar el comando desde la carpeta correcta
4. Revisa que el número total de casillas sea par (filas × columnas)
5. Comprueba que no hay procesos pesados consumiendo recursos

