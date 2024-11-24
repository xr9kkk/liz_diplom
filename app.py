from flask import Flask, render_template, request, jsonify
from warehouse_logic import generate_warehouse_map, calculate_distances, find_optimal_path, reconstruct_path, plot_3d_route, find_accessible_points
import os

app = Flask(__name__)
warehouse = generate_warehouse_map()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_route():
    data = request.json  # Получаем данные из запроса
    warehouse = generate_warehouse_map()

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
        access_points = find_accessible_points(point, warehouse)
        if access_points:
            points.append(access_points[0])
        else:
            return jsonify({"error": f"Для {point} нет доступных точек!"}), 400

    points.append(end_point)

    # Вычисление маршрута
    distances = calculate_distances(points, warehouse)
    optimal_order = [start_point] + list(find_optimal_path(points[1:-1], distances)) + [end_point]

    if not optimal_order:
        return jsonify({"error": "Не удалось найти оптимальный порядок точек!"}), 400

    shortest_path = reconstruct_path(optimal_order, warehouse)
    if not shortest_path:
        return jsonify({"error": "Не удалось построить маршрут!"}), 400

    # Возвращаем результат в JSON-формате
    response = {
        "optimal_order": optimal_order,
        "shortest_path": shortest_path,
        "steps_count": len(shortest_path),
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
