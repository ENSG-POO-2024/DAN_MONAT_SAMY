from abc import abstractmethod, ABCMeta
class Pokemons(metaclass=ABCMeta):

    def __init__(self, name,type1,type2,total,hp,attack,defense,sp_atk,sp_def,speed,generation,legendary):
        self.name=name
        self.type1=type1
        self.type2=type2
        self.total=total
        self.hp=hp
        self.attack=attack
        self.defense=defense
        self.sp_atk=sp_atk
        self.sp_def=sp_def
        self.speed=speed
        self.generation=generation
        self.legendary=legendary
    
    @abstractmethod  
    def attaque_pokemon(self,neutre,type):
        pass

class Joueur:

    def__init__(self,name,p1,p2,p3,p4,p5,p6)
