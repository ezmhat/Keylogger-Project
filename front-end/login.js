document.getElementById("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const userName = document.getElementById("name").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ userName, password })
        });

        const data = await response.json();
        if (response.ok) {
            window.location.href = "computerList.html";
        } else {
            document.getElementById("error-message").innerText = data.error || "❌ An error occurred. Please try again.";
        }
    } catch (error) {
        document.getElementById("error-message").innerText = "Network error. Please try again.";
    }
});
