import string
import itertools


def generate_points(columns, rows, shelves):
    """Генерирует список точек склада с учетом полок."""
    return [f"{col}{row}-{shelf}" for col in columns for row in rows for shelf in shelves]


def calculate_distance(point1, point2):
    """Вычисляет расстояние между двумя точками с учетом высоты."""
    col1, row1, shelf1 = point1[0], int(point1[1]), int(point1.split('-')[1])
    col2, row2, shelf2 = point2[0], int(point2[1]), int(point2.split('-')[1])

    # Переводим буквы столбцов в числа для расчёта
    x1, x2 = string.ascii_lowercase.index(col1), string.ascii_lowercase.index(col2)

    # Манхэттенское расстояние
    horizontal_distance = abs(x1 - x2) + abs(row1 - row2)

    # Затраты на высоту
    height_cost = abs(shelf1 - shelf2) * 2  # 2 шага на каждый уровень

    return horizontal_distance + height_cost


def find_shortest_route(start, waypoints, end):
    """Ищет кратчайший маршрут через все заданные точки."""
    all_points = [start] + waypoints + [end]
    all_permutations = list(itertools.permutations(waypoints))
    min_distance = float('inf')
    best_path = None

    for perm in all_permutations:
        route = [start] + list(perm) + [end]
        distance = sum(calculate_distance(route[i], route[i + 1]) for i in range(len(route) - 1))
        if distance < min_distance:
            min_distance = distance
            best_path = route

    return best_path, min_distance




start =('g1-1').strip()
end = ("g13-1").strip()

# Шаг 1: Задаём параметры склада
columns = list("abcdefgh")  # Столбцы от 'a' до 'h'
rows = range(1, 14)  # Ряды от 1 до 13
shelves = range(1, 4)  # Полки от 1 до 3

# Генерация всех точек склада (на случай валидации)
valid_points = generate_points(columns, rows, shelves)

waypoints = input("Промежуточные точки: ").strip().split(",")
waypoints = [point.strip() for point in waypoints if point.strip()]

# Шаг 3: Находим кратчайший маршрут
best_route, total_distance = find_shortest_route(start, waypoints, end)


# Вывод результата
print("\nЛучший маршрут:", " -> ".join(best_route))
print("Общее расстояние:", total_distance)
