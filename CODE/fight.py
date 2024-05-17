import sys
from abc import abstractmethod, ABCMeta
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox,QWidget
from fightUI import Ui_Form  
from PyQt5.QtCore import QTimer, Qt 
import pandas as pd
from abc import abstractmethod, ABCMeta
import donnees_pokemon as vp
import random as rd
import math
import copy
import time
from inventaireUI import Ui_Form2


types = ["Steel", "Fighting", "Dragon", "Water", "Electric", "Fire", "Fairy", "Ice", "Bug", "Normal", "Grass", "Poison", "Psychic", "Rock", "Ground", "Ghost", "Dark", "Flying"]



# Matrice des affinités de types

affinite_types = [

    [0.5, 1, 1, 0.5, 0.5, 0.5, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],                  

    [2, 1, 1, 1, 1, 1, 0.5, 2, 0.5, 2, 1, 0.5, 0.5, 2, 1, 0, 2, 0.5],                

    [0.5, 1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],                        

    [1, 1, 0.5, 0.5, 1, 2, 1, 1, 1, 1, 0.5, 1, 1, 2, 2, 1, 1, 1],                    

    [1, 1, 0.5, 2, 0.5, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 0, 1, 1, 2],                    

    [2, 1, 0.5, 0.5, 1, 0.5, 1, 2, 2, 1, 2, 1, 1, 0.5, 1, 1, 1, 1],                  

    [0.5, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 2, 1],                    

    [0.5, 1, 2, 0.5, 1, 0.5, 1, 0.5, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2],                  

    [0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 2, 0.5, 2, 1, 1, 0.5, 2, 0.5],            

    [0.5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 1, 0, 1, 1],                      

    [0.5, 1, 0.5, 2, 1, 0.5, 1, 1, 0.5, 1, 0.5, 0.5, 1, 2, 2, 1, 1, 0.5],            

    [0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 0.5, 1, 0.5, 0.5, 0.5, 1, 1],                  

    [0.5, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 0, 1],                      

    [0.5, 0.5, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 0.5, 1, 1, 2],                    

    [2, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 0],                      

    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 2, 0.5, 1],                        

    [1, 0.5, 1, 1, 1, 1, 0.5, 1, 1, 1, 1, 1, 2, 1, 1, 2, 0.5, 1],                    

    [0.5, 2, 1, 1, 0.5, 1, 1, 1, 2, 1, 2, 1, 1, 0.5, 1, 1, 1, 1]                     

]


class Combat:

    """

    Cette classe représente un combat entre un joueur et un Pokémon adverse.

    """

    indice = 0  # Indice du Pokémon en combat dans l'équipe du joueur

    def __init__(self, joueur, pokemon_adversaire):

        """

        Initialise un combat entre un joueur et un Pokémon adverse.



        Parameters:

        ----------

        joueur : Joueur

            Le joueur participant au combat.

        pokemon_adversaire : Pokemons

            Le Pokémon adverse.



        Returns:

        -------

        None

        """

        self.joueur = joueur

        self.pokemon_adversaire = pokemon_adversaire

    def est_mort(self):

        """

        Vérifie si le Pokémon actuel du joueur est mort.



        Returns:

        -------

        bool

            True si le Pokémon actuel est mort, False sinon.

        """

        if self.joueur.pokemon_equipe[self.indice].est_ko():

            return True

    

    def fuir(self):#c'est bon
        """
        Gère la tentative de fuite pendant le combat.

        Returns:
        -------
        bool
            True si le joueur a réussi à fuir, False sinon.
        """
        proba_fuite = ((self.joueur.pokemon_equipe[self.indice].stats['Speed'] * 32) / (math.floor(self.pokemon_adversaire.stats['Speed'] / 4))) + 30
        if proba_fuite > 255:
           
            return True
        else:
            aleatoire = rd.randint(0, 255)
            if aleatoire <= proba_fuite:
                
                return True
            else:
                
                return False

    def attaque_spe(self):
        

            
        attaque = [self.joueur.pokemon_equipe[self.indice].stats['Type 1'], self.joueur.pokemon_equipe[self.indice].stats['puissance'], self.joueur.pokemon_equipe[self.indice].stats['attaque_speciale']]


        return self.joueur.pokemon_equipe[self.indice].attaquer(attaque, self.pokemon_adversaire)
        

    def utiliser_charge(self):#c'est bon
        """
        Gère l'utilisation de l'attaque 'Charge' pendant le combat.

        Returns:
        -------
        bool
            True si l'attaque a été utilisée avec succès, False sinon.
        """
        

            
        attaque = ['Normal', 30, 'Charge']
        deg,message=self.joueur.pokemon_equipe[self.indice].attaquer(attaque, self.pokemon_adversaire)
        return deg,message
        
    def attaquer_adversaire(self):#c'est bon
        """
        Gère l'attaque du Pokémon adverse pendant le combat.

        Returns:
        -------
        bool
            True si l'attaque a été réussie, False sinon.
        """
        attaque_aleatoire = rd.choice([[self.pokemon_adversaire.stats['Type 1'], self.pokemon_adversaire.stats['puissance'], self.pokemon_adversaire.stats['attaque_speciale']], ['Normal', 30, 'Charge']])
        deg,message=self.pokemon_adversaire.attaquer(attaque_aleatoire, self.joueur.pokemon_equipe[self.indice])
        return deg,message,attaque_aleatoire[2]
        
            
    def fuir_adv(self):#c'est bon
        if self.pokemon_adversaire.stats['Legendary']:
            aleatoire = rd.randint(0, 100)
            if aleatoire < 10:
               
            
                return True
            return False
        else:
            aleatoire = rd.randint(0, 100)
            if aleatoire < 5:
                
            
                return True
            return False


class Pokemons(metaclass=ABCMeta):
    """
    Classe représentant les Pokémon du jeu.

    Attributes:
    ----------
    name : str
        Le nom du Pokémon.
    stats : dict
        Dictionnaire contenant les statistiques du Pokémon.
    niveau : int
        Le niveau du Pokémon.
    exp : int
        L'expérience actuelle du Pokémon.
    charge : str, 
        L'attaque de base du Pokémon (Charge de type 'Normal').
    """

    def __init__(self, name):
        """
        Initialise un objet Pokémon avec son niveau, nom et éventuellement une attaque de base.
        
        Parameters:
        ----------
        name : str
            Le nom du Pokémon.

        Returns:
        -------
        None
        """
        self.charge='Normal'
        self.name = name
        self.stats = copy.deepcopy(vp.pokemon_dict[name])
        self.niveau = self.stats['Niveau']
        self.exp=vp.exp_necessaire_par_niveau[self.niveau-1]
     

    def __str__(self):
        """
        Retourne une chaîne de caractères représentant les caractéristiques du Pokémon.

        Returns:
        -------
        str
            Chaîne de caractères représentant les caractéristiques du Pokémon.
        """
        return str(self.name) 
    

    def monter_niveau(self,exp_gagne):
        """
        Fait monter de niveau un Pokémon en fonction de l'expérience gagnée.

        Parameters:
        ----------
        exp_gagne : int
            L'expérience gagnée par le Pokémon.

        Returns:
        -------
        None
        """
        ancien_niveau=self.niveau
        self.exp+=exp_gagne
        self.monte_lvl=False
        self.evolution=False
       
        
        for i in range(len(vp.exp_necessaire_par_niveau)):
            if vp.exp_necessaire_par_niveau[i]<=self.exp<vp.exp_necessaire_par_niveau[i+1]:
                self.niveau=vp.exp_niveau_pokemon[vp.exp_necessaire_par_niveau[i]]
        diff=self.niveau-ancien_niveau
        if diff!=0:
            self.monte_lvl=True
            self.stats['Total']+=6*(2*diff)
            self.stats['Niveau']=self.niveau
            if  self.stats['HP'][0]!=0 :
                self.stats['HP'][0]+=2*diff
            self.stats['HP'][1]+=2*diff
            self.stats['Attack']+=2*diff
            self.stats['Defense']+=2*diff
            self.stats['Sp. Atk']+=2*diff
            self.stats['Sp. Def']+=2*diff
            self.stats['Speed']+=2*diff
        else :
           
            self.monte_lvl=False
        if self.niveau==30 and self.stats['Evolution']==2:
                self.name=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Name']=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Evolution']-=1
                self.evolution=True
            

        elif self.niveau==30 and self.stats['Evolution']==3 :
                self.name=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Name']=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Evolution']=0
                self.evolution=True
                

        elif self.niveau==40 and self.stats['Evolution']==1 :
                self.name=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Name']=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Evolution']-=1
                self.evolution=True
               

        return self.monte_lvl,self.evolution
            

    

    def attaquer(self, attaque, pokemon2):
        """
        Fonction pour attaquer un autre Pokémon.

        Parameters:
        ----------
        attaque : tuple
            Tuple contenant le type de l'attaque sa puissance et son nom.
        pokemon2 : Pokemons
            Le Pokémon attaqué.

        Returns:
        -------
        None
        """
        message=""
        if self.stats['Type 1'] == attaque[0]:
            STAB = 1.5
        else:
            STAB = 1

        if pokemon2.stats['Type 2'] not in types :
            a, b = types.index(attaque[0]), types.index(pokemon2.stats['Type 1'])
            type1 = affinite_types[a][b]
            R = math.floor((rd.uniform(217, 255) * 100) / 255)
            deg = ((((((self.niveau * 2 / 5) + 2) * (attaque[1]) * (self.stats['Sp. Atk']) / 50) / (pokemon2.stats['Sp. Def'])) + 2) * R / 100) * STAB * type1
            deg = math.floor(deg)
            pokemon2.stats['HP'][0] -= deg
            if pokemon2.stats['HP'][0]<0:
                pokemon2.stats['HP'][0]=0
            if  type1==0 :
                message="L'attaque n'a aucun effet !"
                

            elif type1==0.5 :
                message= "Ce n'est pas très efficace ..."
                

            else :
                message= "C'est super efficace !"
                

        else :
            a, b = types.index(attaque[0]), types.index(pokemon2.stats['Type 1'])
            c,d = types.index(attaque[0]), types.index(pokemon2.stats['Type 2'])
            type1 = affinite_types[a][b]
            type2 = affinite_types[c][d]
            R = math.floor((rd.uniform(217, 255) * 100) / 255)
            deg = ((((((self.niveau * 2 / 5) + 2) * (attaque[1]) * (self.stats['Sp. Atk']) / 50) / (pokemon2.stats['Sp. Def'])) + 2) * R / 100) * STAB * type1 * type2
            deg = math.floor(deg)
            pokemon2.stats['HP'][0] -= deg
            if pokemon2.stats['HP'][0]<0:
                pokemon2.stats['HP'][0]=0
            if  type1*type2==0 :
                message="L'attaque n'a aucun effet !"

            elif type1*type2<=0.5 :
                message= "Ce n'est pas très efficace ..."

            elif type1*type2>=2:
               message= "C'est super efficace !"
        return deg,message

    def est_ko(self):
        """
        Vérifie si le Pokémon est KO.

        Returns:
        -------
        bool
            True si le Pokémon est KO, False sinon.
        """
        return self.stats['HP'][0] <= 0
 
class Dresseur:

    def __init__(self, name):
        """
        Initialise un joueur avec son nom.

        Parameters:
        ----------
        name : str
            Le nom du joueur.

        Returns:
        -------
        None
        """
        self.name = name
        self.pokemon_equipe = []


    def __str__(self):
        """
        Retourne une chaîne de caractères représentant les  Pokémons du dresseur.

        Returns:
        -------
        str
            Chaîne de caractères représentant les caractéristiques du Pokémon.
        """
        return f" {self.name} a {len(self.pokemon_equipe)} pokemon: "
    

    def tout_est_ko(self):
        """
        Vérifie si tous les Pokémon du joueur sont KO.

        Returns:
        -------
        bool
            True si tous les Pokémon du joueur sont KO, False sinon.
        """
        for i in self.pokemon_equipe:
            if not  i.est_ko():
                return False
        Soins(self)
        return True 

    def ajouter_pokemon_equipe(self, pokemon,indice):
        """
        Ajoute un Pokémon à l'équipe du joueur.

        Parameters:
        ----------
        pokemon : Pokemons
            Le Pokémon à ajouter à l'équipe.

        Returns:
        -------
        None
        """
        if len(self.pokemon_equipe) < 6:
            pokemon.stats['HP'][0]= pokemon.stats['HP'][1]
            self.pokemon_equipe.append(pokemon)
            print(f"{self.name} a capturé {pokemon.name}.")
        else:
            print("L'équipe est déjà complète, vous devez retirer un Pokémon avant d'en ajouter un autre.")
            self.retirer_pokemon_equipe(self.pokemon_equipe[indice])
            self.ajouter_pokemon_equipe(pokemon,indice)

    def retirer_pokemon_equipe(self, pokemon):
        """
        Retire un Pokémon de l'équipe du joueur.

        Parameters:
        ----------
        pokemon : Pokemons
            Le Pokémon à retirer de l'équipe.

        Returns:
        -------
        None
        """
        if pokemon in self.pokemon_equipe:
            self.pokemon_equipe.remove(pokemon)
            print(f"{pokemon.name} a été retiré de l'équipe de {self.name}.")
        else:
            print(f"{pokemon.name} n'est pas dans l'équipe de {self.name}.")

class Rencontre :
    def __init__(self,joueur,position):
        """
        Initialise une rencontre avec un joueur et une position.

        Parameters:
        ----------
        joueur : Dresseur
            Le joueur rencontré.
        position : tuple
            La position de la rencontre.

        Returns:
        -------
        None
        """
        self.joueur=joueur
        self.position=position
        self.pokemon_sauvage=Pokemons(vp.pokemon_coordinates[self.position])
        self.combat=Combat(self.joueur,self.pokemon_sauvage)
        #combat.commencer()
 
class Starter :

    def __init__(self,joueur,p1,p2,p3):
        """
        Initialise les Pokémon de départ d'un joueur.

        Parameters:
        ----------
        joueur : Dresseur
            Le joueur.
        p1 : str
            Nom du premier Pokémon.
        p2 : str
            Nom du deuxième Pokémon.
        p3 : str
            Nom du troisième Pokémon.

        Returns:
        -------
        None
        """
        self.joueur=joueur
        self.joueur.pokemon_equipe.append(Pokemons( p1))
        self.joueur.pokemon_equipe.append(Pokemons( p2))
        self.joueur.pokemon_equipe.append(Pokemons( p3))


class Soins:
       def __init__(self,joueur):
        """
        Soigne les Pokémon d'un joueur.

        Parameters:
        ----------
        joueur : Dresseur
            Le joueur dont les Pokémon doivent être soignés.

        Returns:
        -------
        None
        """
        self.joueur=joueur
        for pokemon in joueur.pokemon_equipe :
            pokemon.stats['HP'][0]= pokemon.stats['HP'][1]




class FightWindow(QDialog):
    def __init__(self, pokemons=None,dresseur=None,pos=None):
        super(FightWindow, self).__init__()
        loadUi("UI/welcome2.ui", self) 
        self.ui = Ui_Form()  
        self.ui.setupUi(self)
        self.dresseur = dresseur
        # Ajoutez des fonctionnalités de clic aux boutons en définissant des fonctions correspondantes
        df = pd.read_csv("data/merged_data_fr.csv")
        self.current_pokemon = int
        self.text_queue = [] 
        #Dresseur1 = Dresseur("Sacha")
        #dresseur.pokemon_equipe.append(Pokemons('Charmander'))

        self.cb = Rencontre(self.dresseur, pos)
    
        self.liste_numero_pok = []
        
        pokemon_list= self.dresseur.pokemon_equipe
        for pokemon in pokemon_list:
            self.liste_numero_pok.append(df.loc[df['Name'] == pokemon.name, '#'].values[0])
        
        
        #UI ADVERSAIRE
        num_pok_sauv = df.loc[(df['coord_x'] == pos[0]) & (df['coord_y'] == pos[1]), '#'].values
        self.label_3.clear()
        self.changer_image_pok_adv(num_pok_sauv[0])
        self.label.setText(f"{self.cb.pokemon_sauvage.niveau}")
        self.label_2.setText(f"{self.dresseur.pokemon_equipe[self.cb.combat.indice].niveau}")
        self.nom_adv.setText(f"{self.cb.pokemon_sauvage.name}")

        self.phrases_intro = [
            f"Le combat entre {self.cb.joueur.name} et {self.cb.combat.pokemon_adversaire.name} commence !",
            f"Un {self.cb.combat.pokemon_adversaire.name} sauvage apparait !",
            f"{self.cb.joueur.pokemon_equipe[self.cb.combat.indice]} ! Go!",
        ]
        self.compteur = 0
        self.set_dialogue_text(self.phrases_intro[self.compteur])
        self.compteur += 1

        self.ui.progressBar_adv.setMaximum(self.cb.combat.pokemon_adversaire.stats['HP'][1])
        self.ui.progressBar_pv.setMaximum(self.cb.joueur.pokemon_equipe[self.cb.combat.indice].stats['HP'][1])
        self.ui.progressBar_adv.setValue(self.cb.combat.pokemon_adversaire.stats['HP'][1])
        self.ui.progressBar_pv.setValue(self.cb.joueur.pokemon_equipe[self.cb.combat.indice].stats['HP'][0])
        self.ui.progressBar_adv.setStyleSheet("QProgressBar::chunk { background-color: red; }")
        self.ui.progressBar_pv.setStyleSheet("QProgressBar::chunk { background-color: blue; }")
        

        self.nom_adv_2.setText(f"{self.cb.joueur.pokemon_equipe[self.cb.combat.indice].name}")
        
        self.ui.pushButton.setText("Charge")
        self.ui.pushButton.clicked.connect(self.utiliser_charge)
        self.ui.pushButton_2.clicked.connect(self.attaquer_sp2)
        self.ui.pushButton_2.setText(self.cb.joueur.pokemon_equipe[0].stats['attaque_speciale'])
        self.ui.pushButton_3.clicked.connect(self.fuite)
        self.ui.pushButton_4.setText("Pokemon")
        self.ui.pushButton_4.clicked.connect(self.changer_pokemon)
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.setEnabled(False)
        #self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton.clicked.connect(self.on_button_click)
        self.ui.pushButton_2.clicked.connect(self.on_button_click)
        self.ui.pushButton_4.clicked.connect(self.on_button_click)
        self.combat_timer = QTimer(self)
        self.combat_timer.timeout.connect(self.round)
       # self.combat_timer.start(15000)  # 15 secondes par tour de combat

    def progressbar(self,value):
        self.ui.progressBar_adv.setValue(value)

    def on_button_click(self):
        # Redémarrez le timer lorsqu'un bouton est cliqué
            self.combat_timer.stop()
            self.combat_timer.start(1000)  

    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Vérification si toutes les phrases ont été affichées
            
            if self.compteur < len(self.phrases_intro):
                # Affichage de la prochaine phrase d'introduction
                self.ui.dialogue.setPlainText(self.phrases_intro[self.compteur])
                self.compteur += 1
            else:
                # Affichage d'un message lorsque toutes les phrases ont été affichées 
                self.ui.dialogue.setPlainText("Que voulez-vous faire ?")
                self.changer_image_pok(self.liste_numero_pok[self.cb.combat.indice])
                self.round()

    

    def attaquer_sp2(self):
        # Code pour l'action de la deuxième attaque spéciale
        
        if self.cb.joueur.pokemon_equipe[self.cb.combat.indice].stats['Speed'] >= self.cb.combat.pokemon_adversaire.stats['Speed']:
            self.set_dialogue_text("Vous avez été plus rapide!",temps=0.5)
            self.set_dialogue_text(f"C'est au tour de {self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].name} d'attaquer.",0.5)
            self.set_dialogue_text(f"Votre Pokémon utilise {self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].stats['attaque_speciale']}!")
            deg,message=self.cb.combat.attaque_spe()
            self.ui.progressBar_adv.setValue(self.ui.progressBar_adv.value() - deg)
            self.set_dialogue_text(f"{message}",0.5)
            self.defendre()

            
    
        else:
            self.set_dialogue_text("Il a été plus rapide!",1)
            self.defendre()
            self.set_dialogue_text(f"C'est au tour de {self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].name} d'attaquer.",0.5)
            self.set_dialogue_text(f"Votre Pokémon utilise {self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].stats['attaque_speciale']}!")
            deg,message=self.cb.combat.attaque_spe()
            self.ui.progressBar_adv.setValue(self.ui.progressBar_adv.value() - deg)
            self.set_dialogue_text(f"{message}",0.5)

    def fuite(self):
        """
        Gère l'action de fuite dans la fenêtre de combat.
        """
        if self.cb.combat.fuir():
            self.set_dialogue_text("Vous avez pris la fuite !")
            
            QMessageBox.information(self, "", "Vous avez pris la fuite !")
            self.close()
            return True
        else:
            self.set_dialogue_text("Vous n'avez pas réussi à fuir !")

    def utiliser_charge(self):
        """
        Gère l'action d'utiliser l'attaque 'Charge' dans la fenêtre de combat.
        """
        
        if self.cb.joueur.pokemon_equipe[self.cb.combat.indice].stats['Speed'] >= self.cb.combat.pokemon_adversaire.stats['Speed']:

            self.set_dialogue_text("Vous avez été plus rapide!",temps=0.5)
            self.set_dialogue_text(f"C'est au tour de {self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].name} d'attaquer.",0.5)
            self.set_dialogue_text("Votre Pokémon utilise Charge!")
            deg,message=self.cb.combat.utiliser_charge()
            self.ui.progressBar_adv.setValue(self.ui.progressBar_adv.value() - deg)
            self.set_dialogue_text(f"{message}",0.5)
            self.defendre()
        else:
            
            self.set_dialogue_text("Il a été plus rapide!",1)
            self.defendre()
            deg,message=self.cb.combat.utiliser_charge()
            self.set_dialogue_text("Votre Pokémon utilise Charge !")
            self.ui.progressBar_adv.setValue(self.ui.progressBar_adv.value() - deg)
            self.set_dialogue_text(f"{message}",0.5)
       
    def defendre(self):
        if self.cb.combat.fuir_adv():
            self.set_dialogue_text(f"Le {self.cb.combat.pokemon_adversaire.name} sauvage a pris la fuite !",0.5)
            
            QMessageBox.information(self, "", f"Le {self.cb.combat.pokemon_adversaire.name} sauvage a pris la fuite !")
            self.close()
            return True
        else:
            self.set_dialogue_text(f"C'est au tour de {self.cb.combat.pokemon_adversaire.name} d'attaquer.",0.5)
            deg,message,nom_attaque=self.cb.combat.attaquer_adversaire()
            self.set_dialogue_text(f"{self.cb.combat.pokemon_adversaire.name} utilise {nom_attaque}!")
            self.ui.progressBar_pv.setValue(self.ui.progressBar_pv.value() - deg)
            self.set_dialogue_text(f"{message}",0.5)




    def changer_image_pok(self, numero):
        self.label_3.setPixmap(QPixmap(f"CODE/image tiles/pokemon_Combat/back/{numero}.png"))
        self.label_3.setScaledContents(True)

    def changer_image_pok_adv(self, numero):
        self.label_4.setPixmap(QPixmap(f"CODE/image tiles/pokemon_Combat/front/{numero}.png"))
        self.label_4.setScaledContents(True)

    def round(self):
       # Code pour un round de combat

        self.combat_timer.stop()
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_3.setEnabled(True)
        self.ui.pushButton_4.setEnabled(True)
        
        
        if self.cb.combat.est_mort():
              self.ui.pushButton.setEnabled(False)
              self.ui.pushButton_2.setEnabled(False)
              self.set_dialogue_text(f"Votre pokemon est mort, veuillez changer de pokemon !",temps=1)
              self.display_next_text()

        elif self.cb.combat.pokemon_adversaire.est_ko():
            self.set_dialogue_text(f"{self.cb.combat.pokemon_adversaire.name} est KO !\n next..")
            self.ui.progressBar_adv.setValue(self.cb.combat.pokemon_adversaire.stats['HP'][0])
            self.set_dialogue_text(f"Vous avez gagné !\n next..",temps=1)
            self.display_next_text()
            QMessageBox.information(self, "", "Vous avez gagné !\n next..")
            
            self.combat_gagné()
            self.close()
            

        elif self.cb.combat.joueur.tout_est_ko():
            self.set_dialogue_text(f"{self.cb.joueur.pokemon_equipe[self.cb.combat.indice].name} est KO !\n next..")
            self.set_dialogue_text(f"Vous avez perdu !\n next..",temps=1)
            self.display_next_text()
            QMessageBox.information(self, "", "Vous avez perdu !\n next..")
            self.close()
         
        self.display_next_text()
        
    def changer_pokemon(self):
        
        pokemon_nom=[]
        df = pd.read_csv("data/merged_data_fr.csv")
        pokemon_list= self.dresseur.pokemon_equipe
        for pokemon in pokemon_list:
            pokemon_nom.append(df.loc[df['Name'] == pokemon.name, '#'].values[0])
        
        
        self.liste_numero_pok = pokemon_nom
        
        inventaire = Inventaire(pokemon_nom)
        inventaire.exec_()
        self.cb.combat.indice=inventaire.index
        self.changer_image_pok(pokemon_nom[self.cb.combat.indice])
        
        self.ui.progressBar_pv.setMaximum(self.cb.joueur.pokemon_equipe[self.cb.combat.indice].stats['HP'][1])
        self.ui.progressBar_pv.setValue(self.cb.joueur.pokemon_equipe[self.cb.combat.indice].stats['HP'][0])
        self.ui.progressBar_pv.setStyleSheet("QProgressBar::chunk { background-color: blue; }")
        self.nom_adv_2.setText(f"{self.cb.joueur.pokemon_equipe[self.cb.combat.indice].name}")
        self.set_dialogue_text(f"Changement de Pokémon {self.cb.joueur.pokemon_equipe[self.cb.combat.indice].name} Go!")
        
        self.display_next_text()
        
        
    def combat_gagné(self):#c'est bon
         exp=vp.exp_gagne_par_niveau[self.cb.combat.pokemon_adversaire.niveau]
         ancien_nom=self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].name
         monter_lvl,evolution=self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].monter_niveau(int(exp))

         if evolution :
             QMessageBox.information(self, "", f" {ancien_nom } evolue en {self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].name}")
         
         if monter_lvl:
             
             QMessageBox.information(self, "", f"{self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].name} monte au lvl {self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].niveau}")

         else :
             QMessageBox.information(self, "", f"{self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].name} a gagné {exp} d'xp")
        
         
         n=len(self.cb.combat.joueur.pokemon_equipe)

         for i in range(0,n):

             if i != self.cb.combat.indice :
                 ancien_nom=self.cb.combat.joueur.pokemon_equipe[i].name
                 monter_lvl,evolution=self.cb.combat.joueur.pokemon_equipe[i].monter_niveau(math.floor(int(exp)/(n-1)))
                 if evolution :
                     QMessageBox.information(self, "", f" {ancien_nom } evolue en {self.cb.combat.joueur.pokemon_equipe[self.cb.combat.indice].name}")
         
                 if monter_lvl:
             
                     QMessageBox.information(self, "", f"{self.cb.combat.joueur.pokemon_equipe[i].name} a gagné {int(exp)/(n-1)}, il monte au lvl {self.cb.combat.joueur.pokemon_equipe[i].niveau}")

                 else :
                     QMessageBox.information(self, "", f"{self.cb.combat.joueur.pokemon_equipe[i].name} a gagné {int(exp)/(n-1)} d'xp")
        
         if n < 6 :
             self.cb.combat.joueur.ajouter_pokemon_equipe(self.cb.combat.pokemon_adversaire,self.cb.combat.indice)
             QMessageBox.information(self, "", f"{self.cb.combat.pokemon_adversaire.name} a été capturé")
         else :
             
             self.set_dialogue_text("L'équipe est déjà complète, vous devez retirer un Pokémon avant d'en ajouter un autre.")
             self.changer_pokemon()
             self.cb.combat.joueur.ajouter_pokemon_equipe(self.cb.combat.pokemon_adversaire,self.cb.combat.indice)
             

    def set_dialogue_text(self, text, temps=0):
        
        self.text_queue.append(text)  # Ajoute le texte à la file d'attente
        
        
    
    def display_next_text(self):
        if self.text_queue:
            text = self.text_queue.pop(0)  # Récupère le premier texte de la file d'attente
            self.ui.dialogue.setPlainText(text)
            
            #font_id = QFontDatabase.addApplicationFont("data/police.ttf")
            #font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            #font = QFont(font_family)
            #self.ui.dialogue.setFont(font)
        
            # Affiche le prochain texte après 5 secondes
            QTimer.singleShot(50000, self.display_next_text)
    
        


class Inventaire(QDialog):
    def __init__(self,pokemon_liste):
        super(Inventaire, self).__init__()
        loadUi("UI/inventaire.ui", self) 
        self.ui = Ui_Form2()  
        self.ui.setupUi(self)
        
        self.pokemon_liste=pokemon_liste
        self.index=0
        
        self.poke_img_1.clear()
        self.poke_img_2.clear()
        self.poke_img_3.clear()
        self.poke_img_4.clear()
        self.poke_img_5.clear()
        self.poke_main.clear()
        
        self.ui.poke_main.mousePressEvent = self.shift_pokemon
        
        for i, poke_img_attr in enumerate([self.ui.poke_img_1, self.ui.poke_img_2, self.ui.poke_img_3, self.ui.poke_img_4, self.ui.poke_img_5,self.ui.poke_img_6]):
            if i < len(pokemon_liste):
                pokemon_name = pokemon_liste[i]
            else:
                pokemon_name= "ERROR"
                
            # Utilisation de f-strings pour formater le chemin de l'image
            pixmap_path = f"CODE/image tiles/pokemon_Combat/front/{pokemon_name}.png"
            
            poke_img_attr.clear()
            poke_img_attr.setPixmap(QPixmap(pixmap_path))
            poke_img_attr.setScaledContents(True)
            
            # Assignation de la fonction de gestion d'événements pour le clic de souris
            poke_img_attr.mousePressEvent = lambda event, index=i: self.on_pokemon_clicked(index)
        
        
    def on_pokemon_clicked(self, index):
        # Lorsque vous cliquez sur une image de Pokémon, mettez à jour le pixmap de l'image label correspondante
        pokemon_name = self.pokemon_liste[index] #index du pokemon choisit
        self.ui.poke_main.setPixmap(QPixmap(f"CODE/image tiles/pokemon_Combat/front/{pokemon_name}.png"))
        self.ui.poke_main.setScaledContents(True)
        self.index = index
        
        
    def shift_pokemon(self,event):
        print(self.index)
        print("j'arrive ici")
        self.close()
        
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = FightWindow()
    dialog.show()
    sys.exit(app.exec_())
