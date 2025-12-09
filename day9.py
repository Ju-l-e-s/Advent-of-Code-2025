# Advent of Code 2025 - Day 9
# ----------------------------------------------------------
# Contexte général :
# La liste d'entrée contient des coordonnées "x,y".
# PART ONE : calculer la plus grande aire possible d'un rectangle
#            défini par deux tuiles rouges.
# PART TWO : même logique, mais le rectangle doit rester dans une
#            zone autorisée (rouge/verte), ce qui nécessite de
#            vérifier s'il coupe les limites de la boucle.
# ----------------------------------------------------------

import sys

# ==========================================================
# 1. PARSING ET OUTILS DE BASE
# ==========================================================

def read_input(path: str) -> list[str]:
    """Lit les lignes non vides et renvoie ['x,y', ...]."""
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def parse_point(s: str) -> tuple[int, int]:
    """Convertit 'x,y' en tuple (x, y)."""
    x_str, y_str = s.split(",")
    return int(x_str), int(y_str)


def calc_area_part1(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """
    Aire brute en nombre de tuiles.
    Largeur = |x2 - x1| + 1
    Hauteur = |y2 - y1| + 1
    """
    w = abs(p1[0] - p2[0]) + 1
    h = abs(p1[1] - p2[1]) + 1
    return w * h


# ==========================================================
# 2. LOGIQUE PART TWO : VALIDATION DU RECTANGLE
# ==========================================================

def is_rectangle_valid(p1, p2, polygon_points):
    """
    Vérifie si le rectangle formé par p1 et p2 est inclus
    dans la boucle définie par polygon_points.
    (Version basée sur la logique originale de l’utilisateur.)
    """
    min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
    min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])

    # Cas rectangle plat
    if min_x == max_x or min_y == max_y:
        return True

    n = len(polygon_points)

    # Test d'intersection avec les murs
    for i in range(n):
        ua = polygon_points[i]
        ub = polygon_points[(i + 1) % n]

        wx1, wx2 = sorted((ua[0], ub[0]))
        wy1, wy2 = sorted((ua[1], ub[1]))

        # Mur vertical
        if wx1 == wx2:
            if min_x < wx1 < max_x:
                if not (wy2 <= min_y or wy1 >= max_y):
                    return False

        # Mur horizontal
        if wy1 == wy2:
            if min_y < wy1 < max_y:
                if not (wx2 <= min_x or wx1 >= max_x):
                    return False

    # Test point-in-polygon (milieu du rectangle)
    test_x = (min_x + max_x) / 2
    test_y = (min_y + max_y) / 2

    intersections = 0
    for i in range(n):
        ua = polygon_points[i]
        ub = polygon_points[(i + 1) % n]

        if (ua[1] > test_y) != (ub[1] > test_y):
            intersect_x = (ub[0] - ua[0]) * (test_y - ua[1]) / (ub[1] - ua[1]) + ua[0]
            if test_x < intersect_x:
                intersections += 1

    return (intersections % 2 == 1)


# ==========================================================
# 3. RÉSOLUTION PART ONE & PART TWO
# ==========================================================

def solve_part_1(tiles):
    print("--- PART 1 ---")
    max_area = 0

    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            area = calc_area_part1(tiles[i], tiles[j])
            if area > max_area:
                max_area = area

    print(f"Réponse Part 1 : {max_area}")


def solve_part_2(tiles):
    print("\n--- PART 2 ---")
    max_area_valid = 0

    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            p1, p2 = tiles[i], tiles[j]
            area = calc_area_part1(p1, p2)

            if area <= max_area_valid:
                continue

            if is_rectangle_valid(p1, p2, tiles):
                max_area_valid = area

    print(f"Réponse Part 2 : {max_area_valid}")


# ==========================================================
# 4. EXÉCUTION
# ==========================================================

if __name__ == "__main__":
    raw_lines = read_input("./day9.txt")
    tiles = [parse_point(line) for line in raw_lines]

    print(f"Nombre de tuiles rouges chargées : {len(tiles)}")

    solve_part_1(tiles)
    solve_part_2(tiles)
