from flask import Flask, jsonify
import socket
import Adafruit_DHT
import RPi.GPIO as GPIO
import threading

app = Flask(__name__)



sensor = Adafruit_DHT.DHT22     # указываем тип датчика
pin = 5     # указываем пин на реле, к которому подсоединён датчик
relay = 29      # указываем пин на распберри, соответствующий пину на реле

hum = None
temp = None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay, GPIO.HIGH)


def DHT22():
	global hum,  temp
	while True:
		hum,  temp = Adafruit_DHT.read_retry(sensor, pin)
		print("h = ", hum, "t = ", temp)
		


@app.route("/DHT")
def get_DHT22():
    if hum is not None and temp is not None:
        hum_string, temp_string = (hum, temp)
        return jsonify(humidity = hum_string, temperature = temp_string)
    
    GPIO.output(relay, GPIO.LOW)
    GPIO.cleanup()
    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))

	
thread = threading.Thread(target=DHT22)
thread.start()
	
if __name__ == '__main__':
	app.run(host=(s.getsockname()[0]), port=5000, debug=True)
