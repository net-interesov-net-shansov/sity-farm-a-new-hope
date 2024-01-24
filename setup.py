from flask import Flask, render_template, jsonify
import socket
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/time')
def get_current_time():
    return {'time': time.strftime('%H:%M:%S')}

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))

if __name__ == '__main__':
    app.run(host=(s.getsockname()[0]), port=5000, debug=True)
