from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import socket
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import mh_z19
import random

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
MHZ_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

error = "Server Error"

@socketio.on('get_temperature')
def send_temperature():
    while True:
        time.sleep(1)
        temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        DhtTemperature = {'DhtTemperature': temp}
        if DhtTemperature is not None:
            emit('temperature_data', DhtTemperature)
        else:
            DhtTemperature = error
            emit('temperature_data', DhtTemperature)
        
        GPIO.cleanup()

@socketio.on('get_humidity')
def send_humidity():
    while True:
        time.sleep(1)
        hum = mh_z19.read_from_pwm(gpio=12, range=2000)
        DhtHumidity = {'DhtHumidity': hum}
        if DhtHumidity is not None:
            emit('humidity_data', DhtHumidity)
        else:
            DhtHumidity = error
            emit('humidity_data', DhtHumidity)
    
        GPIO.cleanup()
        
@socketio.on('get_time')
def get_current_time():
    while True:
        time.sleep(1)
        current_time = {'current_time': time.strftime('%H:%M:%S')}
        if current_time is not None:
            emit('time_data', current_time)
        else:
            current_time = error
            emit('time_data', current_time, broadcast=True)

chan_list = [5, 6, 13, 16, 19, 20, 21, 26]
GPIO.setup(chan_list, GPIO.OUT)
GPIO.output(chan_list, GPIO.HIGH)

@socketio.on('emergancy_stop')
def emergancy_stop():
    GPIO.output(chan_list, GPIO.LOW)
    GPIO.cleanup()
    print("!!! Гидропоника и сервер экстренно остановлены !!!")
    exit(0)

@socketio.on('button1_click')
def switch_chanel_1():
    while True:
        if GPIO.output(chan_list[0]) == GPIO.LOW:
            GPIO.output(chan_list[0], GPIO.HIGH)
        else:
            GPIO.output(chan_list[0], GPIO.LOW)

@socketio.on('button2_click')
def switch_chanel_2():
    while True:
        if GPIO.output(chan_list[1]) == GPIO.LOW:
            GPIO.output(chan_list[1], GPIO.HIGH)
        else:
            GPIO.output(chan_list[1], GPIO.LOW)

@socketio.on('button3_click')
def switch_chanel_3():
    while True:
        if GPIO.output(chan_list[2]) == GPIO.LOW:
            GPIO.output(chan_list[2], GPIO.HIGH)
        else:
            GPIO.output(chan_list[2], GPIO.LOW)

@socketio.on('button4_click')
def switch_chanel_4():
    while True:
        if GPIO.output(chan_list[3]) == GPIO.LOW:
            GPIO.output(chan_list[3], GPIO.HIGH)
        else:
            GPIO.output(chan_list[3], GPIO.LOW)

@socketio.on('button5_click')
def switch_chanel_5():
    while True:
        if GPIO.output(chan_list[4]) == GPIO.LOW:
            GPIO.output(chan_list[4], GPIO.HIGH)
        else:
            GPIO.output(chan_list[4], GPIO.LOW)

@socketio.on('button6_click')
def switch_chanel_6():
    while True:
        if GPIO.output(chan_list[5]) == GPIO.LOW:
            GPIO.output(chan_list[5], GPIO.HIGH)
        else:
            GPIO.output(chan_list[5], GPIO.LOW)

@socketio.on('button7_click')
def switch_chanel_7():
    while True:
        if GPIO.output(chan_list[6]) == GPIO.LOW:
            GPIO.output(chan_list[6], GPIO.HIGH)
        else:
            GPIO.output(chan_list[6], GPIO.LOW)

@socketio.on('button8_click')
def switch_chanel_8():
    while True:
        if GPIO.output(chan_list[7]) == GPIO.LOW:
            GPIO.output(chan_list[7], GPIO.HIGH)
        else:
            GPIO.output(chan_list[7], GPIO.LOW)

@app.route('/', methods=['GET'])
def home():
    return render_template('DHT.html')

@app.route('/manual_operation.html')
def manual_operation():
    return render_template('manual_operation.html')

@app.route('/DHT.html')
def auto_operation():
    return render_template('DHT.html')

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

if __name__ == '__main__':
    socketio.run(app, host=(local_ip), port = 5000, debug=True)