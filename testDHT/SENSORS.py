import RPi.GPIO as GPIO # Импортируем библиотеку для работы с GPIO
import Adafruit_DHT
import mh_z19
import ADS1x15
import smbus
import time # Импортируем библиотеку для работы со временем
from tabulate import tabulate

# Устанавливаем режим нумерации пинов
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Определяем пин для подключения датчиков
MHZ_PIN = 12
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
# ADS = ADS1x15.ADS1115(1, 0x48)

# ADS.setGain(ADS.PGA_4_096V)

# ADS.setComparatorMode(ADS.COMP_MODE_TRADITIONAL)
# ADS.setComparatorPolarity(ADS.COMP_POL_ACTIV_HIGH)
# ADS.setComparatorLatch(ADS.COMP_LATCH)
# ADS.setComparatorQueue(ADS.COMP_QUE_1_CONV)

# f = ADS.toVoltage()
# ADS.setComparatorThresholdLow(int(1.5 / f))
# ADS.setComparatorThresholdHigh(int(2.5 / f))
# thsL = ADS.getComparatorThresholdLow() * f
# thsH = ADS.getComparatorThresholdHigh() * f

def current_time():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return(current_time)

def DHT_TEMP():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if temperature is not None:
        return (temperature)
    GPIO.cleanup()

def DHT_HUM():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None:
        return (humidity)
    GPIO.cleanup()

def MHZ():
    co2 = mh_z19.read_from_pwm(gpio=12, range=2000)
    return(co2)

def Menu():
    return ("Выберите режим работы фермы \n 1 - AUTO режим \n 2 - Ручной режим \n 3 - Замешивание раствора \n")

    
# def PH():

#     ph = ADS.readADC(0)
    
#     if ph is not None:
#         ADS.requestADC(0)
#         return(ph)
#     else:
#         return("error")

menu = Menu()

back_to_manu = False

while True:

    time_start = time.time()
    # Читаем данные с датчика
    Current_time = current_time()
    co2 = MHZ()
    t = DHT_TEMP()
    hum = DHT_HUM()
    # ph = PH()
    time_end = time.time()
    time_responce = time_end - time_start
    sensors = [f"Текущее время: {Current_time}", f"CO2: {co2}", f"Температура: {t}", f"Влажность: {hum}", f"Время обработки: {time_responce}"]
    
    print(menu)
    command = input()

    if command == "1":
        while True:

            time_start = time.time()
            # Читаем данные с датчиков
            Current_time = current_time()
            co2 = MHZ()
            t = DHT_TEMP()
            hum = DHT_HUM()
            # ph = PH()
            time_end = time.time()
            time_responce = time_end - time_start
            sensors = [[f"Текущее время: {Current_time}", f"CO2: {co2}", f"Температура: {t}"], [f"Влажность: {hum}", f"Время обработки: {time_responce}"]]
            
            print(tabulate(sensors))
            print("-------------------------------------------------------------------------------------")

            if t >= 30:
                print("!!! Критически высокое значение температуры !!!")
                print("-------------------------------------------------------------------------------------")

            elif t <= 20:
                print("!!! Критически низкое значение температуры !!!")
                print("-------------------------------------------------------------------------------------")
            
            else:
                continue

            print("Оптимальные показатели окружающей среды")
            print("Температура: | Влажность: | CO2: ")
            print("-------------------------------------------------------------------------------------")

            command = input("Введите команду (для обновления - update, в меню - menu, остановка - emergancy stop): ")

            if command == "menu":
                break
            
            elif command == "emergancy stop":
                exit(0)

            else:
                continue 
    
    elif command == "2":

        while True:

            time_start = time.time()
            # Читаем данные с датчиков
            Current_time = current_time()
            co2 = MHZ()
            t = DHT_TEMP()
            hum = DHT_HUM()
            # ph = PH()
            time_end = time.time()
            time_responce = time_end - time_start
            sensors = [[f"Текущее время: {Current_time}", f"CO2: {co2}", f"Температура: {t}"], [f"Влажность: {hum}", f"Время обработки: {time_responce}"]]

            print(tabulate(sensors))
            print("-------------------------------------------------------------------------------------")

            if t >= 30:
                print("!!! Критически высокое значение температуры !!!")
                print("-------------------------------------------------------------------------------------")

            elif t <= 20:
                print("!!! Критически низкое значение температуры !!!")
                print("-------------------------------------------------------------------------------------")
            
            else:
                continue

            print("Оптимальные показатели окружающей среды")
            print("Температура: | Влажность: | CO2: ")
            print("-------------------------------------------------------------------------------------")

            command = input("Введите команду (список команд - help): ")

            if command == "menu":
                break

            elif command == "emergancy stop":
                exit(0)

            elif command == "level 1 stop light":

            elif command == "level 2 stop light":

            elif command == "level 3 stop light":
            
            elif command == "level 1 stop water":
            
            elif command == "level 2 stop water":

            elif command == "level 3 stop water":

            elif command == "level 1 set light":

            elif command == "level 2 set light":

            elif command == "level 3 set light":

            elif command == "level 1 set water":

            elif command == "level 2 set water":

            elif command == "level 3 set water":
            
            elif command == "set phase":

            elif command == "help":


            print(tabulate(sensors))
            time.sleep(1)

    elif command == "3":
        
        while True:

            print("Начался процесс смешивания")
            print(tabulate(sensors))

            command = input()
            if command == 'emergency stop':
                GPIO.
                exit(0)
            else:
                continue

    else:
        continue
