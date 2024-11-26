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
        // Отобразить результаты
        displayResults(data);
        // Построить 3D график
        buildPlot(data.coordinates, data.warehouse);
    } else {
        alert('Ошибка: ' + data.error);
    }
}

function displayResults(data) {
    document.getElementById('optimal-order').textContent = `Оптимальный порядок точек: ${data.optimal_order}`;
    document.getElementById('shortest-path').textContent = `Кратчайший маршрут: ${data.shortest_path}`;
    document.getElementById('steps-count').textContent = `Количество шагов: ${data.steps_count}`;
}

function buildPlot(coordinates, warehouse) {
    const xCoords = coordinates.x;
    const yCoords = coordinates.y;
    const zCoords = coordinates.z;

    // Данные маршрута для визуализации
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

    // Создаем данные для полок
    const shelvesData = [];
    const allShelves = Array.from({ length: 13 }, (_, i) => String.fromCharCode(65 + i)); // A-M
    const maxLayer = 13;
    const maxRow = 3;

    for (let letter of allShelves) {
        for (let layer = 1; layer <= maxLayer; layer++) {
            for (let row = 1; row <= maxRow; row++) {
                const shelfKey = `${letter}-${layer}-${row}`;
                if (warehouse[shelfKey] === 'shelf') {
                    shelvesData.push({
                        x: [ord(letter) - ord('A') + 1],
                        y: [layer],
                        z: [row],
                        type: 'scatter3d',
                        mode: 'markers',
                        marker: { color: 'green', size: 6 },
                        name: `Полка ${shelfKey}`
                    });
                }
            }
        }
    }

    // Объединяем данные маршрута и полок
    const dataToPlot = [routeData, ...shelvesData];

    // Настройки для визуализации
    const layout = {
        title: '3D Маршрут на складе',
        scene: {
            xaxis: {
                title: 'Стеллажи (A-M)',
                tickvals: Array.from({ length: 13 }, (_, i) => i + 1), // Значения тиков от 1 до 13
                ticktext: Array.from({ length: 13 }, (_, i) => String.fromCharCode(65 + i)) // Буквы A-M
            },
            yaxis: {
                title: 'Ярусы (1-13)',
                tickvals: Array.from({ length: 13 }, (_, i) => i + 1)
            },
            zaxis: {
                title: 'Ряды (1-3)',
                tickvals: Array.from({ length: 3 }, (_, i) => i + 1)
            }
        }
    };

    Plotly.newPlot('warehouse3d', dataToPlot, layout);
}

// Функция для преобразования буквы в ASCII
function ord(char) {
    return char.charCodeAt(0);
}

// Функция для преобразования буквы в ASCII
function ord(char) {
    return char.charCodeAt(0);
}

document.getElementById('route-form').addEventListener('submit', fetchRouteData);
