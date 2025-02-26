document.getElementById("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const userName = document.getElementById("name").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userName, password })
    });

    if (response.ok) {
        window.location.href = "computerList.html";
    } else {
        alert("Erreur de connexion. Vérifie tes identifiants.");
    }
});
