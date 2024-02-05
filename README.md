# sity-farm-a-new-hope

***В данном файле я постарался структурировать пошагово весь процесс создания веб-интерфейса фермы***

## 0. Описание:
Серверная часть написан на Python, фреймворк Flask.\
Веб-интерфейс запускается с raspberri pi и работает автономно.\
*Полезные ссылки*, ни раз пригодятся:\
        [Распиновка raspberri Pi 3](https://pinout.xyz/)\
        [Консольные команды Linux](https://habr.com/ru/articles/501442/)\
        [HTML и CSS справочник](https://html5css.ru/html/html_elements.php) (обратить внимание на раздел ["как сделать](https://html5css.ru/howto/default.php)")
## 1. Начало работы (raspberri pi):

* [Установка ОС на SD-карту](https://www.youtube.com/watch?v=jf1Rwrdh0aI&t=201s)
* В консоли raspberry:
<ul type='circle'>
<li>Обновление пакетов, вводим: </li>
    
```
sudo apt-get update
sudo apt-get upgrade
```
<li>Установка pip, Python: </li>

```
sudo apt-get install python3-pip
```
</ul>
  
  
* [Установка Flask, создание виртуального окружения и рабочего репозитория](https://flask.palletsprojects.com/en/latest/installation/)
  * В главном репозитории:\
        - Создаём setup.py, в этом файле будет программная/серверная часть веб-интерфейса\
        - Создаём папку templates, в ней файлы index.html, base.html, manual_operation.html\
  * [Настройка автозапуска на raspberry Pi](https://microtechnics.ru/avtozapusk-skripta-na-raspberry-pi/?ysclid=lrev3wsklc806619793) (через /etc/profile)
    
## 2. Серверная часть:
* Мы работаем со следующими датчиками, подключение которых осуществляется через 8ми канальное реле для raspberri Pi:
  - [DHT-22](https://github.com/freedom27/MyPyDHT?ysclid=lrg5djj711316512711)
  - [Mhz-19](https://www.winsen-sensor.com/d/files/PDF/Infrared%20Gas%20Sensor/NDIR%20CO2%20SENSOR/MH-Z19%20CO2%20Ver1.0.pdf) (реализую считывание через PMW порт)
  - 

* Установка пакетов, вводим:

```
sudo pip3 install Adafruit_DHT
sudo pip3 install mh_z19 (так же устанавливает библиотеку pyserial)
```

* setup.py:

```python
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import socket
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import mh_z19

# Объявляем модель датчика DHT и пин, к которому он подсоеденён
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

# Объявляем пин, к которому подсоеденён датчик MHZ
MHZ_PIN = 12

# Установка режима распиновки
GPIO.setmode(GPIO.BCM)
# Отключение вывода ошибок библиотеки RPi.GPIO, чтобы сервер не прекращад работу и выводил ошибки в интерфейс
GPIO.setwarnings(False)

# Инициализация и настройка приложения Flask и socketI/O
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Эти строки кода определяют два обработчика событий Socket.IO в приложении Flask - подключение/отключение клиента
@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# При возникновении ошибки будем выводить "Server Error" в интерфейс
error = "Server Error"

# Считываем с DHT температуру и отправляем клиенту 
@socketio.on('get_temperature')
def send_temperature():
    # Строка отвечает за взаимодействие с кнопкой экстренной остановки
    while not stop_processing_data:
        while True:

            time.sleep(1)
            # Считываем информацию с датчика DHT_SENSOR и пина DHT_PIN
            temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
            # Присваиваем отправляемой переменной id='DhtTemperature' и значение temp
            DhtTemperature = {'DhtTemperature': temp}

            if DhtTemperature is not None:
                # emit отправляет переменную с присвоенным id клиенту по сокету
                emit('temperature_data', DhtTemperature)

            else:
                # emit отправляет ошибку клиенту по сокету, если датчик не отвечает
                DhtTemperature = error
                emit('temperature_data', DhtTemperature)

            # Строка GPIO.cleanup() используется для сброса состояния всех пинов ввода/вывода общего назначения (GPIO) на Raspberry Pi
            GPIO.cleanup()

# С влажностью поступаем по аналогии с температурой
@socketio.on('get_humidity')
def send_humidity():

    while not stop_processing_data:
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

# Функция отвечает за отправку реального времени клиенту
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

# обпаботчик кнопки "Экстренной остановки"
@socketio.on('emergency-stop')
def stop_processing():
    global stop_processing_data
    stop_processing_data = True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/manual_operation.html')
def manual_operation():
    return render_template('manual_operation.html')

@app.route('/index.html')
def auto_operation():
    return render_template('index.html')

# В переменную 's' записывается ip адрес уст-ва в локальной сети, с которго запускается сервер (в нашем случае - raspberry pi)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))

# Запускаем приложение Flask с поддержкой Socket.IO
if __name__ == '__main__':
    socketio.run(app, host=(s.getsockname()[0]), port = 5000, debug=True)
```
