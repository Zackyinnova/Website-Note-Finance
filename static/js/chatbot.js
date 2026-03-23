function sendMessage() {
    let input = document.getElementById("userInput").value;

    if (!input.trim()) return;

    fetch("/chatbot-api", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input })
    })
    .then(res => res.json())
    .then(data => {
        let chatbox = document.getElementById("chatbox");

        chatbox.innerHTML += `<p><b>Anda:</b> ${input}</p>`;
        chatbox.innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;

        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(err => console.error(err));

    document.getElementById("userInput").value = "";
}

// Enter key support
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("userInput").addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});