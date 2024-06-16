
KUDOS_BASE_API_URI = "http://127.0.0.1:8000/"

function toggleSentReceived() {
    const isChecked = document.getElementById("senderReceiver-checkbox").checked;
    const SHOW_RECEIVED = "Show Received";
    const SHOW_SENT = "Show Sent";

    if (isChecked) {
        document.getElementById("labelSenderReceiver").innerText = SHOW_SENT;
    }
    else {
        document.getElementById("labelSenderReceiver").innerText = SHOW_RECEIVED;
    }
}


function getRecieved() {
    apiUri = KUDOS_BASE_API_URI + "items/recieved"
    fetch(apiUri)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("kudos");
            tableBody.innerHTML = "";

            data.forEach(item => {
                const tableRow = document.createElement("tr");
                const descriptionCell = document.createElement("td");
                descriptionCell.textContent = item.description;
                const isOpportunityCell = document.createElement("td");
                isOpportunityCell.textContent = item.is_oppertunity ? "Yes" : "No";
                const idCell = document.createElement("td");
                idCell.textContent = item.id;
                const dateCreatedCell = document.createElement("td");
                dateCreatedCell.textContent = item.date_created;
                const dateModifiedCell = document.createElement("td");
                dateModifiedCell.textContent = item.date_modified;

                // Add the cells to the row
                tableRow.appendChild(descriptionCell);
                tableRow.appendChild(isOpportunityCell);
                tableRow.appendChild(idCell);
                tableRow.appendChild(dateCreatedCell);
                tableRow.appendChild(dateModifiedCell);

                // Add the row to the table
                tableBody.appendChild(tableRow);
            });
        })
        .catch(error => console.error(error));
}
