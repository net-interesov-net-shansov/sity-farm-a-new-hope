import RPi.GPIO as GPIO # Импортируем библиотеку для работы с GPIO
import Adafruit_DHT
import mh_z19
import time # Импортируем библиотеку для работы со временем

# Устанавливаем режим нумерации пинов
GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)


# Определяем пин для подключения датчиков
MHZ_PIN = 12
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

GPIO.setup(MHZ_PIN, GPIO.IN)

def DHT():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        return (f"Влажность = {humidity:.1f}   Температура = {temperature:.1f}")
    GPIO.cleanup()

def MHZ():
    co2 = mh_z19.read_from_pwm(gpio=12, range=2000)
    return(co2)
    

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
