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
    
    shelf_added = False
    for cell, status in warehouse.items():
        if status == "shelf":
            col, row, level = cell.split('-')
            x = ord(col) - ord('A')
            y = int(row) - 1
            z = int(level) - 1
            if not shelf_added:
                ax.scatter(x, y, z, c='k', s=100, label='Shelf')
                shelf_added = True
            else:
                ax.scatter(x, y, z, c='k', s=100)

    ax.set_title("Warehouse Route (3D View)")
    ax.set_xlabel("Columns (A-M)")
    ax.set_ylabel("Rows (1-13)")
    ax.set_zlabel("Levels")
    ax.legend()
    plt.show()

def generate_warehouse_map():
    warehouse = {}
    for row in range(1, 14):  # Ряды 1-13
        for col in string.ascii_uppercase[:13]:  # Секции A-M
            for level in range(1, 4):  # Уровни 1-3
                cell = f"{col}-{row}-{level}"
                # Стеллажи
                if row in [2, 3, 4] and col in "BCEFHIKL":
                    warehouse[cell] = "shelf"
                else:
                    warehouse[cell] = "free"
    return warehouse


def is_valid_move(current, next_point, warehouse):
    if next_point not in warehouse:
        return False  # Точка вне склада

    cur_col, cur_row, cur_level = current.split('-')
    next_col, next_row, next_level = next_point.split('-')
    cur_row, next_row = int(cur_row), int(next_row)
    cur_level, next_level = int(cur_level), int(next_level)

    # Движение по уровням
    if cur_col == next_col and cur_row == next_row and abs(cur_level - next_level) == 1:
        if next_level == 1:  # Спуск всегда разрешен
            return True
        if cur_level == 1:  # Подъем разрешен только с уровня 1
            return True
        return False  # Исключение горизонтального движения между уровнями > 1

    # Движение по горизонтали или вертикали на том же уровне
    if cur_level == next_level:
        # Проверяем горизонтальное движение
        if abs(ord(cur_col) - ord(next_col)) == 1 and cur_row == next_row:
            # Разрешаем только, если между точками нет стеллажей
            if warehouse[current] == "free" and warehouse[next_point] == "free":
                return True
            if warehouse[current] == "shelf" or warehouse[next_point] == "shelf":
                return False  # Нельзя через стеллаж

            # Разрешаем движение вокруг стеллажей, если точки соседние
            if (cur_col, cur_row) in [(next_col, cur_row), (cur_col, next_row)]:
                return True

        # Проверяем вертикальное движение
        if abs(cur_row - next_row) == 1 and cur_col == next_col:
            if warehouse[current] == "free" and warehouse[next_point] == "free":
                return True

    return False



def bfs_shortest_path(start, end, warehouse):
    queue = Queue()
    queue.put([start])
    visited = set()

    while not queue.empty():
        path = queue.get()
        current = path[-1]

        if current == end:
            return path

        if current in visited:
            continue
        visited.add(current)

        # Проверяем соседние клетки
        cur_col, cur_row, cur_level = current.split('-')
        cur_row, cur_level = int(cur_row), int(cur_level)
        neighbors = [
            f"{cur_col}-{cur_row + 1}-{cur_level}",  # Вверх
            f"{cur_col}-{cur_row - 1}-{cur_level}",  # Вниз
            f"{chr(ord(cur_col) + 1)}-{cur_row}-{cur_level}",  # Вправо
            f"{chr(ord(cur_col) - 1)}-{cur_row}-{cur_level}",  # Влево
            f"{cur_col}-{cur_row}-{cur_level + 1}",  # Подъём на уровень выше
            f"{cur_col}-{cur_row}-{cur_level - 1}",  # Спуск на уровень ниже
        ]

        for neighbor in neighbors:
            if is_valid_move(current, neighbor, warehouse):
                queue.put(path + [neighbor])
    return None  



def calculate_distances(points, warehouse):
    distances = {}
    for i, start in enumerate(points):
        for j, end in enumerate(points):
            if i != j:
                path = bfs_shortest_path(start, end, warehouse)
                distances[(start, end)] = len(path) if path else float('inf')
    return distances


def find_optimal_path(points, distances):
    best_path = None
    min_distance = float('inf')

    for perm in permutations(points):
        # Рассчитать длину текущего маршрута
        distance = sum(distances[(perm[i], perm[i + 1])] for i in range(len(perm) - 1))
        if distance < min_distance:
            min_distance = distance
            best_path = perm

    return best_path


def reconstruct_path(order, distances, warehouse):
    full_path = []
    for i in range(len(order) - 1):
        segment = bfs_shortest_path(order[i], order[i + 1], warehouse)
        if full_path:
            segment = segment[1:]  # Удалить повторяющуюся точку
        full_path.extend(segment)
    return full_path


def main():
    warehouse = generate_warehouse_map()

    # Ввод точек маршрута
    print("Введите точки маршрута в формате 'A-1-1'. Для завершения ввода введите 'end'.")
    points = []
    while True:
        point = input("Точка: ").strip().upper()
        if point == "END":
            break
        if point not in warehouse or warehouse[point] == "shelf":
            print(f"Точка {point} недоступна!")
            continue
        points.append(point)

    if len(points) < 2:
        print("Нужно указать как минимум начальную и конечную точку!")
        return

    # Рассчитать расстояния между всеми точками
    distances = calculate_distances(points, warehouse)

    # Найти оптимальный порядок обхода точек
    optimal_order = find_optimal_path(points, distances)
    print("Оптимальный порядок точек:", " -> ".join(optimal_order))

    # Построить полный маршрут
    shortest_path = reconstruct_path(optimal_order, distances, warehouse)
    if shortest_path:
        print("Кратчайший маршрут:", " -> ".join(shortest_path))
        print("Количетсво шагов: ", len(shortest_path))
        plot_3d_route(shortest_path, warehouse)
    else:
        print("Не удалось построить маршрут!")


if __name__ == "__main__":
    main()
