async function updateDashboard() {
    try {
        const res = await fetch('/api/data');
        const data = await res.json();

        // Update temperature
        const temp = data.temperature;
        document.getElementById("temp-value").textContent = `${temp.toFixed(2)} °C`;
        document.body.style.setProperty("--temperature", temp);

        // Update temperature bar
        const tempBar = document.querySelector('.temp-bar');
        let percentage = ((temp - 20) / 10) * 100;
        percentage = Math.max(0, Math.min(100, percentage));
        tempBar.style.width = `${percentage}%`;

        // Update potentiometer
        const potValue = data.potentiometer;
        document.getElementById("pot-value").textContent = potValue;

        // Map potValue (4095 to 0) to 0–360° clockwise, starting from 6 o'clock
        const angleDeg = ((4095 - potValue) / 4095) * 360 + 90;
        const angleRad = angleDeg * (Math.PI / 180);
        const radius = 40;

        const centerX = 50;
        const centerY = 45;
        const offsetX = Math.cos(angleRad) * radius;
        const offsetY = Math.sin(angleRad) * radius;

        const potLine = document.querySelector('.pot-line');
        potLine.style.left = `calc(${centerX}% + ${offsetX}px)`;
        potLine.style.top = `calc(${centerY}% + ${offsetY}px)`;
        potLine.style.transform = `translate(-50%, -50%) rotate(${angleDeg + 90}deg)`;

        // Update physical button state
        const button = document.querySelector('.button-center');
        if (data.button1 === 1) {
            button.classList.add('button-pressed');
        } else {
            button.classList.remove('button-pressed');
        }

        // Update pin configuration table
        const tableBody = document.getElementById("pin-table");
        tableBody.innerHTML = "";

        data.pins.forEach((entry) => {
            const row = document.createElement("tr");

            const indexCell = document.createElement("td");
            indexCell.textContent = entry.pin;

            const labelCell = document.createElement("td");
            labelCell.textContent = entry.label;

            const valueCell = document.createElement("td");
            valueCell.textContent = entry.value;

            row.appendChild(indexCell);
            row.appendChild(labelCell);
            row.appendChild(valueCell);

            tableBody.appendChild(row);
        });

    } catch (err) {
        console.error("Failed to fetch data:", err);
    }
}

setInterval(updateDashboard, 200);

document.querySelector('.button-center').addEventListener('click', async () => {
    try {
        await fetch('/toggle');
    } catch (err) {
        console.error('Failed to send toggle request:', err);
    }
});
