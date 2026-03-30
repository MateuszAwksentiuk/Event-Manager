document.addEventListener("DOMContentLoaded", loadEvents);

async function loadEvents() {
    const container = document.getElementById("events-container");

    const response = await fetch("/api/events/");
    const events = await response.json();

    container.innerHTML = "";

    events.forEach(event => {
        const card = document.createElement("a");
        card.className = "event-card";
        card.href = `/events/${event.id}/`;

        card.innerHTML = `
            <div class="event-image">
                <img src="${event.image || '/static/images/placeholder.png'}">
            </div>
            <div class="event-content">
                <h3>${event.title}</h3>
                <p>${event.description}</p>
            </div>
        `;

        container.appendChild(card);
    });
}

// function formatDate(dateString) {
//     const date = new Date(dateString);
//     return date.toLocaleString();
// }