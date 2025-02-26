let allComputers = [];

async function get_computers() {
    let box = document.getElementById("computerList");

    try {
        const response = await fetch("http://127.0.0.1:5000/computers"); // Correction de l'URL ici

        if (!response.ok) {
            throw new Error("Failed to fetch computers");
        }

        const data = await response.json();
        allComputers = data.computers; // Stocker tous les ordinateurs

        // Afficher tous les ordinateurs
        displayComputers(allComputers);
    } catch (error) {
        console.error("Error:", error);
    }
}

function displayComputers(computers) {
    const box = document.getElementById("computerList");
    box.innerHTML = ""; // Vider la liste avant d'ajouter

    computers.forEach(computer => {
        const item = document.createElement("li");
        const button = document.createElement("button");

        button.textContent = computer;
        button.onclick = () => tocomputer(computer);

        item.appendChild(button);
        box.appendChild(item);
    });
}

function filterComputers() {
    const searchInput = document.getElementById("searchInput").value.toLowerCase();
    const filteredComputers = allComputers.filter(computer =>
        computer.toLowerCase().includes(searchInput)
    );

    displayComputers(filteredComputers); // Afficher les ordinateurs filtrés
}

function tocomputer(computer) {
    window.location.href = `dataPage.html?computer=${computer}`;
}

// Appel de la fonction pour charger les ordinateurs au chargement de la page
document.addEventListener("DOMContentLoaded", get_computers);
