import matplotlib.pyplot as plt
import numpy as np
import random
from heapq import heappush, heappop

# Générer un labyrinthe avec les dimensions spécifiées
def generate_maze(width, height):
    maze = np.zeros((height, width))

    # Placer des murs dans toutes les cellules paires
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            maze[i, j] = 1

    # Créer des passages entre les cellules paires
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            if i > 0:
                # Créer un passage vers le haut ou la gauche
                if random.randint(0, 1) == 0:
                    maze[i - 1, j] = 1
                else:
                    maze[i, j - 1] = 1
            elif j > 0:
                # Créer un passage vers la gauche
                maze[i, j - 1] = 1

    return maze

# Afficher le labyrinthe avec les points de départ et d'arrivée, ainsi que le chemin s'il est fourni
def display_maze(maze, start_point, end_point, path=None):
    plt.figure(figsize=(8, 8))
    plt.imshow(maze, cmap='binary_r', interpolation='nearest')
    plt.xticks([])
    plt.yticks([])

    # Afficher le point de départ (en vert)
    plt.scatter(start_point[0], start_point[1], color='green', s=100, marker='o', edgecolors='black')

    # Afficher le point d'arrivée (en rouge)
    plt.scatter(end_point[0], end_point[1], color='red', s=100, marker='o', edgecolors='black')

    # Afficher le chemin s'il est fourni (en bleu)
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_x, path_y, color='blue', linewidth=2)

    plt.show()

# Implémenter l'algorithme de Dijkstra pour trouver le chemin le plus court
def dijkstra(maze, start, end):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    heap = [(0, start, [])]
    visited = set()

    while heap:
        cost, current, path = heappop(heap)
        if current == end:
            return path + [current]
        if current in visited:
            continue
        visited.add(current)
        for dx, dy in directions:
            x, y = current[0] + dx, current[1] + dy
            if 0 <= x < maze.shape[1] and 0 <= y < maze.shape[0] and maze[y, x] == 1:
                heappush(heap, (cost + 1, (x, y), path + [current]))
    return None


def is_maze_possible(maze, start, end):
    # Effectue un algorithme de remplissage par diffusion (flood-fill) simple à partir du point de départ
    # Si le point d'arrivée est atteignable à partir du point de départ, retourne True
    # Sinon, retourne False

    stack = [start]  # Initialise une pile avec le point de départ
    visited = set()  # Initialise un ensemble pour enregistrer les points visités

    while stack:
        current = stack.pop()  # Récupère le dernier élément de la pile
        if current == end:
            return True  # Si le point actuel est le point d'arrivée, le labyrinthe est possible
        if current in visited:
            continue  # Si le point actuel a déjà été visité, passe au suivant
        visited.add(current)  # Ajoute le point actuel à l'ensemble des points visités
        # Parcourt les directions (haut, bas, gauche, droite)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x, y = current[0] + dx, current[1] + dy  # Calcule les coordonnées du voisin
            # Vérifie si les coordonnées sont valides et si le voisin est un mur
            if 0 <= x < maze.shape[1] and 0 <= y < maze.shape[0] and maze[y, x] == 1:
                stack.append((x, y))  # Ajoute le voisin à la pile pour exploration ultérieure

    return False  # Si le point d'arrivée n'est pas atteignable, le labyrinthe est impossible


if __name__ == "__main__":
    width = int(input("Enter the width of the maze: "))
    height = int(input("Enter the height of the maze: "))
    maze = generate_maze(width, height)

    start_point = (random.randint(0, width - 1), random.randint(0, height - 1))
    end_point = (random.randint(0, width - 1), random.randint(0, height - 1))

    while maze[start_point[1], start_point[0]] != 1 or maze[end_point[1], end_point[0]] != 1:
        start_point = (random.randint(0, width - 1), random.randint(0, height - 1))
        end_point = (random.randint(0, width - 1), random.randint(0, height - 1))

    if is_maze_possible(maze, start_point, end_point):
        path = dijkstra(maze, start_point, end_point)
        if path:
            print("Start Point:", start_point)
            print("End Point:", end_point)
            print("Shortest Path:", path)
            display_maze(maze, start_point, end_point, path)
    else:
        print("The generated maze is impossible. Please try again.")