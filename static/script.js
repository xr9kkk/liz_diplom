document.getElementById("route-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const startPoint = document.getElementById("start-point").value;
    const endPoint = document.getElementById("end-point").value;
    const points = document.getElementById("points").value.split(',').map(p => p.trim());

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            start_point: startPoint,
            end_point: endPoint,
            points: points,
        }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("result").innerHTML = `<p style="color: red;">Ошибка: ${data.error}</p>`;
            } else {
                document.getElementById("result").innerHTML = `
                    <p>Оптимальный порядок точек: ${data.optimal_order.join(' -> ')}</p>
                    <p>Кратчайший маршрут: ${data.shortest_path.join(' -> ')}</p>
                    <p>Количество шагов: ${data.steps_count}</p>
                    <img src="${data.plot_path}" alt="Маршрут">
                `;
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
});

//ошибка в моменте возвращения img src вот здесь надо пофикисить