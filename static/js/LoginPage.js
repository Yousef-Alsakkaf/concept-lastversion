document.addEventListener("DOMContentLoaded", () => {
    const loginRadio = document.getElementById("login-radio");
    const signupRadio = document.getElementById("signup-radio");
    const authTitle = document.getElementById("auth-title");
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");

    // Toggle between Login and Signup forms
    loginRadio.addEventListener("change", () => {
        if (loginRadio.checked) {
            authTitle.textContent = "Login to Coceptiv AI";
            loginForm.classList.remove("hidden");
            signupForm.classList.add("hidden");
        }
    });

    signupRadio.addEventListener("change", () => {
        if (signupRadio.checked) {
            authTitle.textContent = "Signup with Coceptiv AI";
            signupForm.classList.remove("hidden");
            loginForm.classList.add("hidden");
        }
    });

    // Handle Login Form Submission
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = document.getElementById("login-email").value;
        
        const password = document.getElementById("login-password").value;
    
        try {
            const response = await fetch("/loginuser", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });
    
            let data;
            try {
                data = await response.json(); // Attempt to parse JSON
            } catch (jsonError) {
                throw new Error("Server returned invalid response format.");
            }
    
            if (!response.ok) {
                throw new Error(data.message || "Login failed.");
            }
    
            alert(data.message);
    
            // Store user ID and preload chat history
            localStorage.setItem("user_id", data.user.user_id);
            if (data.history) preloadChatHistory(data.history);
    
            if (data.redirect) window.location.href = data.redirect;
        } catch (error) {
            alert(error.message || "An unexpected error occurred.");
            console.error(error);
        }
    });
    

    // Handle Signup Form Submission
    signupForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const fname = document.getElementById("signup-first-name").value;
        const lname = document.getElementById("signup-last-name").value;
        const age = document.getElementById("signup-age").value;
        const gender = document.getElementById("signup-gender").value;
        const email = document.getElementById("signup-email").value;
        const password = document.getElementById("signup-password").value;
        const confirmPassword = document.getElementById("signup-confirm-password").value;

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        try {
            const response = await fetch("/signupuser", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ fname, lname, email, phone: "1234567890", password }),
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.message);

            alert(data.message);
        } catch (error) {
            alert(error.message || "Signup failed.");
        }
    });


    function preloadChatHistory(history) {
        const messagesContainer = document.getElementById("messages");
        if (!messagesContainer) {
            console.warn("Messages container not found. Skipping chat history preload.");
            return;
        }
    
        history.forEach((item) => {
            appendMessage(item.question, "user");
            appendMessage(item.response, "bot");
        });
    }



    // function preloadChatHistory(history) {
    //     history.forEach((item) => {
    //         appendMessage(item.question, "user");
    //         appendMessage(item.response, "bot");
    //     });
    // }

    function appendMessage(text, sender) {
        const messagesContainer = document.getElementById("messages");
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);

        const bubbleDiv = document.createElement("div");
        bubbleDiv.classList.add("bubble");
        bubbleDiv.textContent = text;

        messageDiv.appendChild(bubbleDiv);
        messagesContainer.appendChild(messageDiv);
    }
});
