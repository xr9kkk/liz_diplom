// Функция для отправки данных на сервер и получения маршрута
async function fetchRouteData(event) {
    event.preventDefault();

    const startPoint = document.getElementById('start-point').value.trim().toUpperCase();
    const endPoint = document.getElementById('end-point').value.trim().toUpperCase();
    const points = document.getElementById('points').value
        .split(',')
        .map(point => point.trim().toUpperCase());

    const response = await fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            start_point: startPoint,
            end_point: endPoint,
            points: points
        })
    });

    const data = await response.json();
    if (response.ok) {
        buildPlot(data.coordinates);
    } else {
        alert('Ошибка: ' + data.error);
    }
}

// Функция для построения 3D графика маршрута
function buildPlot(coordinates) {
    const xCoords = coordinates.x;
    const yCoords = coordinates.y;
    const zCoords = coordinates.z;

    const routeData = {
        x: xCoords,
        y: yCoords,
        z: zCoords,
        type: 'scatter3d',
        mode: 'lines+markers',
        line: { color: 'blue', width: 4 },
        marker: { color: 'red', size: 6 },
        name: 'Маршрут'
    };

    const layout = {
        title: '3D Маршрут на складе',
        scene: {
            xaxis: { title: 'Стеллажи (A-M)', tickvals: Array.from({ length: 13 }, (_, i) => i) },
            yaxis: { title: 'Ярусы (1-13)', tickvals: Array.from({ length: 13 }, (_, i) => i) },
            zaxis: { title: 'Ряды (1-3)', tickvals: Array.from({ length: 3 }, (_, i) => i) }
        }
    };

    Plotly.newPlot('warehouse3d', [routeData], layout);
}

// Добавляем обработчик отправки формы
document.getElementById('route-form').addEventListener('submit', fetchRouteData);
