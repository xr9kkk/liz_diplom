const { useEffect } = React;

const Visual = ({ coordinates }) => {
    useEffect(() => {
        if (!coordinates) return;

        const container = document.getElementById('visualization-container');
        container.innerHTML = ''; // Очищаем контейнер

        const { x, y, z } = coordinates;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / container.offsetHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(container.offsetWidth, container.offsetHeight);
        container.appendChild(renderer.domElement);

        const light = new THREE.AmbientLight(0xffffff, 0.8);
        scene.add(light);

        const shelvesMaterial = new THREE.MeshBasicMaterial({ color: 0xdddddd });
        const shelvesGeometry = new THREE.BoxGeometry(0.5, 0.5, 0.5); // Попробуйте уменьшенные размеры


        for (let i = 0; i < 13; i++) {
            for (let j = 0; j < 13; j++) {
                for (let k = 0; k < 3; k++) {
                    const shelf = new THREE.Mesh(shelvesGeometry, shelvesMaterial);
                    shelf.position.set(i, j, k);
                    scene.add(shelf);
                }
            }
        }

        const routeMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });
        const routeGeometry = new THREE.BufferGeometry().setFromPoints(
            x.map((_, i) => new THREE.Vector3(x[i], y[i], z[i]))
        );
        const routeLine = new THREE.Line(routeGeometry, routeMaterial);
        scene.add(routeLine);
        
        camera.position.set(6, 6, 10); // Камера расположена над центром склада
        camera.lookAt(new THREE.Vector3(6, 6, 1)); // Смотрит на середину склада
        
        console.log("Scene children:", scene.children);

        const animate = () => {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        };
        animate();
    }, [coordinates]);

    return React.createElement('div', null); 
};

export default Visual;
