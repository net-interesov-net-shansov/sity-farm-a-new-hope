from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import socket
# import Adafruit_DHT
# import RPi.GPIO as GPIO
import time
# import mh_z19
import random

# DHT_SENSOR = Adafruit_DHT.DHT22
#DHT_PIN = 4

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


#hum, temp = random.randint(0,10), random.randint(11,20) #Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
temp = random.randint(0, 10)
error = "Senser Error"

sensors = {
    'temperature': temp
}

@socketio.on('get_temperature')
def send_temperature():

    time.sleep(1)
    data = {'data': sensors['temperature']}
    emit('temperature_data', data)
        
    # GPIO.cleanup()

@socketio.on('get_humidity')
def send_humidity(sensors, error):

    time.sleep(1)
    if sensors['humidity'] is not None:
        send(sensors['humidity'])
    else:
        send(error)
        
    #GPIO.cleanup()

@app.route('/')
def home():
    return render_template('DHT.html')

@app.route('/time')
def get_current_time():
    return {'time': time.strftime('%H:%M:%S')}

@app.route('/manual_operation.html')
def manual_operation():
    return render_template('manual_operation.html')

@app.route('/DHT.html')
def auto_operation():
    return render_template('DHT.html')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

if __name__ == '__main__':
    socketio.run(app, host=(s.getsockname()[0]), port = 5000, debug=True)