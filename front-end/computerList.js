let allComputers = [];

// Function to fetch the list of computers from the server
async function get_computers() {
    let box = document.getElementById("computerList");

    try {
        const response = await fetch("http://127.0.0.1:5000/computers"); // Fetch computers from the server

        if (!response.ok) {
            throw new Error("Failed to fetch computers");
        }

        const data = await response.json();
        allComputers = data.computers; // Store all computers

        // Display all computers in the list
        displayComputers(allComputers);
    } catch (error) {
        console.error("Error:", error);
    }
}

// Function to display the list of computers
function displayComputers(computers) {
    const box = document.getElementById("computerList");
    box.innerHTML = ""; // Clear the list before adding new items

    computers.forEach(computer => {
        const item = document.createElement("li");
        const button = document.createElement("button");

        button.textContent = computer;
        button.onclick = () => tocomputer(computer);

        // Style the button to fill the entire <li> element
        button.style.cssText = "all: unset; width: 100%; height: 100%; cursor: pointer; display: block;";

        item.appendChild(button);
        box.appendChild(item);
    });
}

// Function to filter computers based on search input
function filterComputers() {
    const searchInput = document.getElementById("searchInput").value.toLowerCase();
    const filteredComputers = allComputers.filter(computer =>
        computer.toLowerCase().includes(searchInput)
    );

    displayComputers(filteredComputers); // Display filtered computers
}

// Function to navigate to the selected computer's data page
function tocomputer(computer) {
    window.location.href = `dataPage.html?computer=${computer}`;
}

// Load the list of computers when the page is fully loaded
document.addEventListener("DOMContentLoaded", get_computers);

document.addEventListener("DOMContentLoaded", () => {
    // Retrieve the user's name from local storage or session storage
    const userName = localStorage.getItem("userName") || sessionStorage.getItem("userName");
    const userLogElement = document.getElementById("userLog");

    if (userLogElement && userName) {
        userLogElement.innerText = userName; // Update the displayed name
    } else {
        console.warn("No name found or element 'userLog' missing.");
    }
});
