async function getBotResponse(message) {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer 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"
        },
        body: JSON.stringify({
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: message }]
        })
    });
    const data = await response.json();
    return data.choices[0].message.content;
}

document.addEventListener("DOMContentLoaded", function () {
    let chatbox = document.createElement("div");
    chatbox.innerHTML = `
        <style>
            #chat-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 250px;
                height: 300px;
                background: white;
                border: 1px solid #ccc;
                padding: 10px;
                display: flex;
                flex-direction: column;
                box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                font-family: Arial, sans-serif;
            }
            #chat-messages {
                flex-grow: 1;
                overflow-y: auto;
                max-height: 230px;
            }
            #chat-input {
                border: none;
                padding: 5px;
                width: 100%;
                border-top: 1px solid #ccc;
            }
        </style>
        <div id="chat-container">
            <div id="chat-messages"></div>
            <input id="chat-input" type="text" placeholder="Type a message..." />
        </div>
    `;
    document.body.appendChild(chatbox);

    let chatMessages = document.getElementById("chat-messages");
    let chatInput = document.getElementById("chat-input");

    chatInput.addEventListener("keypress", async function (event) {
        if (event.key === "Enter") {
            let userInput = chatInput.value.trim();
            if (userInput) {
                chatMessages.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
                chatInput.value = "";
                let botResponse = await getBotResponse(userInput);
                chatMessages.innerHTML += `<p><strong>Bot:</strong> ${botResponse}</p>`;
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }
    });
});
