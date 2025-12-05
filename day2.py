# Advent of Code 2025 - Day 2
# ----------------------------------------------------------
# Contexte général :
# On reçoit une liste de plages d'IDs sous la forme "A-B".
# On doit identifier les IDs invalides selon une règle différente
# en PART ONE et PART TWO, puis sommer ces IDs invalides.
# ----------------------------------------------------------


def read_input(path: str) -> list[str]:
    """Lit le fichier d'entrée et renvoie une liste plate de ranges 'A-B'."""
    ranges = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            ranges.extend(item for item in line.split(",") if item)
    return ranges


ids = read_input("./day2.txt")


# ==========================================================
# PART ONE
# ----------------------------------------------------------
# RÈGLE PART ONE (version condensée) :
# Un ID est invalide si sa représentation contient un bloc
# répété **exactement deux fois**. Autrement dit :
#   - longueur du nombre paire
#   - ID = XY où X == Y après découpe en deux parties égales
# Exemples : 55, 6464, 123123
# ==========================================================

def is_part1_invalid(x: int) -> bool:
    """Renvoie True si x est composé de deux moitiés identiques."""
    s = str(x)
    if len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    return s[:mid] == s[mid:]


invalid_ids_part1 = []

for r in ids:
    start, end = map(int, r.split("-"))
    for value in range(start, end + 1):
        if is_part1_invalid(value):
            invalid_ids_part1.append(value)

print("PART ONE:", sum(invalid_ids_part1))


# ==========================================================
# PART TWO
# ----------------------------------------------------------
# RÈGLE PART TWO (version condensée) :
# Un ID est invalide s'il est composé d'un bloc répété au
# moins **deux fois**, peu importe la taille du bloc.
# Exemples : 55, 6464, 123123, 1212121212, 1111111
#
# Astuce utilisée : s est répétitif si s appartient à
# (s + s)[1:-1]
# ==========================================================

def is_repeated_pattern(x: int) -> bool:
    """Détecte si x est construit par répétition d'un bloc >= 2 fois."""
    s = str(x)
    return s in (s + s)[1:-1]


invalid_ids_part2 = []

for r in ids:
    start, end = map(int, r.split("-"))
    for value in range(start, end + 1):
        if is_repeated_pattern(value):
            invalid_ids_part2.append(value)

print("PART TWO:", sum(invalid_ids_part2))
