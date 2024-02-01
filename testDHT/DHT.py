from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, send
import socket
# import Adafruit_DHT
# import RPi.GPIO as GPIO
import time
# import mh_z19
import random

# DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

app = Flask(__name__)
socketio = SocketIO(app)

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


#hum, temp = random.randint(0,10), random.randint(11,20) #Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
hum, temp = 0,1
error = "Senser Error"

sensors = {
    'temperature': 10,
    'humidity': str(hum)
}

@socketio.on('get_temperature')
def send_temperature(sensors):

    time.sleep(1)
    data = sensors
    print(data)
    send(data)
        
    # GPIO.cleanup()

@socketio.on('get_humidity')
def send_humidity(sensors, error):

    time.sleep(1)
    if sensors['humidity'] is not None:
        send(sensors['humidity'])
    else:
        send(error)
        
    #GPIO.cleanup()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

if __name__ == '__main__':
    socketio.run(app, host=(s.getsockname()[0]), port = 5000, debug=True)