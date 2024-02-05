import RPi.GPIO as GPIO # Импортируем библиотеку для работы с GPIO
import Adafruit_DHT
import mh_z19
import ADS1x15
import smbus
import time # Импортируем библиотеку для работы со временем

# Устанавливаем режим нумерации пинов
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Определяем пин для подключения датчиков
MHZ_PIN = 12
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
ADS = ADS1x15.ADS1115(1, 0x48)

ADS.setGain(ADS.PGA_4_096V)

ADS.setComparatorMode(ADS.COMP_MODE_TRADITIONAL)
ADS.setComparatorPolarity(ADS.COMP_POL_ACTIV_HIGH)
ADS.setComparatorLatch(ADS.COMP_LATCH)
ADS.setComparatorQueue(ADS.COMP_QUE_1_CONV)

f = ADS.toVoltage()
ADS.setComparatorThresholdLow(int(1.5 / f))
ADS.setComparatorThresholdHigh(int(2.5 / f))
thsL = ADS.getComparatorThresholdLow() * f
thsH = ADS.getComparatorThresholdHigh() * f

def DHT():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        return (f"Влажность = {humidity:.1f}   Температура = {temperature:.1f}")
    GPIO.cleanup()

def MHZ():
    co2 = mh_z19.read_from_pwm(gpio=12, range=2000)
    return(co2)

def PH():

    ph = ADS.readADC(0)
    
    if ph is not None:
        ADS.requestADC(0)
        return(ph)
    else:
        return("error")

while True:
    time_start = time.time()
    # Читаем данные с датчика
    co2 = MHZ()
    dht = DHT()
    ph = PH()
    time_end = time.time()
    time_responce = time_end - time_start
    # Выводим их в консоль
    print("__________________________________________________________________")
    print(co2)
    print()
    print(dht)
    print()
    print(ph)
    print()
    print(f"Time for responce: {time_responce:.2f}")
    
    time.sleep(2)
