
import pygame
import time
import random
import sys
import heapq
# set up pygame window
WIDTH = 700
HEIGHT = 650

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255 ,255 ,0)
RED=(255,0,0)
MAGNETA=(255,0,255)
# initalise Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quoridor")

grid = []   #se guarda las coordenadas de los nodos principalmente lo uso para dibujar
tablas_h=[]     #se guarda un arreglo de 64 rectangulos horizontales totales
tablas_v=[]     #se guarda un arreglo de 64 rectangulos verticales totales
tablas_h_p=[None]*64    #se guarda un arreglo de rectangulos que se pusieron por el jugador
tablas_v_p=[None]*64    #se guarda un arreglo de rectangulos que se pusieron por el jugador

# hacemos que cada nodo tenga sus coordenadas, y guardamos 64 rectangulos horizontalees y verticales en sus dos arreglos
def build_grid(x, y, w):
    for i in range(1,10):
        x = 80                                                           
        y = y + 60                                                       
        for j in range(1, 10):
            pygame.draw.rect(screen, WHITE, (x , y, w, w), 0)
            if j!=9 and len(tablas_h)<64:
                a=pygame.Rect(x, y+40,100,20)
                b=pygame.Rect(x+40, y,20,100)
                tablas_h.append(a)
                tablas_v.append(b)
            if len(grid)<81:
                grid.append([x,y])                                           
            x = x + 60                                                   

###############
############### bot 1
###########33
#creamos una clase nodo para cada cuadro blanco
class Node:

    def __init__(self, name):
           self.name = name
           self.visited = False
           self.adjacenciesList = []
           self.predecessor = None
           self.mindistance = sys.maxsize    
    def __lt__(self, other):
           return self.mindistance < other.mindistance

#arista clase
class Edge:

       def __init__(self, weight, startvertex, endvertex):
           self.weight = weight
           self.startvertex = startvertex
           self.endvertex = endvertex

#
def calculateshortestpath(startvertex):
       q = []
       startvertex.mindistance = 0
       heapq.heappush(q, startvertex)

       while q:
           actualnode = heapq.heappop(q)
           for edge in actualnode.adjacenciesList:
               tempdist = edge.startvertex.mindistance + edge.weight
               if tempdist < edge.endvertex.mindistance:
                   edge.endvertex.mindistance = tempdist
                   edge.endvertex.predecessor = edge.startvertex
                   heapq.heappush(q,edge.endvertex)

def getshortestpath(targetvertex):
       print("La distancia mas corta recorrida: ",targetvertex.mindistance)
       node = targetvertex
       sig_paso=node.predecessor.name
       while node:
           print(node.name)
           node = node.predecessor
       return sig_paso
##############################3
#llamamos la funcion de arriba para darle todos los valores a los arreglos tablas y grid
build_grid(0, 0, 40)
#creamos nodos vacios
arrayNodes = [None]*81
for i in range(81):
    arrayNodes[i] = Node(i)
###############
#creamos aristas con los nodos cercanos como arriba, abajo, izquierda y derecha
for i in range(81):
    if i >= 1 and i <= 7:                                                 # 3 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
    elif i >= 73 and i <= 79:                                             # 3 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        
    elif i >= 9 and i <= 63 and i % 9 == 0:                               # 3 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
    elif i >= 17 and i <= 71 and (i + 1) % 9 == 0:                        # 3 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
    elif i != 0 and i != 8 and i != 72 and i != 80:                       # 4 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
    elif i == 0:                                                          # 2 aristas
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
    elif i == 8:
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
    elif i == 72:
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i+1]))
    elif i == 80:
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-9]))
        arrayNodes[i].adjacenciesList.append(Edge(1,arrayNodes[i],arrayNodes[i-1]))
        
#usamos para actualizar vaciando estos valores y poder segir usando esta funcion "calculateshortestpath()"
def update():
    for i in range(81):
        arrayNodes[i].predecessor = None
        arrayNodes[i].mindistance = sys.maxsize

def movbot1(x2_y2,x3_y3,turno,www,cant_tabla_bot):
    ###################
    ##################hallo la distancia minima del bot de arriba mediante esta funcion

    #x2_y2:jugador
    #x3_y3:bot
    ##########3
    relac_x_y_bot_x2_y2=False
    for j in range(len(arrayNodes[x2_y2].adjacenciesList)):
        if arrayNodes[x2_y2].adjacenciesList[j].endvertex.name == x3_y3:
            relac_x_y_bot_x2_y2=True
    ######################
    bloque_ariba,bloque_abajo,bloque_izquierda,bloque_derecha=True,True,True,True

    for p in range(len(arrayNodes[x2_y2].adjacenciesList)):
        if arrayNodes[x2_y2].adjacenciesList[p].endvertex.name == x2_y2-9:
            bloque_ariba=False
        if arrayNodes[x2_y2].adjacenciesList[p].endvertex.name == x2_y2+9:
            bloque_abajo=False
        if arrayNodes[x2_y2].adjacenciesList[p].endvertex.name == x2_y2-1:
            bloque_izquierda=False
        if arrayNodes[x2_y2].adjacenciesList[p].endvertex.name == x2_y2+1:
            bloque_derecha=False
    ######################
    caso_doble_salto=None
    caso_diagonal=None
    #3
    if(relac_x_y_bot_x2_y2==True):
        #intentar hacer solo un camino
       if(x3_y3-9==x2_y2 and bloque_ariba==False):
           arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3-18]))
           arrayNodes[x3_y3-18].adjacenciesList.append(Edge(1,arrayNodes[x3_y3-18],arrayNodes[x3_y3]))
           caso_doble_salto="arriba"

       elif(x3_y3+9==x2_y2 and bloque_abajo==False):
           arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3+18]))
           arrayNodes[x3_y3+18].adjacenciesList.append(Edge(1,arrayNodes[x3_y3+18],arrayNodes[x3_y3]))
           caso_doble_salto="abajo"

       elif(x3_y3-1==x2_y2 and x2_y2%9!=0 and x3_y3%9!=0 and bloque_izquierda==False):
           arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3-2]))
           arrayNodes[x3_y3-2].adjacenciesList.append(Edge(1,arrayNodes[x3_y3-2],arrayNodes[x3_y3]))
           caso_doble_salto="izquierda"

       elif(x3_y3+1==x2_y2 and (x2_y2+1)%9!=0 and (x3_y3+1)%9!=0 and bloque_derecha==False):
           arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3+2]))
           arrayNodes[x3_y3+2].adjacenciesList.append(Edge(1,arrayNodes[x3_y3+2],arrayNodes[x3_y3]))
           caso_doble_salto="derecha"
       ################################3
       
       if (caso_doble_salto==None):
           if(x3_y3-9==x2_y2 and bloque_ariba==True):
               if(bloque_izquierda==False and x3_y3%9!=0):
                   arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3-10]))
                   arrayNodes[x3_y3-10].adjacenciesList.append(Edge(1,arrayNodes[x3_y3-10],arrayNodes[x3_y3]))
                   caso_diagonal="ar-iz"
               if(bloque_derecha==False and (x3_y3+1)%9!=0):
                   arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3-8]))
                   arrayNodes[x3_y3-8].adjacenciesList.append(Edge(1,arrayNodes[x3_y3-8],arrayNodes[x3_y3]))
                   caso_diagonal="ar-de"

           elif(x3_y3+9==x2_y2 and bloque_abajo==True):
               if(bloque_izquierda==False and x3_y3%9!=0):
                   arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3+8]))
                   arrayNodes[x3_y3+8].adjacenciesList.append(Edge(1,arrayNodes[x3_y3+8],arrayNodes[x3_y3]))
                   caso_diagonal="ab-iz"
               if(bloque_derecha==False and (x3_y3+1)%9!=0):
                   arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3+10]))
                   arrayNodes[x3_y3+10].adjacenciesList.append(Edge(1,arrayNodes[x3_y3+10],arrayNodes[x3_y3]))
                   caso_diagonal="ab-de"

           elif(x3_y3-1==x2_y2 and x2_y2%9!=0 and x3_y3%9!=0 and bloque_izquierda==True):
               if(bloque_ariba==False):
                   arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3-10]))
                   arrayNodes[x3_y3-10].adjacenciesList.append(Edge(1,arrayNodes[x3_y3-10],arrayNodes[x3_y3]))
                   caso_diagonal="ar-iz"
               if(bloque_abajo==False):
                   arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3+8]))
                   arrayNodes[x3_y3+8].adjacenciesList.append(Edge(1,arrayNodes[x3_y3+8],arrayNodes[x3_y3]))
                   caso_diagonal="ab-iz"

           elif(x3_y3+1==x2_y2 and (x2_y2+1)%9!=0 and (x3_y3+1)%9!=0 and bloque_derecha==True):
              if(bloque_ariba==False):
                  arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3-8]))
                  arrayNodes[x3_y3-8].adjacenciesList.append(Edge(1,arrayNodes[x3_y3-8],arrayNodes[x3_y3]))
                  caso_diagonal="ar-de"
              if(bloque_abajo==False):
                  arrayNodes[x3_y3].adjacenciesList.append(Edge(1,arrayNodes[x3_y3],arrayNodes[x3_y3+10]))
                  arrayNodes[x3_y3+10].adjacenciesList.append(Edge(1,arrayNodes[x3_y3+10],arrayNodes[x3_y3]))
                  caso_diagonal="ab-de"
    ####################################################################################
    ####################################################################################
    def calcular_distancia_minima_abajo(x_y):
        calculateshortestpath(arrayNodes[72])   
        a_min=arrayNodes[x_y].mindistance
        x_y_aux_min=72
        for i in range(73,81):
            update()
            calculateshortestpath(arrayNodes[i])
            if(a_min>=arrayNodes[x_y].mindistance):
                a_min=arrayNodes[x_y].mindistance
                x_y_aux_min=i
            update()
        return x_y_aux_min,a_min
     ###################
    ##################hallo la distancia minima del jugador de abajo mediante esta funcion
    def calcular_distancia_minima_arriba(x_y):
        calculateshortestpath(arrayNodes[0])   
        a_min=arrayNodes[x_y].mindistance
        x_y_aux_min=0
        for i in range(1,9):
            update()
            calculateshortestpath(arrayNodes[i])
            if(a_min>=arrayNodes[x_y].mindistance):
                a_min=arrayNodes[x_y].mindistance
                x_y_aux_min=i
            update()
        return x_y_aux_min,a_min

    #aplico las funciones
    x_y_aux_min,a_min=calcular_distancia_minima_abajo(x3_y3)
    _,dis_minjugador=calcular_distancia_minima_arriba(x2_y2)

    #imprimo sus distancias minimas y todo esto aplicando dijkstra
    print("\nLa distancia minima del jugador es:"+str(dis_minjugador))
    print("La distancia minima del bot es:"+str(a_min))

    ###################3
    ###################si la distancia minima del jugador es menor al del bot, el bot va a poner barreras
    if(dis_minjugador<a_min and cant_tabla_bot>0 and www==True):

        #creo dos arreglos que me diran todos los lugares posibles donde el bot puede poner barreras
        print("\nVa a poner una barrera")
        arrrrrrrrr_h=[0]*64
        arrrrrrrrr_v=[0]*64
        for i in range(64):
            if tablas_h_p[i]!=None:
                arrrrrrrrr_h[i]=1
                arrrrrrrrr_v[i]=1
                if(obtener_tabla_a_nodo(i)%9!=0):
                    arrrrrrrrr_h[i-1]=1
                if(obtener_tabla_a_nodo(i)+2%9!=0):
                    arrrrrrrrr_h[i+1]=1
            if tablas_v_p[i]!=None:
                arrrrrrrrr_h[i]=1
                arrrrrrrrr_v[i]=1
                if(i>=8):
                    arrrrrrrrr_v[i-8]=1
                if(i<=55):
                    arrrrrrrrr_v[i+8]=1
        ###
        #
        dis_max_para_barre=dis_minjugador       #esta distancia cambiara y buscara la distancia maxima del jugador asta su final ocasiona mediante una barrera
        posicion_barr=None
        direscc=None
        ###

        ##########
        ########## recorro todos los posibles lugares donde el bot pueda poner barreras
        for i in range(63,-1,-1):
            if arrrrrrrrr_h[i]==0:
                #aca veo si el bot encierra o no al jugador o a el mismo y tambien pone una barrera
                encerrado=encerrado_por_tabla(x2_y2,x3_y3,i,'h')
                #en caso que no encierre:
                if encerrado==False:
                    #hallo su distancia minima del jugador mediante de haber puesto una barrera
                    _,dis_minjugador_nuevo=calcular_distancia_minima_arriba(x2_y2)
                    
                    #si una barrera hace que el jugador se demore mas en llegar a la meta reemplaza los valores 
                    if(dis_max_para_barre<dis_minjugador_nuevo):
                        dis_max_para_barre=dis_minjugador_nuevo
                        posicion_barr=i
                        direscc='horizontal'
                        break
                #en caso que esa barrera no hace que el jugador se demore mas, lo elimina la barrera
                arreglar_pared_hori(i)
            ##############
            ##############3 lo mismo pero en vertical
            if arrrrrrrrr_v[i]==0:
                encerrado=encerrado_por_tabla(x2_y2,x3_y3,i,'v')

                if encerrado==False:
                    _,dis_minjugador_nuevo=calcular_distancia_minima_arriba(x2_y2)
                    
                    if(dis_max_para_barre<dis_minjugador_nuevo):
                        dis_max_para_barre=dis_minjugador_nuevo
                        posicion_barr=i
                        direscc='vertical'
                        break
                arreglar_pared_verti(i)
        
        
        ####pone la barrera
        if direscc=='horizontal':

            tablas_h_p[posicion_barr]=tablas_h[posicion_barr]
            romper_aristas_tabla_hori(posicion_barr)
            ####aca solo imprimo que barrera se puso:direccion y su posicion entre 0 a 63
            print("\nSe puso una barrera horizontal en la posicion "+str(posicion_barr))
            cant_tabla_bot-=1
        elif direscc=='vertical':

            tablas_v_p[posicion_barr]=tablas_v[posicion_barr]
            romper_aristas_tabla_verti(posicion_barr)
            ####aca solo imprimo que barrera se puso:direccion y su posicion entre 0 a 63
            print("\nSe puso una barrera vertical en la posicion "+str(posicion_barr))
            cant_tabla_bot-=1
        else:
            print("no encontro un buen lugar para poner pared,ahora se va a mover")
            update()
            calculateshortestpath(arrayNodes[x_y_aux_min]) 
            x3_y3=getshortestpath(arrayNodes[x3_y3])

        #####   busca si llego a la meta nomas
        for i in range(72,81):
            if(x3_y3==i):
                www=False
                break;
       
    ####3$$$$$$$$$$$
    ##################
    else:
        #####   busca si llego a la meta nomas y se mueve
        print("\nSe va a mover")
        if www==True:
            update()
            calculateshortestpath(arrayNodes[x_y_aux_min]) 
            x3_y3=getshortestpath(arrayNodes[x3_y3])
            for i in range(72,81):
                if(x3_y3==i):
                    www=False
                    break;
        
    turno=1
    ################
    ################
    if(caso_doble_salto!=None):
        arrayNodes[x3_y3].adjacenciesList.pop()
    if(caso_doble_salto=="arriba"):
        arrayNodes[x3_y3-18].adjacenciesList.pop()
    elif(caso_doble_salto=="abajo"):
        arrayNodes[x3_y3+18].adjacenciesList.pop()
    elif(caso_doble_salto=="izquierda"):
        arrayNodes[x3_y3-2].adjacenciesList.pop()
    elif(caso_doble_salto=="derecha"):
        arrayNodes[x3_y3+2].adjacenciesList.pop()
    #######
    if(caso_diagonal!=None):
        arrayNodes[x3_y3].adjacenciesList.pop()
    if(caso_diagonal=="ar-iz"):
        arrayNodes[x3_y3-10].adjacenciesList.pop()
    if(caso_diagonal=="ar-de"):
        arrayNodes[x3_y3-8].adjacenciesList.pop()
    if(caso_diagonal=="ab-iz"):
        arrayNodes[x3_y3+8].adjacenciesList.pop()
    if(caso_diagonal=="ab-de"):
        arrayNodes[x3_y3+10].adjacenciesList.pop()

    return turno,www,x3_y3,cant_tabla_bot
######################################3
######################################
##################################
#############tablas
#hacemos que mediante el x_table obtengamos la posicion del nodo que le corresponde a esa tabla
#cada nodo tiene siempre 2 tablas(horizontal y vertical) excepto la ultima fila inferior y la ultima columna de la derecha
def obtener_tabla_a_nodo(x_tabla):

    if x_tabla>=0 and x_tabla<=7:
        x_nodo=x_tabla
    elif x_tabla>=8 and x_tabla<=15:
        x_nodo=x_tabla+1
    elif x_tabla>=16 and x_tabla<=23:
        x_nodo=x_tabla+2
    elif x_tabla>=24 and x_tabla<=31:
        x_nodo=x_tabla+3
    elif x_tabla>=32 and x_tabla<=39:
        x_nodo=x_tabla+4
    elif x_tabla>=40 and x_tabla<=47:
        x_nodo=x_tabla+5
    elif x_tabla>=48 and x_tabla<=55:
        x_nodo=x_tabla+6
    elif x_tabla>=56 and x_tabla<=63:
        x_nodo=x_tabla+7
    return x_nodo

#hacemos que al tener la coordenada de la tabla_horizontal rompa la arista con los nodos que le corresponda eliminar 
#ej:28 29   ->elimna la conexion del nodo 28 con 37 y el 29 con 38
#   37 38
def romper_aristas_tabla_hori(x_tabla):
    
    x_nodo=obtener_tabla_a_nodo(x_tabla)

    for i in range(len(arrayNodes[x_nodo].adjacenciesList)):
        if arrayNodes[x_nodo].adjacenciesList[i].endvertex.name == x_nodo+9:
            arrayNodes[x_nodo].adjacenciesList.pop(i)
            break
    for i in range(len(arrayNodes[x_nodo+9].adjacenciesList)):
        if arrayNodes[x_nodo+9].adjacenciesList[i].endvertex.name == x_nodo:
            arrayNodes[x_nodo+9].adjacenciesList.pop(i)
            break
        
    for i in range(len(arrayNodes[x_nodo+1].adjacenciesList)):
        if arrayNodes[x_nodo+1].adjacenciesList[i].endvertex.name == x_nodo+10:
            arrayNodes[x_nodo+1].adjacenciesList.pop(i)
            break
    for i in range(len(arrayNodes[x_nodo+10].adjacenciesList)):
        if arrayNodes[x_nodo+10].adjacenciesList[i].endvertex.name == x_nodo+1:
            arrayNodes[x_nodo+10].adjacenciesList.pop(i)
            break

#hacemos que al tener la coordenada de la tabla_vertical rompa la arista con los nodos que le corresponda eliminar 
#ej:28 29   ->elimna la conexion del nodo 28 con 29 y el 37 con 38
#   37 38
def romper_aristas_tabla_verti(x_tabla):

    x_nodo=obtener_tabla_a_nodo(x_tabla)

    for i in range(len(arrayNodes[x_nodo].adjacenciesList)):
        if arrayNodes[x_nodo].adjacenciesList[i].endvertex.name == x_nodo+1:
            arrayNodes[x_nodo].adjacenciesList.pop(i)
            break
    for i in range(len(arrayNodes[x_nodo+1].adjacenciesList)):
        if arrayNodes[x_nodo+1].adjacenciesList[i].endvertex.name == x_nodo:
            arrayNodes[x_nodo+1].adjacenciesList.pop(i)
            break
        
    for i in range(len(arrayNodes[x_nodo+9].adjacenciesList)):
        if arrayNodes[x_nodo+9].adjacenciesList[i].endvertex.name == x_nodo+10:
            arrayNodes[x_nodo+9].adjacenciesList.pop(i)
            break
    for i in range(len(arrayNodes[x_nodo+10].adjacenciesList)):
        if arrayNodes[x_nodo+10].adjacenciesList[i].endvertex.name == x_nodo+9:
            arrayNodes[x_nodo+10].adjacenciesList.pop(i)
            break

def dibujar_tablas_general(tablas_h_p,tablas_v_p):
    for i in range(64):
        if tablas_h_p[i]!=None:
            pygame.draw.rect(screen, YELLOW, tablas_h_p[i], 0)
        if tablas_v_p[i]!=None:
            pygame.draw.rect(screen, YELLOW, tablas_v_p[i], 0)

#arregla las aristas que elimino antes tan solo lo uso para ver que no se le puede encerrar al bot
def arreglar_pared_hori(x_tabla):
    
    x_nodo=obtener_tabla_a_nodo(x_tabla)

    arrayNodes[x_nodo].adjacenciesList.append(Edge(1,arrayNodes[x_nodo],arrayNodes[x_nodo+9]))
    arrayNodes[x_nodo+1].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+1],arrayNodes[x_nodo+10]))
    arrayNodes[x_nodo+9].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+9],arrayNodes[x_nodo]))
    arrayNodes[x_nodo+10].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+10],arrayNodes[x_nodo+1]))

#arregla las aristas que elimino antes tan solo lo uso para ver que no se le puede encerrar al bot
def arreglar_pared_verti(x_tabla):
    
    x_nodo=obtener_tabla_a_nodo(x_tabla)

    arrayNodes[x_nodo].adjacenciesList.append(Edge(1,arrayNodes[x_nodo],arrayNodes[x_nodo+1]))
    arrayNodes[x_nodo+1].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+1],arrayNodes[x_nodo]))
    arrayNodes[x_nodo+9].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+9],arrayNodes[x_nodo+10]))
    arrayNodes[x_nodo+10].adjacenciesList.append(Edge(1,arrayNodes[x_nodo+10],arrayNodes[x_nodo+9]))
####################
####################
#####################
def confirmar_movimiento(x2_y2,x_y_bot,movimiento,relac_x_y_bot_x2_y2,sig_pos,bloque_ariba,bloque_abajo,bloque_izquierda,bloque_derecha):

    for j in range(len(arrayNodes[x2_y2].adjacenciesList)):
        if arrayNodes[x2_y2].adjacenciesList[j].endvertex.name == x_y_bot:
            relac_x_y_bot_x2_y2=True

    #calculamos por separado que recorrado todas las arista y busca si existe conexion con sus nodos cercanos
    for p in range(len(arrayNodes[x_y_bot].adjacenciesList)):
        if arrayNodes[x_y_bot].adjacenciesList[p].endvertex.name == x_y_bot-9:
            bloque_ariba=False
        if arrayNodes[x_y_bot].adjacenciesList[p].endvertex.name == x_y_bot+9:
            bloque_abajo=False
        if arrayNodes[x_y_bot].adjacenciesList[p].endvertex.name == x_y_bot-1:
            bloque_izquierda=False
        if arrayNodes[x_y_bot].adjacenciesList[p].endvertex.name == x_y_bot+1:
            bloque_derecha=False

    #recorremos todas la aristas de la posicion del bot para ver si puede realizar un doble salto, o salto en diagonal
    #cuando esta alcostado del bot
    for i in range(len(arrayNodes[x_y_bot].adjacenciesList)):

        if relac_x_y_bot_x2_y2==True and  arrayNodes[x_y_bot].adjacenciesList[i].endvertex.name ==sig_pos:

            #revisamos si puede realizar el doble salto
            if(x2_y2==sig_pos+18):
                movimiento=True
                break
            if(x2_y2==sig_pos-18):
                movimiento=True
                break
            if(x2_y2==sig_pos-2):
                movimiento=True
                break
            if(x2_y2==sig_pos+2):
                movimiento=True
                break

            #revisamos si hay un bloque que impida el doble salto y que se pueda ir en diagonal del jugador
            if((sig_pos+1==x_y_bot or sig_pos-1==x_y_bot) and (bloque_ariba==True) and (x2_y2-9==x_y_bot)):
                movimiento=True
                break
            if((sig_pos+1==x_y_bot or sig_pos-1==x_y_bot) and (bloque_abajo==True) and (x2_y2+9==x_y_bot)):
                movimiento=True
                break
            if((sig_pos+9==x_y_bot or sig_pos-9==x_y_bot)  and (bloque_izquierda==True) and (x2_y2-1==x_y_bot)):
                movimiento=True
                break
            if((sig_pos+9==x_y_bot or sig_pos-9==x_y_bot)  and (bloque_derecha==True) and (x2_y2+1==x_y_bot)):
                movimiento=True
                break

    #recorro otra vez las arista del x2_y2 si puede moverse para arriba, abajo, izquierda, derecha
    for l in range(len(arrayNodes[x2_y2].adjacenciesList)):

        if arrayNodes[x2_y2].adjacenciesList[l].endvertex.name == sig_pos and arrayNodes[x2_y2].adjacenciesList[l].endvertex.name != x_y_bot:
            movimiento=True
            break
    return movimiento



#aca se crea el movimiento del jugador 
def mov_jugador(x,y,x2_y2,x3_y3,turno):

    encontro=False
    movimiento=False

    #mediante el click del mouse sacamos la coordenada del nodo que le corresponde si existe en dicho caso
    for i in range(81):
        if x>=grid[i][0] and x<=grid[i][0]+40 and y>=grid[i][1] and y<=grid[i][1]+40:
            sig_pos=i       #es la coordenada del nodo mediante el mouse click
            encontro=True   #encuentra la posicion del nodo que le corresponde
            break

    #primero creo un if que en caso si encontro el nodo que le corresponde al click
    if encontro==True:
        #calculamos si o no existe una arista que conecte al nodo del jugador y el bot
        movimiento=confirmar_movimiento(x2_y2,x3_y3,movimiento,False,sig_pos,True,True,True,True)
    #y si se puede mover se va a la posicion del nodo donde se dio click y acabo el turno del jugador
    if(movimiento==True):
        x2_y2 = sig_pos
        turno=2

    return x2_y2,turno

#busca si cuando pones tabla encierras al jugador o bot
def encerrado_por_tabla(x2_y2,x3_y3,i,tipo):
    if(tipo=='h'):
        romper_aristas_tabla_hori(i)
    elif(tipo=='v'):
        romper_aristas_tabla_verti(i)
    update()
    calculateshortestpath(arrayNodes[72])
    a_min_bot2=arrayNodes[x3_y3].mindistance
    update()
    calculateshortestpath(arrayNodes[0])
    a_min_jug=arrayNodes[x2_y2].mindistance
    update()
    # a_min>=1000 si pasa esto es que el bot no pudo encontrar ni un solo camino a la vez que impide poner una pared ahi
    if(a_min_jug>=1000 or a_min_bot2>=1000):
        encerrado=True
    else:
        encerrado=False
    return encerrado

#hace que se pueda poner tabla o no
def poner_tablas_jugador(x,y,turno,x2_y2,x3_y3,cant_tabla_jugador):

    encerrado=False
    ###
    arrrrrrrrr_h=[0]*64
    arrrrrrrrr_v=[0]*64
    for i in range(64):
        if tablas_h_p[i]!=None:
            arrrrrrrrr_h[i]=1
            arrrrrrrrr_v[i]=1
            if(obtener_tabla_a_nodo(i)%9!=0):
                arrrrrrrrr_h[i-1]=1
            if(obtener_tabla_a_nodo(i)+2%9!=0):
                arrrrrrrrr_h[i+1]=1
        if tablas_v_p[i]!=None:
            arrrrrrrrr_h[i]=1
            arrrrrrrrr_v[i]=1
            if(i>=8):
                arrrrrrrrr_v[i-8]=1
            if(i<=55):
                arrrrrrrrr_v[i+8]=1
    ####
    for i in range(64):

        #uso in if que para poner la tabla horizontal que debe cumplir que no puede encerrar al bot y saca la posicion del click para poner tabla
        if x>=tablas_h[i].x and x<=tablas_h[i].x+40 and y>=tablas_h[i].y and y<=tablas_h[i].y+20 and arrrrrrrrr_h[i]==0:
           
             encerrado=encerrado_por_tabla(x2_y2,x3_y3,i,'h')

             if(encerrado==False):
                 tablas_h_p[i]=tablas_h[i]
                 turno=2
                 cant_tabla_jugador-=1
                 print("fasafas",i)
                 ###
             else:
                 arreglar_pared_hori(i)
             break

        #casi lo mismo que el horizontal pero en vertical
        if x>=tablas_v[i].x and x<=tablas_v[i].x+20 and y>=tablas_v[i].y and y<=tablas_v[i].y+40 and arrrrrrrrr_v[i]==0:
            
            encerrado=encerrado_por_tabla(x2_y2,x3_y3,i,'v')

            if(encerrado==False):
                tablas_v_p[i]=tablas_v[i]
                turno=2
                cant_tabla_jugador-=1
                print("fasafas",i)
                #####
            else:
                arreglar_pared_verti(i)
            break

    return turno,cant_tabla_jugador

 ###############################
 ###############################


x3_y3=4         #nodo inicio del bot arriba
x2_y2=76        #nodo incio del jugador abajo
www=True        #cuando alguien llega al final acaba la partida
turno=1
cant_tabla_jugador=10       #cantidad de tablas maximas que puede poner el jugador
cant_tabla_bot=10
miFuente=pygame.font.Font(None,25)

while (True):
    #dibujo la tabla y los circulo de los jugadores
    pygame.draw.rect(screen, BLUE, (60, 40, 560, 560), 0)
    build_grid(40, 0, 40)  
    pygame. draw. circle(screen, RED, (grid[x2_y2][0]+20, grid[x2_y2][1]+20), 10, 0)
    pygame. draw. circle(screen, MAGNETA, (grid[x3_y3][0]+20, grid[x3_y3][1]+20), 10, 0)
    dibujar_tablas_general(tablas_h_p,tablas_v_p)

    #turno jugador
    if(www==True):
        if turno==1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    x2_y2,turno=mov_jugador(x,y,x2_y2,x3_y3,turno)
                    if(cant_tabla_jugador>0):
                        turno,cant_tabla_jugador=poner_tablas_jugador(x,y,turno,x2_y2,x3_y3,cant_tabla_jugador)
                    for i in range(0,9):
                        if(x2_y2==i):
                            www=False
                            break;
        #turno bot
        elif turno==2:
            turno,www,x3_y3,cant_tabla_bot=movbot1(x2_y2,x3_y3,turno,www,cant_tabla_bot)
        ###
        



    #aca muestra la cantidad de tablas que le queda al jugador y la velocidad en que transcurre cada movimiento
    pygame.draw.rect(screen, (0,0,0), (0, 0, 650, 40), 0)
    Texto1=miFuente.render("Player walls: "+str(cant_tabla_jugador),5,RED)
    Texto2=miFuente.render("Bot walls: "+str(cant_tabla_bot),5,RED)
    screen.blit(Texto1,(60,10))
    screen.blit(Texto2,(500,10))
    pygame.display.update()   
    update()