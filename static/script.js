document.getElementById("routeForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const start = document.getElementById("start").value.trim();
    const end = document.getElementById("end").value.trim();
    const points = document.getElementById("points").value.trim().split(",").map(p => p.trim());

    const response = await fetch('/route', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ start, end, points }),
    });

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    if (response.ok) {
        const data = await response.json();
        resultDiv.innerHTML = `
            <h3>Shortest Path:</h3>
            <p>${data.path.join(" -> ")}</p>
            <p>Steps: ${data.steps}</p>
        `;
    } else {
        const error = await response.json();
        resultDiv.innerHTML = `<p style="color: red;">Error: ${error.error}</p>`;
    }
});
