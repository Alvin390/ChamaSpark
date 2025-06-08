document.addEventListener("DOMContentLoaded", function() {
    const fab = document.getElementById("sparkgal-fab");
    const modal = document.getElementById("sparkgal-modal");
    const closeBtn = document.querySelector(".sparkgal-close");
    const chatBody = document.getElementById("sparkgal-chat-body");
    const chatForm = document.getElementById("sparkgal-chat-form");
    const input = document.getElementById("sparkgal-input");
    const typing = document.getElementById("sparkgal-typing");
    let conversationId = null;

    function formatTime() {
        const now = new Date();
        return now.getHours().toString().padStart(2, '0') + ":" +
               now.getMinutes().toString().padStart(2, '0');
    }

    function appendMessage(text, who) {
        const row = document.createElement("div");
        row.className = "sparkgal-message-row " + who;

        const icon = document.createElement("img");
        icon.className = "sparkgal-message-icon";
        if (who === "user") {
            icon.src = "/static/images/sender_placeholder.png";
            icon.alt = "You";
        } else {
            icon.src = "/static/images/SparkGal_Icon.png";
            icon.alt = "Spark Gal";
        }

        const bubble = document.createElement("div");
        bubble.className = "sparkgal-bubble";
        bubble.innerText = text;

        const timestamp = document.createElement("div");
        timestamp.className = "sparkgal-timestamp";
        timestamp.innerText = formatTime();

        if (who === "user") {
            row.appendChild(icon);
            row.appendChild(bubble);
            row.appendChild(timestamp);
        } else {
            row.appendChild(icon);
            row.appendChild(bubble);
            row.appendChild(timestamp);
        }
        chatBody.appendChild(row);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    function appendFeedback() {
        const feedbackDiv = document.createElement("div");
        feedbackDiv.className = "sparkgal-feedback";
        feedbackDiv.innerHTML = `
            <button title="Helpful" class="sparkgal-thumb" data-fb="up">&#128077;</button>
            <button title="Not Helpful" class="sparkgal-thumb" data-fb="down">&#128078;</button>
        `;
        chatBody.appendChild(feedbackDiv);
        chatBody.scrollTop = chatBody.scrollHeight;
        feedbackDiv.querySelectorAll("button").forEach(btn => {
            btn.onclick = function() {
                sendFeedback(btn.getAttribute("data-fb"));
                feedbackDiv.innerHTML = "<span style='color:#888;'>Thanks for your feedback!</span>";
            }
        });
    }

    function sendFeedback(feedback) {
        if (!conversationId) return;
        fetch("/sparkgal/chat/", {
            method: "POST",
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            body: new URLSearchParams({
                feedback: feedback,
                conversation_id: conversationId
            })
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Blur on hover, remove on modal open
    fab.onmouseenter = () => {
        document.body.classList.add("sparkgal-blur");
    };
    fab.onmouseleave = () => {
        document.body.classList.remove("sparkgal-blur");
    };
    fab.onclick = () => {
        modal.classList.add("active");
        document.body.classList.remove("sparkgal-blur"); // Remove blur when modal opens
        setTimeout(() => input.focus(), 300);
    };
    closeBtn.onclick = () => {
        modal.classList.remove("active");
    };

    chatForm.onsubmit = function(e) {
        e.preventDefault();
        const msg = input.value.trim();
        if (!msg) return;
        appendMessage(msg, "user");
        input.value = "";
        typing.style.display = "flex";
        chatBody.scrollTop = chatBody.scrollHeight;
        fetch("/sparkgal/chat/", {
            method: "POST",
            headers: {"X-CSRFToken": getCookie("csrftoken")},
            body: new URLSearchParams({
                message: msg,
                conversation_id: conversationId || ""
            })
        })
        .then(res => res.json())
        .then(data => {
            typing.style.display = "none";
            appendMessage(data.response, "ai");
            appendFeedback();
            conversationId = data.conversation_id;
        })
        .catch(() => {
            typing.style.display = "none";
            appendMessage("Sorry, Spark Gal is unavailable right now.", "ai");
        });
    };
});