import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,QProgressBar, QScrollArea, QListView, QFrame,QMainWindow, QDialog, QRadioButton, QCheckBox
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QMessageBox,QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar, QScrollArea, QListView, QFrame
import random
import csv
from pokedex import PokemonList
from fight import FightWindow,Dresseur,Starter,Pokemons,Soins






class GameBoard(QDialog):
    def __init__(self,selected_pokemon=[],name_dresseur="Entrez nom Dresseur"):
        """
        Initialise le plateau de jeu avec les Pokémon sélectionnés et le nom du dresseur.
        
        Parameters:
            selected_pokemon (list): Liste des Pokémon sélectionnés.
            name_dresseur (str): Nom du dresseur.
        """
        super().__init__()
        self.showFullScreen()
        self.starter_data = selected_pokemon
        self.pokemon_list = PokemonList("data/pokemons_fr.csv")
        self.pokemon_list.add_starters(selected_pokemon)  # Appel de la méthode pour ajouter les starters
        self.name_dresseur = name_dresseur
        
        if self.name_dresseur == "Entrez nom Dresseur":
            self.name_dresseur = "Red"
            self.dresseur = Dresseur(self.name_dresseur)  # Initialisation de self.dresseur
        else:
            self.dresseur = Dresseur(self.name_dresseur)
        
        
        
        if selected_pokemon==[]:
            
            Starter(self.dresseur, 'Charmander', 'Bulbasaur', 'Squirtle')
        else:
            Starter(self.dresseur, selected_pokemon[0]['Name'], selected_pokemon[1]['Name'], selected_pokemon[2]['Name'])
            #self.dresseur.ajouter_pokemon_equipe(Pokemons('Charizard'))
 
        

        
        self.square_size = 63  # Taille de chaque carré (plus gros pour le zoom)
        self.camera_size = 13  # Taille de la caméra (20x20 )
        self.board_size = 100  # Taille du plateau (100x100)
        self.direction = "right"  # Direction initiale
        
        self.white_square_pos = [0, 0]  # Position initiale de la case blanche (coin supérieur gauche)
        
        self.road_image = QPixmap("CODE/image tiles/road.png").scaled(self.square_size, self.square_size)  
        self.heal_zone = QPixmap("CODE/image tiles/heal_zone.png").scaled(self.square_size, self.square_size)
        self.grass_image = QPixmap("CODE/image tiles/grass.png").scaled(self.square_size, self.square_size) 
        self.tree_image = QPixmap("CODE/image tiles/arbre.png").scaled(self.square_size, self.square_size)  
        self.tall_grass_image = QPixmap("CODE/image tiles/tall_grass.png").scaled(self.square_size, self.square_size)
        self.tall_grass_div_image = QPixmap("CODE/image tiles/tall_grass.png").scaled(self.square_size, self.square_size)
        
        self.setStyleSheet("background-color: lightblue;")  # Changer la couleur de fond
        
        # Générer la grille une seule fois au démarrage
        self.grid, self.tree_positions ,self.heal_positions= self.generate_grid()

        # Ajouter un attribut pour stocker les coordonnées de chaque case
        self.coordinates = [[(i, j) for j in range(self.board_size)] for i in range(self.board_size)]

        # Charger les images du personnage
        self.player_images = {
            "left": QPixmap("CODE/image tiles/left.png").scaled(self.square_size, self.square_size),
            "right": QPixmap("CODE/image tiles/right.png").scaled(self.square_size, self.square_size),
            "up": QPixmap("CODE/image tiles/top.png").scaled(self.square_size, self.square_size),
            "down": QPixmap("CODE/image tiles/bot.png").scaled(self.square_size, self.square_size)
        }
        
        self.load_coordinates("data/pokemon_coordinates_modified.csv")

        self.initUI()
        
    def load_coordinates(self, file_path):
        """
        Charge les coordonnées des Pokémon depuis un fichier CSV.
        
        Parameters:
            file_path (str): Chemin du fichier CSV contenant les coordonnées des Pokémon.
        """
        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    x, y = int(row['coord_x']), int(row['coord_y'])
                    if 0 <= x < self.board_size and 0 <= y < self.board_size:
                        self.grid[x][y] = 'tall_grass'
        except FileNotFoundError:
            print("Fichier CSV introuvable.")

    

    def initUI(self):
        """
        Initialise l'interface utilisateur du plateau de jeu.
        """
        self.setWindowTitle('Game Board')
        self.setGeometry(100, 100, 800, 800)  # Taille de la fenêtre
        
        layout = QVBoxLayout(self)
        
        # Créer le bouton "Open Pokedex"
        self.button_open_pokedex = QPushButton("Pokedex")
        self.button_open_pokedex.clicked.connect(self.open_pokedex_window)
        layout.addWidget(self.button_open_pokedex, alignment=Qt.AlignBottom)  # Aligner le bouton en bas de la fenêtre
        
        self.setLayout(layout)
        
    def open_pokedex_window(self):
        """
        Ouvre la fenêtre du Pokédex.
        """
        pokemon_list_data = self.pokemon_list.pokemon_list  # Accéder à la liste de Pokémon à l'intérieur de l'objet PokemonList
        pokedex_window = PokedexUI(pokemon_list_data)
        pokedex_window.exec_()
        
    def generate_grid(self):
        """
        Génère la grille du plateau de jeu avec des éléments comme les routes, les arbres et les herbes hautes.
        
        Returns:
            tuple: La grille générée, les positions des arbres et les positions des zones de soins.
        """
        
        TOP_ZONE_SIZE = 1  
        grid = [['grass' for _ in range(self.board_size)] for _ in range(self.board_size)]  # Commencez par remplir tout de herbe

        # Charger les positions des herbes hautes depuis le fichier CSV
        tall_grass_positions = []
        try:
            with open("data/pokemon_coordinates_modified.csv", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    x, y = int(row['coord_x']), int(row['coord_y'])
                    if 0 <= x < self.board_size and 0 <= y < self.board_size:
                        tall_grass_positions.append((x, y))
        except FileNotFoundError:
            print("Fichier CSV introuvable.")

        # Placez les herbes hautes sur la grille aux positions spécifiées
        for x, y in tall_grass_positions:
            grid[x][y] = 'tall_grass'
            for i in range(x - TOP_ZONE_SIZE, x + TOP_ZONE_SIZE + 1):
                for j in range(y - TOP_ZONE_SIZE, y + TOP_ZONE_SIZE + 1):
                    if 0 <= i < self.board_size and 0 <= j < self.board_size and (i, j) != (x, y):
                             grid[i][j] = 'tall_grass_div'

        # Placez aléatoirement les routes et les arbres là où il n'y a pas d'herbes hautes
        tree_positions = []
        heal_positions = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if grid[i][j] != 'tall_grass' and grid[i][j] != 'tall_grass_div':
                    if random.random() < 0.4:  
                        grid[i][j] = 'road'
                    elif random.random() < 0.2:  
                        tree_positions.append((i, j))
                    
                    elif random.random() < 0.03:
                        heal_positions.append((i, j))
                        
                    else:
                        grid[i][j] = 'grass' 

        return grid, tree_positions, heal_positions



        
    def paintEvent(self, event):
        """
        Gère l'événement de peinture pour dessiner le plateau de jeu.
        
        Parameters:
            event (QPaintEvent): L'événement de peinture.
        """
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0))  # Couleur des lignes

        # Calculer les coordonnées du coin supérieur gauche de la zone de caméra
        camera_top_left_x = max(0, self.white_square_pos[0] - self.camera_size // 2)
        camera_top_left_y = max(0, self.white_square_pos[1] - self.camera_size // 2)

        # Centrer la zone de caméra dans la fenêtre
        camera_top_left_x = max(0, min(camera_top_left_x, self.board_size - self.camera_size))
        camera_top_left_y = max(0, min(camera_top_left_y, self.board_size - self.camera_size))

        # Calculer la position de départ pour dessiner la grille centrée dans la fenêtre
        start_x = (self.width() - self.camera_size * self.square_size) // 2
        start_y = (self.height() - self.camera_size * self.square_size) // 2

        # Dessiner les carrés dans la zone de caméra
        for i in range(camera_top_left_x, min(camera_top_left_x + self.camera_size, self.board_size)):
            for j in range(camera_top_left_y, min(camera_top_left_y + self.camera_size, self.board_size)):
                x = start_x + (i - camera_top_left_x) * self.square_size
                y = start_y + (j - camera_top_left_y) * self.square_size

                # Dessiner d'abord l'herbe sur toute la caméra
                painter.drawPixmap(x, y, self.grass_image)

                # Dessiner les arbres
                for tree_x, tree_y in self.tree_positions:
                    if (tree_x, tree_y) == (i, j):
                        painter.drawPixmap(x, y, self.tree_image)
                        
                for heal_x, heal_y in self.heal_positions:
                    if (heal_x, heal_y) == (i, j):
                        painter.drawPixmap(x, y, self.heal_zone)
                        
                

        # Dessiner les autres éléments
        for i in range(camera_top_left_x, min(camera_top_left_x + self.camera_size, self.board_size)):
            for j in range(camera_top_left_y, min(camera_top_left_y + self.camera_size, self.board_size)):
                x = start_x + (i - camera_top_left_x) * self.square_size
                y = start_y + (j - camera_top_left_y) * self.square_size

                if self.grid[i][j] == 'tall_grass':
                    painter.drawPixmap(x, y, self.tall_grass_image)
                elif self.grid[i][j] == 'tall_grass_div':
                    painter.drawPixmap(x, y, self.tall_grass_div_image)
                elif self.grid[i][j] == 'road':
                    painter.drawPixmap(x, y, self.road_image)
                elif self.grid[i][j] == 'grass':
                
                    continue  # Déjà dessiné l'herbe, on passe à la suivante

        # Dessiner le personnage
        player_x = start_x + (self.white_square_pos[0] - camera_top_left_x) * self.square_size
        player_y = start_y + (self.white_square_pos[1] - camera_top_left_y) * self.square_size
        painter.drawPixmap(player_x, player_y, self.player_images[self.direction])



    def keyPressEvent(self, event):
        """
        Gère les événements liés aux touches du clavier pour le déplacement du joueur.

        Args:
            event (QKeyEvent): Événement de touche pressée.
        """
        key = event.key()
        if key == Qt.Key_Up:
            self.direction = "up"
            new_pos = (self.white_square_pos[0], self.white_square_pos[1] - 1)
            self.try_move_player(new_pos)
        elif key == Qt.Key_Down:
            self.direction = "down"
            new_pos = (self.white_square_pos[0], self.white_square_pos[1] + 1)
            self.try_move_player(new_pos)
        elif key == Qt.Key_Left:
            self.direction = "left"
            new_pos = (self.white_square_pos[0] - 1, self.white_square_pos[1])
            self.try_move_player(new_pos)
        elif key == Qt.Key_Right:
            self.direction = "right"
            new_pos = (self.white_square_pos[0] + 1, self.white_square_pos[1])
            self.try_move_player(new_pos)

    def is_valid_move(self, pos):
        """
        Vérifie si un déplacement vers une position donnée est valide.

        Args:
            pos (tuple): Position à vérifier.

        Returns:
            bool: True si le déplacement est valide, False sinon.
        """
        if 0 <= pos[0] < self.board_size and 0 <= pos[1] < self.board_size:
            if (pos[0], pos[1]) in self.tree_positions:
                return False  # Le joueur ne peut pas se déplacer sur un arbre
            if self.grid[pos[0]][pos[1]] == 'tall_grass':
                pass
            return True
        return False
    
    def get_pokemon_name(self, pos):
        """
        Récupère le nom d'un Pokémon à partir de sa position sur le plateau.

        Args:
            pos (tuple): Position du Pokémon.

        Returns:
            str: Nom du Pokémon.
        """
        try:
            with open("data/merged_data_fr.csv", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    x, y = int(row['coord_x']), int(row['coord_y'])
                    if (x, y) == pos:
                        return row['pokemon'], row['#']
        except FileNotFoundError:
            print("Fichier CSV introuvable.")
        return "Pokemon Inconnu"
    
    
    
    def show_combat_ui(self,pos):
        """
        Affiche l'interface utilisateur du combat avec un Pokémon sauvage.

        Args:
            pos (tuple): Position du Pokémon sauvage sur le plateau.
        """
        combat_ui = FightWindow(pokemons=None,dresseur=self.dresseur,pos=pos)
        combat_ui.exec_()

    def get_pokemon_info(self, pos):
        """
        Récupère les informations d'un Pokémon à partir de sa position sur le plateau.

        Args:
            pos (tuple): Position du Pokémon.

        Returns:
            tuple: Numéro et nom du Pokémon.
        """
        try:
            with open("data/merged_data_fr.csv", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    x, y = int(row['coord_x']), int(row['coord_y'])
                    if (x, y) == pos:
                        return row['#'], row['pokemon']
        except FileNotFoundError:
            print("Fichier CSV introuvable.")
        return None, "Pokemon Inconnu"

                
                
    def try_move_player(self, new_pos):
        """
        Tente de déplacer le joueur vers une nouvelle position.

        Args:
            new_pos (tuple): Nouvelle position du joueur.
        """
        if self.is_valid_move(new_pos):
            self.move_player(new_pos)
            if (new_pos[0], new_pos[1]) in self.heal_positions:
                Soins(self.dresseur)
                print(self.dresseur.pokemon_equipe[0].stats["HP"][0])
                QMessageBox.information(self, "Case de Soins", "Vos pokémons ont été soignés.")
            if self.grid[new_pos[0]][new_pos[1]] == 'tall_grass':
                pokemon_number, pokemon_name = self.get_pokemon_info(new_pos)
                if pokemon_number and pokemon_name: 
                    self.show_combat_ui(new_pos)
                    self.pokemon_list.modify_pokemon(pokemon_number, pokemon_name, f"CODE/image tiles/pokemon_Combat/front/{pokemon_number}.png")
                    self.grid[new_pos[0]][new_pos[1]] = 'tall_grass_div'
                    


    def move_player(self, new_pos):
        """
        Déplace le joueur vers une nouvelle position.

        Args:
            new_pos (tuple): Nouvelle position du joueur.
        """
        self.white_square_pos = new_pos
        self.update()


         


def get_first_gen_pokemon_list(csv_file_path):
    """
    Récupère une liste des Pokémon de la première génération à partir d'un fichier CSV.

    Args:
        csv_file_path (str): Chemin d'accès vers le fichier CSV contenant les données des Pokémon.

    Returns:
        list: Liste des noms des Pokémon de la première génération.
    """
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        pokemon_list = []
        for row in reader:
            if row[-1] == '1':
                pokemon_str = f"{row[0]} - {row[1]}"
                pokemon_list.append(pokemon_str)
    return pokemon_list


class PokedexUI(QDialog):
   
    def __init__(self, pokemon_list):
        """
        Initialise une instance de la classe PokedexUI.

        Args:
            pokemon_list (list): Liste des Pokémon à afficher dans le Pokédex.
        """
        super().__init__()
         # Afficher le nombre de Pokémon découverts / total dans le titre de la fenêtre
        print(pokemon_list)
        discovered_pokemon_count = sum(1 for pokemon in pokemon_list if pokemon['name'] != "????")
        total_pokemon_count = len(pokemon_list)
        self.setWindowTitle(f"Pokédex ({discovered_pokemon_count}/{total_pokemon_count})")
        
        self.resize(300, 500) 
        # Créer un layout vertical pour contenir les étiquettes et les images
        layout = QVBoxLayout()
        
        # Créer un widget de défilement
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Rendre le widget de défilement redimensionnable
        
        # Créer un widget qui contiendra le layout vertical des étiquettes et des images
        content_widget = QWidget(scroll_area)
        content_layout = QVBoxLayout(content_widget)
        
        # Ajouter une étiquette pour chaque Pokémon dans la liste
        for pokemon in pokemon_list:
            # Créer une étiquette pour afficher le nom du Pokémon
            pokemon_label = QLabel(f"n° {pokemon['number']}     Nom: {pokemon['name']}")
            
            # Créer une étiquette pour afficher l'image du Pokémon
            pokemon_image_label = QLabel()
            pokemon_image_label.setPixmap(QPixmap(pokemon['image_name']))  # Définir l'image du Pokémon
            
            # Créer un layout horizontal pour organiser l'étiquette du Pokémon et son image côte à côte
            pokemon_layout = QHBoxLayout()
            pokemon_layout.addWidget(pokemon_label)
            pokemon_layout.addWidget(pokemon_image_label)
            
            # Ajouter le layout horizontal au layout vertical du contenu
            content_layout.addLayout(pokemon_layout)
        
        # Définir le layout du contenu comme le layout du widget de défilement
        content_widget.setLayout(content_layout)
        
        # Définir le widget de contenu du widget de défilement
        scroll_area.setWidget(content_widget)
        
        # Ajouter le widget de défilement au layout vertical principal
        layout.addWidget(scroll_area)
        
        # Définir le layout principal de la fenêtre
        self.setLayout(layout)



    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_board = GameBoard()  # Passer une référence à l'instance de Pokedex
    game_board.show()
    sys.exit(app.exec_())
