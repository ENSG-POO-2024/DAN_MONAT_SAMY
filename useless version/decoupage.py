from PIL import Image
import numpy as np
import os

def decouper_image(image_path, taille_carre, dossier_sortie):
    # Charger l'image
    image = Image.open(image_path)
    largeur, hauteur = image.size
    
    # Convertir l'image en tableau numpy pour une manipulation plus facile
    image_array = np.array(image)
    
    # Calculer le nombre de lignes et de colonnes de carrés
    nb_lignes = hauteur // taille_carre
    nb_colonnes = largeur // taille_carre
    compteur = 1
    
    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(dossier_sortie, exist_ok=True)
    
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            # Découper le carré
            x0 = j * taille_carre
            y0 = i * taille_carre
            x1 = x0 + taille_carre
            y1 = y0 + taille_carre
            sous_image = image_array[y0:y1, x0:x1, :]
            
            # Enregistrer la sous-image dans le dossier de sortie
            nom_fichier = os.path.join(dossier_sortie, f"{compteur}.png")
            compteur += 1
            sous_image = Image.fromarray(sous_image)
            sous_image.save(nom_fichier)
            
            print(f"Sous-image {nom_fichier} enregistrée.")
            
# Chemin vers l'image à découper
chemin_image = "/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/pokemon_Combat/back.png"

# Taille des carrés
taille_carre = 64 # Vous pouvez ajuster cette valeur selon votre besoin

# Dossier de sortie
dossier_sortie = "/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/pokemon_Combat/out"

# Appeler la fonction pour découper l'image
decouper_image(chemin_image, taille_carre, dossier_sortie)
