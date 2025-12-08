import math
from collections import Counter
from typing import List, Tuple

# Advent of Code 2025 - Day 8
# ----------------------------------------------------------
# Contexte général :
# On reçoit une liste de points en 3D sous la forme "x,y,z".
# Chaque point est un nœud dans un espace 3D.
# On relie les points deux à deux par ordre de distance croissante
# et on observe les "circuits" (composantes connexes) qui se forment.
# ----------------------------------------------------------


Point3D = Tuple[int, int, int]


# ==========================================================
# 0. LECTURE ET PRÉPARATION DES DONNÉES (COMMUN)
# ----------------------------------------------------------
# On lit le fichier CSV "x,y,z" et on obtient une liste de points.
# Ensuite, on pré-calcule toutes les paires possibles de points
# avec leur distance au carré, puis on les trie par distance.
# ==========================================================

def read_points(path: str) -> List[Point3D]:
    """Lit le fichier d'entrée et renvoie une liste de points (x, y, z)."""
    pts: List[Point3D] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("x"):
                continue
            x, y, z = map(int, line.split(","))
            pts.append((x, y, z))
    return pts


def direction(p1: Point3D, p2: Point3D) -> Point3D:
    """Renvoie le vecteur p1 -> p2 (dx, dy, dz)."""
    return p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2]


def distance_sq(dx: int, dy: int, dz: int) -> int:
    """Calcule la distance au carré entre deux points 3D."""
    return dx ** 2 + dy ** 2 + dz ** 2


points: List[Point3D] = read_points("./day8.csv")
n = len(points)

print("--- Chargement ---")
print(f"Nombre de points : {n}")

# Calcul de TOUTES les distances (graphe complet)
distances: List[Tuple[int, int, int]] = []  # (distance², i, j)

for i in range(n):
    for j in range(i + 1, n):
        dx, dy, dz = direction(points[i], points[j])
        d2 = distance_sq(dx, dy, dz)
        distances.append((d2, i, j))

# Tri global (nécessaire pour les deux parties)
distances.sort()
print(f"Nombre de paires possibles : {len(distances)}")


# ==========================================================
# PART ONE
# ----------------------------------------------------------
# RÈGLE PART ONE (version condensée) :
# - On ne considère que les 1000 paires les plus courtes.
# - Chaque paire relie deux points ; si les points sont dans des
#   "circuits" (groupes) différents, on fusionne ces groupes.
# - À la fin, on obtient plusieurs circuits de tailles diverses.
# - La réponse est le produit des tailles des 3 plus grands circuits.
# ==========================================================

print("\n=== PART ONE ===")

# 1. On prend seulement les 1000 premiers "câbles"
closest_1000 = distances[:1000]

# 2. Initialisation des groupes :
#    au début, chaque point est dans son propre circuit.
groups_ids: List[int] = [i for i in range(n)]  # groups_ids[k] = id de circuit du point k

# 3. Fusion des groupes au fil des connexions
for d2, i, j in closest_1000:
    id_group_a = groups_ids[i]
    id_group_b = groups_ids[j]

    if id_group_a != id_group_b:
        id_cible = id_group_a
        id_a_remplacer = id_group_b

        # Remplacer id_a_remplacer par id_cible partout :
        # tous les points de l'ancien groupe B passent dans le groupe A.
        for k in range(n):
            if groups_ids[k] == id_a_remplacer:
                groups_ids[k] = id_cible

# 4. Calcul du résultat : tailles des circuits, tri, produit des 3 plus grands
counts = Counter(groups_ids)              # id_de_groupe -> taille_du_circuit
sizes = sorted(counts.values(), reverse=True)

a = sizes[0]
b = sizes[1]
c = sizes[2]
result_part1 = a * b * c

print(f"Tailles des 3 plus grands circuits : {a}, {b}, {c}")
print(f"PART ONE: {result_part1}")


# ==========================================================
# PART TWO
# ----------------------------------------------------------
# RÈGLE PART TWO (version condensée) :
# - On repart de zéro (tous les points sont de nouveau isolés).
# - On parcourt TOUTES les paires triées par distance.
# - À chaque fois qu'on relie deux groupes distincts, on fusionne.
# - On suit le nombre de groupes restants.
# - Dès qu'il ne reste plus qu'UN seul circuit, la dernière paire
#   utilisée donne la réponse : on prend les coordonnées X des
#   deux points de cette paire et on les multiplie.
# ==========================================================

print("\n=== PART TWO ===")

# 1. Réinitialisation des groupes
groups_ids = [i for i in range(n)]
nombre_groupes_actifs = n

# 2. Parcours de toutes les distances jusqu'à ce qu'il ne reste qu'un circuit
for d2, i, j in distances:
    id_group_a = groups_ids[i]
    id_group_b = groups_ids[j]

    if id_group_a != id_group_b:
        # Une fusion de deux circuits a lieu
        nombre_groupes_actifs -= 1

        id_cible = id_group_a
        id_a_remplacer = id_group_b

        # Mise à jour des groupes : tous les points de B passent dans A
        for k in range(n):
            if groups_ids[k] == id_a_remplacer:
                groups_ids[k] = id_cible

        # Condition de fin : il ne reste plus qu'un seul circuit
        if nombre_groupes_actifs == 1:
            print("Connexion finale trouvée !")

            point_a = points[i]
            point_b = points[j]

            x_a = point_a[0]
            x_b = point_b[0]

            result_part2 = x_a * x_b

            print(f"Dernière connexion entre : {point_a} et {point_b}")
            print(f"Coordonnées X : {x_a} * {x_b}")
            print(f"PART TWO: {result_part2}")
            break
