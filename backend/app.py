from flask import Flask, render_template, request, jsonify, send_from_directory
import warehouse_logic as wl

app = Flask(__name__, static_folder='static', static_url_path='/static')

warehouse = wl.generate_warehouse_map()

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate_route():
    data = request.json
    print("Полученные данные:", data)  # Логируем данные, которые приходят с клиента
    start_point = data.get("start_point", "").strip().upper()
    end_point = data.get("end_point", "").strip().upper()
    intermediate_points = [p.strip().upper() for p in data.get("points", [])]

    if not start_point or not end_point:
        return jsonify({"error": "Укажите начальную и конечную точки!"}), 400

    # Проверка корректности точек
    points = [start_point]
    for point in intermediate_points:
        if point not in warehouse or warehouse[point] != "shelf":
            print(f"Ошибка: точка {point} недоступна!")  # Логируем ошибку
            return jsonify({"error": f"Точка {point} недоступна!"}), 400
        access_points = wl.find_accessible_points(point, warehouse)
        if access_points:
            points.append(access_points[0])
        else:
            print(f"Ошибка: для точки {point} нет доступных точек!")  # Логируем ошибку
            return jsonify({"error": f"Для {point} нет доступных точек!"}), 400

    points.append(end_point)

    # Вычисление маршрута
    distances = wl.calculate_distances(points, warehouse)
    optimal_order = [start_point] + list(wl.find_optimal_path(points[1:-1], distances)) + [end_point]

    if not optimal_order:
        print("Ошибка: не удалось найти оптимальный порядок точек!")  # Логируем ошибку
        return jsonify({"error": "Не удалось найти оптимальный порядок точек!"}), 400

    shortest_path = wl.reconstruct_path(optimal_order, warehouse)
    if not shortest_path:
        print("Ошибка: не удалось построить маршрут!")  # Логируем ошибку
        return jsonify({"error": "Не удалось построить маршрут!"}), 400

    # Преобразование маршрута в координаты для визуализации
    x_coords = []
    y_coords = []
    z_coords = []

    for point in shortest_path:
        shelf, layer, row = point.split('-')
        x_coords.append(ord(shelf[0]) - ord('A') + 1)
        y_coords.append(int(layer))
        z_coords.append(int(row))

    response = {
    "optimal_order": optimal_order,
    "shortest_path": shortest_path,
    "steps_count": len(shortest_path),
    "coordinates": {
        "x": x_coords,
        "y": y_coords,
        "z": z_coords
    },
    "warehouse": warehouse  
}

    return jsonify(response)

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
