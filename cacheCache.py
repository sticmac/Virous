#Lemaire Julien - Casagrande Guillaume - G2
#Projet de programmation impérative

#chargement des modules
from turtle import *
from grille import *
from tortue import *
from objets import *
from tkinter import messagebox

def initialiser():
    global objetsCases, coordonneesTortue, capturer, selection
    selection = False
    reset() #Efface l'écran

    title("VIROUS") #Titre de la fenetre
    
    #Réinitialisation des variables aux valeurs de départ
    setnvirus(0)
    setnvie(getvieTotale())
    setnbonus(0)
    setnantidotes(0)
    setscore(0)
    coordonneesTortue = [0,0]

    dessinerFenetre(1000,800)#La résolution du jeu est donc de 1000*800
    objetsCases = remplirCases()

    images() #On charge les images et on initialise la deuxième Turtle qui les dessinera sur la grille (Charb)

    afficherScore() #Affiche les valeurs initiales du score, de la vie, etc...
    setCoordonnees(coordonneesTortue)

    seth(270) #Turtle qui pointe vers le haut
    speed(0) #Turtle qui se déplace instantanément
    #Le jeu commence, on ouvre une boite de dialogue :
    messagebox.showinfo("VIROUS","Bienvenue dans Virous !\nLe monde est touché par une épidémie mondiale\nVous devez trouver les 5 antidotes (fioles) pour éradiquer le virus, sans découvrir de nouveaux foyers... Bonne chance !")
    capturer = True #Si ce booléen vaut True, alors on peut executer les évenements liés aux touches du clavier.
    selection = True #On peut de nouveau selectionner des cases

#Gestion des événements
def deplacements():
    #Applique les fonctions événementielles aux touches directionnelles
    onkey(haut, "Up")
    onkey(bas, "Down")
    onkey(droite, "Right")
    onkey(gauche, "Left")
    #Touche de selection de case
    onkey(selectionner, "space")

def haut():
    coordonneesTortue[1]-=1

    #On ne peut se déplacer QUE si l'on ne sort pas de la fenetre ET si la turtle ne fait pas autre chose (comme dessiner le score par exemple).
    if coordonneesOK(coordonneesTortue) and capturer:
        setCoordonnees(coordonneesTortue)
    else:
        coordonneesTortue[1]+=1

def bas():
    coordonneesTortue[1]+=1
        
    if coordonneesOK(coordonneesTortue) and capturer:
        setCoordonnees(coordonneesTortue)
    else:
        coordonneesTortue[1]-=1

def droite():
    coordonneesTortue[0]+=1
        
    if coordonneesOK(coordonneesTortue) and capturer:
        setCoordonnees(coordonneesTortue)
    else:
        coordonneesTortue[0]-=1

def gauche():
    coordonneesTortue[0]-=1

    if coordonneesOK(coordonneesTortue) and capturer:
        setCoordonnees(coordonneesTortue)
    else:
        coordonneesTortue[0]+=1
        
def selectionner():
    global capturer, selection

    if selection:
        #On fixe les valeurs de la case où la fonction d'applique (pour éviter les bugs)
        x = coordonneesTortue[0]
        y = coordonneesTortue[1]

        #Execute les commandes des fonctions correspondantes à l'objet trouvé, situées dans le module "objets"
        #0 = Plouf, 1 = Virus, 2 = Antidote, 3 = Bonus, -1 = Déjà sélectionnée précédemment
        objet = objetsCases[x][y]
        if objet == 0:
            plouf()
        elif objet == 1:
            virus()
        elif objet == 2:
            antidote()
        elif objet == 3:
            bonus()
        objetsCases[x][y] = -1

        if getnvie() < 0: #La vie ne peut pas être négative
            setnvie(0)
        
        capturer = False #La turtle ne peut pas se déplacer sur la grille tant qu'elle dessine le score...

        afficherScore() 
        if getnvie() <= 0 or getnvirus() == 5: #Game Over
            if not messagebox.askokcancel("Game Over", "La population mondiale a été éradiquée, vous avez perdu.\nScore : "+str(getscore())+"\nRecommencer ?"):
                bye() #Fin du jeu
            else:
                initialiser() #Nouvelle partie
        elif getnantidotes() == 5: #Victoire
            setscore(getscore()+1000+(int(getnvie()/getvieTotale())*1000)) #En cas de victoire, le score augmente de 1000 points + 10 fois le pourcentage de la population restante en points
            if not messagebox.askokcancel("Victoire", "Vous avez sauvé l'humanité ! Bravo !\nScore :"+str(getscore())+"\nRecommencer ?"): 
                bye()
            else:
                initialiser() 
        else: #Déroulement habituel du jeu
            setCoordonnees(coordonneesTortue) #La turtle se déplace sur ses nouvelles coordonnées
            
        capturer = True #La turtle peut de nouveau se déplacer sur la grille
    

initialiser()

#Lancement de la boucle principale : passage en programmation événementielle (tout ne peut-être changé que par pression de touche par exemple).
deplacements()
listen()
mainloop()
