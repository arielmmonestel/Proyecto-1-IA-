from turtle import TurtleScreen, RawTurtle, TK
from random import randint
from time import *
from datetime import timedelta
import tkinter as tk
from tkinter import Text
import time

class Maze():

    def on_double(self,event):
        items = self.canvas.find_closest(event.x, event.y)
        if items:
            rect_id = items[0]
            self.canvas.itemconfigure(rect_id, fill="green")

        

    def on_clickR(self, event):
        """
        Encargado de los movimiento del Mouse
        """    
        self._dragging = True
        self.on_move(event)


    def on_clickL(self, event):
        items = self.canvas.find_closest(event.x, event.y)
        if items:
            rect_id = items[0]
            self.canvas.itemconfigure(rect_id, fill="pink")
    


    def on_move(self, event):
        if self._dragging:
            items = self.canvas.find_closest(event.x, event.y)
            if items:
                rect_id = items[0]
                if self.canvas.itemcget(rect_id, "fill") == "red":
                    self.canvas.itemconfigure(rect_id, fill="yellow")
                else:
                    self.canvas.itemconfigure(rect_id, fill="red")


    def on_release(self, event):
        self._dragging = False


    def dibuja(self):
        """
        Dibuja los cuadros dentro del Canvas 
        """    
        start_time = time.monotonic()
        for i in range (0,150,15):
            for j in range (0,150,15):
                self.canvas.create_rectangle(i, j, i+15, j+15, fill='red')
        end_time = time.monotonic()
        self.duracionDibujoUpdate(start_time, end_time)


    def duracionDibujoUpdate(self,start_time, end_time):
        self.durationMaze = str(timedelta(seconds = end_time - start_time))[0:10]
        text = "Duracion construccion : " + self.durationMaze
        self.duracionMaze.config(text=text)
        self.duracionMaze.update_idletasks()


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
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
                
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
        self.canvas.bind("<ButtonPress-3>", self.on_clickL)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Double-Button-1>", self.on_double)

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

        titulillo = tk.Message(self.root, text = "Maze Solver Machine", font = ("Courier",20), width = 500)
        titulillo.pack()

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
        self.botonLeer = tk.Button(labelframe, text="Generar", font = 8, command = self.CrearVentana,  \
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

        self._dragging = False
        
        self.root.mainloop()


##    def validateInput(self):
##        try:
##            if int(self.altext.get()) > 0 and int(self.anchtext.get()) > 0 and int(self.ladotext.get()) > 0:
##                CrearVentana()
##            else:
##                tk.messagebox.showerror("Error", "Valores deben ser mayores a 0")     
##        except:
##            tk.messagebox.showerror("Error", "Valores deben ser numericos")


    def CrearVentana(self):
        self.altext.config(state='disabled')
        self.anchtext.config(state='disabled')
        self.ladotext.config(state='disabled')
        self.botonLeer.config(state='disabled')
        self.movDiagAble.config(state='disabled')
        self.botonLimpia["state"] ="normal"
        self.rutaShow["state"] ="normal"
        
        
        if int(self.altext.get()) * int(self.ladotext.get()) + 20 < 550:
            Xdef = 550
        else:
            Xdef = int(self.altext.get()) * int(self.ladotext.get()) + 20

        if int(self.anchtext.get()) * int(self.ladotext.get()) + 20 < 1320:
            Ydef = 1320
        else:
            Ydef = int(self.anchtext.get()) * int(self.ladotext.get()) + 20
        
        self.Ventana(Xdef, Ydef)
        


###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################
###################################################################################################################################



    @staticmethod
    def deme_posicion(i, j):
        """ Retorna la posicion superior izquierda en eje x, eje y
            de un casilla i,j del laberinto.
            Entradas:
                i     : Fila del laberinto.
                j     : Columna del laberinto.
            Salidas:
                (x,y) : Posición de la esquina superior izquierda
                        en donde se encuentra la entrada (i,j)
            Supuesto:
                (i,j) es una posición válida en el laberinto.
        """
        x = self.Xdis + j * (self.Ancho + 1)
        y = self.Ydis + i * (self.Alto  + 1)
        return (x, y)
 
             
    def Laberinto(self, laberinto):
        """ Constructor para la creación de un laberinto.
            Entradas:
                 area_dibujo : TurtleScreen en donde se dibujará
                               el laberinto.
                 laberinto   : tira que contiene el diseño del
                               laberinto.
            Salidas:
                 Instancia de la clase.
                 Laberinto representado por una matriz, tal que
                 la entrada i,j contiene: 0 - si la casilla está
                 libre, 1 - si hay pared, 3 - posición en donde
                 está el queso.
            Restricciones:
                 Todas las entradas de la tira son 0, 1 o 3. Las
                 filas se representan por un cambio de línea.
                 No hay líneas vacías.
        """

        self.Xdis = int(self.ladotext.get())
        self.Ydis = int(self.ladotext.get())
     
        self.Alto = int(self.altext.get())
        self.Ancho= int(self.anchtext.get())
           
        ## Construye una lista de listas a partir de la
        ## tira que se recibe como parámetro.
        lista = laberinto.split()
        lista = [ x[:-1] if x[-1] == "\n" else x for x in lista]
        lista = [[int(ch) for ch in x] for x in lista]
 
 
        ## Crea los atributos.
        self.laberinto = lista
        self.lienzo = self.fondo_ventana
 
        ## Dibuja el laberinto.
        self.dibuja_laberinto()
 
    def dibuja_laberinto(self):
        """ Dibuja el laberinto.
        Entradas:
            Ninguna.
        Salidas:
            Dibujo del laberinto.
        """
 
        self.lienzo.fondo_ventana.tracer(False)
        self.lienzo.pencil.pencolor("white")
 
        ## Dibuja el laberinto.
 
        for i in range(len(self.laberinto)):
 
            for j in range(len(self.laberinto[i])):
 
                if self.laberinto[i][j] == 1:
                    self.casilla("yellow", i, j)
                elif self.laberinto[i][j] == 3:
                    self.casilla("red", i, j)
                elif self.laberinto[i][j] == 0:
                    self.casilla("black", i, j)
 
        self.lienzo.fondo_ventana.tracer(True)
 
    def casilla(self, color, i, j):
        """ Dibuja la casilla i, j con el color
            indicado.
        Entradas:
            color : Color de la casilla a dibujar.
            (i,j) : Ubicación de la casilla.
        Salidas:
            Dibujo de la casilla con el color indicado en
            la posición (i,j) del laberinto.
        Supuesto:
            El color es uno válido en Tkinter.
            (i,j) es una posición válida en el
            laberinto.
        """
 
        ## Determina la posición en los ejes
        ## reales de la posición (i,j) de la
        ## casilla.
        x, y = self.deme_posicion(i, j)
 
        ## Prepara el lápiz para dibujar
        ## un rectánculo relleno.
        self.lienzo.pencil.fillcolor(color)
        self.lienzo.pencil.pu()
        self.lienzo.pencil.setpos(x, y)
        self.lienzo.pencil.seth(0)
        self.lienzo.pencil.pd()
        self.lienzo.pencil.begin_fill()
 
        ## Dibuja la casilla con 4
        ## movimientos !!!
        for i in range(2):
            self.lienzo.pencil.fd(Laberinto.Ancho+1)
            self.lienzo.pencil.left(90)
            self.lienzo.pencil.fd(Laberinto.Alto+1)
            self.lienzo.pencil.left(90)
 
        ## Cierra el relleno.
        self.lienzo.pencil.end_fill()
 
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
    stringLab = "00000000000000\n" + \
            "01111111011110\n" + \
            "00000001000010\n" + \
            "01111111111110\n" + \
            "01111111111110\n" + \
            "01111111111110\n" + \
            "00000000003110"

    l1 = Maze()
    #l1.Laberinto(stringLab)
    #ll.recorrido(6,13)
    #ll.reset()
 
if __name__ == "__main__":
    principal()
