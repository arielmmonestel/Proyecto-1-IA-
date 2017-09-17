from turtle import TurtleScreen, RawTurtle, TK
from time import *
from datetime import timedelta
import tkinter as tk
from tkinter import Text
import time
from math import sqrt
import functools

def catch_exception(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(" - Se ha cerrado el programa sin finalizar el recorrido - ")
    return func


class Maze():


    def on_clickR(self, event):
        """
        Encargado de los movimiento del Mouse
        """    
        self._dragging = True
        self.on_move(event)


    def on_move(self, event):
        if self._dragging:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            
            if x < self.AnchoFix and y < self.AltoFix:
                items = self.canvas.find_closest(x,y)
            else:
                items = None

            if items:
                rect_id = items[0]
                if self.canvas.itemcget(rect_id, "fill") == "#5a9089" and self.lastBttn != rect_id:
                    self.canvas.itemconfigure(rect_id, fill="#334a58")
                elif self.canvas.itemcget(rect_id, "fill") == "#334a58" and self.lastBttn != rect_id:
                    self.canvas.itemconfigure(rect_id, fill="#5a9089")
                else:
                    pass

                self.lastBttn  = rect_id

    def on_release(self, event):
        self._dragging = False
        self.lastBttn  = None


    def dibuja(self):
        """
        Dibuja los cuadros dentro del Canvas 
        """    
        start_time = time.monotonic()

        k = 6
        for i in range (0, self.AnchoFix, self.LadoFix):
            for j in range (0, self.AltoFix, self.LadoFix):
                self.canvas.create_rectangle(i, j, i + self.LadoFix, j + self.LadoFix, fill="#5a9089", outline = "#146d60")
        
        end_time = time.monotonic()
        self.duracionDibujoUpdate(start_time, end_time)


    def Limpiar(self):
        """
        Elimina el juego
        """    
        self.root.destroy()
        l1 = Maze()


    def duracionDibujoUpdate(self,start_time, end_time):
        self.durationMaze = str(timedelta(seconds = end_time - start_time))[0:12]
        text = "Duracion construccion : " + self.durationMaze
        self.duracionMaze.config(text=text)
        self.duracionMaze.update_idletasks()
        self.ubicAgente()


    def iniciaMovimientoM(self, event):
        """ Metodo de clase que recuerda la posición de inicio del objeto a mover """
        self.lastxM = event.x
        self.lastyM = event.y
        

    def iniciaMovimiento(self, event):
        """ Metodo de clase que recuerda la posición de inicio del objeto a mover """
        self.lastx = event.x
        self.lasty = event.y


    def mueveAgente(self, event):
        """ Metodo de clase que hace que el ratón tenga movimiento.
            Siempre y cuando el circulo(ratón) cumpla todas las condiciones que serán descritas a continuación,
            el ratón podrá moverse. 
        """
        self._dragging = False
        cumple = ((event.x - self.agente_radio >= 0) and (event.x + self.agente_radio <= int(self.AnchoFix))) \
                 and ((event.y - self.agente_radio >= 0) and (event.y + self.agente_radio <= int(self.AltoFix)))

        # Mueve el ratón.
        ## Accion que pasa si el ratón se sale del canvas.
        if cumple == False:
            self.canvas.move(self.agente, 0, 0)
            
        else:
            moveX = (self.canvas.canvasx(event.x) // 20) * 20 + 10
            moveY = (self.canvas.canvasy(event.y) // 20) * 20 + 10
            self.canvas.coords(self.agente, moveX-7, moveY-7, moveX+7,  moveY+7)
            self.lastx = moveX
            self.lasty = moveY
            

    def mueveMeta(self, event):
        """ Metodo de clase que hace que el ratón tenga movimiento.
            Siempre y cuando el circulo(ratón) cumpla todas las condiciones que serán descritas a continuación,
            el ratón podrá moverse. 
        """
        self._dragging = False
        cumple = ((event.x - self.agente_radio >= 0) and (event.x + self.agente_radio <= int(self.AnchoFix))) \
                 and ((event.y - self.agente_radio >= 0) and (event.y + self.agente_radio <= int(self.AltoFix)))


        # Mueve el ratón.
        ## Accion que pasa si el ratón se sale del canvas.
        if cumple == False:
            self.canvas.move(self.meta, 0, 0)

        else:
            moveX = (self.canvas.canvasx(event.x) // 20) * 20 + 10
            moveY = (self.canvas.canvasy(event.y) // 20) * 20 + 10
            self.canvas.coords(self.meta, moveX-7, moveY-7, moveX+7,  moveY+7)
            self.lastxM = moveX
            self.lastyM = moveY


    def esquinas(self,x,y):
        '''Regresa una tupla (x1,y1,x2,y2)'''

        self.agente_radio = 7
        return x-self.agente_radio, y-self.agente_radio, \
               x+self.agente_radio, y+self.agente_radio


    def ubicAgente(self):
        self.agente_x = 10
        self.agente_y = 10
        self.meta_x = self.AnchoFix - 10
        self.meta_y = self.AltoFix - 10
        self.meta = self.canvas.create_oval(self.esquinas(self.meta_x, self.meta_y), fill="#FFD700")
        self.agente = self.canvas.create_oval(self.esquinas(self.agente_x, self.agente_y), fill="#ff6600")
        self.canvas.tag_bind(self.agente, "<1>", self.iniciaMovimiento)
        self.canvas.tag_bind(self.agente, "<B1-Motion>", self.mueveAgente)
        self.canvas.tag_bind(self.meta, "<1>", self.iniciaMovimientoM)
        self.canvas.tag_bind(self.meta, "<B1-Motion>", self.mueveMeta)


    def disableCanvas(self):
        self.canvas.tag_unbind(self.agente, "<1>")
        self.canvas.tag_unbind(self.agente, "<B1-Motion>")
        self.canvas.tag_unbind(self.meta, "<1>")
        self.canvas.tag_unbind(self.meta, "<B1-Motion>")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.Astar()


    #HEURISTICA
    def gridDistance(self, casilla, X2, Y2):
        X1 = self.canvas.coords(casilla)[0] + 7
        Y1 = self.canvas.coords(casilla)[1] + 7
        return sqrt((X2 - X1)**2 + (Y2 - Y1)**2)

    #HEURISTICA
    def gridDistanceR(self, casilla, casilla2):
        X1 = self.canvas.coords(casilla)[0] + 7
        Y1 = self.canvas.coords(casilla)[1] + 7
        X2 = self.canvas.coords(casilla2)[0] + 7
        Y2 = self.canvas.coords(casilla2)[1] + 7
        return sqrt((X2 - X1)**2 + (Y2 - Y1)**2)


        # Lista Visitados, Costo

    def getMin(self, opens, score):
        minNeighb = opens[0]
        for i in opens:
            if  score[minNeighb] > score[i]:
                minNeighb = i

        return minNeighb


    def isWall(self, ID):
        if self.canvas.itemcget(ID, "fill") == "#334a58":
            return True
        else:
            return False


    def getNeighbors(self, Min_ID):
        neighbList = []

        if Min_ID % self.AltoS != 6:
            Norte = Min_ID - 1
            if (not self.isWall(Norte)):neighbList.append(Norte)
            
    
        if Min_ID % self.AltoS != 5:
            Sur = Min_ID + 1
            if (not self.isWall(Sur)): neighbList.append(Sur)
                                
                        
        if Min_ID + self.AltoS < self.Last:
            Este = Min_ID + self.AltoS
            if (not self.isWall(Este)): neighbList.append(Este)
                                
                        
        if Min_ID - self.AltoS > 6:
            Oeste = Min_ID - self.AltoS
            if (not self.isWall(Oeste)): neighbList.append(Oeste)


        if self.DiagOn.get():

            #NOROESTE
            if Min_ID % self.AltoS != 6 and Min_ID - self.AltoS > 6 :
                Noroeste = (Min_ID - self.AltoS) - 1

                if (not self.isWall(Noroeste)):neighbList.append(Noroeste)
                        
            #NORESTE
            if Min_ID % self.AltoS != 6 and Min_ID + self.AltoS < self.Last :
                Noreste = (Min_ID + self.AltoS) - 1

                if (not self.isWall(Noreste)):neighbList.append(Noreste)
                                
            #SUROESTE
            if Min_ID % self.AltoS != 5 and Min_ID - self.AltoS > 6 :
                Suroeste = (Min_ID - self.AltoS) + 1

                if (not self.isWall(Suroeste)): neighbList.append(Suroeste)

                        
            #SURESTE
            if Min_ID % self.AltoS != 5 and Min_ID + self.AltoS < self.Last :
                Sureste = (Min_ID + self.AltoS) + 1

                if(not self.isWall(Sureste)): neighbList.append(Sureste)


        return neighbList

    @catch_exception
    def Astar(self):
        # Apagar boton de generar
        self.rutaShow["state"] ="disabled"
        
        # Variables 
        self.AltoS = int(self.altext.get())
        self.AnchoS = int(self.anchtext.get())

        # Donde esta el Agente + (Centrado) | Puro Centro
        AgX = self.canvas.coords(self.agente)[0] + 7
        AgY = self.canvas.coords(self.agente)[1] + 7

        # Donde esta la meta + (Centrado) | Puro Centro
        Mtx = self.canvas.coords(self.meta)[0] + 7
        Mty = self.canvas.coords(self.meta)[1] + 7

        # Devuelve el ID de Agente y Meta
        start = self.canvas.find_closest(AgX + 9 , AgY + 9)[0]
        goal  = self.canvas.find_closest(Mtx + 9 , Mty + 9)[0]

        # Inicializacion
        closedSet = []
        openSet = [start]
        cameFrom = {}
        gScore = {}
        gScore[start] = 0 # Costo desde Agente hasta Agente
        fScore = {} # Costos estimados de ruta desde Agente
        Found = False
        Last = start
        self.Last = (self.AnchoS * self.AltoS) + 5

        fScore[start] = gScore[start] + self.gridDistance(start, Mtx, Mty)

        if(self.isWall(start)):
            self.noPathFound()

        else:

            # Mientras existan para Visitar
            start_time = time.monotonic()
            while openSet:
                current = self.getMin(openSet, fScore)

                if self.DiagOn.get() and current + self.AltoS + 1 == goal or current + self.AltoS - 1 == goal or \
                   current - self.AltoS - 1 == goal or current - self.AltoS + 1 == goal:
                    end_time = time.monotonic()
                    cameFrom[goal] = current
                    Last = current
                    self.duracionResolucion(start_time, end_time)
                    Found = True
                    break
                   

                if current + 1 == goal or current - 1 == goal or current + self.AltoS == goal or current - self.AltoS == goal:
                    
                    end_time = time.monotonic()
                    cameFrom[goal] = current
                    Last = current
                    self.duracionResolucion(start_time, end_time)
                    Found = True
                    break

                else:
                    openSet.remove(current)
                    closedSet.append(current)

                    for neighb in self.getNeighbors(current) :
                        if neighb in closedSet:
                            continue

                        if current + 1 == Last or current - 1 == Last or current + self.AltoS == Last or current - self.AltoS == Last:
                            tentativeGScore = gScore[current] + int(self.ladotext.get()) # Agrega la distancia del vecino Lateral
                        else:
                            tentativeGScore = gScore[current] + sqrt(2)* int(self.ladotext.get())  # Agrega la distancia del vecino Diagonal

                        if neighb not in openSet:
                            openSet.append(neighb)
                            
                        elif tentativeGScore >= gScore[neighb]:
                            continue 

                        cameFrom[neighb] = current
                        gScore[neighb] = tentativeGScore
                        fScore[neighb] = gScore[neighb] + self.gridDistanceR(neighb, goal)
                        Last = current
                        
                        
            if not Found: self.noPathFound()
            else:
                Camino = self.reconstructPath(cameFrom, current)
                Camino.insert(len(Camino),goal)
                self.dibujaPath(Camino)
            

    def reconstructPath(self, cameFrom, current):
        totalPath = [current]
        while current in cameFrom.keys():
            current = cameFrom[current]
            totalPath.append(current)

        # get the reverse array...
        return totalPath[::-1]
    
    @catch_exception
    def dibujaPath(self, lista):
        for i in lista:
            self.canvas.itemconfigure(i, fill="#6ad8ca")
            self.canvas.delete(self.agente)
            X = self.canvas.coords(i)[0] + 10
            Y = self.canvas.coords(i)[1] + 10
            self.agente = self.canvas.create_oval(self.esquinas(X,Y), fill="#ff6600")
            self.canvas.update()
            time.sleep(0.08)
        self.PathFound()
            

    def duracionResolucion(self, start_time, end_time):
        self.durationVoyage = str(timedelta(seconds = end_time - start_time))[0:12]
        text = "Duracion recorrido : " + self.durationVoyage
        self.duracionVoyage.config(text=text)
        self.duracionVoyage.update_idletasks()
        

    def noPathFound(self):
        tk.messagebox.showerror("No Path", "No hay ruta hacia el destino")
        

    def PathFound(self):
        tk.messagebox.showerror("Listo", "Has llegado al destino")
            

    def Ventana(self, alto, ancho):
        """ Crea una ventana para dibujar el laberinto.
            Entradas:
                titulo : título de la ventana.
                alto   : alto de la ventana en pixeles.
                ancho  : ancho de la ventna en pixeles.
            Salidas:
                Ninguna.
            Restricciones:
                Alto y ancho son enteros positivos.
        """
        assert isinstance(alto, int) and alto > 0
        assert isinstance(ancho, int) and ancho > 0

        #SCROLLBAR
        yscrollbar = tk.Scrollbar(self.root)
        xscrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)

        #CANVAS
        self.canvas = TK.Canvas(self.root, width=ancho, height=alto, yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

        #Scrollbar Conf
        yscrollbar.config(command= self.canvas.yview)
        yscrollbar.pack(side =tk.RIGHT, fill=tk.Y)

        xscrollbar.config(command= self.canvas.xview)
        xscrollbar.pack(side = tk.BOTTOM, fill=tk.X)

        #FRAME
        self.frame = tk.Frame(self.canvas)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(0,0,window=self.frame, anchor='nw')

        #Updated the screen before calculating the scrollregion
        self.root.update()
        self.canvas.config(scrollregion=(0,0,alto,ancho))
                
        ## Crea un TurtleScreen y la tortuga para dibujar
        self.fondo_ventana = TurtleScreen(self.canvas)
        self.fondo_ventana.setworldcoordinates(0,-1,-1,0)
 
        ## Establece el color de fondo
        self.canvas["bg"] = "black"
        self.canvas.pack()
 
        ## Crea una tortuga para dibujar
        self.pencil = RawTurtle(self.fondo_ventana)
        self.pencil.pencolor("white")
        self.canvas.bind("<ButtonPress-1>", self.on_clickR)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.dibuja()


    def __init__(self):
        """ Crea una ventana para dibujar el laberinto.
            Entradas:
                alto   : alto de la ventana en pixeles.
                ancho  : ancho de la ventna en pixeles.
            Salidas:
                Ventana con Laberinto
            Restricciones:
                Alto y ancho son enteros positivos.
        """

        ## Crea la ventana y un canvas para dibujar
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.lastBttn = None

        #Titulo
        titulillo = tk.Message(self.root, text = "◄ ♦ ○ Maze Solver Machine ○ ♦ ►", font = ("Courier",20), width = 500)
        titulillo.pack()

        #Contenedor de Botones
        labelframe = tk.LabelFrame(self.root, text=" Parámetros ", bd = 5, font = 10)
        labelframe.pack(fill="x")

        ## Alto
        self.botonLeer = tk.Button(labelframe, text="Alto", font = 8,  \
                                   activeforeground = "Blue", padx = 2, relief = "groove")
        self.botonLeer["state"] ="disabled"
        self.botonLeer.grid(column = 0, row = 0)

        self.altext = tk.Entry(labelframe, width = 10, relief = "ridge")
        self.altext.grid(column = 1, row = 0, padx = 10)

        ## Ancho
        self.botonReinicia = tk.Button(labelframe, text="Ancho", font = "5",  \
                                       activeforeground = "Blue", padx = 2, relief = "groove")
        self.botonReinicia["state"] ="disabled"
        self.botonReinicia.grid(column = 2, row = 0)

        self.anchtext = tk.Entry(labelframe, width = 10, relief = "ridge")
        self.anchtext.grid(column = 3, row = 0, padx = 8)

        ## Tamaño Cuadro
        self.botonCuadro = tk.Button(labelframe, text="Cuadro", font = "5",  \
                                     activeforeground = "Blue", padx = 2, relief = "groove")
        self.botonCuadro["state"] ="disabled"
        self.botonCuadro.grid(column = 4, row = 0)

        self.ladotext = tk.Entry(labelframe, width = 10, relief = "ridge")
        self.ladotext.grid(column = 5, row = 0, padx = 8)

        ## Diagonal
        self.DiagOn = tk.IntVar()
        self.movDiagAble = tk.Checkbutton(labelframe, text="Movimiento Diagonal", variable = self.DiagOn)
        self.movDiagAble.grid(column = 6, row = 0, padx = 8)

        ## Limpiar
        self.botonLimpia = tk.Button(labelframe, text="Limpiar Laberinto", font = "5", command = self.Limpiar, \
                                     activeforeground = "Blue", padx = 2, relief = "groove")
        self.botonLimpia.grid(column = 7, row = 0, padx = 8 )
        self.botonLimpia["state"] ="disabled"

        ## Boton Generar
        self.botonLeer = tk.Button(labelframe, text="Generar", font = 8, command = self.validateInt,  \
                                   activeforeground = "Blue", padx = 2, relief = "groove")
        self.botonLeer.grid(column = 8, row = 0, padx = 8, pady = 10)

        ##Mostrar Ruta
        self.rutaShow = tk.Button(labelframe, text="Mostrar Ruta", font = 8, command = self.disableCanvas, \
                                   activeforeground = "Blue", padx = 2, relief = "groove")
        self.rutaShow.grid(column = 9, row = 0, padx = 8, pady = 10)
        self.rutaShow["state"] ="disabled"

        ## Estadisticas
        self.durationMaze = "00:00:00.00"
        self.durationRoute = "00:00:00.00"
        self.duracionMaze = tk.Label(labelframe, text="Duracion construccion :" + self.durationMaze )
        self.duracionMaze.grid(column = 10, row = 0, padx = 8)
        self.duracionVoyage = tk.Label(labelframe, text="Duracion recorrido : " + self.durationRoute  )
        self.duracionVoyage.grid(column = 11, row = 0, padx = 8)

        ## Flag de Arrastre
        self._dragging = False
        
        self.root.mainloop()


    def validateInt(self):
        try:
            alto = int(self.altext.get())
            ancho = int(self.anchtext.get())
            lado = int(self.ladotext.get())
            
            self.validatePositive(alto,ancho,lado)
  
        except ValueError:
            tk.messagebox.showerror("Error", "Valores deben ser numericos")


    def validatePositive(self,alto,ancho,lado):
        if alto > 0 and ancho > 0 and lado > 0:
            self.ValidarConfVentana(alto,ancho,lado)

        else:
            tk.messagebox.showerror("Error", "Valores deben ser positivos")


    def ValidarConfVentana(self,alto,ancho,lado):
        #Lados del cuadro en INT
        self.LadoFix = 20
        self.AltoFix = alto * self.LadoFix
        self.AnchoFix = ancho * self.LadoFix
        self.CrearVentana()


    def CrearVentana(self):
        self.altext.config(state='disabled')
        self.anchtext.config(state='disabled')
        self.ladotext.config(state='disabled')
        self.botonLeer.config(state='disabled')
        self.movDiagAble.config(state='disabled')
        self.botonLimpia["state"] ="normal"
        self.rutaShow["state"] ="normal" 

        # Crear una ventana default si es muy pequeño el Laberinto
        # o agrandar la pantalla si es muy grande
        
        if self.AltoFix < 550:
            self.Xdef = 550
        else:
            self.Xdef = self.AltoFix

        if self.AnchoFix < 1300:
            self.Ydef = 1320
        else:
            self.Ydef = self.AnchoFix 
        
        self.Ventana(self.Xdef, self.Ydef)
 
 
def principal():

    l1 = Maze()

if __name__ == "__main__":
    principal()
