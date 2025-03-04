import numpy as np
import matplotlib.pyplot as plt

class RobotEnv:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.robot_pos = [1, 1]  # Position initiale du robot
        self.obstacles = [(3, 3), (4, 4), (5, 5), (6, 6)]  # Positions des obstacles
        self.goal = (8, 8)  # Position de l'objectif
    
    def get_sensor_readings(self):
        """Simule les lectures des capteurs."""
        left_sensor = self._get_distance(self.robot_pos, -1, 0)  # Gauche
        right_sensor = self._get_distance(self.robot_pos, 1, 0)  # Droite
        front_sensor = self._get_distance(self.robot_pos, 0, 1)  # Devant
        return [left_sensor, right_sensor, front_sensor]
    
    def _get_distance(self, pos, dx, dy):
        """Calcule la distance jusqu'à un obstacle dans une direction donnée."""
        x, y = pos
        distance = 0
        while 0 <= x + dx < self.width and 0 <= y + dy < self.height:
            x += dx
            y += dy
            distance += 1
            if (x, y) in self.obstacles:
                return 1 / distance  # Normalisation
        return 1.0  # Pas d'obstacle
    
    def move_robot(self, action):
        """Déplace le robot en fonction de l'action."""
        x, y = self.robot_pos
        if action == 0:  # Gauche
            x -= 1
        elif action == 1:  # Droite
            x += 1
        elif action == 2:  # Haut
            y += 1
        elif action == 3:  # Bas
            y -= 1
        
        # Vérifier les collisions
        if (x, y) not in self.obstacles and 0 <= x < self.width and 0 <= y < self.height:
            self.robot_pos = [x, y]
    
    def is_goal_reached(self):
        """Vérifie si le robot a atteint l'objectif."""
        return tuple(self.robot_pos) == self.goal
    
    def reset(self):
        """Réinitialise la position du robot."""
        self.robot_pos = [1, 1]
        return self.get_sensor_readings()
    
    def render(self):
        """Affiche l'environnement."""
        plt.clf()
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
        plt.grid()
        
        # Afficher les obstacles
        for obs in self.obstacles:
            plt.plot(obs[0], obs[1], 'ro')
        
        # Afficher le robot
        plt.plot(self.robot_pos[0], self.robot_pos[1], 'bo')
        
        # Afficher l'objectif
        plt.plot(self.goal[0], self.goal[1], 'go')
        
        plt.pause(0.1)
        class QLearningAgent:
    def __init__(self, num_states, num_actions, alpha=0.8, gamma=0.95, epsilon=1.0):
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((num_states, num_actions))
    
    def choose_action(self, state):
        """Choisit une action en fonction de l'état."""
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.num_actions)  # Exploration
        else:
            return np.argmax(self.q_table[state])  # Exploitation
    
    def update_q_table(self, state, action, reward, next_state):
        """Met à jour la Q-table."""
        old_value = self.q_table[state, action]
        next_max = np.max(self.q_table[next_state])
        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state, action] = new_value
    
    def decay_epsilon(self, decay_rate=0.995):
        """Réduit epsilon pour diminuer l'exploration."""
        self.epsilon *= decay_rate

# Fonction pour convertir les lectures des capteurs en état discret
def sensors_to_state(sensors):
    return int(sum(sensors) * 10)  # Exemple simple de discrétisation

# Hyperparamètres
num_episodes = 1000
alpha = 0.8
gamma = 0.95
epsilon = 1.0

# Environnement et agent
env = RobotEnv()
num_states = 100  # Nombre d'états discrets
num_actions = 4  # Gauche, Droite, Haut, Bas
agent = QLearningAgent(num_states, num_actions, alpha, gamma, epsilon)

# Boucle d'entraînement
for episode in range(num_episodes):
    state = sensors_to_state(env.reset())
    done = False
    
    while not done:
        action = agent.choose_action(state)
        env.move_robot(action)
        next_state = sensors_to_state(env.get_sensor_readings())
        
        # Récompense
        if env.is_goal_reached():
            reward = 10
            done = True
        elif tuple(env.robot_pos) in env.obstacles:
            reward = -10
            done = True
        else:
            reward = -1  # Pénalité pour chaque pas
        
        agent.update_q_table(state, action, reward, next_state)
        state = next_state
    
    agent.decay_epsilon()
    if episode % 100 == 0:
        print(f"Épisode {episode}, Epsilon {agent.epsilon}")

# Afficher la politique apprise
print("Q-Table :")
print(agent.q_table)