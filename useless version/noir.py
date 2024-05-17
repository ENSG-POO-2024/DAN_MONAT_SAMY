import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,QProgressBar, QScrollArea, QListView, QFrame
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QMessageBox,QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QProgressBar
import random
import csv


class HighGrassWindow(QDialog):
    def __init__(self, pokemon_data):
        super().__init__()
        self.setWindowTitle("COMBAT !!")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pokemon_data = pokemon_data
        
        layout = QVBoxLayout()
        
        # Ajouter un bouton pour fermer la fenêtre en haut de la fenêtre
        button_close = QPushButton("Fuir")
        button_close.clicked.connect(self.close)
        layout.addWidget(button_close, alignment=Qt.AlignTop)
        
        # Charger les images et les redimensionner si nécessaire
        pixmap_main = QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/pokemon_Combat/field.png")
        poke_att = QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/pokemon_Combat/back/1.png").scaled(300, 300)
        poke_def = QPixmap(f"/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/pokemon_Combat/front/{pokemon_data[1]}.png").scaled(250, 250)
        
        # Créer une nouvelle image qui sera la combinaison de toutes les images
        combined_pixmap = QPixmap(pixmap_main.size())
        combined_pixmap.fill(Qt.transparent)
        
        offset = -100
        # Dessiner les images principales et superposées sur l'image combinée
        painter = QPainter(combined_pixmap)
        painter.drawPixmap(0, 0, pixmap_main)
        painter.drawPixmap(70, combined_pixmap.height() - poke_att.height() + 80, poke_att)
        painter.drawPixmap(-140 + combined_pixmap.width() - poke_def.width(), 150, poke_def)
        painter.end()
        
        
        
        # Afficher l'image combinée dans un QLabel
        combined_label = QLabel()
        combined_label.setPixmap(combined_pixmap)
        
        # Créer un layout horizontal pour les boutons et l'image combinée
        hbox_layout = QHBoxLayout()
        
        # Ajouter un QLabel avec texte stylisé à gauche de l'image combinée
        label_left = QLabel("Gauche")
        label_left.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        label_left.setStyleSheet("font-size: 10px; color: blue;")
        label_left.setFixedSize(80, 30)  # Définir la taille du QLabel
        hbox_layout.addWidget(label_left)
        
        # Ajouter une barre de progression remplie à 70% sous le label "Gauche"
        progress_bar_left = QProgressBar()
        progress_bar_left.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        progress_bar_left.setValue(70)
        hbox_layout.addWidget(progress_bar_left)
        
        # Ajouter l'image combinée au centre
        hbox_layout.addWidget(combined_label)

        # Ajouter un QLabel avec texte stylisé à droite de l'image combinée
        label_right = QLabel(f"{pokemon_data[0]}")
        label_right.setAlignment(Qt.AlignTop)
        label_right.setFixedSize(80, 30)  # Définir la taille du QLabel
        label_right.setStyleSheet("font-size: 15px; color: black;")
        hbox_layout.addWidget(label_right)
        progress_bar_right = QProgressBar()
        progress_bar_right.setValue(70)
        hbox_layout.addWidget(progress_bar_right)
        
        # Ajouter le layout horizontal au layout principal
        layout.addLayout(hbox_layout)
        
        self.setLayout(layout)
        self.showFullScreen()
        QApplication.processEvents()


class GameBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.square_size = 50  # Taille de chaque carré (plus gros pour le zoom)
        self.camera_size = 10  # Taille de la caméra (20x20 )
        self.board_size = 100  # Taille du plateau (100x100)
        self.direction = "right"  # Direction initiale
        
        self.white_square_pos = [0, 0]  # Position initiale de la case blanche (coin supérieur gauche)
        
        self.road_image = QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/road.png").scaled(self.square_size, self.square_size)  
        self.grass_image = QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/grass.png").scaled(self.square_size, self.square_size) 
        self.tree_image = QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/arbre.png").scaled(self.square_size, self.square_size)  
        self.tall_grass_image = QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/tall_grass.png").scaled(self.square_size, self.square_size)
        self.tall_grass_div_image = QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/tall_grass.png").scaled(self.square_size, self.square_size)
        
        self.setStyleSheet("background-color: lightblue;")  # Changer la couleur de fond
        
        # Générer la grille une seule fois au démarrage
        self.grid, self.tree_positions = self.generate_grid()

        # Ajouter un attribut pour stocker les coordonnées de chaque case
        self.coordinates = [[(i, j) for j in range(self.board_size)] for i in range(self.board_size)]

        # Charger les images du personnage
        self.player_images = {
            "left": QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/left.png").scaled(self.square_size, self.square_size),
            "right": QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/right.png").scaled(self.square_size, self.square_size),
            "up": QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/top.png").scaled(self.square_size, self.square_size),
            "down": QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/bot.png").scaled(self.square_size, self.square_size)
        }
        
        self.load_coordinates("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/data/pokemon_coordinates_modified.csv")

        self.initUI()
        
    def load_coordinates(self, file_path):
        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    x, y = int(row['coord_x']), int(row['coord_y'])
                    if 0 <= x < self.board_size and 0 <= y < self.board_size:
                        self.grid[x][y] = 'tall_grass'
        except FileNotFoundError:
            print("Fichier CSV introuvable.")


    def open_pokedex(self):
        pokedex = Pokedex()
        pokedex.show()
        
    def initUI(self):
        self.setWindowTitle('Game Board')
        self.setGeometry(100, 100, 800, 800)  # Taille de la fenêtre
        
        # Créer le bouton "Open Pokedex"
        button_open_pokedex = QPushButton('Open Pokedex', self)
        button_open_pokedex.clicked.connect(self.open_pokedex)
        
        # Ajouter le bouton à la mise en page
        layout = QVBoxLayout(self)
        layout.addWidget(button_open_pokedex)

    def generate_grid(self):
        
        TOP_ZONE_SIZE = 1  
        grid = [['grass' for _ in range(self.board_size)] for _ in range(self.board_size)]  # Commencez par remplir tout de herbe

        # Charger les positions des herbes hautes depuis le fichier CSV
        tall_grass_positions = []
        try:
            with open("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/data/pokemon_coordinates_modified.csv", newline='') as csvfile:
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
        for i in range(self.board_size):
            for j in range(self.board_size):
                if grid[i][j] != 'tall_grass' and grid[i][j] != 'tall_grass_div':
                    if random.random() < 0.4:  
                        grid[i][j] = 'road'
                    elif random.random() < 0.2:  
                        tree_positions.append((i, j))
                    else:
                        grid[i][j] = 'grass' 

        return grid, tree_positions


    def paintEvent(self, event):
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
        if 0 <= pos[0] < self.board_size and 0 <= pos[1] < self.board_size:
            if (pos[0], pos[1]) in self.tree_positions:
                return False  # Le joueur ne peut pas se déplacer sur un arbre
            if self.grid[pos[0]][pos[1]] == 'tall_grass':
                pass
            return True
        return False
    
    def get_pokemon_name(self, pos):
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
    
    
    def show_high_grass_window(self, pokemon_name):
        high_grass_window = HighGrassWindow(pokemon_name)
        high_grass_window.exec_()

    def try_move_player(self, new_pos):
        if self.is_valid_move(new_pos):
            self.move_player(new_pos)
            if self.grid[new_pos[0]][new_pos[1]] == 'tall_grass':
                self.move_player(new_pos)
                pokemon_name = self.get_pokemon_name(new_pos)
                self.show_high_grass_window(pokemon_name)
                #self.show_high_grass_window()
    


    def move_player(self, new_pos):
        self.white_square_pos = new_pos
        self.update()

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Haute herbe")
        msg.setText("Vous avez trouvé de l'herbe haute !")
        msg.exec_()
         


def get_first_gen_pokemon_list(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        pokemon_list = []
        for row in reader:
            if row[-1] == '1':
                pokemon_str = f"{row[0]} - {row[1]}"
                pokemon_list.append(pokemon_str)
    return pokemon_list



class Pokedex(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Pokedex')
        
        self.setGeometry(100, 100, 400, 400)
        

        # Liste de Pokémon avec leurs numéros
        self.pokemon_list = get_first_gen_pokemon_list("data/pokemons_fr.csv")

        self.model = QStringListModel()
        self.model.setStringList(self.pokemon_list)

        self.list_view = QListView()
        self.list_view.setModel(self.model)

        self.label_header = QLabel(" n° - NOM")

        layout = QVBoxLayout()
        layout.addWidget(self.label_header)

        # Ajout d'un espacement vertical entre chaque ligne
        layout.addSpacing(5)

        # Ajouter les frames pour chaque Pokémon
        for pokemon in self.pokemon_list:
            frame = self.create_pokemon_frame(pokemon)
            layout.addWidget(frame)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        container = QWidget()
        container.setLayout(layout)
        scroll_area.setWidget(container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def create_pokemon_frame(self, pokemon):
        frame = QFrame()
        frame_layout = QHBoxLayout()

        # Ajouter le texte du Pokémon
        pokemon_label = QLabel(pokemon)
        frame_layout.addWidget(pokemon_label)

        # Récupérer le numéro de Pokémon
        pokemon_number = pokemon.split(' - ')[0]
        image_path = f"/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/pokemon_Combat/front/{pokemon_number}.png"

        # Charger l'image et l'afficher dans un QLabel
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            frame_layout.addWidget(image_label)

        frame.setLayout(frame_layout)
        return frame

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_board = GameBoard()
    game_board.show()
    sys.exit(app.exec_())
