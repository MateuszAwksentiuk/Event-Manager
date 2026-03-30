document.addEventListener("DOMContentLoaded", loadEvents);

async function loadEvents() {
    const container = document.getElementById("events-container");

    try {
        const response = await fetch("/api/events/");
        const events = await response.json();

        container.innerHTML = "";

        if (events.length === 0) {
            container.innerHTML = "<p>Brak wydarzeń</p>";
            return;
        }

        events.forEach(event => {
            const div = document.createElement("div");

            div.innerHTML = `
                <h3>${event.title}</h3>
                <p>${event.description}</p>
                <p>Start: ${formatDate(event.start_datetime)}</p>
                <hr>
            `;

            container.appendChild(div);
        });

    } catch (error) {
        container.innerHTML = "<p>Błąd ładowania danych</p>";
        console.error(error);
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}