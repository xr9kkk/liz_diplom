import string
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from queue import Queue
from itertools import permutations

def plot_3d_route(route, warehouse):
    x_coords, y_coords, z_coords = [], [], []

    for point in route:
        col, row, level = point.split('-')
        x_coords.append(ord(col) - ord('A'))
        y_coords.append(int(row) - 1)
        z_coords.append(int(level) - 1)

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
    ax.set_ylabel("Rows (1-13)")
    ax.set_zlabel("Levels")
    ax.legend()
    plt.show()

def generate_warehouse_map():
    warehouse = {}
    for row in range(1, 14):  
        for col in string.ascii_uppercase[:13]:  
            for level in range(1, 4):  
                cell = f"{col}-{row}-{level}"
                if row in [2, 3, 4] and col in "BCEFHIKL":
                    warehouse[cell] = "shelf"
                else:
                    warehouse[cell] = "free"
    return warehouse

def find_accessible_points(shelf_point, warehouse):
    col, row, level = shelf_point.split('-')
    row, level = int(row), int(level)
    accessible_points = []

    if level == 2: 
        candidates = [
            f"{chr(ord(col) - 1)}-{row}-{level}",  
            f"{chr(ord(col) + 1)}-{row}-{level}", 
            f"{col}-{row - 1}-{level}", 
            f"{col}-{row + 1}-{level}",  
        ]
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
        return False  # Возвращаем, если движение недопустимо

    cur_col, cur_row, cur_level = current.split('-')
    next_col, next_row, next_level = next_point.split('-')
    cur_row, next_row = int(cur_row), int(next_row)
    cur_level, next_level = int(cur_level), int(next_level)

    # Если находимся на втором уровне
    if is_on_second_level:
        if next_level == 1:  # Разрешаем движение только на первый уровень
            return True
        return False  # Запретить движение на второй уровень или выше

    # Проверка на движение вверх
    if cur_col == next_col and cur_row == next_row and next_level > cur_level:
        return True  # Разрешить движение вверх на второй уровень

    # Проверка на движение вниз
    if cur_col == next_col and cur_row == next_row and next_level < cur_level:
        return True  # Разрешить движение вниз

    # Проверка на горизонтальное движение на первом уровне
    if cur_level == next_level:
        if cur_col == next_col and abs(cur_row - next_row) == 1: 
            return True  # Вертикальное движение
        if cur_row == next_row and abs(ord(cur_col) - ord(next_col)) == 1: 
            return True  # Горизонтальное движение

    return False  # Если движение недопустимо


def bfs_shortest_path(start, end, warehouse):
    queue = Queue()
    queue.put((start, [], False))  # Начинаем с пустого пути и флага второго уровня
    visited = set()

    while not queue.empty():
        current, path, is_on_second_level = queue.get()
        path = path + [current]

        if current == end:
            return path

        if current in visited:
            continue
        visited.add(current)

        cur_col, cur_row, cur_level = current.split('-')
        cur_row, cur_level = int(cur_row), int(cur_level)
        neighbors = [
            f"{cur_col}-{cur_row + 1}-{cur_level}",  # Up
            f"{cur_col}-{cur_row - 1}-{cur_level}",  # Down
            f"{chr(ord(cur_col) + 1)}-{cur_row}-{cur_level}",  # Right
            f"{chr(ord(cur_col) - 1)}-{cur_row}-{cur_level}",  # Left
            f"{cur_col}-{cur_row}-{cur_level + 1}",  # Up one level
            f"{cur_col}-{cur_row}-{cur_level - 1}",  # Down one level
        ]

        for neighbor in neighbors:
            valid_move = is_valid_move(current, neighbor, warehouse, is_on_second_level)
            if valid_move:
                new_is_on_second_level = is_on_second_level or (neighbor.split('-')[2] == '2')
                queue.put((neighbor, path, new_is_on_second_level))
    
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
                segment = segment[1:]  # Remove duplicate point
            full_path.extend(segment)
    return full_path

def main():
    warehouse = generate_warehouse_map()

    start_point = "G-1-1"
    end_point = "G-13-1"

    points = [start_point]

    print("Введите точки маршрута в формате 'A-1-1'. Для завершения ввода введите 'end'.")
    while True:
        point = input("Точка: ").strip().upper()
        if point == "END":
            break
        if point not in warehouse or warehouse[point] != "shelf":
            print(f"Точка {point} недоступна!")
            continue
        access_points = find_accessible_points(point, warehouse)
        if access_points:
            points.append(access_points[0])
        else:
            print(f"Не удалось найти доступные точки для {point}.")

    points.append(end_point)

    if len(points) < 2:
        print("Нужно указать как минимум начальную и конечную точку!")
        return

    distances = calculate_distances(points, warehouse)
    optimal_order = [start_point] + list(find_optimal_path(points[1:-1], distances)) + [end_point]

    if not optimal_order:
        print("Не удалось найти оптимальный порядок точек!")
        return

    print("Оптимальный порядок точек:", " -> ".join(optimal_order))
    shortest_path = reconstruct_path(optimal_order, warehouse)
    if shortest_path:
        print("Кратчайший маршрут:", " -> ".join(shortest_path))
        print("Количество шагов:", len(shortest_path))
        plot_3d_route(shortest_path, warehouse)
    else:
        print("Не удалось построить маршрут!")

if __name__ == "__main__":
    main()