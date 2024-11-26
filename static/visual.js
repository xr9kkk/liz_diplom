const { useEffect, useState } = React;

const Visual = ({ coordinates }) => {
    const [OrbitControls, setOrbitControls] = useState(null);

    useEffect(() => {
        // Динамически загружаем OrbitControls
        const loadOrbitControls = async () => {
            const module = await import('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/examples/js/controls/OrbitControls.js');
            setOrbitControls(module.OrbitControls); 
        };

        loadOrbitControls();
    }, []);

    useEffect(() => {
        if (!coordinates || !OrbitControls) return;

        const container = document.getElementById('visualization-container');
        container.innerHTML = ''; // Очищаем контейнер

        const { x, y, z } = coordinates;

        // Создаем сцену, камеру и рендерер
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / container.offsetHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(container.offsetWidth, container.offsetHeight);
        container.appendChild(renderer.domElement);

        // Освещение
        const light = new THREE.AmbientLight(0xffffff, 0.8);
        scene.add(light);

        // Стеллажи
        const shelvesMaterial = new THREE.MeshBasicMaterial({ color: 0xdddddd });
        const shelvesGeometry = new THREE.BoxGeometry(1, 1, 1);

        for (let i = 0; i < 13; i++) {
            for (let j = 0; j < 13; j++) {
                for (let k = 0; k < 3; k++) {
                    const shelf = new THREE.Mesh(shelvesGeometry, shelvesMaterial);
                    shelf.position.set(i, j, k);
                    scene.add(shelf);
                }
            }
        }

        // Маршрут
        const routeMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });
        const routeGeometry = new THREE.BufferGeometry().setFromPoints(
            x.map((_, i) => new THREE.Vector3(x[i], y[i], z[i]))
        );
        const routeLine = new THREE.Line(routeGeometry, routeMaterial);
        scene.add(routeLine);

        // Позиция камеры
        camera.position.set(6, 6, 15);
        camera.lookAt(new THREE.Vector3(6, 6, 1));

        // Добавляем OrbitControls
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true; // Плавное торможение
        controls.dampingFactor = 0.05;
        controls.enableZoom = true; // Включить зум
        controls.minDistance = 5; // Минимальное расстояние камеры
        controls.maxDistance = 50; // Максимальное расстояние камеры

        // Анимация
        const animate = () => {
            requestAnimationFrame(animate);
            controls.update(); // Обновление OrbitControls
            renderer.render(scene, camera);
        };
        animate();

        // Очистка ресурса при размонтировании компонента
        return () => {
            renderer.dispose();
            controls.dispose();
        };
    }, [coordinates, OrbitControls]);

    return null;
};

export default Visual;
