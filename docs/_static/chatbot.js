const responses = {
    "hello": "Hi there! How can I assist you?",
    "help": "I can answer common questions about our documentation. Try asking about installation or configuration.",
    "installation": "To install the package, run `pip install your-package-name`.",
    "configuration": "Configuration settings can be modified in the `conf.py` file of your Sphinx setup.",
    "default": "I'm not sure how to respond to that. Try asking something else!"
};

function sendMessage() {
    const input = document.getElementById('chatbot-input').value.toLowerCase();
    const response = responses[input] || responses["default"];
    displayMessage("You: " + input);
    displayMessage("Bot: " + response);
    document.getElementById('chatbot-input').value = '';
}

function displayMessage(message) {
    const chatBody = document.getElementById('chatbot-body');
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    chatBody.appendChild(messageElement);
    chatBody.scrollTop = chatBody.scrollHeight;
}
