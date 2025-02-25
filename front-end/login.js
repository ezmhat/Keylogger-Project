document.getElementById("loginForm").addEventListener("enter", async function (event) {
    event.preventDefault();
    const username = document.getElementById("name").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (response.ok) {

        window.location.href = "computerList.html";

    } else {
        document.getElementById("error-message").innerText = data.error;
    }
});