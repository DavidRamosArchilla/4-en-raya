tablero = [[], [], [], [], [], [], []]

jugador_actual = 'O'  # X persona; O es la ia

ALTURA_MAXIMA = 6

def cambiar_jugador():
    if jugador_actual == 'X':
        return 'O'
    else:
        return 'X'


def meter_ficha(columna):
    if (len(tablero[columna]) < ALTURA_MAXIMA):
        tablero[columna].append(jugador_actual)


def hay_ganador():
    cont = 1
    # columnas
    for columna in tablero:
        ficha_ant = ''
        for ficha in columna:
            if ficha_ant == ficha:
                cont += 1
            else:
                cont = 1
            if cont == 4:
                return ficha
            ficha_ant = ficha
    # filas
    filas = get_filas()
    posible_ganador_filas = hay_4_seguidos(filas)
    if posible_ganador_filas is not None:
        return posible_ganador_filas

    # diagonales
    # daigonales hacia la derecha
    diagonales = get_diagonales()
    posible_ganador_diag = hay_4_seguidos(diagonales)
    if posible_ganador_diag is not None:
        return posible_ganador_diag
    return '-'


def imprimir_tablero():
    filas = get_filas()
    for fila in filas[::-1]:
        print("|", end='')
        for item in fila:
            print(item + "|", end='')
        print('')
    print("|0|1|2|3|4|5|6|")


def get_filas():
    filas = []
    for i in range(ALTURA_MAXIMA):
        fila = [columna[i] if i < len(columna) else '-' for columna in tablero]
        filas.append(fila)
    return filas


def get_diagonales():
    filas = get_filas()
    # daigonales hacia la derecha
    diagonales = []
    for i in range(ALTURA_MAXIMA):
        diagonal_arriba = [filas[j + i][j] for j in range(ALTURA_MAXIMA) if i + j < ALTURA_MAXIMA]
        diagonal_abajo = [filas[j][j + i] for j in range(ALTURA_MAXIMA) if i + j < len(tablero)]
        if i != 0 and len(diagonal_abajo) > 3:
            diagonales.append(diagonal_abajo)
        diagonales.append(diagonal_arriba)

        # diagonales hacia la izquierda
    for i in range(ALTURA_MAXIMA):
        diagonal_arriba = [filas[j][-j - 1 - i] for j in range(ALTURA_MAXIMA) if -j - 1 - i >= -7]
        diagonal_abajo = [filas[j + i][-j - 1] for j in range(ALTURA_MAXIMA) if j + i < ALTURA_MAXIMA]
        diagonales.append(diagonal_abajo)
        if i != 0 and len(diagonal_arriba) > 3:  # para que no se duplique la primera diagonal
            diagonales.append(diagonal_arriba)
    return diagonales


def hay_4_seguidos(lineas):
    cont = 1
    for fila in lineas:
        ficha_ant = ''
        for ficha in fila:
            if ficha_ant != '-' and ficha_ant == ficha:
                cont += 1
            else:
                cont = 1
            if cont == 4:
                return ficha
            ficha_ant = ficha


def get_abiertos():
    columnas = [3,4,2,5,1,6,0] #con este orden se priorizan las columnas del medio
    for i in range(len(tablero)):
        if len(tablero[i]) >=ALTURA_MAXIMA:
            columnas.remove(i)
    return columnas #[i for i in range(len(tablero)) if len(tablero[i]) < ALTURA_MAXIMA]


# def minimax(profundidad,jugador):
#     ganador = hay_ganador()
#     if ganador == 'X':
#         return -1000000,None
#     if ganador == 'O':
#         return 1000000,None
#     if profundidad == 0:
#         return valorar_tablero(),None
#     if jugador == 'O':
#         val = -1000000
#         abiertos = get_abiertos()
#         posicion_mejor = 0
#         mejor_valor = -1000000
#         valores = []
#         for pos in abiertos:
#             tablero[pos].append(jugador) # "generar" estado hijo
#             val = max(val, minimax(profundidad-1,'X')[0])
#             tablero[pos].pop() #volver al estado actual
#             if val > mejor_valor:  #guardar la columna de la mejor jugada
#                 mejor_valor = val
#                 posicion_mejor = pos
#             valores.append(val)
#         return val,posicion_mejor
#     else:
#         val2 = 1000000
#         abiertos = get_abiertos()
#         for pos in abiertos:
#             tablero[pos].append(jugador)
#             val2 = min(val2, minimax(profundidad - 1,'O')[0])
#             tablero[pos].pop()
#
#         return val2,None

def minimax_alpha_beta(profundidad, alpha, beta, jugador):
    # ganador = hay_ganador()
    # if ganador == 'X':
    #     return -1000000, None
    # if ganador == 'O':
    #     return 1000000, None
    if profundidad == 0:
        return heuristico(), None
    if jugador == 'O':
        valor = -10000000
        abiertos = get_abiertos()
        posicion_mejor = 0
        mejor_valor = -100000000
        for pos in abiertos:
            tablero[pos].append(jugador)  # "generar" estado hijo
            valor = max(valor, minimax_alpha_beta(profundidad - 1, alpha, beta, 'X')[0])
            tablero[pos].pop()  # volver al estado actual
            alpha = max(alpha, valor)
            if alpha >= beta:
                break  # poda
            if valor > mejor_valor:  # guardar la columna de la mejor jugada
                mejor_valor = valor
                posicion_mejor = pos
        return valor, posicion_mejor
    else:
        valor2 = 10000000
        abiertos = get_abiertos()
        for pos in abiertos:
            tablero[pos].append(jugador)
            valor2 = min(valor2, minimax_alpha_beta(profundidad - 1, alpha, beta, 'O')[0])
            tablero[pos].pop()
            beta = min(beta, valor2)
            if alpha >= beta:
                break  # poda
        return valor2, None


def heuristico():
    # sobre el tablero acutal
    valor = 0
    filas = get_filas()
    diagonales = get_diagonales()
    columnas = [[fila[i] for fila in filas] for i in range(len(filas[0]))]
    lineas = diagonales + filas + columnas
    for linea in lineas:
        valor += heuristico_linea(linea)
        if valor<-1000 or valor>1000:
            return valor
    return valor


def heuristico_linea(linea):
    # devuelve el numero de fichas que hay pos cada posible(un jugador puede ganar en ella)
    puntuacion = 0
    for i in range(len(linea) - 3):
        puntuacion += evaluar_4_elementos(linea[i:4 + i])
        if puntuacion<-1000 or puntuacion>1000:
            return puntuacion
    return puntuacion


def evaluar_4_elementos(linea):
    # linea va a tener 4 elementos
    cant_o = 0
    cant_x = 0
    for elemento in linea:
        if elemento == 'X':
            cant_x += 1
        elif elemento == 'O':
            cant_o += 1
    if cant_x == 0:
        return 100000 if cant_o == 4 else cant_o
    elif cant_o == 0:
        return -1000000 if cant_x==4 else -1 * cant_x

    return 0


imprimir_tablero()
PROFUNDIDAD = 7
ALPHA = -1000000000
BETA = 1000000000

while True:
    if jugador_actual == 'X':
        try:
            columna = int(input("juegan" + jugador_actual + " : "))
            meter_ficha(columna)
        except:
            print("no valido")
            continue
    else:
        tupla = minimax_alpha_beta(PROFUNDIDAD, ALPHA, BETA, 'O')
        print("heuristico: ", tupla[0], "columna: ", tupla[1])
        meter_ficha(tupla[1])
    imprimir_tablero()
    posible_ganador = hay_ganador()
    if posible_ganador != '-':
        print("Ganan " + jugador_actual)
        break
    jugador_actual = cambiar_jugador()


"""
otro posible heuristico

def valorar_tablero():
    puntuacion = 0
    filas = get_filas()
    diagonales = get_diagonales()
    columnas = [[fila[i] for fila in filas] for i in range(len(filas[0]))]
    lineas = filas + columnas + diagonales
    for fila in lineas:
        maq = 0
        per = 0
        hue = 0
        segmaq = 0
        segper = 0
        seghue = 0
        for elemento in fila:
            if elemento == 'O':
                maq += 1
                segmaq += 1
                if (per > 0):
                    hue = seghue
                else:
                    hue += seghue
                per = 0
                seghue = 0
                segper = 0
            if (elemento == 'X'):
                per += 1
                segper += 1
                if (maq > 0):
                    hue = seghue
                else:
                    hue += seghue
                maq = 0
                seghue = 0
                segmaq = 0
            if (elemento == '-'):
                seghue += 1
                segmaq = 0
                segper = 0
            if (segmaq + hue + seghue >= 4):
                puntuacion += valoraTira(segmaq, maq, seghue, hue)
            if (segper + hue + seghue >= 4):
                puntuacion -= valoraTira(segper, per, seghue, hue)

    return puntuacion


def valoraTira(numFichasSeguidas, numFichas, numHuecosSeguidos, numHuecos):
    PESOS_PUNTUACION = [0, 10, 100, 10000, 0, 0, 0]
    if (numFichas + numHuecos) >= 4:
        return PESOS_PUNTUACION[numFichasSeguidas] + 10 * numFichas + 3 * numHuecosSeguidos + numHuecos
    else:
        return 0
"""