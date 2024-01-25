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

@app.route('/', methods = ["GET", "POST"])
def SENSORS():
    session.clear()
    GPIO.cleanup()
    
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        return render_template('DHT.html', humidity, temperature)
    else:
        return render_template('DHT.html', error="Sensor does not return valid response")
    

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

if __name__ == '__main__':
    socketio.run(app, host=(s.getsockname()[0]), port = 5000, debug=True)