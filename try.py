import string
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from queue import Queue
from itertools import permutations

def generate_warehouse_map():
    warehouse = {}
    for row in range(1, 14):  
        for col in string.ascii_uppercase[:13]:  
            for level in range(1, 4):  
                cell = f"{col}-{row}-{level}"
                if row in [2, 3, 4, 6, 7, 8, 10, 11, 12] and col in "BCEFHIKL":
                    warehouse[cell] = "shelf"
                else:
                    warehouse[cell] = "free"
    return warehouse

def plot_3d_route( warehouse):
    x_coords, y_coords, z_coords = [], [], []


    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x_coords, y_coords, z_coords, marker='o', color='b', label='Route')
    ax.scatter(x_coords, y_coords, z_coords, c='r', s=50, label='Waypoints')

    for cell, status in warehouse.items():
        if status == "shelf":
            col, row, level = cell.split('-')
            x = ord(col) - ord('A')
            y = int(row) - 1
            z = int(level) - 1
            ax.scatter(x, y, z, c='k', s=100)

    ax.set_title("Warehouse Route (3D View)")
    ax.set_xlabel("Columns (A-M)")
    ax.set_xticks(range(1, 13))
    ax.set_ylabel("Rows (1-13)")
    ax.set_yticks(range(1,13))
    ax.set_zlabel("Levels")
    ax.set_zticks(range(1,3))
    ax.legend()
    plt.show()

plot_3d_route(generate_warehouse_map())