import matplotlib.pyplot as plt
import pandas as pd
import re

data = pd.read_csv('/Users/cleme/Documents/DAN_MONAT_SAMY/data_traité/pokemon_coordonnes_modifie.csv')


# Définir une fonction pour extraire les coordonnées des chaînes de caractères
def extract_coordinates(coord_str):
    coord_str = re.findall(r'\d+', coord_str)
    return int(coord_str[0]), int(coord_str[1])

# Appliquer la fonction pour extraire les coordonnées
data['coordinates'] = data['coordinates'].apply(extract_coordinates)

# Créer un dictionnaire pour stocker les coordonnées de chaque Pokémon
pokemon_coordinates = {}

# Remplir le dictionnaire avec les données
for index, row in data.iterrows():
    pokemon_name = row['pokemon']
    pokemon_coord = row['coordinates']
    pokemon_coordinates[pokemon_name] = pokemon_coord

# Afficher le dictionnaire
print(pokemon_coordinates)
# Extraire les coordonnées x et y des données
x = [coord[0] for coord in data['coordinates']]
y = [coord[1] for coord in data['coordinates']]

# Créer le quadrillage
plt.figure(figsize=(20, 5))  # Définir la taille de la figure
plt.grid(True)                # Activer le quadrillage

# Tracer les points
plt.scatter(x, y, color='blue')

# Définir les limites du quadrillage
plt.xlim(0, 4000)
plt.ylim(0, 1000)

plt.xticks(range(0, 4000, 20))
plt.yticks(range(0, 1000, 20))

# Afficher le quadrillage
plt.show()



# Charger les données à partir du fichier CSV
pokemon_data = pd.read_csv('/Users/cleme/Documents/DAN_MONAT_SAMY/data/pokemon_first_gen.csv')

# Créer un dictionnaire pour stocker les données de chaque Pokémon
pokemon_dict = {}

# Remplir le dictionnaire avec les données
for index, row in pokemon_data.iterrows():
    pokemon_id = row['Name']
    pokemon_info = {
        'Name': row['Name'],
        'Type 1': row['Type 1'],
        'Type 2': row['Type 2'],
        'Total': row['Total'],
        'HP': row['HP'],
        'Attack': row['Attack'],
        'Defense': row['Defense'],
        'Sp. Atk': row['Sp. Atk'],
        'Sp. Def': row['Sp. Def'],
        'Speed': row['Speed'],
        'Generation': row['Generation'],
        'Legendary': row['Legendary']
    }
    pokemon_dict[pokemon_id] = pokemon_info

# Afficher le dictionnaire
print(pokemon_dict)


attaques_speciales_par_pokemon = {
    "Bulbasaur": {"attaque": "Fouet Lianes", "puissance": 45},
    "Ivysaur": {"attaque": "Vampigraine", "puissance": 60},
    "Venusaur": {"attaque": "Lance-Soleil", "puissance": 120},
    "Charmander": {"attaque": "Flammèche", "puissance": 40},
    "Charmeleon": {"attaque": "Grozyeux", "puissance": 60},
    "Charizard": {"attaque": "Déflagration", "puissance": 110},
    "Squirtle": {"attaque": "Pistolet à O", "puissance": 40},
    "Wartortle": {"attaque": "Hydrocanon", "puissance": 110},
    "Blastoise": {"attaque": "Laser Glace", "puissance": 95},
    "Caterpie": {"attaque": "Dard Venin", "puissance": 40},
    "Metapod": {"attaque": "Étreinte", "puissance": 20},
    "Butterfree": {"attaque": "Papillodanse", "puissance": 90},
    "Weedle": {"attaque": "Dard Venin", "puissance": 40},
    "Kakuna": {"attaque": "Bélier", "puissance": 50},
    "Beedrill": {"attaque": "Dard-Nuée", "puissance": 90},
    "Pidgey": {"attaque": "Jet de Sable", "puissance": 35},
    "Pidgeotto": {"attaque": "Tour Rapide", "puissance": 60},
    "Pidgeot": {"attaque": "Tornade", "puissance": 80},
    "Rattata": {"attaque": "Vive-Attaque", "puissance": 40},
    "Raticate": {"attaque": "Morsure", "puissance": 60},
    "Spearow": {"attaque": "Picpic", "puissance": 60},
    "Fearow": {"attaque": "Cru-Aile", "puissance": 90},
    "Ekans": {"attaque": "Morsure", "puissance": 60},
    "Arbok": {"attaque": "Laser Glace", "puissance": 95},
    "Pikachu": {"attaque": "Éclair", "puissance": 40},
    "Raichu": {"attaque": "Tonnerre", "puissance": 90},
    "Sandshrew": {"attaque": "Griffe", "puissance": 40},
    "Sandslash": {"attaque": "Séisme", "puissance": 100},
    "Nidoran♀": {"attaque": "Griffe", "puissance": 40},
    "Nidorina": {"attaque": "Morsure", "puissance": 60},
    "Nidoqueen": {"attaque": "Pistolet à O", "puissance": 40},
    "Nidoran♂": {"attaque": "Griffe", "puissance": 40},
    "Nidorino": {"attaque": "Morsure", "puissance": 60},
    "Nidoking": {"attaque": "Poing-Karaté", "puissance": 75},
    "Clefairy": {"attaque": "Métronome", "puissance": 40},
    "Clefable": {"attaque": "Métronome", "puissance": 50},
    "Vulpix": {"attaque": "Flammèche", "puissance": 40},
    "Ninetales": {"attaque": "Danse-Flamme", "puissance": 65},
    "Jigglypuff": {"attaque": "Métronome", "puissance": 60},
    "Wigglytuff": {"attaque": "Métronome", "puissance": 60},
    "Zubat": {"attaque": "Ultrason", "puissance": 60},
    "Golbat": {"attaque": "Crochetvenin", "puissance": 65},
    "Oddish": {"attaque": "Tranch'Herbe", "puissance": 55},
    "Gloom": {"attaque": "Poudre Toxik", "puissance": 60},
    "Vileplume": {"attaque": "Lance-Soleil", "puissance": 120},
    "Paras": {"attaque": "Tranch'Herbe", "puissance": 55},
    "Parasect": {"attaque": "Poudre Toxik", "puissance": 60},
    "Venonat": {"attaque": "Piqûre", "puissance": 60},
    "Venomoth": {"attaque": "Toxik", "puissance": 60},
    "Diglett": {"attaque": "Griffe", "puissance": 40},
    "Dugtrio": {"attaque": "Séisme", "puissance": 100},
    "Meowth": {"attaque": "Griffe", "puissance": 40},
    "Persian": {"attaque": "Morsure", "puissance": 60},
    "Psyduck": {"attaque": "Pistolet à O", "puissance": 40},
    "Golduck": {"attaque": "Hydrocanon", "puissance": 110},
    "Mankey": {"attaque": "Poing-Karaté", "puissance": 75},
    "Primeape": {"attaque": "Poing-Karaté", "puissance": 75},
    "Growlithe": {"attaque": "Lance-Flammes", "puissance": 90},
    "Arcanine": {"attaque": "Lance-Flammes", "puissance": 90},
    "Poliwag": {"attaque": "Écume", "puissance": 40},
    "Poliwhirl": {"attaque": "Hydrocanon", "puissance": 110},
    "Poliwrath": {"attaque": "Poing-Karaté", "puissance": 75},
    "Abra": {"attaque": "Téléport", "puissance": 60},
    "Kadabra": {"attaque": "Psyko", "puissance": 90},
    "Alakazam": {"attaque": "Psyko", "puissance": 90},
    "Machop": {"attaque": "Poing-Karaté", "puissance": 75},
    "Machoke": {"attaque": "Poing-Karaté", "puissance": 75},
    "Machamp": {"attaque": "Poing-Karaté", "puissance": 75},
    "Bellsprout": {"attaque": "Tranch'Herbe", "puissance": 55},
    "Weepinbell": {"attaque": "Poudre Toxik", "puissance":  60},
    "Victreebel": {"attaque": "Tranch'Herbe", "puissance": 55},
    "Tentacool": {"attaque": "Ultrason", "puissance": 60},
    "Tentacruel": {"attaque": "Ultrason", "puissance": 60},
    "Geodude": {"attaque": "Poliroche", "puissance": 40},
    "Graveler": {"attaque": "Roulade", "puissance": 30},
    "Golem": {"attaque": "Éboulement", "puissance": 100},
    "Ponyta": {"attaque": "Pied Brûleur", "puissance": 50},
    "Rapidash": {"attaque": "Fatal-Foudre", "puissance": 65},
    "Slowpoke": {"attaque": "Amnésie", "puissance": 60},
    "Slowbro": {"attaque": "Psyko", "puissance": 90},
    "Magnemite": {"attaque": "Éclair", "puissance": 40},
    "Magneton": {"attaque": "Éclair", "puissance": 40},
    "Farfetch'd": {"attaque": "Picpic", "puissance": 65},
    "Doduo": {"attaque": "Picpic", "puissance": 65},
    "Dodrio": {"attaque": "Picpic", "puissance": 65},
    "Seel": {"attaque": "Ultrason", "puissance": 60},
    "Dewgong": {"attaque": "Ultrason", "puissance": 60},
    "Grimer": {"attaque": "Pistolet à O", "puissance": 40},
    "Muk": {"attaque": "Pistolet à O", "puissance": 40},
    "Shellder": {"attaque": "Pistolet à O", "puissance": 40},
    "Cloyster": {"attaque": "Pistolet à O", "puissance": 40},
    "Gastly": {"attaque": "Ultrason", "puissance": 60},
    "Haunter": {"attaque": "Ultrason", "puissance": 60},
    "Gengar": {"attaque": "Ultrason", "puissance": 60},
    "Onix": {"attaque": "Jet-Pierres", "puissance": 40},
    "Drowzee": {"attaque": "Ultrason", "puissance": 60},
    "Hypno": {"attaque": "Ultrason", "puissance": 60},
    "Krabby": {"attaque": "Pince-Masse", "puissance": 75},
    "Kingler": {"attaque": "Pince-Masse", "puissance": 75},
    "Voltorb": {"attaque": "Chargeur", "puissance": 40},
    "Electrode": {"attaque": "Chargeur", "puissance": 40},
    "Exeggcute": {"attaque": "Ultrason", "puissance": 60},
    "Exeggutor": {"attaque": "Tranch'Herbe", "puissance": 55},
    "Cubone": {"attaque": "Osmerang", "puissance": 50},
    "Marowak": {"attaque": "Osmerang", "puissance": 50},
    "Hitmonlee": {"attaque": "Ultimapoing", "puissance": 85},
    "Hitmonchan": {"attaque": "Ultimawashi", "puissance": 85},
    "Lickitung": {"attaque": "Fouet Lianes", "puissance": 45},
    "Koffing": {"attaque": "Pistolet à O", "puissance": 40},
    "Weezing": {"attaque": "Pistolet à O", "puissance": 40},
    "Rhyhorn": {"attaque": "Anti-air", "puissance": 40},
    "Rhydon": {"attaque": "Fracass'Tête", "puissance": 80},
    "Chansey": {"attaque": "Métronome", "puissance": 60},
    "Tangela": {"attaque": "Tranch'Herbe", "puissance": 55},
    "Kangaskhan": {"attaque": "Morsure", "puissance": 60},
    "Horsea": {"attaque": "Pistolet à O", "puissance": 40},
    "Seadra": {"attaque": "Hydrocanon", "puissance": 110},
    "Goldeen": {"attaque": "Tourniquet", "puissance": 65},
    "Seaking": {"attaque": "Tourniquet", "puissance": 65},
    "Staryu": {"attaque": "Pistolet à O", "puissance": 40},
    "Starmie": {"attaque": "Psyko", "puissance": 90},
    "Mr. Mime": {"attaque": "Barrière", "puissance": 60},
    "Scyther": {"attaque": "Coup d'Boule", "puissance": 65},
    "Jynx": {"attaque": "Blizzard", "puissance": 110},
    "Electabuzz": {"attaque": "Éclair", "puissance": 40},
    "Magmar": {"attaque": "Lance-Flammes", "puissance": 90},
    "Pinsir": {"attaque": "Tranche", "puissance": 70},
    "Tauros": {"attaque": "Morsure", "puissance": 60},
    "Magikarp": {"attaque": "Trempette", "puissance": 15},
    "Gyarados": {"attaque": "Ultralaser", "puissance": 150},
    "Lapras": {"attaque": "Blizzard", "puissance": 110},
    "Ditto": {"attaque": "Transform", "puissance": 60},
    "Eevee": {"attaque": "Mimi-Queue", "puissance": 40},
    "Vaporeon": {"attaque": "Hydrocanon", "puissance": 110},
    "Jolteon": {"attaque": "Tonnerre", "puissance": 90},
    "Flareon": {"attaque": "Lance-Flammes", "puissance": 90},
    "Porygon": {"attaque": "Psyko", "puissance": 90},
    "Omanyte": {"attaque": "Ultrason", "puissance": 60},
    "Omastar": {"attaque": "Ultrason", "puissance": 60},
    "Kabuto": {"attaque": "Griffe", "puissance": 40},
    "Kabutops": {"attaque": "Poing-Karaté", "puissance": 75},
    "Aerodactyl": {"attaque": "Vol", "puissance": 90},
    "Snorlax": {"attaque": "Écrasement", "puissance": 85},
    "Articuno": {"attaque": "Blizzard", "puissance": 110},
    "Zapdos": {"attaque": "Tonnerre", "puissance": 90},
    "Moltres": {"attaque": "Lance-Flammes", "puissance": 90},
    "Dratini": {"attaque": "Ouragan", "puissance": 40},
    "Dragonair": {"attaque": "Draco-Rage", "puissance": 80},
    "Dragonite": {"attaque": "Déflagration", "puissance": 110},
    "Mewtwo": {"attaque": "Amnésie", "puissance": 60},
    "Mew": {"attaque": "Métronome", "puissance": 60}
}





for pokemon, attaque in attaques_speciales_par_pokemon.items():
    pokemon_dict[pokemon]["attaque_speciale"] = attaque["attaque"]
    pokemon_dict[pokemon]["puissance"] = attaque["puissance"]

print(pokemon_dict)