async function askAssistant() {
    let query = document.getElementById("query").value;
    let responseDiv = document.getElementById("response-container");
    
    if(!query.trim()) {
        responseDiv.innerHTML = "<p>Please enter a valid query.</p>";
        return;
    }
    responseDiv.innerHTML = "<p>Loading...</p>";

    try {
        let response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });         
        let data = await response.json();

        if (response.ok) {
            responseDiv.innerHTML = `<p><strong>Response:</strong> ${data.answer}</p>`;
        } else {
            responseDiv.innerHTML = `<p><strong>Error:</strong> ${data.error}</p>`;
        }
    } catch (error) {
        responseDiv.innerHTML = `<p><strong>Error:</strong> ${error.message}</p>`;
    }       
}