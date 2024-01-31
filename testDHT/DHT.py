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

@socketio.on('get_temperature')
def temperature(data):  
    time.sleep(1)

    humidity, temperature = 0, 1 #Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    temp_error = "error"
    if temperature is not None:
        data = temperature
        send('send_temperature', data)
    else:
        data = temp_error
        send('temp_error', data)
        
    # GPIO.cleanup()

@socketio.on('get_humidity')
def humidity():  
    
    humidity, temperature = 1, 0 #Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    temp_error = "error"
    if humidity is not None:
        socketio.emit('send_humidity', humidity)
    else:
        socketio.emit('temp_error', temp_error)
        
    #GPIO.cleanup()

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