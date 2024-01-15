# sity-farm-a-new-hope

***В данном файле я постарался структурировать пошагово весь процесс создания веб-интерфейса фермы***

0) Description:
    Веб-интерфейс содержит одну страницу (index.html), на которой по очереди расположены модули взыимодействия с гидропоникой. 
    Написан на Python, фреймворк Flask. 
    Содержит в себе файлы, отвечающие за внешний вид и взаимодействие с интерфейсом, и файлы, отвечающие за считывание и обработку информации с датчиков. 
    Веб-интерфейс запускается с raspberri pi и работает автономно.

    Полезные ссылки, ни раз пригодятся:
        - Распиновка raspberri Pi 3: https://myraspberry.ru/opisanie-raspinovki-gpio-na-raspberry-pi-3.html
        - Консольные команды Linux: https://habr.com/ru/articles/501442/
        - HTML и CSS справочник (обратить внимание на раздел "как сделать"): https://html5css.ru/html/html_elements.php

1) Getting started (raspberri pi):
    • Установка ОС на SD-карту: https://www.youtube.com/watch?v=jf1Rwrdh0aI&t=201s

    • В консоли:
        - Обновление пакетов, вводим:    
        >>>    sudo apt-get update
        >>>    sudo apt-get upgrade

        - Установка pip, Python:
        >>>    sudo apt-get install python3-pip
        
        - Установка Flask, создание виртуального окружения и рабочего репозитория: https://flask.palletsprojects.com/en/latest/installation/
    
    • В главном репозитории:
        - Создаём setup.py, в этом файле будет программная часть веб-интерфейса (будет подтягивать все .html и .py файлы)
        - Создаём папку templates, в ней файл index.html, в этом файле будет код отображаемых элементов
        - Создаём папку static,  в ней файл CSS, в нём редактируется внешний вид отображаемых элементов
        - Создаём файл sensors.py, в нём будет обрабатываться информация с датчиков

    • Настройка автозапуска на raspberry Pi (через /etc/profile): https://microtechnics.ru/avtozapusk-skripta-na-raspberry-pi/?ysclid=lrev3wsklc806619793
    
2) setup.py:
    • Импортруем в проект:
        from flask import Flask, render_template
        import time
        import socket