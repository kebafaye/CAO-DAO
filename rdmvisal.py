# Imports necessaires
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration des styles de visualisation
def configure_visualization():
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['axes.titlesize'] = 20
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.rcParams['legend.fontsize'] = 14
    plt.rcParams['lines.linewidth'] = 2.5

configure_visualization()

# Partie 1 : Preparation et Initialisation
def initialize_parameters():
    """
    Initialisation des propriétés du matériau et des paramètres géométriques.
    Retourne un dictionnaire contenant les paramètres nécessaires.
    """
    params = {
        'E': 210e9,  # Module d'élasticité (Pa)
        'A': 0.01,   # Section transversale (m^2)
        'L': 2.0,    # Longueur de la barre (m)
        'F': 50e3    # Force appliquée (N)
    }
    return params

# Partie 2 : Calculs de Contrainte et Déformation
def compute_stress_and_strain(params):
    """
    Calcule la contrainte et la déformation axiales basées sur les paramètres fournis.
    """
    sigma = params['F'] / params['A']  # Contrainte axiale (Pa)
    epsilon = sigma / params['E']      # Déformation axiale (sans unité)
    delta = epsilon * params['L']      # Allongement total (m)
    
    return sigma, epsilon, delta

# Partie 3 : Visualisation améliorée

def plot_stress_variation(params, sigma):
    """
    Affiche la variation de la contrainte le long de la barre avec des améliorations visuelles.
    """
    x = np.linspace(0, params['L'], 100)
    stress_distribution = sigma * x / params['L']

    plt.figure()
    sns.lineplot(x=x, y=stress_distribution, label='Contrainte (Pa)', color='dodgerblue')
    plt.fill_between(x, 0, stress_distribution, color='dodgerblue', alpha=0.3)
    plt.title("Variation de la contrainte le long de la barre", fontsize=22, fontweight='bold')
    plt.xlabel("Position le long de la barre (m)", fontsize=16)
    plt.ylabel("Contrainte (Pa)", fontsize=16)
    plt.legend(title="Légende", title_fontsize=14)
    plt.grid(color='gray', linestyle='--', linewidth=0.7, alpha=0.7)
    plt.show()

def display_results(sigma, epsilon, delta):
    """
    Affiche les résultats des calculs de contrainte, déformation et allongement.
    """
    print(f"Contrainte axiale : {sigma:.2e} Pa")
    print(f"Déformation axiale : {epsilon:.2e}")
    print(f"Allongement total : {delta:.4f} m")

# Partie principale : Execution du code
if __name__ == "__main__":
    # Initialisation des paramètres
    params = initialize_parameters()

    # Calcul des résultats
    sigma, epsilon, delta = compute_stress_and_strain(params)

    # Affichage des résultats
    display_results(sigma, epsilon, delta)

    # Visualisation de la contrainte
    plot_stress_variation(params, sigma)

