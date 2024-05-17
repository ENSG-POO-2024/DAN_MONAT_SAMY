import matplotlib.pyplot as plt
import pandas as pd
import re

data = pd.read_csv('data/pokemon_coordinates_modified.csv')





# Créer un dictionnaire pour stocker les coordonnées de chaque Pokémon
pokemon_coordinates = {}

# Remplir le dictionnaire avec les données
for index, row in data.iterrows():
    pokemon_name = row['pokemon']
    pokemon_coord = row['coord_x'], row['coord_y']
    pokemon_coordinates[pokemon_coord] = pokemon_name



# Charger les données à partir du fichier CSV
pokemon_data = pd.read_csv('data/pokemon_first_gen.csv')

# Créer un dictionnaire pour stocker les données de chaque Pokémon
pokemon_dict = {}

# Remplir le dictionnaire avec les données
for index, row in pokemon_data.iterrows():
    pokemon_id = row['Name']
    pokemon_info = {
        'Numero':row['#'],
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
        'Legendary': row['Legendary'],
        'Niveau':'',
        'Evolution':''
    }
    pokemon_dict[pokemon_id] = pokemon_info
pokemon_dict = {nom: {cle: [valeur, valeur] if cle == 'HP' else valeur for cle, valeur in details.items()} for nom, details in pokemon_dict.items()}

#mise en place du système de niveau et d'évolution dans le dictionnaire
liste=[20,30,40,20,30,40,20,30,40,20,30,40,20,30,40,20,30,40,20,30,20,30,20,30,20,30,20,30,20,30,40,20,30,40,20,30,20,30,20,30,20,30,20,30,40,20,30,20,30,20,30,20,30,20,30,20,30,20,30,20,30,40,20,30,40,20,30,40,20,30,40,20,30,20,30,40,20,30,20,30,20,30,30,20,30,20,30,20,30,20,30,20,30,40,30,20,30,20,30,20,30,20,30,20,30,30,30,30,20,30,20,30,30,30,30,20,30,20,30,20,30,30,30,30,30,30,30,30,20,30,30,30,20,30,30,30,30,20,30,20,30,30,30,50,50,50,20,30,40,50,50]
for i, (pokemon, niveau) in enumerate(zip(pokemon_dict.keys(), liste)):
    pokemon_dict[pokemon]['Niveau'] = niveau
evolutions_liste = [2,1,0,2,1,0,2,1,0,2,1,0,2,1,0,2,1,0,3,0,3,0,3,0,3,0,3,0,2,1,0,2,1,0,3,0,3,0,3,0,3,0,2,1,0,3,0,3,0,3,0,3,0,3,0,3,0,3,0,2,1,0,2,1,0,2,1,0,2,1,0,3,0,2,1,0,3,0,3,0,3,0,0,3,0,3,0,3,0,3,0,2,1,0,0,3,0,3,0,3,0,3,0,3,0,0,0,0,0,3,0,3,0,0,0,0,3,0,3,0,3,0,0,0,0,0,0,0,0,3,0,0,0,3,0,0,0,0,3,0,3,0,0,0,0,0,0,2,1,0,0,0]

for i, (pokemon, evolution) in enumerate(zip(pokemon_dict.keys(), evolutions_liste)):
    pokemon_dict[pokemon]['Evolution'] = evolution




#ajout des attaques spéciales au dictionnaire
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



pokemons_liste = [
    "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard",
    "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree",
    "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata",
    "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu",
    "Sandshrew", "Sandslash", "Nidoran♀", "Nidorina", "Nidoqueen", "Nidoran♂",
    "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales",
    "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume",
    "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth",
    "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine",
    "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop",
    "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool",
    "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke",
    "Slowbro", "Magnemite", "Magneton", "Farfetch'd", "Doduo", "Dodrio", "Seel",
    "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter",
    "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode",
    "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan",
    "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela",
    "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie",
    "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros",
    "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon",
    "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl",
    "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite",
    "Mewtwo", "Mew"
]

#dictionnaire servant au système de niveau 
exp_niveau_pokemon = {
    0: 1,
    100: 2,
    300: 3,
    600: 4,
    1000: 5,
    1500: 6,
    2100: 7,
    2800: 8,
    3600: 9,
    4500: 10,
    5500: 11,
    6600: 12,
    7800: 13,
    9100: 14,
    10500: 15,
    12000: 16,
    13600: 17,
    15300: 18,
    17100: 19,
    19000: 20,
    21000: 21,
    23100: 22,
    25300: 23,
    27600: 24,
    30000: 25,
    32500: 26,
    35100: 27,
    37800: 28,
    40600: 29,
    43500: 30,
    46500: 31,
    49600: 32,
    52800: 33,
    56100: 34,
    59500: 35,
    63000: 36,
    66600: 37,
    70300: 38,
    74100: 39,
    78000: 40,
    82000: 41,
    86100: 42,
    90300: 43,
    94600: 44,
    99000: 45,
    103500: 46,
    108100: 47,
    112800: 48,
    117600: 49,
    122500: 50
}

exp_necessaire_par_niveau = [
    0,      # Niveau 1
    100,    # Niveau 2
    300,    # Niveau 3
    600,    # Niveau 4
    1000,   # Niveau 5
    1500,   # Niveau 6
    2100,   # Niveau 7
    2800,   # Niveau 8
    3600,   # Niveau 9
    4500,   # Niveau 10
    5500,   # Niveau 11
    6600,   # Niveau 12
    7800,   # Niveau 13
    9100,   # Niveau 14
    10500,  # Niveau 15
    12000,  # Niveau 16
    13600,  # Niveau 17
    15300,  # Niveau 18
    17100,  # Niveau 19
    19000,  # Niveau 20
    21000,  # Niveau 21
    23100,  # Niveau 22
    25300,  # Niveau 23
    27600,  # Niveau 24
    30000,  # Niveau 25
    32500,  # Niveau 26
    35100,  # Niveau 27
    37800,  # Niveau 28
    40600,  # Niveau 29
    43500,  # Niveau 30
    46500,  # Niveau 31
    49600,  # Niveau 32
    52800,  # Niveau 33
    56100,  # Niveau 34
    59500,  # Niveau 35
    63000,  # Niveau 36
    66600,  # Niveau 37
    70300,  # Niveau 38
    74100,  # Niveau 39
    78000,  # Niveau 40
    82000,  # Niveau 41
    86100,  # Niveau 42
    90300,  # Niveau 43
    94600,  # Niveau 44
    99000,  # Niveau 45
    103500, # Niveau 46
    108100, # Niveau 47
    112800, # Niveau 48
    117600, # Niveau 49
    122500  # Niveau 50
]

exp_gagne_par_niveau = {
    1: 50,
    2: 100,
    3: 150,
    4: 200,
    5: 250,
    6: 300,
    7: 350,
    8: 400,
    9: 450,
    10: 500,
    11: 550,
    12: 600,
    13: 650,
    14: 700,
    15: 750,
    16: 800,
    17: 850,
    18: 900,
    19: 950,
    20: 1000,
    21: 1050,
    22: 1100,
    23: 1150,
    24: 1200,
    25: 1250,
    26: 1300,
    27: 1350,
    28: 1400,
    29: 1450,
    30: 1500,
    31: 1550,
    32: 1600,
    33: 1650,
    34: 1700,
    35: 1750,
    36: 1800,
    37: 1850,
    38: 1900,
    39: 1950,
    40: 2000,
    41: 2050,
    42: 2100,
    43: 2150,
    44: 2200,
    45: 2250,
    46: 2300,
    47: 2350,
    48: 2400,
    49: 2450,
    50: 2500
}