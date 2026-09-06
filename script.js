const API_URL = "http://127.0.0.1:8000";


// IMAGE INPUT

const imageInput = document.getElementById("imageInput");

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (!file) {
        return;
    }

    document.getElementById("fileName").textContent =
        file.name;

    const imageURL = URL.createObjectURL(file);

    document.getElementById("preview").src =
        imageURL;

    document.getElementById("previewSection")
        .style.display = "block";

});


// PREDICT DISEASE

async function predictDisease() {

    const file = imageInput.files[0];

    if (!file) {

        alert("Please select a crop image.");

        return;
    }


    const formData = new FormData();

    formData.append("file", file);


    // Hide previous result

    document.getElementById("resultSection")
        .style.display = "none";


    // Show loading

    document.getElementById("loadingSection")
        .style.display = "block";


    try {

        const response = await fetch(
            `${API_URL}/predict`,
            {
                method: "POST",
                body: formData
            }
        );


        if (!response.ok) {

            throw new Error(
                "Server returned an error"
            );

        }


        const result = await response.json();


        // Display result

        document.getElementById("disease")
            .textContent = result.disease;


        document.getElementById("confidence")
            .textContent =
            result.confidence + "%";


        document.getElementById("severity")
            .textContent =
            result.severity;


        document.getElementById("cause")
            .textContent =
            result.cause;


        document.getElementById("solution")
            .textContent =
            result.solution;


        // Show result

        document.getElementById("resultSection")
            .style.display = "block";


        // Update history

        loadHistory();


    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to the AI server. " +
            "Please make sure the backend is running."
        );

    } finally {

        document.getElementById("loadingSection")
            .style.display = "none";

    }

}


// LOAD HISTORY

async function loadHistory() {

    try {

        const response = await fetch(
            `${API_URL}/history`
        );


        if (!response.ok) {
            throw new Error("History loading failed");
        }


        const data = await response.json();


        const history =
            document.getElementById("history");


        history.innerHTML = "";


        if (data.length === 0) {

            history.innerHTML =
                `<p class="empty">
                    No prediction history available.
                 </p>`;

            return;
        }


        data.forEach(item => {

            const div =
                document.createElement("div");


            div.className =
                "history-item";


            div.innerHTML = `
                <strong>
                    ${item.prediction}
                </strong>

                <br>

                File:
                ${item.filename}

                <br>

                Confidence:
                ${item.confidence}%
            `;


            history.appendChild(div);

        });


    } catch (error) {

        console.error(
            "History error:",
            error
        );

    }

}


// LOAD HISTORY WHEN PAGE OPENS

window.addEventListener(
    "load",
    loadHistory
);