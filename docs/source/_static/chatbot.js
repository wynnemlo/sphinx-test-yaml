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

    chatInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            let userInput = chatInput.value.trim();
            if (userInput) {
                chatMessages.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
                chatInput.value = "";
                setTimeout(() => {
                    chatMessages.innerHTML += `<p><strong>Bot:</strong> Hello! I am a simple chatbot.</p>`;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }, 500);
            }
        }
    });
});
