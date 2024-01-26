from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO
import socket
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import mh_z19

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('DHT.html')

@socketio.on('get_temperature')
def DHT():  
    
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    temp_error = "error"
    if temperature is not None:
        socketio.emit('send_temperature', temperature)
    else:
        socketio.emit('temp_error', temp_error)
        
    GPIO.cleanup()

@socketio.on('get_humidity')
def DHT():  
    
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    temp_error = "error"
    if humidity is not None:
        socketio.emit('send_humidity', humidity)
    else:
        socketio.emit('temp_error', temp_error)
        
    GPIO.cleanup()

@app.route('/time')
def get_current_time():
    return {'time': time.strftime('%H:%M:%S')}

@app.route('/manual_operation')
def manual_operation():
    return render_template('manual_operation.html')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

if __name__ == '__main__':
    socketio.run(app, host=(s.getsockname()[0]), port = 5000, debug=True)