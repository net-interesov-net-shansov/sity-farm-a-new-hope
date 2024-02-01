from flask import Flask, render_template
from flask_socketio import SocketIO,send
import time

datch = {
    "temp":11,
    "high":22,
}

print(datch['high'])

app = Flask(__name__)

socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('socket.html')


@socketio.on('message')
def handle_message(data):
    time.sleep(1)
    print('received message: ' + data)
    mas = datch
    send(mas )

"""
ggdgdgdg
dgdgdgdgg 
"""


if __name__ == '__main__':
    socketio.run(app, debug=True)