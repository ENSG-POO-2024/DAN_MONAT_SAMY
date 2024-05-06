from abc import abstractmethod, ABCMeta
import visualisation_pokemon as vp
import Projet_POO_Pokemon_Dan_Samy_Monat as p
import random as rd
import math
class Pokemons(metaclass=ABCMeta) :

    def __init__(self,niveau, name, charge='Normal',):
        self.niveau=niveau
        self.name=name
        self.stats = vp.pokemon_dict[name]
        
        

    def __str__(self):
        '''
        Fonction retournant une chaine de caracteres definissant les 
        caracteristiques de l'objet "Pokemons"
        '''
        return "Pokemon : " 'Niveau : '+(str)(self.niveau)+", " 'Nom : '+(str)(self.name) + "," 
    

    def attaquer(self,attaque,pokemon2):
        """
        Parameters
        ----------
        Pokemon1: est la pokemon qui attaque
        Pokemon2: est le pokemon qui se fait attaquer
        STAB : 1, 2
            La valeur de STAB dépend si l'attaque est de même type que cel du lanceur. Si elles sont identique elle vaut 2 sinon 1
        type1 :0, 0.5, 1 ,2
        type1 renvoie la valeur d'affinité entre le type de l'attaque et le type de la défense
    
        Returns
        -------
        deg : INTEGER
            deg est le nombre de dégats causé par l'attaque au pokemon sauvage
        """
        if self.stats['Type 1'] == attaque[0] :
            STAB = 1.5
        else:
            STAB = 1
        a,b = p.types.index(attaque[0]), p.types.index(pokemon2.stats['Type 1']) # faisant réference aux tableau des affinités de types
        type1 = p.affinite_types[a][b]
        R = math.floor((rd.uniform(217,255)*100) /255)
        deg = ((((((self.niveau*2/5)+2)*(attaque[1])*(self.stats['Sp. Atk'])/50)/(pokemon2.stats['Sp. Def']))+2)*R/100)*STAB*type1
        deg = math.floor(deg)#  arrondi à l'entier inférieur 
        deg = max(1,deg) # les dégats minimum sont au moins de 1
        pokemon2.stats['HP'] -= deg
        print (f"{self.name} attaque {pokemon2.name} avec {attaque[2]} et lui inflige {deg} points de dégâts.")
    
    
    
    def est_ko(self):
        return self.stats['HP'] <=0
    

    

    
    




   


class Joueur :

    def __init__(self,name) :
        self.name=name
        self.pokemon_equipe = []

    def tout_est_ko(self):
        for i in self.pokemon_equipe:
            if not  i.est_ko() :
                return False
        
        return True 
        

    def ajouter_pokemon_equipe(self, pokemon):
        if len(self.pokemon_equipe) < 6:
            self.pokemon_equipe.append(pokemon)
            print(f"{pokemon.name} a été ajouté à l'équipe de {self.name}.")
        else:
            print("L'équipe est déjà complète, vous devez retirer un Pokémon avant d'en ajouter un autre.")
            choix=input("Tapez 1 pour éffectuer l'échange sinon 0 pour conserver l'équipe: ")
            if choix== 1 :
                choix_pokemon=input("Taper le numéro du pokemon que voulez retirer:")
                self.retirer_pokemon_equipe(self.pokemon_equipe[int(choix_pokemon)-1])
                self.ajouter_pokemon_equipe(pokemon)

    def retirer_pokemon_equipe(self, pokemon):
        if pokemon in self.pokemon_equipe:
            self.pokemon_equipe.remove(pokemon)
            print(f"{pokemon.name} a été retiré de l'équipe de {self.name}.")
        else:
            print(f"{pokemon.name} n'est pas dans l'équipe de {self.name}.")

    


if __name__=='__main__':
    Bulbasaur=Pokemons(2,'Bulbasaur')
    Kabuto=Pokemons(100,'Kabuto')
    Dan=Joueur('Dan')
    ratata=Pokemons(2,'Rattata')
    Dan.pokemon_equipe.append(ratata)
    Dan.pokemon_equipe.append(Bulbasaur)
    combat1=p.Combat(Dan,Kabuto)
    combat1.commencer()