import string
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

def find_accessible_points(shelf_point, warehouse):
    col, row, level = shelf_point.split('-')
    row, level = int(row), int(level)
    accessible_points = []

    candidates = [
        f"{chr(ord(col) - 1)}-{row}-{level}",  
        f"{chr(ord(col) + 1)}-{row}-{level}",  
        f"{col}-{row - 1}-{level}",
        f"{col}-{row + 1}-{level}",  
    ]
   
    if level > 1:
        candidates.append(f"{col}-{row}-{level - 1}")  
    if level < 3:
        candidates.append(f"{col}-{row}-{level + 1}")  

    for candidate in candidates:
        if candidate in warehouse and warehouse[candidate] == "free":
            accessible_points.append(candidate)

    return accessible_points

def calculate_distances(points, warehouse):
    distances = {}
    for i, start in enumerate(points):
        for j, end in enumerate(points):
            if i != j:
                path = bfs_shortest_path(start, end, warehouse)
                distances[(start, end)] = len(path) if path else float('inf')
    return distances


def is_valid_move(current, next_point, warehouse, is_on_second_level=False):
    if next_point not in warehouse or warehouse[next_point] == "shelf":
        return False  
    
    cur_col, cur_row, cur_level = current.split('-')
    next_col, next_row, next_level = next_point.split('-')
    cur_row, next_row = int(cur_row), int(next_row)
    cur_level, next_level = int(cur_level), int(next_level)

    if cur_level > 1 or next_level > 1:
        if cur_col != next_col or cur_row != next_row:
            return False

    if cur_col == next_col and cur_row == next_row and next_level < cur_level:
        return True

    if cur_level == next_level == 1:
        if cur_col == next_col and abs(cur_row - next_row) == 1: 
            return True  
        if cur_row == next_row and abs(ord(cur_col) - ord(next_col)) == 1: 
            return True  

    if cur_col == next_col and cur_row == next_row and next_level > cur_level:
        return True

    return False 


def bfs_shortest_path(start, end, warehouse):
    queue = Queue()
    queue.put((start, []))  
    visited = set()

    while not queue.empty():
        current, path = queue.get()
        path = path + [current]

        if current == end:
            return path

        if current in visited:
            continue
        visited.add(current)

        cur_col, cur_row, cur_level = current.split('-')
        cur_row, cur_level = int(cur_row), int(cur_level)
        neighbors = [
            f"{cur_col}-{cur_row + 1}-{cur_level}", 
            f"{cur_col}-{cur_row - 1}-{cur_level}", 
            f"{chr(ord(cur_col) + 1)}-{cur_row}-{cur_level}",
            f"{chr(ord(cur_col) - 1)}-{cur_row}-{cur_level}",  
            f"{cur_col}-{cur_row}-{cur_level + 1}",  
            f"{cur_col}-{cur_row}-{cur_level - 1}",  
        ]

        for neighbor in neighbors:
            if is_valid_move(current, neighbor, warehouse):
                queue.put((neighbor, path))
    return None


def find_optimal_path(points, distances):
    best_path = None
    min_distance = float('inf')

    for perm in permutations(points):
        distance = 0
        for i in range(len(perm) - 1):
            dist = distances.get((perm[i], perm[i + 1]), float('inf'))
            if dist == float('inf'):
                distance = float('inf')
                break
            distance += dist
        
        if distance < min_distance:
            min_distance = distance
            best_path = perm

    return best_path

def reconstruct_path(order, warehouse):
    full_path = []
    for i in range(len(order) - 1):
        segment = bfs_shortest_path(order[i], order[i + 1], warehouse)
        if segment is not None:
            if full_path:
                segment = segment[1:] 
            full_path.extend(segment)
    return full_path
