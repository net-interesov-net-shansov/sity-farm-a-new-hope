from flask import Flask, jsonify
import socket
import Adafruit_DHT
import RPi.GPIO as GPIO
import threading
import time, serial
import mh_z19

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# ___--- Сменить режим нумерации на GPIO.BOARD, тк это режим не зависит от модели 
# ___--- распберри и более универсален
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = Flask(__name__)

@app.route('/')
def SENSORS():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        return jsonify("Влажность = ", humidity, "Температура = ", temperature)
    GPIO.cleanup()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

if __name__ == '__main__':
    app.run(host=(s.getsockname()[0]), port = 5000, debug=True)