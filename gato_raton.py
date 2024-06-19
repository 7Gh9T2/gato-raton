
import pygame
import sys
import random

# Inicializamos pygame
pygame.init()

# Configuración del tablero y jugadores
TAMANO_TABLERO = 5
ANCHO_CELDA = 100
ALTURA_CELDA = 100
ANCHO_VENTANA = TAMANO_TABLERO * ANCHO_CELDA
ALTURA_VENTANA = TAMANO_TABLERO * ALTURA_CELDA
COLOR_FONDO = (255, 255, 255)
COLOR_LINEA = (0, 0, 0)
COLOR_GATO = (255, 0, 0)
COLOR_RATON = (0, 0, 255)
COLOR_MADRIGUERA = (0, 255, 0)  # Color de la madriguera

# Cargar las imágenes del gato, el ratón y la madriguera.Para la madriguera utilizamos pygame Surface para generar el color verde
#directamente con el codigo sin necesidad de un archivo externo  
gato_imagen = pygame.image.load("static/gato.png")
raton_imagen = pygame.image.load("static/raton.png")
madriguera_imagen = pygame.Surface((ANCHO_CELDA, ALTURA_CELDA))
madriguera_imagen.fill(COLOR_MADRIGUERA)

# Redimensionar las imágenes para que encajen en el tamaño de la celda
gato_imagen = pygame.transform.scale(gato_imagen, (ANCHO_CELDA, ALTURA_CELDA))
raton_imagen = pygame.transform.scale(raton_imagen, (ANCHO_CELDA, ALTURA_CELDA))

# Inicializar la pantalla
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTURA_VENTANA)) #definimos como se va ver la pantalla
pygame.display.set_caption('Gato y Ratón con Madriguera')# proporcionamos un titulo para identificar la ventana

MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

#verificar si una posición está dentro de los límites de un tablero de tamaño dado, 

def movimiento_valido(pos):
    return 0 <= pos[0] < TAMANO_TABLERO and 0 <= pos[1] < TAMANO_TABLERO 

# calcula la distancia entre dos posiciones en el tablero.

def distancia(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

#evalúamos el estado actual del tablero y asigna una puntuación en función de las posiciones del gato, el ratón y la madriguera

def evaluacion_tablero(gato_pos, raton_pos, madriguera_pos):
    if gato_pos == raton_pos:
        return 1000  # Gato ha atrapado al ratón
    if raton_pos == madriguera_pos:
        return -1000  # El ratón ha llegado a la madriguera
    return -distancia(gato_pos, raton_pos)  # El gato quiere minimizar la distancia al ratón

def minimax(gato_pos, raton_pos, madriguera_pos, profundidad, es_maximizar):
    if profundidad == 0 or gato_pos == raton_pos or raton_pos == madriguera_pos:
        return evaluacion_tablero(gato_pos, raton_pos, madriguera_pos)

    if es_maximizar:  # Maximizar: Gato
        max_eval = float('-inf')#Empieza con el peor número posible
        for mov in MOVIMIENTOS:
            nueva_pos = (gato_pos[0] + mov[0], gato_pos[1] + mov[1])
            if movimiento_valido(nueva_pos) and nueva_pos != madriguera_pos:
                eval = minimax(nueva_pos, raton_pos, madriguera_pos, profundidad - 1, False)
                max_eval = max(max_eval, eval)#Actualiza max_eval si encuentra un número más grande
        return max_eval#Devuelve el mejor número encontrado
    
    else:  # Minimizar: Ratón
        min_eval = float('inf')#Empieza con el mejor número posible
        for mov in MOVIMIENTOS:
            nueva_pos = (raton_pos[0] + mov[0], raton_pos[1] + mov[1])
            if movimiento_valido(nueva_pos) and nueva_pos != madriguera_pos and nueva_pos != gato_pos:
                eval = minimax(gato_pos, nueva_pos, madriguera_pos, profundidad - 1, True)
                min_eval = min(min_eval, eval)
        return min_eval#Devuelve el peor número encontrado

def mejor_movimiento_gato(gato_pos, raton_pos, madriguera_pos, profundidad):
    mejor_valor = float('-inf')
    mejor_mov = gato_pos
    for mov in MOVIMIENTOS:
        nueva_pos = (gato_pos[0] + mov[0], gato_pos[1] + mov[1])
        if movimiento_valido(nueva_pos) and nueva_pos != madriguera_pos:
            valor = minimax(nueva_pos, raton_pos, madriguera_pos, profundidad - 1, False)
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_mov = nueva_pos
    return mejor_mov

def mejor_movimiento_raton(gato_pos, raton_pos, madriguera_pos):
    posibles_movimientos = []
    if raton_pos[0] < madriguera_pos[0]:
        posibles_movimientos.append((1, 0))
    elif raton_pos[0] > madriguera_pos[0]:
        posibles_movimientos.append((-1, 0))
    if raton_pos[1] < madriguera_pos[1]:
        posibles_movimientos.append((0, 1))
    elif raton_pos[1] > madriguera_pos[1]:
        posibles_movimientos.append((0, -1))

    for mov in posibles_movimientos:
        nueva_pos = (raton_pos[0] + mov[0], raton_pos[1] + mov[1])
        if movimiento_valido(nueva_pos) and nueva_pos != gato_pos:
            return nueva_pos
    return raton_pos

def dibujar_tablero(pantalla, gato_pos, raton_pos, madriguera_pos):
    pantalla.fill(COLOR_FONDO)
    for fila in range(TAMANO_TABLERO):
        for col in range(TAMANO_TABLERO):
            rect = pygame.Rect(col * ANCHO_CELDA, fila * ALTURA_CELDA, ANCHO_CELDA, ALTURA_CELDA)
            pygame.draw.rect(pantalla, COLOR_LINEA, rect, 1)
            if (fila, col) == gato_pos:
                pantalla.blit(gato_imagen, rect)
            elif (fila, col) == raton_pos:
                pantalla.blit(raton_imagen, rect)
            elif (fila, col) == madriguera_pos:
                pantalla.blit(madriguera_imagen, rect)
    pygame.display.flip()

def jugar_maquina_vs_maquina():
    gato_pos = (random.randint(0, TAMANO_TABLERO - 1), random.randint(0, TAMANO_TABLERO - 1))
    raton_pos = (random.randint(0, TAMANO_TABLERO - 1), random.randint(0, TAMANO_TABLERO - 1))

    # Asegurarse de que gato y ratón no comiencen en la misma posición
    while gato_pos == raton_pos:
        raton_pos = (random.randint(0, TAMANO_TABLERO - 1), random.randint(0, TAMANO_TABLERO - 1))

    # Generar una madriguera en una esquina aleatoria
    esquina = random.choice(['noroeste', 'noreste', 'suroeste', 'sureste'])
    if esquina == 'noroeste':
        madriguera_pos = (0, 0)
    elif esquina == 'noreste':
        madriguera_pos = (0, TAMANO_TABLERO - 1)
    elif esquina == 'suroeste':
        madriguera_pos = (TAMANO_TABLERO - 1, 0)
    else:
        madriguera_pos = (TAMANO_TABLERO - 1, TAMANO_TABLERO - 1)

    while gato_pos != raton_pos:
        dibujar_tablero(pantalla, gato_pos, raton_pos, madriguera_pos)
        pygame.time.wait(500)  # Pausa para visualización del movimiento

        # Turno del gato
        gato_pos = mejor_movimiento_gato(gato_pos, raton_pos, madriguera_pos, profundidad=3)
        if gato_pos == raton_pos:
            mostrar_mensaje("¡El gato atrapó al ratón!")
            break

        # Turno del ratón
        raton_pos = mejor_movimiento_raton(gato_pos, raton_pos, madriguera_pos)
        if raton_pos == madriguera_pos:
            mostrar_mensaje("¡El ratón ha llegado a la madriguera!")
            break

    pygame.quit()

def mostrar_mensaje(mensaje):
    pantalla.fill(COLOR_FONDO)
    fuente = pygame.font.SysFont(None, 40)
    texto = fuente.render(mensaje, True, COLOR_LINEA)
    texto_rect = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTURA_VENTANA // 2))
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

if __name__ == "__main__":
    jugar_maquina_vs_maquina()



