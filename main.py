import string
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from queue import Queue


def generate_warehouse_map():
    """
    Создаёт карту склада с указанием стеллажей и проходимых зон.
    """
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
    """
    Проверяет, можно ли двигаться из текущей точки в следующую.
    """
    if next_point not in warehouse or warehouse[next_point] == "shelf":
        return False

    # Проверяем движение только по вертикали или горизонтали
    cur_col, cur_row, cur_level = current.split('-')
    next_col, next_row, next_level = next_point.split('-')
    cur_row, next_row = int(cur_row), int(next_row)
    cur_level, next_level = int(cur_level), int(next_level)

    if cur_col == next_col and cur_row == next_row and abs(cur_level - next_level) == 1:
        return True  # Переход между уровнями
    if cur_level == next_level:
        if cur_col == next_col and abs(cur_row - next_row) == 1:
            return True  # Вертикальное движение
        if cur_row == next_row and abs(ord(cur_col) - ord(next_col)) == 1:
            return True  # Горизонтальное движение
    return False


def bfs_shortest_path(start, end, warehouse):
    """
    Находит кратчайший путь с учётом ограничений движения.
    """
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
    return None  # Если путь не найден


def plot_3d_route(route, warehouse):
    """
    Визуализация маршрута в 3D.
    """
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

    # Отмечаем стеллажи
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


def main():
    warehouse = generate_warehouse_map()

    print("Введите начальную точку (например, A-1-1):")
    start = input().strip().upper()

    print("Введите конечную точку (например, M-13-1):")
    end = input().strip().upper()

    if start not in warehouse or warehouse[start] == "shelf":
        print(f"Точка {start} недоступна!")
        return
    if end not in warehouse or warehouse[end] == "shelf":
        print(f"Точка {end} недоступна!")
        return

    shortest_path = bfs_shortest_path(start, end, warehouse)
    if shortest_path:
        print("Кратчайший маршрут:", " -> ".join(shortest_path))
        plot_3d_route(shortest_path, warehouse)
    else:
        print("Путь не найден!")


if __name__ == "__main__":
    main()
