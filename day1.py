# Advent of Code 2025 - Day 1
# ----------------------------------------------------------
# Contexte général :
# On contrôle un cadran circulaire numéroté de 0 à 99.
# Il démarre sur 50. On applique une suite de rotations
# (L/R + distance) décrites dans le fichier d'entrée.
# Les règles pour compter les passages par 0 diffèrent
# entre PART ONE et PART TWO.
# ----------------------------------------------------------


from typing import List


def read_input(path: str) -> List[str]:
    """Lit le fichier d'entrée et renvoie la liste brute des rotations."""
    with open(path, "r", encoding="utf-8") as f:
        # On enlève les espaces / lignes vides
        return [line.strip() for line in f if line.strip()]


moves = read_input("./day1.txt")


# ==========================================================
# PART ONE
# ----------------------------------------------------------
# RÈGLE PART ONE (version condensée) :
# - Le cadran va de 0 à 99 (modulo 100), il commence à 50.
# - Chaque ligne est une rotation :
#     Lx : tourner vers les nombres plus petits de x "clics"
#     Rx : tourner vers les nombres plus grands de x "clics"
# - On compte le nombre de fois où, après une rotation complète,
#   le cadran est exactement sur 0.
# ==========================================================

def count_zeros_end_only(moves: List[str], start: int = 50) -> int:
    """Compte les fois où le cadran pointe sur 0 à la fin de chaque rotation."""
    position = start
    zero_times = 0

    for move in moves:
        direction = 1 if move[0] == "R" else -1
        distance = int(move[1:])
        position = (position + direction * distance) % 100
        if position == 0:
            zero_times += 1

    return zero_times


part1_result = count_zeros_end_only(moves)
print("PART ONE:", part1_result)


# ==========================================================
# PART TWO
# ----------------------------------------------------------
# RÈGLE PART TWO (version condensée) :
# - On compte désormais chaque "clic" qui fait passer le cadran
#   sur 0, pas seulement la position finale après la rotation.
# - Exemple : un tour complet de 100 clics passe une fois par 0.
# - Une rotation peut donc faire passer plusieurs fois par 0
#   avant d'arriver à sa position finale.
# - Attention : une rotation du type R1000 peut faire passer le
#   cadran par 0 plusieurs fois avant de revenir à sa position.
# ==========================================================

def zeros_during_rotation(position: int, direction: int, distance: int) -> int:
    """
    Calcule le nombre de fois où le cadran pointe sur 0 pendant une
    rotation (clics intermédiaires + éventuellement la fin).
    On ne s'occupe ici que des clics intermédiaires ; la position
    finale sera gérée par la formule globale.
    """
    # Nombre de tours complets de 100 clics -> 1 passage par 0 à chaque tour
    full_turns = distance // 100
    zeros = full_turns

    # Reste après les tours complets
    remainder = distance % 100
    if remainder == 0:
        return zeros

    # Distance (en clics) pour atteindre 0 à partir de la position actuelle
    if direction == 1:  # droite (vers les nombres plus grands)
        dist_to_zero = (-position) % 100
    else:               # gauche (vers les nombres plus petits)
        dist_to_zero = position % 100

    # Si on est déjà sur 0, il faut un tour complet pour y repasser
    if dist_to_zero == 0:
        dist_to_zero = 100

    # Si le reste couvre la distance jusqu'à 0, on passe une fois de plus par 0
    if remainder >= dist_to_zero:
        zeros += 1

    return zeros


def count_zeros_all_clicks(moves: List[str], start: int = 50) -> int:
    """
    Compte le nombre total de fois où le cadran pointe sur 0,
    en comptant tous les clics intermédiaires et les positions finales.
    """
    position = start
    zero_times = 0

    for move in moves:
        direction = 1 if move[0] == "R" else -1
        distance = int(move[1:])

        # Zéros rencontrés pendant la rotation (intermédiaires + éventuel passage)
        zero_times += zeros_during_rotation(position, direction, distance)

        # Nouvelle position après la rotation
        position = (position + direction * distance) % 100

    return zero_times


part2_result = count_zeros_all_clicks(moves)
print("PART TWO:", part2_result)
