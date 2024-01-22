import RPi.GPIO as GPIO # Импортируем библиотеку для работы с GPIO
import Adafruit_DHT
import mh_z19
import time # Импортируем библиотеку для работы со временем

# Устанавливаем режим нумерации пинов
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)


# Определяем пин для подключения датчиков
MHZ_PIN = 12
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
DFT_PIN = 3

def DHT():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        return (f"Влажность = {humidity:.1f}   Температура = {temperature:.1f}")
    GPIO.cleanup()

def MHZ():
    co2 = mh_z19.read_from_pwm(gpio=12, range=2000)
    return(co2)

# Define constants and variables
sensorValue = 0
avgValue = 0
b = 0
buf = [0] * 10
temp = 0

# Define a function to read and sort the analog input
def DFT():
  
    global buf, temp, avgValue
    # Read the analog input 10 times and store in a list
    for i in range(10):
        buf[i] = analogRead(DFT_PIN)

    # Sort the list in ascending order
    for i in range(9):
        for j in range(i+1, 10):
      
            if buf[i] > buf[j]:

                temp = buf[i]
                buf[i] = buf[j]
                buf[j] = temp

    # Calculate the average of the middle six values
    avgValue = 0
    for i in range(2, 8):
        avgValue += buf[i]

    # Convert the average value to voltage and pH
    pHVol = avgValue * 5.0 / 1024 / 6
    ph = -5.70 * pHVol + 21.34

    return(ph)

# Import the serial module and initialize the serial port
import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

# Define a function to read from the serial port
def analogRead(pin):
    # Send the pin number to the Arduino
    ser.write(str(pin).encode())
    # Read the value from the Arduino
    value = ser.readline().decode().strip()
    # Convert the value to an integer
    return int(value)


    

# Бесконечный цикл
while True:
    time_start = time.time()
    # Читаем данные с датчика
    co2 = MHZ()
    dht = DHT()
    time_end = time.time()
    time_responce = time_end - time_start
    # Выводим их в консоль
    print("__________________________________________________________________")
    print(co2)
    print()
    print(dht)
    print()
    print(f"Time for responce: {time_responce:.2f}")
    
    time.sleep(2)
