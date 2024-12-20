document.addEventListener("DOMContentLoaded", () => {
    const loginRadio = document.getElementById("login-radio");
    const signupRadio = document.getElementById("signup-radio");
    const authTitle = document.getElementById("auth-title");
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const login = document.getElementById("loginButton")

    // Toggle between Login and Signup forms
    loginRadio.addEventListener("change", () => {
        if (loginRadio.checked) {
            authTitle.textContent = "Login to Your Existing Account";
            loginForm.classList.remove("hidden");
            signupForm.classList.add("hidden");
        }
    });

    signupRadio.addEventListener("change", () => {
        if (signupRadio.checked) {
            authTitle.textContent = "Create an Account";
            signupForm.classList.remove("hidden");
            loginForm.classList.add("hidden");
        }
    });



   login.addEventListener("click", () => {
        window.location.replace("http://127.0.0.1:8000/home");
        localStorage.setItem("premiumUser",true);
        localStorage.setItem("premiumremaining",true);
   });

    // // Handle Login OTP Request
    // document.getElementById("get-otp").addEventListener("click", () => {
    //     const email = document.getElementById("login-email").value;
    //     if (email) {
    //         alert(`OTP sent to ${email} (placeholder).`);
    //         // Add backend logic to send OTP.
    //     } else {
    //         alert("Please enter your email.");
    //     }
    // });

    // // Handle Signup OTP Request
    // document.getElementById("get-signup-otp").addEventListener("click", () => {
    //     const email = document.getElementById("signup-email").value;
    //     if (email) {
    //         alert(`Signup OTP sent to ${email} (placeholder).`);
    //         // Add backend logic to send OTP.
    //     } else {
    //         alert("Please enter your email.");
    //     }
    // });
});
