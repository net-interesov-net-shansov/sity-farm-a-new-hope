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
hum = random.randint(10,20)
error = "Server Error"

sensors = {
    'temperature': temp,
    'humidity': hum
}

@socketio.on('get_temperature')
def send_temperature():
    
    while not stop_processing_data:
        while True:
            time.sleep(1)
            DhtTemperature = {'DhtTemperature': sensors['temperature']}
            if DhtTemperature is not None:
                emit('temperature_data', DhtTemperature)
            else:
                DhtTemperature = error
                emit('temperature_data', DhtTemperature)
        
    # GPIO.cleanup()

@socketio.on('get_humidity')
def send_humidity():

    while not stop_processing_data:
        while True:
            time.sleep(1)
            DhtHumidity = {'DhtHumidity': sensors['humidity']}
            if DhtHumidity is not None:
                emit('humidity_data', DhtHumidity)
            else:
                DhtHumidity = error
                emit('humidity_data', DhtHumidity)
        
    #GPIO.cleanup()
        
@socketio.on('get_time')
def get_current_time():

    while not stop_processing_data:
        while True:
            time.sleep(1)
            current_time = {'current_time': time.strftime('%H:%M:%S')}
            if current_time is not None:
                emit('time_data', current_time)
            else:
                current_time = error
                emit('time_data', current_time, broadcast=True)

@socketio.on('emergency-stop')
def stop_processing():
    global stop_processing_data
    stop_processing_data = True

@app.route('/')
def home():
    return render_template('DHT.html')

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