import numpy as np
import random

# Définition de l’environnement (5x5 avec obstacles)
grid_size = (5, 5)
obstacles = [(1, 1), (2, 2), (3, 3)]  # Positions des obstacles
start = (0, 0)  # Départ
goal = (4, 4)   # Arrivée

# Génération d’un individu (chemin aléatoire)
def create_individual():
    return [random.choice([(0,1), (1,0), (0,-1), (-1,0)]) for _ in range(10)]

# Évaluation de la fitness (distance + obstacles évités)
def fitness(individual):
    x, y = start
    score = 0
    for move in individual:
        nx, ny = x + move[0], y + move[1]
        if (0 <= nx < grid_size[0]) and (0 <= ny < grid_size[1]):  # Vérifier les limites
            if (nx, ny) in obstacles:
                score -= 5  # Pénalité pour obstacle
            x, y = nx, ny
    score -= abs(goal[0] - x) + abs(goal[1] - y)  # Distance restante
    return -score  # Minimisation

# Sélection, croisement et mutation
def select(population, scores):
    return random.choices(population, weights=scores, k=2)

def crossover(parent1, parent2):
    cut = random.randint(1, len(parent1)-1)
    return parent1[:cut] + parent2[cut:]

def mutate(individual, mutation_rate=0.2):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
    return individual

# Algorithme Génétique
def genetic_algorithm(generations=50, population_size=10):
    population = [create_individual() for _ in range(population_size)]
    
    for _ in range(generations):
        scores = [fitness(ind) for ind in population]
        new_population = []
        for _ in range(population_size // 2):
            p1, p2 = select(population, scores)
            child = crossover(p1, p2)
            new_population.append(mutate(child))
        population = new_population
    
    best_path = max(population, key=lambda ind: fitness(ind))
    return best_path

# Exécuter le GA
best_solution = genetic_algorithm()
print(f"Meilleur chemin trouvé: {best_solution}")
