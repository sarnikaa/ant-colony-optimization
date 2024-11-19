import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import Label, Entry, Button, Text
import networkx as nx
import random
import math
from PIL import Image, ImageTk

# Constants
NUM_ANTS = 5
NUM_CITIES = 7
ALPHA = 1.0
BETA = 2.0
EVAPORATION_RATE = 0.5
Q = 100
INITIAL_PHEROMONE = 1.0
MAX_DISTANCE = 1000  # Maximum distance between cities

# City locations (randomly generated)
cities = [(random.uniform(0, MAX_DISTANCE), random.uniform(0, MAX_DISTANCE)) for _ in range(NUM_CITIES)]

# Calculate distances between cities
distances = [[0] * NUM_CITIES for _ in range(NUM_CITIES)]
for i in range(NUM_CITIES):
    for j in range(i + 1, NUM_CITIES):
        dx = cities[i][0] - cities[j][0]
        dy = cities[i][1] - cities[j][1]
        distances[i][j] = distances[j][i] = math.sqrt(dx**2 + dy**2)

# Initialize pheromone levels
pheromones = [[INITIAL_PHEROMONE] * NUM_CITIES for _ in range(NUM_CITIES)]

# Ant class
class Ant:
    def __init__(self):
        self.visited = [False] * NUM_CITIES
        self.tour = []

    def select_next_city(self, current_city):
        print("Current city:", current_city)
        # Calculate the probability to move to each unvisited city
        probabilities = [0.0] * NUM_CITIES
        total = 0.0
        for city in range(NUM_CITIES):
            if not self.visited[city]:
                print("Calculating probability for city:", city)
                pheromone = pheromones[current_city][city]
                print("Pheromone level for edge (", current_city, ",", city, "):", pheromone)
                distance = distances[current_city][city]
                probabilities[city] = (pheromone ** ALPHA) * ((1 / distance) ** BETA)
                total += probabilities[city]

        # Choose the next city based on probabilities
        if total > 0:
            print("Total probability:", total)
            r = random.uniform(0, total)
            for city in range(NUM_CITIES):
                if not self.visited[city]:
                    r -= probabilities[city]
                    if r <= 0:
                        print("Next city selected:", city)
                        return city

        # If all cities have been visited, return to the starting city
        print("All cities visited. Returning to the starting city.")
        return self.tour[0]


    def find_tour(self):
        current_city = random.randint(0, NUM_CITIES - 1)
        self.tour = [current_city]
        self.visited[current_city] = True
        while len(self.tour) < NUM_CITIES:
            next_city = self.select_next_city(current_city)
            self.tour.append(next_city)
            self.visited[next_city] = True
            current_city = next_city

    def tour_length(self):
        total_length = 0
        for i in range(NUM_CITIES):
            total_length += distances[self.tour[i - 1]][self.tour[i]]
        return total_length

# ACO functions
def update_pheromones(ants):
    for i in range(NUM_CITIES):
        for j in range(i + 1, NUM_CITIES):
            evaporation = (1 - EVAPORATION_RATE) * pheromones[i][j]
            pheromones[i][j] = evaporation
            pheromones[j][i] = evaporation
    for ant in ants:
        tour_length = ant.tour_length()
        for i in range(NUM_CITIES):
            j = (i + 1) % NUM_CITIES
            pheromones[ant.tour[i]][ant.tour[j]] += Q / tour_length
            pheromones[ant.tour[j]][ant.tour[i]] += Q / tour_length

def reset_ants(ants):
    for ant in ants:
        ant.visited = [False] * NUM_CITIES
        ant.tour = []

# ACO main loop
def aco_main(iterations):
    ants = [Ant() for _ in range(NUM_ANTS)]
    best_tour = None
    best_length = float('inf')

    for _ in range(iterations):
        for ant in ants:
            ant.find_tour()
            length = ant.tour_length()
            if length < best_length:
                best_tour = ant.tour[:]
                best_length = length
        update_pheromones(ants)
        reset_ants(ants)

    return best_tour, best_length

# Create a tkinter window for input
window = tk.Tk()
window.title("Ant Colony Optimization")

# Load the ant image

background = ImageTk.PhotoImage(file="C:/Users/Sarnika/OneDrive/Desktop/sem 4/scl Package/final package/final pack/ant1.jpeg")


background_label = Label(window, image=background)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Entry fields for the number of ants and cities
Label(window, text="Number of Ants:", anchor="e").grid(row=0, column=0, padx=10)  # Align to the right
ants_entry = Entry(window)
ants_entry.grid(row=0, column=1, padx=10)

Label(window, text="Number of Cities:", anchor="e").grid(row=1, column=0, padx=10)  # Align to the right
cities_entry = Entry(window)
cities_entry.grid(row=1, column=1, padx=10)

# Entry field for the number of iterations
Label(window, text="Number of Iterations:", anchor="e").grid(row=2, column=0, padx=10)  # Align to the right
iterations_entry = Entry(window)
iterations_entry.grid(row=2, column=1, padx=10)

# Text widget for output
output_text = Text(window, height=10, width=40)
output_text.grid(row=3, column=0, columnspan=2)
output_text.tag_configure("center", justify='center')  # Configure text widget to center text
output_text.insert("1.0", "\n\n", "center")  # Insert an empty line with center alignment
output_text.config(state="disabled")  # Make the text widget read-only

# Function to run ACO and display the results
def start_aco():
    global NUM_ANTS, NUM_CITIES, ALPHA, BETA, EVAPORATION_RATE, Q, INITIAL_PHEROMONE, MAX_DISTANCE
    NUM_ANTS = int(ants_entry.get())
    NUM_CITIES = int(cities_entry.get())
    ALPHA = 1.0
    BETA = 2.0
    EVAPORATION_RATE = 0.5
    Q = 100
    INITIAL_PHEROMONE = 1.0
    MAX_DISTANCE = 1000

    iterations = int(iterations_entry.get())
    best_tour, best_length = aco_main(iterations)
    output_text.config(state="normal")  # Enable editing of the text widget
    output_text.delete(1.0, tk.END)  # Clear the previous content
    output_text.insert(tk.END, f"Best Tour: {best_tour}\n")
    output_text.insert(tk.END, f"Best Tour Length: {best_length}\n")
    output_text.config(state="disabled")  # Make the text widget read-only



# Function to create a NetworkX graph from city locations and pheromone levels
def create_networkx_graph():
    G = nx.Graph()
    for i in range(NUM_CITIES):
        G.add_node(i, pos=cities[i])
    for i in range(NUM_CITIES):
        for j in range(i + 1, NUM_CITIES):
            G.add_edge(i, j, weight=pheromones[i][j])
    return G

# Function to draw the network graph with improved clarity
def draw_networkx():
    G = create_networkx_graph()
    pos = nx.get_node_attributes(G, 'pos')
    edge_labels = {(i, j): f"{pheromones[i][j]:.2f}" for i, j in G.edges}  # Format the label values
    edge_colors = [pheromones[i][j] for i, j in G.edges]

    plt.figure(figsize=(12, 12))  # Increase the figure size
    nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue', edge_color=edge_colors, width=3, edge_cmap=plt.cm.inferno)  # Increase node size and edge width
    labels = nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=10)  # Increase font size
    for (_, t), label in labels.items():
        label.set_text(label.get_text())

    plt.axis('off')
    plt.show()

# Buttons to start ACO and show the network graph
Button(window, text="Start ACO", command=start_aco).grid(row=5, column=0, columnspan=2)
Button(window, text="Show Network", command=draw_networkx).grid(row=6, column=0, columnspan=2)

window.mainloop()
