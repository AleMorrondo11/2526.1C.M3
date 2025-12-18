"""Módulo de lógica del juego de memoria.

Contiene las funciones principales para crear y gestionar el estado del juego,
incluyendo la creación del tablero, revelación de cartas y verificación de parejas.
"""
from __future__ import annotations

import random
from typing import Dict, List, Tuple

# Estados de las cartas (estos nombres NO se pueden cambiar)
STATE_HIDDEN = "hidden"
STATE_VISIBLE = "visible"
STATE_FOUND = "found"

Carta = Dict[str, str]
Tablero = List[List[Carta]]
Posicion = Tuple[int, int]
EstadoJuego = Dict[str, object]


def build_symbol_pool(filas: int, columnas: int) -> List[str]:
    """
    El juego de memoria requiere que cada carta tenga una pareja idéntica.
    
    Esta función existe para garantizar que siempre haya exactamente dos
    cartas con el mismo símbolo, asegurando que el juego sea resoluble.
    La mezcla aleatoria aporta rejugabilidad, haciendo cada partida única.
    
    Args:
        filas: Número de filas del tablero.
        columnas: Número de columnas del tablero.
    
    Returns:
        Lista de símbolos mezclados, donde cada símbolo aparece exactamente
        dos veces para formar parejas.
    """
    total_casillas = filas * columnas
    total_parejas = total_casillas // 2

    simbolos_base = []
    for i in range(total_parejas):
        simbolos_base.append(str(i))

    simbolos = []
    for simbolo in simbolos_base:
        simbolos.append(simbolo)
        simbolos.append(simbolo)

    random.shuffle(simbolos)
    return simbolos


def create_game(filas: int, columnas: int) -> EstadoJuego:
    """
    Centraliza la inicialización del juego para evitar estados inconsistentes.
    
    Tener un único punto de entrada garantiza que todas las partidas comiencen
    con un estado válido y coherente. Esto evita errores como tableros sin
    parejas completas o contadores desincronizados, facilitando el testing
    y mantenimiento del código.
    
    Args:
        filas: Número de filas del tablero.
        columnas: Número de columnas del tablero.
    
    Returns:
        Diccionario con el estado del juego que contiene:
        - board: Tablero de cartas (matriz 2D).
        - pending: Lista de posiciones de cartas pendientes de resolver.
        - moves: Contador de movimientos realizados.
        - matches: Contador de parejas encontradas.
        - total_pairs: Número total de parejas a encontrar.
        - rows: Número de filas del tablero.
        - cols: Número de columnas del tablero.
    """
    simbolos = build_symbol_pool(filas, columnas)

    tablero: Tablero = []
    indice = 0

    for _fila in range(filas):
        fila_cartas: List[Carta] = []
        for _columna in range(columnas):
            carta = {
                "symbol": simbolos[indice],   # ESTA CLAVE NO SE CAMBIA
                "state": STATE_HIDDEN
            }
            fila_cartas.append(carta)
            indice += 1
        tablero.append(fila_cartas)

    juego: EstadoJuego = {
        "board": tablero,        # ESTA CLAVE NO SE CAMBIA
        "pending": [],            # posiciones pendientes
        "moves": 0,
        "matches": 0,
        "total_pairs": (filas * columnas) // 2,
        "rows": filas,  
        "cols": columnas
    }

    return juego


def reveal_card(juego: EstadoJuego, fila: int, columna: int) -> bool:
    """
    Encapsula las reglas de negocio para voltear una carta.
    
    El juego de memoria tiene restricciones específicas: solo se pueden
    voltear dos cartas por turno y no se pueden seleccionar cartas ya
    descubiertas. Esta función protege la integridad del juego validando
    estas reglas antes de permitir cualquier acción.
    
    Args:
        juego: Diccionario con el estado actual del juego.
        fila: Número de fila de la carta a revelar.
        columna: Número de columna de la carta a revelar.
    
    Returns:
        True si la carta fue revelada exitosamente, False en caso contrario.
        Retorna False si:
        - Las coordenadas están fuera del tablero.
        - Ya hay 2 cartas pendientes.
        - La carta ya está visible o encontrada.
    """
    filas = juego.get("rows", 0)
    columnas = juego.get("cols", 0)

    # Coordenadas fuera del tablero
    if fila < 0 or fila >= filas or columna < 0 or columna >= columnas:
        return False

    pendientes: List[Posicion] = juego.get("pending", [])
    if len(pendientes) >= 2:
        return False

    tablero: Tablero = juego.get("board", [])
    carta = tablero[fila][columna]

    # No se puede revelar una carta ya visible o encontrada
    if carta["state"] != STATE_HIDDEN:
        return False

    carta["state"] = STATE_VISIBLE
    pendientes.append((fila, columna))
    return True


def resolve_pending(juego: EstadoJuego) -> Tuple[bool, bool]:
    """
    Implementa la mecánica central del juego: comparar dos cartas.
    
    La esencia del juego de memoria es recordar ubicaciones y encontrar
    parejas. Esta función determina si el jugador acertó, actualizando
    el estado del juego de forma atómica para mantener la consistencia
    entre el tablero, los contadores y las cartas pendientes.
    
    Args:
        juego: Diccionario con el estado actual del juego.
    
    Returns:
        Tupla de dos booleanos (resuelto, pareja_encontrada):
        - resuelto: True si había exactamente 2 cartas pendientes, False si no.
        - pareja_encontrada: True si las cartas formaban pareja, False si no.
    """
    pendientes: List[Posicion] = juego.get("pending", [])

    if len(pendientes) != 2:
        return False, False

    tablero: Tablero = juego.get("board", [])
    (f1, c1), (f2, c2) = pendientes

    carta1 = tablero[f1][c1]
    carta2 = tablero[f2][c2]

    pareja_encontrada = False

    if carta1["symbol"] == carta2["symbol"]:
        carta1["state"] = STATE_FOUND
        carta2["state"] = STATE_FOUND
        juego["matches"] = int(juego.get("matches", 0)) + 1
        pareja_encontrada = True
    else:
        carta1["state"] = STATE_HIDDEN
        carta2["state"] = STATE_HIDDEN

    juego["moves"] = int(juego.get("moves", 0)) + 1
    pendientes.clear()

    return True, pareja_encontrada


def has_won(juego: EstadoJuego) -> bool:
    """
    Permite saber cuándo terminar la partida y mostrar la victoria.
    
    El juego necesita un criterio claro de finalización para poder
    felicitar al jugador, registrar estadísticas o iniciar una nueva
    partida. Centralizar esta lógica evita duplicar la condición de
    victoria en múltiples lugares del código.
    
    Args:
        juego: Diccionario con el estado actual del juego.
    
    Returns:
        True si el número de parejas encontradas es igual al total de parejas,
        False en caso contrario.
    """
    return juego.get("matches", 0) == juego.get("total_pairs", 0)
