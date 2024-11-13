import pygame
import time
import random

# Inicializar Pygame
pygame.init()

# Dimensiones
lado_tablero = 450
ancho_ventana = 480
alto_ventana = 550
margen = (ancho_ventana - lado_tablero) // 2 

# Configuración de la ventana
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Juego de Sudoku")

# Colores 
blanco = "#ffffff"
color_contraste = "#f5b041" # (245, 176, 65) rgb
rojo_fondo = "#e74c3c"
rojo = "#c0392b"
color_fondo = "#196f3d" # (25, 111, 61)

# Fuentes
try:
    fuente_titulos = pygame.font.Font("fuentes/Montserrat-LightItalic.ttf", 40)
    fuente_detalles = pygame.font.Font("fuentes/Montserrat-Thin.ttf",16)
    fuente_numeros = pygame.font.Font("fuentes/Montserrat-SemiBoldItalic.ttf", 40)
    fuente_texto = pygame.font.Font("fuentes/Montserrat-Regular.ttf", 16)
except FileNotFoundError: 
    # Maneja el error en caso que no encuentre los archivos para que no se rompa el programa
    print("Error en la carga de las fuentes")
    fuente_titulos = pygame.font.Font(None, 40)
    fuente_detalles = pygame.font.Font(None, 16)
    fuente_numeros = pygame.font.Font(None, 40)
    fuente_texto = pygame.font.Font(None, 16)

# Función para generar un tablero de sudoku completo random 
def generar_sudoku_completo():

    def patron(fila, columna): 
        return (3*(fila % 3) + fila // 3 + columna) % 9

    def mezclar(lista): 
        return random.sample(lista, len(lista))

    base_filas = range(3)  # Rango de los índices de las filas y columnas
    filas = [g * 3 + f for g in mezclar(base_filas) for f in mezclar(base_filas)]  # Filas aleatorias
    columnas = [g * 3 + c for g in mezclar(base_filas) for c in mezclar(base_filas)]  # Columnas aleatorias
    numeros = mezclar(range(1, 9 + 1))  # Los números que van en el tablero (1-9)

    tablero = [[numeros[patron(fila, columna)] for columna in columnas] for fila in filas]

    return tablero

# Función para eliminar cierta cantidad de celdas de un sudoku completo
def eliminar_celdas(tablero, vacios=30):
    tablero_copia = [fila[:] for fila in tablero]  
    for _ in range(vacios):
        fila = random.randint(0, 8)
        columna = random.randint(0, 8)
        tablero_copia[fila][columna] = 0
    return tablero_copia

# Función para generar un sudoku 
def generar_sudoku(dificultad):
    # Retorna el sudoku puzle y su resolución
    # Recibe la dificultad (0,1,2)

    random.seed() 

    tablero_completado = generar_sudoku_completo()

    if dificultad == 0:
        vacios = 20 
    elif dificultad == 1:
        vacios = 40 
    else:
        vacios = 60 

    sudoku = eliminar_celdas(tablero_completado, vacios)

    return sudoku, tablero_completado

def main():

    # Título de la pantalla principal
    try:
        titulo = pygame.image.load("imagenes/Titulo.png")
    except FileNotFoundError:
        # Maneja el error en caso que no encuentre los archivos para que no se rompa el programa
        fuente = pygame.font.Font(None,80)
        titulo = fuente.render("Juego Sudoku", True, blanco)
    titulo_RECT = titulo.get_rect(center=(ancho_ventana // 2, alto_ventana // 4))

    # Botones para empezar el juego
    facil_TXT = fuente_titulos.render("Nivel Fácil", True, blanco)
    medio_TXT = fuente_titulos.render("Nivel Medio", True, blanco)
    dificil_TXT = fuente_titulos.render("Nivel Dificil", True, blanco)

    facil_RECT = facil_TXT.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 + 30))
    medio_RECT = medio_TXT.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 + 90))
    dificil_RECT = dificil_TXT.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 + 150))

    bucle_principal = True
    # Bucle principal de la aplicación
    while bucle_principal:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                bucle_principal = False

            # Cambiar el cursor cuando está sobre el botón
            elif evento.type == pygame.MOUSEMOTION:
                x, y = evento.pos

                # Cursor sobre el boton facil
                if validar_cursor_sobre_rectangulo(x,y,facil_RECT):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                    facil_TXT = fuente_titulos.render("Nivel Fácil", True, color_contraste)

                # Cursor sobre el boton medio
                elif validar_cursor_sobre_rectangulo(x,y,medio_RECT):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                    medio_TXT = fuente_titulos.render("Nivel Medio", True, color_contraste)
                
                # Cursor sobre el boton dificil
                elif validar_cursor_sobre_rectangulo(x,y,dificil_RECT):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                    dificil_TXT = fuente_titulos.render("Nivel Dificil", True, color_contraste)

                # Cursor cuando no se está en ningun boton
                else:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    facil_TXT = fuente_titulos.render("Nivel Fácil", True, blanco)
                    medio_TXT = fuente_titulos.render("Nivel Medio", True, blanco)
                    dificil_TXT = fuente_titulos.render("Nivel Dificil", True, blanco)

            # Empezar el juego cuando se clickea el botón
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos

                # Click en los botones de los niveles
                if validar_cursor_sobre_rectangulo(x, y, facil_RECT):
                    sudoku, solucion = generar_sudoku(0)
                    bucle_principal = juego(sudoku, solucion) # Empieza el juego nivel facil
                elif validar_cursor_sobre_rectangulo(x, y, medio_RECT):
                    sudoku, solucion = generar_sudoku(1)
                    bucle_principal = juego(sudoku, solucion) # Empieza el juego nivel medio
                elif validar_cursor_sobre_rectangulo(x, y, dificil_RECT):
                    sudoku, solucion = generar_sudoku(2)
                    bucle_principal = juego(sudoku, solucion) # Empieza el juego nivel dificil

        # Color de fondo de pantalla
        ventana.fill(color_fondo) 

        # Dibujar el título y los botones en la pantalla
        ventana.blit(titulo, titulo_RECT)
        ventana.blit(facil_TXT, facil_RECT)
        ventana.blit(medio_TXT, medio_RECT)
        ventana.blit(dificil_TXT, dificil_RECT)
        

        # Actualiza la pantalla
        pygame.display.flip()

    pygame.quit()  # Cerrar Pygame

# Función para verificar la posición del cursor sobre un objeto rectangular
def validar_cursor_sobre_rectangulo(x, y, rectangulo):
    return (rectangulo.left < x < rectangulo.right and rectangulo.top < y < rectangulo.bottom)

# Función para verificar si la posición el cursor esta sobre una casilla vacía
def validar_cursor_sobre_casilla_vacia(x,y,sudoku_usuario):
    # Recibe como parametros las coordenadas x,y del mouse y el sudoku del juego del usuario

    fila, columna = calcular_fila_columna(x,y)
    if fila not in range(9) or columna not in range(9):
        return False

    if sudoku_usuario[fila][columna] != 0: 
        return False

    return True

# Función para dibujar el sudoku del usuario con los números correctos
def dibujar_sudoku(sudoku_usuario, dimensiones, numero_seleccionado=0, fuente=fuente_numeros):
    # Recibe como parametros el sudoku del juego del usuario un array con las dimensiones (lado del tablero, margen en x, margen en y)

    lado_tablero = dimensiones[0]
    margen_x = dimensiones[1]
    margen_y = dimensiones[2]
    lado_casilla = lado_tablero // 9

    # Lineas horizontales
    for i in range(10):
        pygame.draw.line(ventana, blanco, (margen_x, i * lado_casilla + margen_y), (lado_tablero + margen_x, i * lado_casilla + margen_y), width = 1)
        if i % 3 == 0:
            pygame.draw.line(ventana, blanco, (margen_x, i * lado_casilla + margen_y), (lado_tablero + margen_x, i * lado_casilla + margen_y), width = 3)
    
    # Lineas verticales
    for i in range(10):
        pygame.draw.line(ventana, blanco, (i * lado_casilla + margen_x, margen_y), (i * lado_casilla + margen_x, margen_y + lado_tablero), width = 1)
        if i % 3 == 0:
            pygame.draw.line(ventana, blanco, (i * lado_casilla + margen_x, margen_y), (i * lado_casilla + margen_x, margen_y + lado_tablero), width = 3)
    
    # Sudoku
    for fila in range(9):
        for columna in range(9):
            # Dibuja el sudoku inicial
            if sudoku_usuario[fila][columna] != 0:
                if numero_seleccionado != sudoku_usuario[fila][columna]:
                    n_TXT = fuente.render(str(sudoku_usuario[fila][columna]), True, blanco)
                else:
                    n_TXT = fuente.render(str(sudoku_usuario[fila][columna]), True, color_contraste)
                n_RECT = n_TXT.get_rect(center=(margen_x + columna*lado_casilla + lado_casilla // 2, margen_y + fila*lado_casilla + lado_casilla // 2))
                ventana.blit(n_TXT, n_RECT)

# Función para dibujar los números escritos por el usuario
def dibujar_numeros_incorrectos(sudoku_usuario, error):
    if error == [None]*3:
        return # Si no hay errores retorna sin dibujar nada

    n_TXT = fuente_numeros.render(str(error[0]), True, rojo)
    fila = error[1]
    columna = error[2]
    n_RECT = n_TXT.get_rect(center=(columna*lado_tablero//9 + margen + lado_tablero//9//2, fila*lado_tablero//9 + margen + lado_tablero//9// 2))
    ventana.blit(n_TXT, n_RECT)

# Función para marcar los errores del usuario
def marcar_errores(sudoku_usuario, error):
    if error == [None]*3:
        return # Si no hay errores retorna sin marcar nada
    
    # Encontrar los números incorrectos
    n = error[0]
    fila = error[1]
    columna = error[2]
        
    # Comprobar si esta en el minitablero 3x3
    tablero3x3_fila = fila // 3
    tablero3x3_columna = columna // 3
    tablero3x3 = [[0 for k in range(3)] for k in range(3)]
    indice_tablero3x3 = 0
    error_tablero3x3 = False
    for k in range(tablero3x3_fila * 3, tablero3x3_fila * 3 + 3):
        # Obtener el tablero3x3
        tablero3x3[indice_tablero3x3] = sudoku_usuario[k][tablero3x3_columna*3:tablero3x3_columna*3+3]
        indice_tablero3x3 += 1

        # Comprobar si el error esta dentro del tablero 3x3
        if n in sudoku_usuario[k][tablero3x3_columna*3:tablero3x3_columna*3+3]:
            error_tablero3x3 = True
                
    if error_tablero3x3:
        tablero3x3_RECT = pygame.Rect(margen + tablero3x3_columna*lado_tablero//3, margen + tablero3x3_fila*lado_tablero//3, lado_tablero//3,lado_tablero//3)
        ventana.fill(rojo_fondo, tablero3x3_RECT) # Agrega el fondo rojo al objeto RECT creado en la sección del error

    # Comprobar si se repitió en la línea (por fuera del 3x3)
    if n in sudoku_usuario[fila] and n not in tablero3x3[fila % 3]:
        linea_RECT = pygame.Rect(margen, margen + fila*lado_tablero//9, lado_tablero, lado_tablero // 9)
        ventana.fill(rojo_fondo, linea_RECT) # Agrega el fondo rojo al objeto RECT creado en la sección del error

    # Comprobar si se repitió en la columna (por fuera del 3x3)
    error_columna = False
    for fila in range(9):
        if n == sudoku_usuario[fila][columna] and n != tablero3x3[fila % 3][columna % 3]:
            error_columna = True
            break
                
    if error_columna:
        columna_RECT = pygame.Rect(margen + columna*lado_tablero//9, margen, lado_tablero // 9, lado_tablero)
        ventana.fill(rojo_fondo, columna_RECT) # Agrega el fondo rojo al objeto RECT creado en la sección del error

# Función para usar pista
def usar_pista(sudoku_usuario, solucion):
    while True:
        i = random.randint(0,8)
        j = random.randint(0,8)
        if sudoku_usuario[i][j] == 0:
            sudoku_usuario[i][j] = solucion[i][j]
            return sudoku_usuario
        

# Función para validar una jugada
def validar_jugada(fila, columna, n, solucion):
    return n == solucion[fila][columna]

# Función para calcular el indice de fila y columna a partir de las coordenadas de mouse
def calcular_fila_columna(x,y):
    return (y - margen) // (lado_tablero // 9), (x - margen) // (lado_tablero // 9)

def juego(sudoku_usuario, solucion_sudoku):

    # array que contendrá los dos errores que puede tener el usuario
    error1_sudoku = [None]*3
    error2_sudoku = [None]*3

    # Datos del jugador
    errores = 0 # contador de errores (hasta 3 errores)
    errores_TXT = fuente_detalles.render(f"Errores: {errores}/3", True, blanco)
    altura = lado_tablero + margen + errores_TXT.get_height() // 2 + 5
    errores_RECT = errores_TXT.get_rect(center=(margen + errores_TXT.get_width() // 2, altura))

    pistas = 3 # contador de pistas (empieza con 3 pistas)
    pistas_TXT = fuente_detalles.render(f"Pistas: {pistas}/3", True, blanco)
    pistas_RECT = pistas_TXT.get_rect(center=(10 + errores_RECT.right + pistas_TXT.get_width() // 2, altura))

    usar_pista_TXT = fuente_detalles.render("Usar pista", True, blanco)
    usar_pista_RECT = usar_pista_TXT.get_rect(center=(10 + pistas_RECT.right + usar_pista_TXT.get_width() // 2, altura))

    # Botón para terminar el juego
    rendirse_TXT = fuente_detalles.render("Rendirse", True, blanco)
    rendirse_RECT = rendirse_TXT.get_rect(center=(lado_tablero + margen - rendirse_TXT.get_width() // 2, altura))

    # Selección de números
    lista_numeros_TXT = [fuente_titulos.render(str(i), True, blanco) for i in range(0,10)]
    lista_numeros_RECT = [None]*10
    for i in range(10):
        lista_numeros_RECT[i] = lista_numeros_TXT[i].get_rect(center=(55 + i * 40, alto_ventana - (alto_ventana - lado_tablero - margen*2) // 2 - 3))

    # Como jugar
    reglas_TXT = fuente_detalles.render("Reglas", True, blanco)
    reglas_RECT = reglas_TXT.get_rect(center=(reglas_TXT.get_width() // 2 + 3, alto_ventana - reglas_TXT.get_height() // 2))

    # Número seleccionado
    num = 1

    # Estadísticas 
    tiempo_inicio = time.time()

    bucle_juego = True
    # Bucle del juego
    while bucle_juego:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False # Corta el bucle principal si se cierra bruscamente
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x,y = evento.pos

                # Selección de números con click en el número
                for i in range(10):
                    if validar_cursor_sobre_rectangulo(x,y, lista_numeros_RECT[i]):
                        num = i
                
                # Fila y columna de la casilla clickeada
                fila, columna = calcular_fila_columna(x,y)
                
                if (fila == error1_sudoku[1] and columna == error1_sudoku[2]):
                    error1_sudoku = [None]*3
                elif (fila == error2_sudoku[1] and columna == error2_sudoku[2]):
                    error2_sudoku = [None]*3
                
                if validar_cursor_sobre_casilla_vacia(x,y,sudoku_usuario) and num != 0:  
                    if validar_jugada(fila, columna, num, solucion_sudoku):
                        sudoku_usuario[fila][columna] = num
                    else:
                        errores += 1
                        if errores < 3:
                            errores_TXT = fuente_detalles.render(f"Errores: {errores}/3", True, blanco)
                        else:
                            sudoku_completado = False
                            bucle_juego = False # Termino el juego
                        
                        if error1_sudoku == [None]*3:
                            error1_sudoku = [num, fila, columna]
                        else:
                            error2_sudoku = [num, fila, columna]
                
                # Click sobre el boton 'reglas'
                if validar_cursor_sobre_rectangulo(x,y,reglas_RECT):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    if reglas() == False:
                        return False # Cortar el bucle principal si la ventana de reglas se cerro bruscamente
                
                # Click sobre el boton 'rendirse'
                elif validar_cursor_sobre_rectangulo(x,y,rendirse_RECT):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    sudoku_completado = False
                    bucle_juego = False

                # Click sobre el boton 'usar pista'
                elif validar_cursor_sobre_rectangulo(x,y,usar_pista_RECT):
                    if pistas > 0:
                        sudoku_usuario = usar_pista(sudoku_usuario, solucion_sudoku)
                        pistas -= 1
                        pistas_TXT = fuente_detalles.render(f"Pistas: {pistas}/3", True, blanco)
            
            elif evento.type == pygame.MOUSEMOTION:
                x,y = evento.pos

                # Cursor sobre un número a seleccionar
                puntero = False
                for i in range(10):
                    if validar_cursor_sobre_rectangulo(x,y,lista_numeros_RECT[i]):
                        puntero = True
                if puntero:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                
                # Cursor sobre una casilla vacía
                elif validar_cursor_sobre_casilla_vacia(x,y,sudoku_usuario):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)

                    # Cursor sobre números borrables
                    if num == 0:
                        fila, columna = calcular_fila_columna(x,y)
                        if (fila == error1_sudoku[1] and columna == error1_sudoku[2]) or (fila == error2_sudoku[1] and columna == error2_sudoku[2]):
                            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                        else:
                            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

                # Cursor sobre el botón 'usar pista'
                elif validar_cursor_sobre_rectangulo(x,y,usar_pista_RECT):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                    usar_pista_TXT = fuente_detalles.render("Usar pista", True, color_contraste)
                
                # Cursor sobre el botón 'reglas'
                elif validar_cursor_sobre_rectangulo(x,y,reglas_RECT):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                    reglas_TXT = fuente_detalles.render("Reglas", True, color_contraste)

                # Cursor sobre el boton 'rendirse'
                elif validar_cursor_sobre_rectangulo(x,y,rendirse_RECT):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                    rendirse_TXT = fuente_detalles.render("Rendirse", True, color_contraste)
                    
                else:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    usar_pista_TXT = fuente_detalles.render("Usar pista", True, blanco)
                    reglas_TXT = fuente_detalles.render("Reglas", True, blanco)
                    rendirse_TXT = fuente_detalles.render("Rendirse", True, blanco)
                
            # Controla si el usuario eligio un número por el teclado
            elif evento.type == pygame.KEYDOWN:
                if evento.key in range(48, 59):
                    num = evento.key - 48 # Las teclas de números empiezan su codigo ASCII desde el 48 que es el 0
        
        # Color de fondo de pantalla
        ventana.fill(color_fondo)

        # Marcar errores del usuario
        marcar_errores(sudoku_usuario, error1_sudoku)
        marcar_errores(sudoku_usuario, error2_sudoku)

        # Dibujar sudoku
        dibujar_sudoku(sudoku_usuario, [lado_tablero, margen, margen], numero_seleccionado=num)

        # Dibujar números incorrectos
        dibujar_numeros_incorrectos(sudoku_usuario, error1_sudoku)
        dibujar_numeros_incorrectos(sudoku_usuario, error2_sudoku)
        
        # Dibujar los datos del jugador
        ventana.blit(errores_TXT, errores_RECT)
        ventana.blit(pistas_TXT, pistas_RECT)
        ventana.blit(usar_pista_TXT, usar_pista_RECT)

        # Dibujar los números a seleccionar 
        for i in range(10):
            ventana.blit(lista_numeros_TXT[i], lista_numeros_RECT[i])

        # Dibujar boton 'reglas'
        ventana.blit(reglas_TXT, reglas_RECT)

        # Dibujar el boton para rendirse
        ventana.blit(rendirse_TXT, rendirse_RECT)

        # Marcar número seleccionado
        num_pantalla = fuente_titulos.render(str(num), True, color_contraste)
        ventana.blit(num_pantalla, lista_numeros_RECT[num])

        # Termina el juego si se completa el sudoku
        if all(0 not in sudoku_usuario[i] for i in range(9)):
            sudoku_completado = True
            bucle_juego = False

        # Actualiza la pantalla
        pygame.display.flip()

    return juego_terminado(solucion_sudoku, errores, pistas, tiempo_inicio, sudoku_completado)

def reglas():

    # Titulo
    titulo_TXT = fuente_titulos.render("¿Cómo jugar?", True, blanco)
    titulo_RECT = titulo_TXT.get_rect(center=(ancho_ventana // 2, titulo_TXT.get_height() // 2 + 30))

    # Imagen ilustrativa de las reglas
    try:
        reglas_IMG = pygame.image.load("imagenes/reglas.png")
        reglas_RECT = reglas_IMG.get_rect(center=(ancho_ventana // 2, titulo_RECT.bottom + 30 + reglas_IMG.get_height() // 2))
    except FileNotFoundError:
        reglas_IMG = None
        tablero_ejemplo = [
            [0,0,1,0,0,0,0,0,0],
            [0,0,2,0,0,0,0,0,0],
            [0,0,3,0,0,0,0,0,0],
            [5,1,4,2,3,6,8,7,9],
            [0,0,5,0,0,0,0,0,0],
            [0,0,6,0,0,0,0,0,0],
            [0,0,7,0,0,0,6,8,1],
            [0,0,8,0,0,0,9,5,2],
            [0,0,9,0,0,0,7,4,3],
        ]

    # Reglas
    regla1_TXT = fuente_texto.render("• Cada fila contiene los números del 1 al 9", True, blanco)
    if reglas_IMG:
        regla1_RECT = regla1_TXT.get_rect(center=(ancho_ventana // 2, reglas_RECT.bottom + 30))
    else:
        regla1_RECT = regla1_TXT.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 + 120))

    regla2_TXT = fuente_texto.render("• Cada columna contiene los números del 1 al 9", True, blanco)
    regla2_RECT = regla2_TXT.get_rect(center=(ancho_ventana // 2, regla1_RECT.bottom + 16))

    regla3_TXT = fuente_texto.render("• Cada minitablero 3x3 contiene los números del 1 al 9", True, blanco)
    regla3_RECT = regla3_TXT.get_rect(center=(ancho_ventana // 2, regla2_RECT.bottom + 16))

    regla4_TXT = fuente_texto.render("por lo tanto, no hay números repetidos en ellos", True, blanco)
    regla4_RECT = regla4_TXT.get_rect(center=(ancho_ventana // 2, regla3_RECT.bottom + 16))

    regla5_TXT = fuente_texto.render("Completa el tablero para ganar!!", True, blanco)
    regla5_RECT = regla5_TXT.get_rect(center=(ancho_ventana // 2, regla4_RECT.bottom + 20))

    regla6_TXT = fuente_texto.render("Si acumulas mas de 3 errores pierdes el juego", True, blanco)
    regla6_RECT = regla6_TXT.get_rect(center=(ancho_ventana // 2, regla5_RECT.bottom + 16))

    # Boton retroceder 
    retroceder_TXT = fuente_titulos.render("←", True, blanco)
    retroceder_RECT = retroceder_TXT.get_rect(center=(retroceder_TXT.get_width() // 2 + 5, retroceder_TXT.get_height() // 2))

    bucle_reglas = True
    # Bucle de la ventana reglas
    while bucle_reglas:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False # Corta el bucle principal si se cierra bruscamente la aplicacion
            
            elif evento.type == pygame.MOUSEMOTION:
                x,y = evento.pos
                
                # Cursor sobre el boton de retroceder
                if validar_cursor_sobre_rectangulo(x,y,retroceder_RECT):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                    retroceder_TXT = fuente_titulos.render("←", True, color_contraste)
                else:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    retroceder_TXT = fuente_titulos.render("←", True, blanco)
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x,y = evento.pos

                # Click sobre el boton para retroceder
                if validar_cursor_sobre_rectangulo(x,y,retroceder_RECT):
                    bucle_reglas = False 
        

        # Color de fondo de pantalla
        ventana.fill(color_fondo)

        # Dibuja el titulo
        ventana.blit(titulo_TXT, titulo_RECT)

        # Dibuja imagen ilustrativa de las reglas
        if reglas_IMG:
           ventana.blit(reglas_IMG, reglas_RECT)
        else:
            dimensiones_tablero = [270, (ancho_ventana - 270) // 2, 90]
            dibujar_sudoku(tablero_ejemplo, dimensiones_tablero, fuente_detalles)

        # Dibuja las reglas
        ventana.blit(regla1_TXT, regla1_RECT)
        ventana.blit(regla2_TXT, regla2_RECT)
        ventana.blit(regla3_TXT, regla3_RECT)
        ventana.blit(regla4_TXT, regla4_RECT)
        ventana.blit(regla5_TXT, regla5_RECT)
        ventana.blit(regla6_TXT, regla6_RECT)

        # Dibuja el boton para retroceder
        ventana.blit(retroceder_TXT, retroceder_RECT)

        # Actualiza la pantalla
        pygame.display.flip()
    return True # Mantiene el ciclo si se vuelve a la ventana anterior

def segundos_a_hs(seg):
    if seg < 60:
        return f"0 hs 0 min {int(seg)} s"
    elif seg < 3600:
        min = seg // 60
        seg = seg % 60
        return f"0 hs {int(min)} min {int(seg)} seg"
    else:
        hs = seg // 3600
        min = (seg % 3600) // 60
        seg = seg % 60
        return f"{int(hs)} hs {int(min)} min {int(seg)} seg"
    
def pantalla_final_ganador(tiempo_inicio, errores, pistas):

    # Texto final
    ganaste_TXT = fuente_titulos.render("Has ganado el juego!!", True, blanco)
    ganaste_RECT = ganaste_TXT.get_rect(center=(ancho_ventana // 2, 50))

    # Imagen ganador
    try:
        trofeo_IMG = pygame.image.load("imagenes/trofeo.png")
        trofeo_RECT = trofeo_IMG.get_rect(center=(ancho_ventana // 2, trofeo_IMG.get_height() // 2 + 50))
    except FileNotFoundError:
        trofeo_IMG = fuente_detalles.render("image not found", True, blanco) 
        trofeo_RECT = trofeo_IMG.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 - 30))

    # Estadísticas
    tiempo_jugado = segundos_a_hs(time.time() - tiempo_inicio)
    tiempo_jugado_TXT = fuente_titulos.render(f"{tiempo_jugado}", True, blanco)
    tiempo_jugado_RECT = tiempo_jugado_TXT.get_rect(center=(ancho_ventana // 2, alto_ventana // 2 + 120))

    errores_TXT = fuente_texto.render(f"{errores} errores", True, blanco)
    errores_RECT = errores_TXT.get_rect(center=(ancho_ventana // 2, tiempo_jugado_RECT.bottom + 16))

    pistas_usadas_TXT = fuente_texto.render(f"{3 - pistas} pistas usadas", True, blanco)
    pistas_usadas_RECT = pistas_usadas_TXT.get_rect(center=(ancho_ventana // 2, errores_RECT.bottom + 16))

    # volver a jugar
    jugar_de_nuevo_TXT = fuente_detalles.render("Presiona Enter para volver a jugar", True, blanco)
    jugar_de_nuevo_RECT = jugar_de_nuevo_TXT.get_rect(center=(ancho_ventana // 2, alto_ventana - 30))

    bucle = True
    # bucle del final de pantalla
    while bucle:

        for evento in pygame.event.get():
            
            # Cerrar la ventana
            if evento.type == pygame.QUIT:
                return False # Rompe el ciclo principal de la aplicación si se cierra bruscamente la ventana
            
            # Detecta el enter del usuario
            elif evento.type == pygame.KEYDOWN:
                if evento.key == 13:
                    bucle = False
        
        # Color de pantalla
        ventana.fill(color_fondo)

        # Dibuja el texto final
        ventana.blit(ganaste_TXT, ganaste_RECT)

        # Dibuja el trofeo
        ventana.blit(trofeo_IMG, trofeo_RECT)

        # Dibuja las estadísticas del juego
        ventana.blit(tiempo_jugado_TXT, tiempo_jugado_RECT)
        ventana.blit(errores_TXT, errores_RECT)
        ventana.blit(pistas_usadas_TXT, pistas_usadas_RECT)

        # Dibuja el texto
        ventana.blit(jugar_de_nuevo_TXT, jugar_de_nuevo_RECT)

        # Actualiza la pantalla
        pygame.display.flip()
    
    return True # Mantiene el ciclo primario de la aplicación
        
def juego_terminado(solucion_sudoku, errores, pistas, tiempo_inicio, ganador):

    # Dimensiones del tablero del sudoku solución 
    lado_tablero = 270
    margen_x = (ancho_ventana - lado_tablero) // 2
    margen_y = (alto_ventana - lado_tablero) // 2 + 16
    dimensiones_tablero = [lado_tablero, margen_x, margen_y]

    # Resultado
    resultado_TXT = fuente_titulos.render("Juego terminado", True, blanco)
    resultado_RECT = resultado_TXT.get_rect(center=(ancho_ventana // 2, resultado_TXT.get_height() // 2 + 50))

    # Solución 
    solucion_TXT = fuente_texto.render("Solución", True, blanco)
    solucion_RECT = solucion_TXT.get_rect(center=(ancho_ventana // 2, resultado_RECT.bottom + 30))

    # volver a jugar
    jugar_de_nuevo_TXT = fuente_detalles.render("Presiona Enter para volver a jugar", True, blanco)
    jugar_de_nuevo_RECT = jugar_de_nuevo_TXT.get_rect(center=(ancho_ventana // 2, alto_ventana - 30))

    # Si se gana se muestra otra pantalla final sin la solución
    if ganador:
        return pantalla_final_ganador(tiempo_inicio, errores, pistas)

    bucle_juego_terminado = True
    # Bucle de la ventana de fin del juego
    while bucle_juego_terminado:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False # Corta el bucle principal si se cierra bruscamente

            elif evento.type == pygame.KEYDOWN:
                if evento.key == 13:
                    bucle_juego_terminado = False

        # Color de fondo de pantalla
        ventana.fill(color_fondo)

        # Dibujar texto solucion
        ventana.blit(solucion_TXT, solucion_RECT)

        # Dibujar solución
        dibujar_sudoku(solucion_sudoku, dimensiones_tablero, fuente=fuente_detalles)

        # Dibuja el resultado del juego
        ventana.blit(resultado_TXT, resultado_RECT)

        # Dibuja el volver a jugar
        ventana.blit(jugar_de_nuevo_TXT, jugar_de_nuevo_RECT)

        # Actualiza la pantalla
        pygame.display.flip()
    
    return True # Mantiene el bucle principal si se presiona Enter

main()