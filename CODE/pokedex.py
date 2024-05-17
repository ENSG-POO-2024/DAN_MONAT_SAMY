import csv

class PokemonList:
    def __init__(self, csv_file_path,cheat=False):
        """
        Initialise la liste des Pokémon à partir d'un fichier CSV.
        
        :param csv_file_path: Chemin vers le fichier CSV contenant les données des Pokémon
        :param cheat: Booléen indiquant si les images doivent être en couleur ou en noir et blanc
        """
        self.csv_file_path = csv_file_path
        
        if cheat==False :    
            self.pokemon_list = self.get_first_gen_pokemon_list(csv_file_path,cheat)
            self.initialize_pokemon_names()
        else :   
            self.pokemon_list = self.get_first_gen_pokemon_list(csv_file_path,cheat)

    def get_first_gen_pokemon_list(self, csv_file_path, cheat=False):
        """
        Lit le fichier CSV et renvoie une liste de Pokémon de la première génération.
        
        :param csv_file_path: Chemin vers le fichier CSV contenant les données des Pokémon
        :param cheat: Booléen indiquant si les images doivent être en couleur ou en noir et blanc
        :return: Liste de dictionnaires représentant les Pokémon
        """
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader)
            pokemon_list = []
            for row in reader:
                if row[-1] == '1' and cheat==False:
                    pokemon_info = {
                        "number": row[0],
                        "name": row[1],
                        "image_name": f"CODE/image tiles/pokemon_Combat/front_black/{row[0]}.png"
                    }
                    pokemon_list.append(pokemon_info)
                elif row[-1] == '1' and cheat:  
                    pokemon_info = {
                        "number": row[0],
                        "name": row[1],
                        "image_name": f"CODE/image tiles/pokemon_Combat/front/{row[0]}.png"
                    }
                    
                    pokemon_list.append(pokemon_info)
        return pokemon_list

    def initialize_pokemon_names(self):
        """
        Initialise les noms des Pokémon de la liste à "????".
        """
        for pokemon in self.pokemon_list:
            pokemon['name'] = "????"

    def print_pokemon_list(self):
        """
        Affiche la liste des Pokémon avec leur numéro, nom et chemin de l'image.
        """
        for pokemon in self.pokemon_list:
            print(f"Numéro: {pokemon['number']}, Nom: {pokemon['name']}, Image: {pokemon['image_name']}")

    def modify_pokemon(self, number, new_name, new_image_name):
        """
        Modifie les informations d'un Pokémon dans la liste.
        
        :param number: Numéro du Pokémon à modifier
        :param new_name: Nouveau nom du Pokémon
        :param new_image_name: Nouveau chemin de l'image du Pokémon
        """
        for pokemon in self.pokemon_list:
            if pokemon['number'] == number:
                pokemon['name'] = new_name
                pokemon['image_name'] = new_image_name
                break
            print("Pokemon found.")
            print(pokemon['name'])
        else:
            print("Pokemon not found.")
            
    def add_starters(self, starters_data):
        """
        Ajoute les Pokémon de départ (starters) à la liste en modifiant leurs informations.
        
        :param starters_data: Liste de dictionnaires contenant les données des starters
        """
    
        for starter_data in starters_data:
            number = starter_data['Numero']
            name = starter_data['name']
            image_name = starter_data['image_name']        
            self.modify_pokemon(number, name, image_name)

if __name__ == '__main__':
    #pokemon_list = PokemonList("data/pokemons_fr.csv",cheat=False)
    #pokemon_list.print_pokemon_list()
    
    # Modifier un Pokémon (par exemple, numéro 1)
    #pokemon_list.modify_pokemon("1", 'Bulbizarre', f"/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/pokemon_Combat/front_black/{1}.png")
    #print("\nAprès modification :")
    #pokemon_list.print_pokemon_list()
    pass
