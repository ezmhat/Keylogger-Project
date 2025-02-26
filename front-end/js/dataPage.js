async function get_log(date) {
    let box = document.getElementById("dataTable");
    const urlParams = new URLSearchParams(window.location.search);
    const computer = urlParams.get("computer");

    if (!computer) {
        console.error("No computer parameter found in URL");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/logs/${computerId}/${date}`);
        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }

        const data = await response.json();
        box.innerHTML = "";

        Object.entries(data).forEach(([time, log]) => {
            const row = document.createElement("tr");

            const timeCell = document.createElement("td");
            timeCell.innerText = time;

            const logCell = document.createElement("td");
            logCell.innerText = log;

            row.appendChild(timeCell);
            row.appendChild(logCell);
            box.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

document.getElementById("searchDate").addEventListener("submit", async (event) => {
    event.preventDefault();
    const date = document.getElementById("date").value;
    if (date) {
        get_log(date);
    }
});
