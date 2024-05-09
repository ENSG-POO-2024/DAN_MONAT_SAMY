from abc import abstractmethod, ABCMeta
import visualisation_pokemon as vp
import Projet_POO_Pokemon_Dan_Samy_Monat as p
import random as rd
import math
import copy

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
        print(f"{self.name} a gagné {exp_gagne} d'exp")
        for i in range(len(vp.exp_necessaire_par_niveau)):
            if vp.exp_necessaire_par_niveau[i]<=self.exp<vp.exp_necessaire_par_niveau[i+1]:
                self.niveau=vp.exp_niveau_pokemon[vp.exp_necessaire_par_niveau[i]]
        diff=self.niveau-ancien_niveau
        if diff!=0:
            print(f"{self.name} monte au lvl {self.niveau}")
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
            print(f"{self.name} est lvl {self.niveau}")

        if self.niveau==30 and self.stats['Evolution']==2:
                self.name=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Name']=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Evolution']-=1
                print('evolution')

        elif self.niveau==30 and self.stats['Evolution']==3 :
                self.name=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Name']=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Evolution']=0
                print('evolution')

        elif self.niveau==40 and self.stats['Evolution']==1 :
                self.name=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Name']=vp.pokemons_liste[self.stats['Numero']]
                self.stats['Evolution']-=1
                print('evolution')


            

    

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
        if self.stats['Type 1'] == attaque[0]:
            STAB = 1.5
        else:
            STAB = 1

        if pokemon2.stats['Type 2'] not in p.types :
            a, b = p.types.index(attaque[0]), p.types.index(pokemon2.stats['Type 1'])
            type1 = p.affinite_types[a][b]
            R = math.floor((rd.uniform(217, 255) * 100) / 255)
            deg = ((((((self.niveau * 2 / 5) + 2) * (attaque[1]) * (self.stats['Sp. Atk']) / 50) / (pokemon2.stats['Sp. Def'])) + 2) * R / 100) * STAB * type1
            deg = math.floor(deg)
            pokemon2.stats['HP'][0] -= deg
            if pokemon2.stats['HP'][0]<0:
                pokemon2.stats['HP'][0]=0
            print (f"{self.name} utilise {attaque[2]}  sur {pokemon2.name}  et lui inflige {deg} points de dégâts.")
            if  type1==0 :
                print("L'attaque n'a aucun effet !")

            elif type1==0.5 :
                print("Ce n'est pas très efficace ...")

            elif type1==2:
                print("C'est super efficace !")

        else :
            a, b = p.types.index(attaque[0]), p.types.index(pokemon2.stats['Type 1'])
            c,d = p.types.index(attaque[0]), p.types.index(pokemon2.stats['Type 2'])
            type1 = p.affinite_types[a][b]
            type2 = p.affinite_types[c][d]
            R = math.floor((rd.uniform(217, 255) * 100) / 255)
            deg = ((((((self.niveau * 2 / 5) + 2) * (attaque[1]) * (self.stats['Sp. Atk']) / 50) / (pokemon2.stats['Sp. Def'])) + 2) * R / 100) * STAB * type1 * type2
            deg = math.floor(deg)
            pokemon2.stats['HP'][0] -= deg
            if pokemon2.stats['HP'][0]<0:
                pokemon2.stats['HP'][0]=0
            print (f"{self.name} utilise {attaque[2]}  sur {pokemon2.name}  et lui inflige {deg} points de dégâts.")
            if  type1*type2==0 :
                print("L'attaque n'a aucun effet !")

            elif type1*type2<=0.5 :
                print("Ce n'est pas très efficace ...")

            elif type1*type2>=2:
                print("C'est super efficace !")


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

    def ajouter_pokemon_equipe(self, pokemon):
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
            choix = input("Tapez 1 pour éffectuer l'échange sinon 0 pour conserver l'équipe: ")
            if choix == 1:
                choix_pokemon = input("Taper le numéro du pokemon que vous voulez retirer:")
                self.retirer_pokemon_equipe(self.pokemon_equipe[int(choix_pokemon) - 1])
                self.ajouter_pokemon_equipe(pokemon)

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
        combat=p.Combat(self.joueur,self.pokemon_sauvage)
        combat.commencer()

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
        Dan.pokemon_equipe.append(Pokemons( p1))
        Dan.pokemon_equipe.append(Pokemons( p2))
        Dan.pokemon_equipe.append(Pokemons( p3))

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
        

if __name__ == '__main__':
    Dan = Dresseur('Dan')
    Starter(Dan,'Charmander','Bulbasaur','Squirtle')
    Rencontre(Dan,(1033, 101))
    Rencontre(Dan,(1033, 101))
