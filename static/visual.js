import React from 'react';
import ReactDOM from 'react-dom';

// Компонент для визуализации маршрута
const RouteVisualization = ({ coordinates }) => {
    const { x, y, z } = coordinates;

    return (
        <div className="visualization">
            <h2>Визуализация маршрута</h2>
            <svg width="500" height="500">
                {x.map((coord, index) => (
                    <circle
                        key={index}
                        cx={coord * 30} // Масштабирование координат
                        cy={z[index] * 30}
                        r="5"
                        fill="blue"
                    />
                ))}
                {x.map((_, index) => {
                    if (index === 0) return null;
                    return (
                        <line
                            key={index}
                            x1={x[index - 1] * 30}
                            y1={z[index - 1] * 30}
                            x2={x[index] * 30}
                            y2={z[index] * 30}
                            stroke="red"
                        />
                    );
                })}
            </svg>
        </div>
    );
};

// Получаем данные маршрута из глобального объекта
const coordinates = JSON.parse(document.getElementById('coordinates-data').textContent);

ReactDOM.render(
    <RouteVisualization coordinates={coordinates} />,
    document.getElementById('root')
);
