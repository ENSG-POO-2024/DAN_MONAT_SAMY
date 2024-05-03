import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt, QPoint
import random


class GameBoard(QWidget):
    def __init__(self):
        super().__init__()

        self.square_size = 50  # Taille de chaque carré (plus gros pour le zoom)
        self.camera_size = 10  # Taille de la caméra (20x20)
        self.board_size = 100  # Taille du plateau (100x100)
        self.direction = "right"  # Direction initiale

        self.white_square_pos = [0, 0]  # Position initiale de la case blanche (coin supérieur gauche)
        self.road_image = QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/road.png").scaled(self.square_size, self.square_size)  # Charger l'image de route
        self.grass_image = QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/grass.png").scaled(self.square_size, self.square_size)  # Charger l'image d'herbe
        self.tree_image = QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/arbre.png").scaled(self.square_size, self.square_size)  # Charger l'image d'arbre

        # Charger les images du personnage
        self.player_images = {
            "left": QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/left.png").scaled(self.square_size, self.square_size),
            "right": QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/right.png").scaled(self.square_size, self.square_size),
            "up": QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/top.png").scaled(self.square_size, self.square_size),
            "down": QPixmap("/Users/samy/PROJET_POO_REAL/DAN_MONAT_SAMY/CODE/image tiles/bot.png").scaled(self.square_size, self.square_size)
        }

        # Générer la grille une seule fois au démarrage
        self.grid, self.tree_positions = self.generate_grid()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game Board')
        self.setGeometry(100, 100, 800, 800)  # Taille de la fenêtre

    def generate_grid(self):
        grid = [['road' for _ in range(self.board_size)] for _ in range(self.board_size)]  # Commencez par remplir tout de route
        tree_positions = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if random.random() < 0.8:  # Probabilité de 80% pour la route
                    grid[i][j] = 'grass'
                if grid[i][j] == 'grass' and random.random() < 0.2:  # Probabilité de 20% pour l'arbre sur l'herbe
                    tree_positions.append((i, j))
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
               
                # Dessiner l'image de route ou d'herbe selon la grille générée au démarrage
                if self.grid[i][j] == 'road':
                    painter.drawPixmap(x, y, self.road_image)
                elif self.grid[i][j] == 'grass':
                    painter.drawPixmap(x, y, self.grass_image)

                # Dessiner les arbres
                for tree_x, tree_y in self.tree_positions:
                    if (tree_x, tree_y) == (i, j):
                        painter.drawPixmap(x, y, self.tree_image)

        # Dessiner le personnage
        player_x = start_x + (self.white_square_pos[0] - camera_top_left_x) * self.square_size
        player_y = start_y + (self.white_square_pos[1] - camera_top_left_y) * self.square_size
        painter.drawPixmap(player_x, player_y, self.player_images[self.direction])


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            self.direction = "up"
            if self.white_square_pos[1] > 0 and (self.white_square_pos[0], self.white_square_pos[1] - 1) not in self.tree_positions:
                self.white_square_pos[1] -= 1
                self.direction = "up"
        elif key == Qt.Key_Down:
            self.direction = "down"
            if self.white_square_pos[1] < self.board_size - 1 and (self.white_square_pos[0], self.white_square_pos[1] + 1) not in self.tree_positions:
                self.white_square_pos[1] += 1
                self.direction = "down"
        elif key == Qt.Key_Left:
            self.direction = "left"
            if self.white_square_pos[0] > 0 and (self.white_square_pos[0] - 1, self.white_square_pos[1]) not in self.tree_positions:
                self.white_square_pos[0] -= 1
                self.direction = "left"
        elif key == Qt.Key_Right:
            self.direction = "right"
            if self.white_square_pos[0] < self.board_size - 1 and (self.white_square_pos[0] + 1, self.white_square_pos[1]) not in self.tree_positions:
                self.white_square_pos[0] += 1
                self.direction = "right"

        self.update()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    game_board = GameBoard()
    game_board.show()
    sys.exit(app.exec_())
