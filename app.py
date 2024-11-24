from flask import Flask, render_template, request, jsonify
import warehouse_logic as wl


app = Flask(__name__)
warehouse = wl.generate_warehouse_map()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_route():
    data = request.json  # Получаем данные из запроса
    warehouse = wl.generate_warehouse_map()

    start_point = data.get("start_point", "").strip().upper()
    end_point = data.get("end_point", "").strip().upper()
    intermediate_points = [p.strip().upper() for p in data.get("points", [])]

    if not start_point or not end_point:
        return jsonify({"error": "Укажите начальную и конечную точки!"}), 400

    # Проверка корректности точек
    points = [start_point]
    for point in intermediate_points:
        if point not in warehouse or warehouse[point] != "shelf":
            return jsonify({"error": f"Точка {point} недоступна!"}), 400
        access_points = wl.find_accessible_points(point, warehouse)
        if access_points:
            points.append(access_points[0])
        else:
            return jsonify({"error": f"Для {point} нет доступных точек!"}), 400

    points.append(end_point)

    # Вычисление маршрута
    distances = wl.calculate_distances(points, warehouse)
    optimal_order = [start_point] + list(wl.find_optimal_path(points[1:-1], distances)) + [end_point]

    if not optimal_order:
        return jsonify({"error": "Не удалось найти оптимальный порядок точек!"}), 400

    shortest_path = wl.reconstruct_path(optimal_order, warehouse)
    if not shortest_path:
        return jsonify({"error": "Не удалось построить маршрут!"}), 400

    # Преобразование маршрута в координаты для визуализации
    # Предположим, что shortest_path - это список точек вида "A-01-01", "B-02-03" и т.д.
    x_coords = []
    y_coords = []
    z_coords = []

    # Преобразование точек маршрута в координаты (x, y, z) для визуализации
    for point in shortest_path:
        shelf, layer, row = point.split('-')
        x_coords.append(ord(shelf[0]) - ord('A') + 1)
        y_coords.append(int(layer))     # Ярусы 1-3
        z_coords.append(int(row))       # Ряды 1-13

    response = {
        "optimal_order": optimal_order,
        "shortest_path": shortest_path,
        "steps_count": len(shortest_path),
        "coordinates": {
            "x": x_coords,
            "y": y_coords,
            "z": z_coords
        }
    }

    return jsonify(response)

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
