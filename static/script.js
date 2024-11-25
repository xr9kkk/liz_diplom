// Функция для отправки данных на сервер и получения ответа
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

    // Отправляем запрос на сервер
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
            // Обработка успешного ответа
            displayRoute(data);
        }
    })
    .catch(error => {
        console.error("Ошибка при отправке запроса:", error);
        alert("Произошла ошибка при расчете маршрута.");
    });
}

// Функция для отображения маршрута
function displayRoute(data) {
    // Отображаем оптимальный порядок точек
    document.getElementById('result').innerHTML = `
        <h2>Маршрут найден!</h2>
        <p><strong>Оптимальный порядок точек:</strong> ${data.optimal_order.join(' → ')}</p>
        <p><strong>Кратчайший путь:</strong> ${data.shortest_path.join(' → ')}</p>
        <p><strong>Количество шагов:</strong> ${data.steps_count}</p>
    `;

    // Визуализация маршрута с помощью Three.js
    plotRoute(data.coordinates);
}

// Функция для визуализации маршрута в 3D с помощью Three.js
function plotRoute(coordinates) {
    const x_coords = coordinates.x;
    const y_coords = coordinates.y;
    const z_coords = coordinates.z;

    // Получаем контейнер для отображения визуализации
    const container = document.getElementById('visualization-container');

    // Создаем сцену, камеру и рендерер
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / container.offsetHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(container.offsetWidth, container.offsetHeight);
    container.appendChild(renderer.domElement);

    // Линия маршрута
    const geometry = new THREE.BufferGeometry();
    const vertices = [];
    for (let i = 0; i < x_coords.length; i++) {
        vertices.push(x_coords[i], y_coords[i], z_coords[i]);
    }
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    const material = new THREE.LineBasicMaterial({ color: 0x0000ff, linewidth: 2 });
    const line = new THREE.Line(geometry, material);
    scene.add(line);

    // Точки маршрута
    const pointMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    for (let i = 0; i < x_coords.length; i++) {
        const pointGeometry = new THREE.SphereGeometry(0.1);
        const point = new THREE.Mesh(pointGeometry, pointMaterial);
        point.position.set(x_coords[i], y_coords[i], z_coords[i]);
        scene.add(point);
    }

    // Камера
    camera.position.z = 5;

    // Переменные для управления камерой вручную
    let isMouseDown = false;
    let mouseX = 0;
    let mouseY = 0;
    let deltaX = 0;
    let deltaY = 0;

    // Слушатели событий мыши для вращения
    container.addEventListener('mousedown', (event) => {
        isMouseDown = true;
        mouseX = event.clientX;
        mouseY = event.clientY;
    });

    container.addEventListener('mousemove', (event) => {
        if (!isMouseDown) return;

        deltaX = event.clientX - mouseX;
        deltaY = event.clientY - mouseY;

        // Изменение углов обзора на основе перемещения мыши
        camera.rotation.y += deltaX * 0.005;
        camera.rotation.x += deltaY * 0.005;

        mouseX = event.clientX;
        mouseY = event.clientY;
    });

    container.addEventListener('mouseup', () => {
        isMouseDown = false;
    });

    // Для зума с помощью колеса мыши
    container.addEventListener('wheel', (event) => {
        camera.position.z += event.deltaY * 0.1;
    });

    // Анимация
    function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    }
    animate();
}

// Подключаем обработчик на форму для отправки данных
document.getElementById('route-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы
    calculateRoute(); // Отправляем запрос для вычисления маршрута
});
