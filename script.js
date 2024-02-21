console.log("helo")
document.getElementById("summarise").addEventListener("click", function() {
    const url = document.getElementById("youtubeLink").value;
    const outputElement = document.getElementById("output");

    if (url.trim() === "") {
        displayErrorMessage(outputElement, "Please enter a valid YouTube link.");
        return;
    }

    document.getElementById("summarise").disabled = true;
    document.getElementById("summarise").innerHTML = "Summarising...";

    fetch(`http://127.0.0.1:5000/summary?url=${encodeURIComponent(url)}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { throw new Error(data.error) });
            }
            return response.text();
        })
        .then(data => {
            displayResult(outputElement, data);
        })
        .catch(error => {
            console.error("Error:", error);
            displayErrorMessage(outputElement, error.message || "An error occurred while summarising.");
        })
        .finally(() => {
            document.getElementById("summarise").disabled = false;
            document.getElementById("summarise").innerHTML = "Summarise";
        });
});

function displayErrorMessage(element, message) {
    element.style.display = "block";
    element.style.color = "#ff0000"; // Red color for error messages
    element.style.fontWeight = "bold";
    element.innerHTML = message;
}

function displayResult(element, result) {
    element.style.display = "block";
    element.style.color = "black"; // Reset color
    element.style.fontWeight = "500"; // Reset font weight
    element.innerHTML = result;
}
