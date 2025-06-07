document.addEventListener("DOMContentLoaded", function () {
    // Form toggling and loader logic (only if forms exist)
    const signupForm = document.getElementById("signup-form");
    const registerForm = document.getElementById("register-form");
    const loginForm = document.getElementById("login-form");
    const formTitle = document.getElementById("form-title");

    if (signupForm && registerForm && loginForm) {
        const toggleToLoginLinks = document.querySelectorAll(".toggle-to-login");
        const toggleToSignupLink = document.getElementById("toggle-to-signup");
        const toggleToRegisterLink = document.getElementById("toggle-to-register");

        // Toggle to login
        toggleToLoginLinks.forEach(link => {
            link.addEventListener("click", function (e) {
                e.preventDefault();
                loginForm.style.display = "block";
                signupForm.style.display = "none";
                registerForm.style.display = "none";
                if (formTitle) formTitle.innerText = "Login";
            });
        });

        // Toggle to signup
        if (toggleToSignupLink) {
            toggleToSignupLink.addEventListener("click", function (e) {
                e.preventDefault();
                signupForm.style.display = "block";
                loginForm.style.display = "none";
                registerForm.style.display = "none";
                if (formTitle) formTitle.innerText = "Sign Up";
            });
        }

        // Toggle to register
        if (toggleToRegisterLink) {
            toggleToRegisterLink.addEventListener("click", function (e) {
                e.preventDefault();
                registerForm.style.display = "block";
                signupForm.style.display = "none";
                loginForm.style.display = "none";
                if (formTitle) formTitle.innerText = "Register Chama";
            });
        }

        // Show spark loader on form submit for signup, register, login
        ["signup-form", "register-form", "login-form"].forEach(function(formId) {
            const form = document.getElementById(formId);
            if (form) {
                form.addEventListener("submit", function(e) {
                    showSparkLoader();
                });
            }
        });

        // Show login form by default if ?show=login is in the URL
        if (window.location.search.includes("show=login")) {
            loginForm.style.display = "block";
            signupForm.style.display = "none";
            registerForm.style.display = "none";
            if (formTitle) formTitle.innerText = "Login";
        }
    }

    // Splash logic (only if splash exists)
    const splash = document.getElementById('splash-screen');
    if (splash && (window.location.pathname === "/" || window.location.pathname === "/home")) {
        showSplashScreen();
    }
});
window.showSplashScreen = function() {
    const splash = document.getElementById('splash-screen');
    if (!splash) return;
    splash.style.display = 'flex';
    setTimeout(() => {
        splash.classList.add('fade-out');
        setTimeout(() => {
            splash.style.display = 'none';
            splash.classList.remove('fade-out');
        }, 800);
    }, 1800); // Duration of splash in ms
};
window.showSparkLoader = function() {
    const loader = document.getElementById('spark-loader');
    loader.style.display = 'flex';
    // Clear previous canvas
    document.getElementById('spark-canvas').innerHTML = '';
    // Destroy previous tsParticles instances
    if (window.tsParticles && tsParticles.dom().length > 0) {
        tsParticles.dom().forEach(instance => instance.destroy());
    }
    tsParticles.load("spark-canvas", {
        fullScreen: { enable: false },
        particles: {
            number: { value: 30 },
            color: { value: ["#ff69b4", "#ffd700", "#fff"] },
            shape: { type: "circle" },
            opacity: { value: 0.8 },
            size: { value: { min: 2, max: 5 } },
            move: { enable: true, speed: 2, direction: "none", outModes: "bounce" }
        },
        interactivity: { detectsOn: "canvas", events: {} },
        background: { color: "transparent" }
    });
};
window.hideSparkLoader = function() {
    document.getElementById('spark-loader').style.display = 'none';
    tsParticles.dom().forEach(instance => instance.destroy());
};


