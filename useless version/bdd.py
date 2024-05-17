import pandas as pd

def merge_data(pokemon_file, coordinates_file, output_file):
    # Charger les données des fichiers CSV
    pokemon_data = pd.read_csv(pokemon_file)
    coordinates_data = pd.read_csv(coordinates_file,sep=';')

    # Fusionner les deux jeux de données en fonction du nom du Pokémon
    merged_data = pd.merge(pokemon_data, coordinates_data, left_on='#', right_on='#')
    
    # Sélectionner les colonnes pertinentes
    merged_data = merged_data[['#', 'pokemon', 'coord_x', 'coord_y','Name']]
    
    # Enregistrer les données fusionnées dans un fichier CSV
    merged_data.to_csv(output_file, index=False)



merge_data('data/merged_data.csv', 'data/pokemons_fr.csv', 'data/merged_data_fr.csv')