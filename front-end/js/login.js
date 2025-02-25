

    
 document.getElementById("loginForm").addEventListener("submit",async (event)=>{
    event.preventDefault();
    const userName = document.getElementById("name").value;
    const password = document.getElementById("password").value;
    const responds = await fetch("http://127.0.0.1:5000/login",{
        method:"POST",
        header:{"Content type":"application/json"},
        body: JSON.stringify({userName,password})

    });
    if (responds.ok){
        windows.location.href = computerList.html
    }


})