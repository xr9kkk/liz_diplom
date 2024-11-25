import React, { useEffect } from 'react';
import * as THREE from 'three';

const Visual = ({ coordinates }) => {
  useEffect(() => {
    if (coordinates) {
      const { x, y, z } = coordinates;

      const container = document.getElementById('visualization-container');
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / container.offsetHeight, 0.1, 1000);
      const renderer = new THREE.WebGLRenderer();
      renderer.setSize(container.offsetWidth, container.offsetHeight);
      container.appendChild(renderer.domElement);

      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambientLight);

      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(5, 5, 5).normalize();
      scene.add(directionalLight);

      const shelfMaterial = new THREE.MeshLambertMaterial({ color: 0xeeeeee });
      const shelfGeometry = new THREE.BoxGeometry(1, 1, 1);

      for (let xCoord = 0; xCoord < 13; xCoord++) {
        for (let yCoord = 0; yCoord < 13; yCoord++) {
          for (let zCoord = 0; zCoord < 3; zCoord++) {
            const shelf = new THREE.Mesh(shelfGeometry, shelfMaterial);
            shelf.position.set(xCoord, yCoord, zCoord);
            scene.add(shelf);
          }
        }
      }

      const routeGeometry = new THREE.BufferGeometry();
      const routeVertices = [];
      for (let i = 0; i < x.length; i++) {
        routeVertices.push(x[i], y[i], z[i]);
      }
      routeGeometry.setAttribute('position', new THREE.Float32BufferAttribute(routeVertices, 3));
      const routeMaterial = new THREE.LineBasicMaterial({ color: 0x0000ff, linewidth: 2 });
      const routeLine = new THREE.Line(routeGeometry, routeMaterial);
      scene.add(routeLine);

      const pointMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
      for (let i = 0; i < x.length; i++) {
        const pointGeometry = new THREE.SphereGeometry(0.1);
        const point = new THREE.Mesh(pointGeometry, pointMaterial);
        point.position.set(x[i], y[i], z[i]);
        scene.add(point);
      }

      camera.position.z = 15;

      const animate = () => {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
      };
      animate();
    }
  }, [coordinates]);

  return null;
};

export default Visual;
