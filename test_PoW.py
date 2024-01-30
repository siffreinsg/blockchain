"""
Simple algorithme de preuve de travail.
L'objectif est de trouver une valeur de y tel que le hash SHA-256 de "x*y" commence par un nombre de 0 voulu.
"""
from hashlib import sha256
from time import process_time

x = int(input("Valeur de x ? "))
leading_zeros = int(input("Quantité de 0 de tête exigée ? "))

y = 0
solution = None
hash = None
start = process_time()

while not solution:
    hash = sha256(f"{x*y}".encode()).hexdigest()
    if (hash.startswith("0" * leading_zeros)):
        solution = y
    else:
        y += 1

print(f"\n\nSolution trouvée en {process_time() - start}s !")
print(f"y = {solution}")
print(f"hash = {hash}\n")
