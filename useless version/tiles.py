from PIL import Image
import os

def split_tiles(input_file, output_dir, tile_width, tile_height):
    # Ouvrir l'image d'entrée
    image = Image.open(input_file)

    # Assurer que le répertoire de sortie existe
    os.makedirs(output_dir, exist_ok=True)

    # Obtenir la taille de l'image
    width, height = image.size

    # Vérifier si l'image est divisée uniformément en tuiles
    if width % tile_width != 0 or height % tile_height != 0:
        print("Erreur: La taille des tuiles n'est pas compatible avec la taille de l'image.")
        return

    # Diviser l'image en tuiles et les sauvegarder dans le répertoire de sortie
    for y in range(0, height, tile_height):
        for x in range(0, width, tile_width):
            tile = image.crop((x, y, x + tile_width, y + tile_height))
            tile_name = f"tile_{x // tile_width}_{y // tile_height}.png"
            tile.save(os.path.join(output_dir, tile_name))

    print("Les tuiles ont été séparées avec succès.")

# Exemple d'utilisation
split_tiles("/Users/samy/Cours/tiles/tree_tiles.png", "output_tiles", 32, 32)  # Remplacez "tiles.png" par le chemin de votre fichier PNG de tiles
