from flask import Flask, request, jsonify
import random
import webbrowser
import threading

# Initialize Flask app
app = Flask(__name__)

# Chatbot response logic
def get_chatbot_response(user_input):
    responses = {
        "hi": "Hello! How can I help you?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "what is your name": "I'm ChatBot, your friendly assistant!",
        "bye": "Goodbye! Have a great day!",
    }
    user_input = user_input.lower()
    return responses.get(user_input, "I'm sorry, I didn't understand that. Can you rephrase?")

# Routes
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ChatBot</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background: linear-gradient(135deg, #89f7fe, #66a6ff);
                color: #333;
            }
            .chat-container {
                width: 100%;
                max-width: 500px;
                background: #ffffff;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            .messages {
                height: 350px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 15px;
                background-color: #f9f9f9;
            }
            .message {
                margin: 10px 0;
                padding: 12px 16px;
                border-radius: 10px;
                font-size: 15px;
                max-width: 75%;
            }
            .user {
                text-align: right;
                background-color: #4caf50;
                color: #fff;
                margin-left: auto;
            }
            .bot {
                background-color: #eeeeee;
                color: #000;
                margin-right: auto;
            }
            input[type="text"] {
                width: calc(100% - 120px);
                padding: 12px;
                margin-right: 10px;
                border: 1px solid #ccc;
                border-radius: 10px;
                font-size: 15px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            button {
                padding: 12px;
                background: #4caf50;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 15px;
                cursor: pointer;
                transition: background 0.3s, transform 0.2s;
            }
            button:hover {
                background: #45a049;
                transform: scale(1.05);
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="messages" id="messages"></div>
            <div>
                <input type="text" id="user-input" placeholder="Type your message here...">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            function appendMessage(message, sender) {
                const messagesDiv = document.getElementById('messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                messageDiv.textContent = message;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }

            function sendMessage() {
                const userInput = document.getElementById('user-input');
                const message = userInput.value;
                if (message.trim() === "") return;

                appendMessage(message, 'user');
                userInput.value = "";

                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message }),
                })
                    .then(response => response.json())
                    .then(data => {
                        appendMessage(data.response, 'bot');
                    })
                    .catch(error => {
                        appendMessage("Sorry, something went wrong.", 'bot');
                    });
            }
        </script>
    </body>
    </html>
    """

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    response = get_chatbot_response(user_input)
    return jsonify({"response": response})

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
