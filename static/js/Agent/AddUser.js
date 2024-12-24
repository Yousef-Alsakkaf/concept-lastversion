document.addEventListener("DOMContentLoaded", () => {
    const createUserForm = document.getElementById("create-user-form");

    createUserForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const agent_name = document.getElementById("user-name").value;
        const userId = localStorage.getItem('user_id');
        const formData = {
            userId: userId,
            agent_name: agent_name,
            gender: document.getElementById("user-gender").value,
            image_url: `${agent_name}.png`,
            agent_prompt: document.getElementById("user-prompt").value,
            agent_role: document.getElementById("user-role").value,
        };

        try {
            const response = await fetch("/add_user", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                const data = await response.json();
                alert(`Agent added successfully! Agent ID: ${data.agent_id}`);
                createUserForm.reset();
                document.getElementById("create-user-popup").style.display = "none";
                location.reload(true)
            } else {
                const error = await response.json();
                alert(`Error: ${error.error}`);
            }
        } catch (error) {
            console.error("An error occurred:", error);
            alert("An error occurred while adding the agent.");
        }
    });

    const popup = document.getElementById("create-user-popup");
    const openButton = document.querySelector(".create-user-button");
    const closeButton = document.querySelector(".popup-close");

    openButton.addEventListener("click", () => {
        popup.style.display = "block";
    });

    closeButton.addEventListener("click", () => {
        popup.style.display = "none";
    });

    window.addEventListener("click", (event) => {
        if (event.target === popup) {
            popup.style.display = "none";
        }
    });

});

document.addEventListener("DOMContentLoaded", function () {
    const bro = document.querySelector(".popup-close");

    if (bro) {  // Ensure the element exists
        bro.addEventListener("click", async (event) => {
            console.log('close button is being clicked');
        });
    } else {
        console.log("close button not found");
    }
});
