from flask import Flask, render_template, request, jsonify
from warehouse_logic import generate_warehouse_map, bfs_shortest_path, plot_3d_route, calculate_distances, reconstruct_path, find_optimal_path

app = Flask(__name__)

# Генерация карты склада
warehouse = generate_warehouse_map()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/route', methods=['POST'])
def calculate_route():
    data = request.json
    start_point = data['start']
    end_point = data['end']
    points = data['points']

    points = [start_point] + points + [end_point]
    distances = calculate_distances(points, warehouse)
    optimal_order = [start_point] + list(find_optimal_path(points[1:-1], distances)) + [end_point]

    if not optimal_order:
        return jsonify({"error": "Не удалось найти оптимальный порядок точек!"}), 400

    shortest_path = reconstruct_path(optimal_order, warehouse)
    if shortest_path:
        plot_3d_route(shortest_path, warehouse)  # Генерация графика
        return jsonify({"path": shortest_path, "steps": len(shortest_path)})
    else:
        return jsonify({"error": "Не удалось построить маршрут!"}), 400

if __name__ == "__main__":
    app.run(debug=True)
