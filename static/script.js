import Visual from './visual.js';

function calculateRoute() {
    const startPoint = document.getElementById('start-point').value.trim().toUpperCase();
    const endPoint = document.getElementById('end-point').value.trim().toUpperCase();
    const pointsInput = document.getElementById('points').value.trim();
    const points = pointsInput ? pointsInput.split(',').map(p => p.trim().toUpperCase()) : [];

    const data = {
        start_point: startPoint,
        end_point: endPoint,
        points: points
    };

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            displayRoute(data);
        }
    })
    .catch(error => {
        console.error("Ошибка при отправке запроса:", error);
        alert("Произошла ошибка при расчете маршрута.");
    });
}

function displayRoute(data) {
    document.getElementById('result').innerHTML = `
        <h2>Маршрут найден!</h2>
        <p><strong>Оптимальный порядок точек:</strong> ${data.optimal_order.join(' → ')}</p>
        <p><strong>Кратчайший путь:</strong> ${data.shortest_path.join(' → ')}</p>
        <p><strong>Количество шагов:</strong> ${data.steps_count}</p>
    `;

    ReactDOM.render(
        React.createElement(Visual, { coordinates: data.coordinates }),
        document.getElementById('react-root')
    );
}

document.getElementById('route-form').addEventListener('submit', function(event) {
    event.preventDefault();
    calculateRoute();
});
