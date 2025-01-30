function redirectToNewPage() {
    window.location.href = "index.html"; // Replace with the desired URL
}

function runScript(scriptName) {
    fetch('/run_script', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'script=' + scriptName,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerText = data.output;
    });
}

function redirectToNewPage1() {
    window.location.href = "http://127.0.0.1:5000"; // Replace with the desired URL
}
