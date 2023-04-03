from tkinter import Tk, Canvas, LabelFrame, Entry, Button, Checkbutton, Scale, Label, TOP, LEFT, RIGHT, IntVar
from tkinter.messagebox import showerror
from random import random
from math import sqrt
from scipy.special import binom


class Window:
    def __init__(self):
        """
        Window()

        Créé une fenêtre contenant le canevas sur lequel est dessiné le graphique et des entrées permettant de choisir le nombre de clous et le nombre de billes voulut pour l'expérience.

        Attributs:

        __button
        __button_isanim
        __canvas_anim
        __canvas_graph
        __c_height
        __c_width
        __entry_marbles
        __entry_nails
        __entry_probleft
        __fps
        __frame_canvas
        __frame_marbles
        __frame_nails
        __frame_probleft
        __images_marbles
        __info
        __isanim
        __label_fps
        __l_simulation
        __l_theoretical
        __marbles
        __n_marbles
        __n_nails
        __prob_left
        __window

        Méthodes:

        __animation(self, n)
            Joue une frame de l'animation

        __display_anim(self)
            Affiche l'écran de l'animation

        __display_graph(self)
            Affiche la liste des résultats expérimentaux et des résultats théoriques sous forme d'un diagramme en bâtons

        __display_info(self, event)
            Affiche les informations d'une colonne du graphique

        __experience(self)
            Simule l'expérience de la planche de Galton

        __init_animation(self)
            Initialise l'animation

        __margin_error(self, l1, l2)
            Calcule la marge d'erreur entre deux listes entrées

        __set_label_fps(self, event)
            Défini le texte du label correspondant au délai entre chaque frame de l'animation

        __simulate(self, n_nails, n_marbles, prob_left)
            Retourne une liste contenant les résultats expérimentaux de l'expérience de la planche de Galton

        __theoretical(self, n_nails, n_marbles, prob_left)
            Retourne une liste contenant les résultats théoriques de l'expérience de la planche de Galton
        """
        self.__window = Tk()
        self.__window.title("Planche de Galton")
        self.__window.resizable(width=True, height=True)

        self.__c_width = self.__window.winfo_screenwidth()-4
        self.__c_height = self.__window.winfo_screenheight()-160
        self.__a_width = 0
        self.__a_height = self.__c_height
        self.__n_nails = 10
        self.__n_marbles = 100
        self.__prob_left = 0.5
        self.__l_simulation = []
        self.__l_theoretical = []
        self.__marbles = []
        self.__images_marbles = []
        self.__info = []

        self.__frame_canvas = LabelFrame(self.__window, borderwidth=0)
        self.__frame_canvas.pack(side=TOP, anchor="w", padx=0, pady=0, fill="x")
        self.__canvas_graph = Canvas(self.__frame_canvas, width=self.__c_width, height=self.__c_height, bg="white")
        self.__canvas_graph.pack(side=LEFT, padx=0, pady=0)
        self.__canvas_graph.bind("<Motion>", self.__display_info)
        self.__canvas_anim = Canvas(self.__frame_canvas, width=self.__a_width, height=self.__a_height, bg="green")
        self.__canvas_anim.pack(side=RIGHT, padx=0, pady=0)

        self.__frame_nails = LabelFrame(self.__window, borderwidth=0)
        self.__frame_nails.pack(side=TOP, anchor="w", padx=0, pady=0, fill="x")
        Label(self.__frame_nails, text="Nombre de clous : ").pack(side=LEFT, padx=0, pady=0)
        self.__entry_nails = Entry(self.__frame_nails, width=10)
        self.__entry_nails.insert(0, str(self.__n_nails))
        self.__entry_nails.pack(side=LEFT, padx=0, pady=0)

        self.__frame_marbles = LabelFrame(self.__window, borderwidth=0)
        self.__frame_marbles.pack(side=TOP, anchor="w", padx=0, pady=0, fill="x")
        Label(self.__frame_marbles, text="Nombre de billes : ").pack(side=LEFT, padx=0, pady=0)
        self.__entry_marbles = Entry(self.__frame_marbles, width=10)
        self.__entry_marbles.insert(0, str(self.__n_marbles))
        self.__entry_marbles.pack(side=LEFT, padx=0, pady=0)

        self.__frame_probleft = LabelFrame(self.__window, borderwidth=0)
        self.__frame_probleft.pack(side=TOP, anchor="w", padx=0, pady=0, fill="x")
        Label(self.__frame_probleft, text="Probabilité qu'une bille aille à gauche : ").pack(side=LEFT, padx=0, pady=0)
        self.__entry_probleft = Entry(self.__frame_probleft, width=10)
        self.__entry_probleft.insert(0, "0.5")
        self.__entry_probleft.pack(side=LEFT, padx=0, pady=0)

        Label(self.__frame_nails, text="Résultats expérimentaux", fg="red").pack(side=RIGHT, padx=0, pady=0)
        Label(self.__frame_nails, text=" | ").pack(side=RIGHT, padx=0, pady=0)
        Label(self.__frame_nails, text="Résultats théoriques", fg="blue").pack(side=RIGHT, padx=0, pady=0)
        self.__isanim = IntVar()
        self.__button_isanim = Checkbutton(self.__frame_marbles, text="Animation", offvalue=0, onvalue=1, variable=self.__isanim, command=self.__change_anim)
        self.__button_isanim.pack(side=RIGHT, padx=0, pady=0)
        self.__fps = Scale(self.__frame_probleft, orient="horizontal", showvalue=0, length=200, sliderlength=10, from_=0, to=1000, resolution=5, command=self.__set_label_fps)
        self.__fps.set(100)
        self.__fps.pack(side=RIGHT, padx=0, pady=0)
        self.__label_fps = Label(self.__frame_probleft, text="")
        self.__set_label_fps(None)
        self.__label_fps.pack(side=RIGHT, padx=0, pady=0)

        self.__button = Button(self.__window, text="Simuler", command=self.__experience)
        self.__button.pack(side=TOP, anchor="w", padx=0, pady=0)

        self.__window.mainloop()

    def __animation(self, n):
        """
        __animation(self, n)

        Joue une frame de l'animation.

        n -> Billes restantes
        """
        if n > 0 and (len(self.__marbles) == 0 or self.__marbles[-1].y > self.__a_height/2/self.__n_nails):
            self.__marbles += [Marble(self.__a_width/2, 0, self.__a_height, self.__a_width/(self.__n_nails+1)/2, self.__a_height/2/self.__n_nails, self.__prob_left, self.__a_width/(self.__n_nails+1)/2.5)]
            self.__images_marbles += [-1]
            n -= 1
        is_notend = 0
        for i in range(len(self.__marbles)):
            if self.__marbles[i] != -1:
                if self.__images_marbles[i] != -1: self.__canvas_anim.delete(self.__images_marbles[i])
                is_notend = 1
                rep = self.__marbles[i].down()
                if rep != None:
                    self.__l_simulation[rep] += 1
                    self.__display_graph()
                    self.__marbles[i] = -1
                else:
                    self.__images_marbles[i] = self.__canvas_anim.create_oval(self.__marbles[i].x-self.__a_width/(self.__n_nails+1)/5+2, self.__marbles[i].y-self.__a_width/(self.__n_nails+1)/2.5+2, self.__marbles[i].x+self.__a_width/(self.__n_nails+1)/5+2, self.__marbles[i].y+2, fill="black")
        if is_notend and self.__isanim.get():
            sleep = self.__fps.get()
            if sleep == 0: sleep = 1
            self.__canvas_anim.after(sleep, lambda x=n: self.__animation(x))

    def __change_anim(self):
        """
        __change_anim(self)

        Affiche ou supprime l'animation.
        """
        if self.__isanim.get():
            self.__a_width = self.__c_width/3
            self.__c_width *= 2/3
        else:
            self.__c_width = self.__window.winfo_screenwidth()-4
            self.__a_width = 0
        self.__canvas_graph["width"] = self.__c_width
        self.__canvas_anim["width"] = self.__a_width
        if len(self.__l_simulation) > 0: self.__display_graph()
        if self.__isanim.get(): self.__display_anim()

    def __display_anim(self):
        """
        __display_anim(self)

        Affiche l'écran de l'animation.
        """
        self.__canvas_anim.delete("all")
        self.__canvas_anim.create_polygon(2, self.__a_height/2+2, (self.__a_width-self.__a_width/(self.__n_nails+1))/2, 2, (self.__a_width+self.__a_width/(self.__n_nails+1))/2, 2, self.__a_width+2, self.__a_height/2+2, self.__c_width+2, self.__a_height+2, 2, self.__a_height+2, fill="#efe4b0", outline="brown")
        for i in range(self.__n_nails):
            self.__canvas_anim.create_line(self.__a_width/(self.__n_nails+1)*(i+1)+2, self.__a_height/2+2, self.__a_width/(self.__n_nails+1)*(i+1)+2, self.__a_height+2, fill="brown")
            for j in range(i+1):
                x = (self.__a_width-self.__a_width/(self.__n_nails+1)*i)/2+self.__a_width/(self.__n_nails+1)*j
                y = self.__a_height/2/self.__n_nails*(i+1)
                self.__canvas_anim.create_oval(x-self.__a_width/(self.__n_nails+1)/20+2, y-self.__a_width/(self.__n_nails+1)/20+2, x+self.__a_width/(self.__n_nails+1)/20+2, y+self.__a_width/(self.__n_nails+1)/20+2, fill="brown", outline="brown")

    def __display_graph(self):
        """
        __display_graph(self)

        Affiche la liste des résultats expérimentaux et des résultats théoriques sous forme d'un diagramme en bâtons.
        """
        m = max(self.__l_simulation)
        n = len(self.__l_simulation)
        if max(self.__l_theoretical) > m: m = max(self.__l_theoretical)
        self.__canvas_graph.delete("all")
        for i in range(n):
            self.__canvas_graph.create_line(self.__c_width/n*(i+1)+2, 2, self.__c_width/n*(i+1)+2, self.__c_height+2, fill="black")
            self.__canvas_graph.create_text(self.__c_width/n*(i+0.5)+2, 12, text=str(self.__l_theoretical[i]), fill="blue")
            self.__canvas_graph.create_text(self.__c_width/n*(i+0.5)+2, 24, text=str(self.__l_simulation[i]), fill="red")
            self.__canvas_graph.create_rectangle(self.__c_width/n*i+2, self.__c_height-self.__l_theoretical[i]*(self.__c_height-32)/m+2, self.__c_width/n*(i+0.5)+2, self.__c_height+2, fill="blue")
            self.__canvas_graph.create_rectangle(self.__c_width/n*(i+0.5)+2, self.__c_height-self.__l_simulation[i]*(self.__c_height-30)/m+2, self.__c_width/n*(i+1)+2, self.__c_height+2, fill="red")
        self.__canvas_graph.create_text(12, self.__c_height/2, anchor="w", text="Marge d'erreur : "+str(self.__margin_error(self.__l_simulation, self.__l_theoretical))+"%", fill="green")

    def __display_info(self, event):
        """
        __display_info(self, event)

        Affiche les informations d'une colonne du graphique.

        event -> L'évènement relatif au mouvement de la souris
        """
        for i in self.__info:
            self.__canvas_graph.delete(i)
        self.__info = []
        if len(self.__l_simulation) > 0 and 0 <= event.x < self.__c_width and 0 <= event.y < self.__c_height:
            c = int(event.x//(self.__c_width/(self.__n_nails+1)))
            a = ["Colonne : "+str(c), "Thérorique : "+str(self.__l_theoretical[c]), "Simulation : "+str(self.__l_simulation[c])]
            x = event.x
            if x+len(a[1])*6 > self.__c_width: x = self.__c_width-len(a[1])*6
            y = event.y
            if y+35 > self.__c_height: y = self.__c_height-35
            self.__info += [self.__canvas_graph.create_rectangle(x+2, y+2, x+len(a[1])*6+2, y+37, fill="white")]
            for i in range(3):
                self.__info += [self.__canvas_graph.create_text(x+4, y+10*i+2, anchor="nw", text=a[i])]

    def __experience(self):
        """
        __experience(self)

        Simule l'expérience de la planche de Galton.
        """
        try:
            self.__n_nails = int(self.__entry_nails.get())
            self.__n_marbles = int(self.__entry_marbles.get())
            if self.__n_nails >= 0 and self.__n_marbles >= 0:
                try:
                    self.__prob_left = float(self.__entry_probleft.get())
                    if 0 <= self.__prob_left <= 1:
                        self.__l_theoretical = self.__theoretical(self.__n_nails, self.__n_marbles, self.__prob_left)
                        if self.__isanim.get():
                            self.__l_simulation = [0 for i in range(self.__n_nails+1)]
                            self.__init_animation()
                        else: self.__l_simulation = self.__simulate(self.__n_nails, self.__n_marbles, self.__prob_left)
                        self.__display_graph()
                        self.__display_anim()
                    else: showerror("Erreur", "Il faut que la probabilité qu'une bille aille à gauche soit un nombre compris dans l'intervalle [0;1].")
                except: showerror("Erreur", "Il faut que la probabilité qu'une bille aille à gauche soit un nombre compris dans l'intervalle [0;1].")
            else: showerror("Erreur", "Il faut que le nombre de clous et le nombre de billes soient des nombres entiers positifs.")
        except: showerror("Erreur", "Il faut que le nombre de clous et le nombre de billes soient des nombres entiers positifs.")

    def __init_animation(self):
        """
        __init_animation(self)

        Initialise l'animation.
        """
        self.__marbles = []
        self.__images_marbles = []
        self.__animation(self.__n_marbles)

    def __margin_error(self, l1, l2):
        """
        __margin_error(self, l1, l2)

        Calcule la marge d'erreur entre deux listes entrées.

        l1 -> La première liste à comparer
        l2 -> La deuxième liste à comparer
        """
        #=====Partie 3.2=====#
        return sqrt(sum([(l1[i]-l2[i])**2 for i in range(len(l1))]))/self.__n_marbles*100
        #====================#

    def __set_label_fps(self, event):
        """
        __set_label_fps(self, event)

        Défini le texte du label correspondant au délai entre chaque frame de l'animation.

        event -> Evènement correspondant au changement du curseur (non utilisé)
        """
        self.__label_fps["text"] = "Délai entre chaque frame (ms) = "+str(self.__fps.get())

    def __simulate(self, n_nails, n_marbles, prob_left):
        """
        __simulate(self, n_nails, n_marbles, prob_left)

        Retourne une liste contenant les résultats expérimentaux de l'expérience de la planche de Galton.

        n_nails -> Le nombre de clous
        n_marbles -> Le nombre de billes
        prob_left -> La probabilité qu'une bille aille à gauche
        """
        #=====Partie 1=====#
        l = [0 for i in range(n_nails+1)]
        for i in range(n_marbles):
            l[sum([random() > prob_left for j in range(n_nails)])] += 1
        #==================#
        return l

    def __theoretical(self, n_nails, n_marbles, prob_left):
        """
        __theoretical(self, n_nails, n_marbles, prob_left)

        Retourne une liste contenant les résultats théoriques de l'expérience de la planche de Galton.

        n_nails -> Le nombre de clous
        n_marbles -> Le nombre de billes
        prob_left -> La probabilité qu'une bille aille à gauche
        """
        #=====Partie 3.1=====#
        return [binom(n_nails, i)*(1-prob_left)**i*prob_left**(n_nails-i)*n_marbles for i in range(n_nails+1)]
        #====================#

class Marble:
    def __init__(self, x, y, ymax, increment_x, increment_y, prob_left, size):
        """
        Marble(x, y, ymax, increment_x, increment_y, prob_left, size)

        Créé une billes pouvant ensuite se déplacer sur la planche.

        x -> Abscisse de la bille
        y -> Ordonnée de la bille
        ymax -> Ordonnée maximum que la bille peut atteindre
        increment_x -> Pas que la bille fait lorsqu'elle se déplace à l'horizontale
        increment_y -> Pas que la bille fait lorsqu'elle se déplace à la verticale
        prob_left -> Probabilité que la bille aille à gauche lorsqu'elle tombe sur un clou
        size -> Diamètre de la bille

        Attributs:

        x
        y
        __ymax
        __increment_x
        __increment_y
        __prob_left
        __direction
        __size

        Méthodes:

        down(self)
            Fait bouger la bille
        """
        self.x = x
        self.y = y
        self.__ymax = ymax
        self.__increment_x = increment_x
        self.__increment_y = increment_y
        self.__prob_left = prob_left
        self.__direction = 0
        self.__size = size

    def down(self):
        """
        down(self)

        Fait bouger la bille.
        """
        if self.y < self.__ymax+self.__size:
            if self.__direction == 0:
                self.y += self.__increment_y
                if self.y <= self.__ymax/2+self.__increment_y-1: self.__direction = (random() > self.__prob_left)*2-1
            else:
                self.x += self.__increment_x*self.__direction
                self.__direction = 0
        else: return int(self.x//(self.__increment_x*2))

window = Window()
