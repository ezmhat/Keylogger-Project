
async function get_computers() {
    let box = document.getElementById("computerList");

    try {
        const response = await fetch("http://127.0.0.1:5000/computer");

        if (!response.ok) {
            throw new Error("Failed to fetch computers");
        }

        const data = await response.json();

        box.innerHTML = ""; 

        data.computers.forEach(computer => {
            const item = document.createElement("li");
            const button = document.createElement("button");

            button.textContent = computer;
            button.onclick = () => tocomputer(computer);

            item.appendChild(button);
            box.appendChild(item);
        });
    } catch (error) {
        console.error("Error:", error);
    }
}

function tocomputer(computer) {
    window.location.href = `dataPage.html?computer=${computer}`;
}
