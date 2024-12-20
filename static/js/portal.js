document.addEventListener('DOMContentLoaded', function () {
    const latestUsersTable = document.querySelector('#latest-users-table tbody');
    const messagesTable = document.querySelector('#messages-table tbody');
    const emailDropdown = document.getElementById('email-dropdown');
    const fetchButton = document.getElementById('fetch-button');

    // Display a loading spinner while data is being fetched
    function showLoadingSpinner(parentElement) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = `<div class="spinner"></div>`;
        parentElement.innerHTML = '';
        parentElement.appendChild(spinner);
    }

    // Fetch and populate latest user interactions
    fetch('/fetch_latest_users')
        .then(response => {
            if (!response.ok) throw new Error(`Error: ${response.statusText}`);
            return response.json();
        })
        .then(data => {
            if (!Array.isArray(data)) throw new Error("Unexpected response format");

            data.forEach(user => {
                const row = `
                    <tr>
                        <td>${user.user_id}</td>
                        <td>${user.fname}</td>
                        <td>${user.lname}</td>
                        <td>${new Date(user.timestamp).toLocaleString()}</td>
                    </tr>
                `;
                latestUsersTable.innerHTML += row;

                if (user.email) {
                    const option = document.createElement('option');
                    option.value = user.email;
                    option.textContent = user.email;
                    emailDropdown.appendChild(option);
                }
            });
        })
        .catch(error => console.error("Failed to fetch latest users:", error));

    // Fetch messages based on email
    fetchButton.addEventListener('click', function () {
        const selectedEmail = emailDropdown.value;

        showLoadingSpinner(messagesTable);

        fetch(`/fetch_messages?email=${selectedEmail}`)
            .then(response => {
                if (!response.ok) throw new Error(`Error: ${response.statusText}`);
                return response.json();
            })
            .then(data => {
                if (!Array.isArray(data)) throw new Error("Unexpected response format");

                messagesTable.innerHTML = '';
                data.forEach(message => {
                    const row = `
                        <tr>
                            <td>${message.user_id}</td>
                            <td>${message.email}</td>
                            <td>${message.fname}</td>
                            <td>${message.lname}</td>
                            <td>${message.user_message}</td>
                            <td>${message.bot_reply}</td>
                            <td>${new Date(message.timestamp).toLocaleString()}</td>
                        </tr>
                    `;
                    messagesTable.innerHTML += row;
                });
            })
            .catch(error => console.error("Failed to fetch messages:", error));
    });
});
