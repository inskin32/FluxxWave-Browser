"""
Fluxx AI - Official complete module for FluxxWave Browser
Ready to be run via Python IDLE and published on GitHub.

Description: Standalone interface that connects directly to the official
             OpenAI (ChatGPT) APIs using the gpt-4o-mini model.
             Does not require JavaScript, CSS, or manual terminal commands.
"""

import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from openai import OpenAI

# ==========================================
# OPENAI API KEY CONFIGURATION
# ==========================================
# Insert your secret OpenAI API key between the quotes below.
OPENAI_KEY = "YOUR_OPENAI_API_KEY_HERE"

# ==========================================
# INITIAL HTML INTERFACE (Native Browser Style)
# ==========================================
HTML_INTERFACE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fluxx AI - Chat</title>
</head>
<body>

    <h1>⚡ Fluxx AI</h1>
    <p>Official assistant integrated into FluxxWave Browser (Powered by ChatGPT)</p>
    <hr>

    <!-- The native HTML form sends the text directly to Python -->
    <form action="/ask-fluxx" method="POST">
        <label for="question">What would you like to ask Fluxx AI?</label><br><br>
        <input type="text" id="question" name="user_text" placeholder="Ask a question..." required size="50">
        <button type="submit">Send to Fluxx AI</button>
    </form>

</body>
</html>"""

# ==========================================
# PYTHON LOGIC ENGINE (INTERNAL SERVER MANAGEMENT)
# ==========================================
class FluxxAIHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        return  # Hides technical logs in the IDLE console to avoid clutter

    # 1. Displays the initial chat screen upon opening
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_INTERFACE.encode('utf-8'))

    # 2. Receives the question, queries ChatGPT, and returns the response
    def do_POST(self):
        if self.path == "/ask-fluxx":
            # Extracts and decodes the data sent by the HTML form
            data_length = int(self.headers['Content-Length'])
            received_data = self.rfile.read(data_length).decode('utf-8')
            parameters = parse_qs(received_data)
            
            # Reads the string entered by the user in the input box
            user_text = parameters.get('user_text', [''])[0]
            ai_text = ""

            try:
                # Security check before sending the request to the internet
                if "YOUR_OPENAI" in OPENAI_KEY or OPENAI_KEY == "":
                    ai_text = "Error: You have not entered your OpenAI API key inside the Python code. Please edit the file to continue."
                else:
                    # Queries the official OpenAI servers using their official library
                    client = OpenAI(api_key=OPENAI_KEY)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini", # Fixed high-performance and cost-effective model
                        messages=[
                            {
                                "role": "system", 
                                "content": "You are Fluxx AI, the official assistant integrated into the FluxxWave Browser. Always answer directly, helpfully, and straight to the point."
                            },
                            {"role": "user", "content": user_text}
                        ]
                    )
                    ai_text = response.choices.message.content

            except Exception as e:
                ai_text = f"Error communicating with ChatGPT servers: {str(e)}"

            # 3. Generates and returns the results page with cascading chat
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html_response = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Fluxx AI - Response</title>
            </head>
            <body>
                <h1>⚡ Fluxx AI</h1>
                <p><b>Your question:</b> {user_text}</p>
                <p><b>Fluxx AI Response:</b></p>
                <blockquote style="background: #eef2f3; padding: 15px; border-left: 5px solid #00adb5;">
                    {ai_text}
                </blockquote>
                <hr>
                
                <!-- Integrated native form below to continue chatting indefinitely -->
                <form action="/ask-fluxx" method="POST">
                    <input type="text" name="user_text" placeholder="Ask another question..." required size="50">
                    <button type="submit">Send</button>
                </form>
                <br>
                <p><a href="/">← Clear conversation and return to home screen</a></p>
            </body>
            </html>"""
            
            self.wfile.write(html_response.encode('utf-8'))

# ==========================================
# AUTOMATIC START UP (NO MANUAL TERMINAL)
# ==========================================
if __name__ == "__main__":
    local_port = 8080
    server_address = '127.0.0.1'
    
    # Creates the private local server on port 8080
    fluxx_server = HTTPServer((server_address, local_port), FluxxAIHandler)
    
    # Automatically opens the Fluxx AI interface inside the browser
    webbrowser.open(f"http://{server_address}:{local_port}")
    
    # Keeps the application listening to receive questions
    fluxx_server.serve_forever()
