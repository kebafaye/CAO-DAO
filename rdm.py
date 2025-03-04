import numpy as np
import matplotlib.pyplot as plt

# Fonction pour calculer la section transversale selon la forme
def calculer_section_transversale():
    forme = input("Entrez la forme de la section transversale (cercle/rectangle) : ").lower()
    if forme == "cercle":
        rayon = float(input("Entrez le rayon de la section circulaire (en m) : "))
        A = np.pi * (rayon ** 2)
        print(f"Section transversale (A) = {A:.4f} m^2")
    elif forme == "rectangle":
        largeur = float(input("Entrez la largeur de la section rectangulaire (en m) : "))
        hauteur = float(input("Entrez la hauteur de la section rectangulaire (en m) : "))
        A = largeur * hauteur
        print(f"Section transversale (A) = {A:.4f} m^2")
    else:
        print("Forme non reconnue.")
        A = None
    return A

# Fonction pour calculer la contrainte axiale
def calcul_contrainte_axiale(F, A):
    return F / A

# Fonction pour calculer la déformation axiale
def calcul_deformation_axiale(sigma, E):
    return sigma / E

# Fonction pour la gestion des charges
def gestion_charge(L):
    type_charge = input("Entrez le type de charge (concentrée/distribuée) : ").lower()
    if type_charge == "concentrée":
        F = float(input("Entrez la force concentrée (F) en N : "))
        return F, np.full(100, F)
    elif type_charge == "distribuée":
        q = float(input("Entrez la charge distribuée (q) en N/m : "))
        positions = np.linspace(0, L, 100)
        F_total = q * L
        F = q * positions
        return F_total, F
    else:
        print("Type de charge non reconnu.")
        return None, None

# Fonction pour visualiser les contraintes
def visualisation_contrainte(positions, contraintes, type_contrainte):
    plt.figure(figsize=(8, 6))
    plt.plot(positions, contraintes, label=f"Contrainte {type_contrainte}", color='blue')
    plt.title(f"Variation de la Contrainte {type_contrainte} le long de la barre")
    plt.xlabel("Position le long de la barre (m)")
    plt.ylabel("Contrainte (Pa)")
    plt.grid(True)
    plt.legend()
    plt.show()

# Fonction principale
def main():
    # Propriétés du matériau
    E = float(input("Entrez le module d'élasticité (E) en Pa : "))  # Module de Young (en Pascal)
    L = float(input("Entrez la longueur de la barre (L) en m : "))  # Longueur de la barre (en mètres)

    # Calcul de la section transversale
    A = calculer_section_transversale()
    if A is None:
        return
    
    # Gestion des charges (concentrée ou distribuée)
    F_total, F_variation = gestion_charge(L)
    if F_total is None:
        return
    
    # Calcul de la contrainte axiale
    sigma = calcul_contrainte_axiale(F_total, A)
    print(f"Contrainte axiale (σ) : {sigma:.4f} Pa")
    
    # Calcul de la déformation axiale
    epsilon = calcul_deformation_axiale(sigma, E)
    print(f"Déformation axiale (ε) : {epsilon:.6f}")

    # Comparaison avec la limite élastique
    limite_elastique = float(input("Entrez la limite élastique du matériau (en Pa, sinon entrez 0) : "))
    if limite_elastique > 0:
        if sigma <= limite_elastique:
            print("La barre se déforme élastiquement.")
        else:
            print("La barre se déforme plastiquement.")
    else:
        print("Limite élastique non fournie.")
    
    # Visualisation de la contrainte le long de la barre
    positions = np.linspace(0, L, 100)
    contraintes = F_variation / A  # Calcul des contraintes tout au long de la barre
    visualisation_contrainte(positions, contraintes, "Axiale")

# Exécution du programme principal
if __name__ == "__main__":
    main()