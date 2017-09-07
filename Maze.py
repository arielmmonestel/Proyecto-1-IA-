from turtle import TurtleScreen, RawTurtle, TK
from random import randint
from time import *
from datetime import timedelta
import tkinter as tk
from tkinter import Text
import time

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
                if self.canvas.itemcget(rect_id, "fill") == "#5a9089" and self.last != rect_id:
                    self.canvas.itemconfigure(rect_id, fill="#334a58")
                elif self.last != rect_id:
                    self.canvas.itemconfigure(rect_id, fill="#5a9089")
                self.last = rect_id


    def on_release(self, event):
        self._dragging = False


    def dibuja(self):
        """
        Dibuja los cuadros dentro del Canvas 
        """    
        start_time = time.monotonic()
        
        for i in range (0, self.AnchoFix, self.LadoFix):
            for j in range (0, self.AltoFix, self.LadoFix):
                self.canvas.create_rectangle(i, j, i + self.LadoFix, j + self.LadoFix, fill="#5a9089")

        end_time = time.monotonic()
        self.duracionDibujoUpdate(start_time, end_time)


    def duracionDibujoUpdate(self,start_time, end_time):
        self.durationMaze = str(timedelta(seconds = end_time - start_time))[0:10]
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
        
        cumple = ((event.x - self.agente_radio >= 0) and (event.x + self.agente_radio <= int(self.AnchoFix))) \
                 and ((event.y - self.agente_radio >= 0) and (event.y + self.agente_radio <= int(self.AltoFix)))

        # Mueve el ratón.
        ## Accion que pasa si el ratón se sale del canvas.
        if cumple == False:
            self.canvas.move(self.agente, 0, 0)
            
        else:
            self.canvas.move(self.agente, event.x - self.lastx, event.y - self.lasty)
            self.lastx = event.x
            self.lasty = event.y



    def mueveMeta(self, event):
        """ Metodo de clase que hace que el ratón tenga movimiento.
            Siempre y cuando el circulo(ratón) cumpla todas las condiciones que serán descritas a continuación,
            el ratón podrá moverse. 
        """
        
        cumple = ((event.x - self.agente_radio >= 0) and (event.x + self.agente_radio <= int(self.AnchoFix))) \
                 and ((event.y - self.agente_radio >= 0) and (event.y + self.agente_radio <= int(self.AltoFix)))

        # Mueve el ratón.
        ## Accion que pasa si el ratón se sale del canvas.
        if cumple == False:
            self.canvas.move(self.meta, 0, 0)

        else:
            self.canvas.move(self.meta, event.x - self.lastxM, event.y - self.lastyM)
            self.lastxM = event.x
            self.lastyM = event.y


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
        self.meta = self.canvas.create_oval(self.esquinas(self.meta_x, self.meta_y), fill="#ffbf6b")
        self.agente = self.canvas.create_oval(self.esquinas(self.agente_x, self.agente_y), fill="#d1675a")

        self.canvas.tag_bind(self.agente, "<1>", self.iniciaMovimiento)
        self.canvas.tag_bind(self.agente, "<B1-Motion>", self.mueveAgente)
        self.canvas.tag_bind(self.meta, "<1>", self.iniciaMovimientoM)
        self.canvas.tag_bind(self.meta, "<B1-Motion>", self.mueveMeta)



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
        self.last = None

        #Titulo
        titulillo = tk.Message(self.root, text = "Maze Solver Machine", font = ("Courier",20), width = 500)
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
        self.movDiagAble = tk.Checkbutton(labelframe, text="Movimiento Diagonal")
        self.movDiagAble.grid(column = 6, row = 0, padx = 8)

        ## Limpiar
        self.botonLimpia = tk.Button(labelframe, text="Limpiar Laberinto", font = "5", \
                                     activeforeground = "Blue", padx = 2, relief = "groove")
        self.botonLimpia.grid(column = 7, row = 0, padx = 8 )
        self.botonLimpia["state"] ="disabled"

        ## Boton Generar
        self.botonLeer = tk.Button(labelframe, text="Generar", font = 8, command = self.validateInt,  \
                                   activeforeground = "Blue", padx = 2, relief = "groove")
        self.botonLeer.grid(column = 8, row = 0, padx = 8, pady = 10)

        ##Mostrar Ruta
        self.rutaShow = tk.Button(labelframe, text="Mostrar Ruta", font = 8,  \
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
        

###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################


    ## COLOR RECORRDIDO #EDF2F4 #D7EDF0 #D6CBE1 #AFB7D2 #978FB0
 
    def recorrido(self, i, j):
        """ Dado un laberinto en donde se ubica una meta,
            retorna en una lista de pares ordenados (x,y)
            que indican el camino desde una posición inicial
            (i,j) hasta la posición en que se encuentra el
            queso.
            Entradas:
                 (i, j) : posición inicial a partir de donde
                          se realizará la búsqueda de un camino
                          hasta la posición del queso.
            Salidas:
                 Lista con las casillas, expresadas como pares
                 ordenados, que llevan desde la posición inicial
                 hasta la posición en que se encuentra el queso.
                 Si no existe un camino retorna la lista vacía.
        """
 
        if self.laberinto[i][j] == 3:
            return [(i, j)]
 
        if self.laberinto[i][j] == 1:
            return []
 
        self.laberinto[i][j] = -1
 
        sleep(0.01)
        self.lienzo.fondo_ventana.tracer(False)
        self.casilla("cyan", i, j)
        self.lienzo.fondo_ventana.tracer(True)
 
        if i > 0 and self.laberinto[i - 1][j] in [0, 3]:     # Norte
            camino = self.recorrido(i - 1, j)
            if camino: return [(i, j)] + camino
 
        if j < len(self.laberinto[i]) - 1 and \
           self.laberinto[i][j + 1] in [0, 3]:               # Este
            camino = self.recorrido(i, j + 1)
            if camino: return [(i, j)] + camino
 
        if i < len(self.laberinto) - 1 and \
           self.laberinto[i + 1][j] in [0, 3]:               # Sur
            camino = self.recorrido(i + 1, j)
            if camino: return [(i, j)] + camino
 
        if j > 0 and self.laberinto[i][j - 1] in [0, 3]:     # Oeste
            camino = self.recorrido(i, j - 1) 
            if camino: return [(i, j)] + camino


        #SuroEste
        #NoroEste
        #NorEste
        #SurEste
        #http://www.redblobgames.com/pathfinding/a-star/implementation.html

        sleep(0.10)
        self.lienzo.fondo_ventana.tracer(False)
        self.casilla("black", i, j)
        self.lienzo.fondo_ventana.tracer(True)
 
        return []


 
def principal():

    l1 = Maze()

if __name__ == "__main__":
    principal()
