
##SMLS

Стегоанализ изображений с помощью CatboostClassfier и SPAM feature selection.

###Запуск: 

1) pip3 install -r requirements.txt

2) sudo service rabbitmq-server start

3) python3 -m workers.consumer

4) python3 -m workers.server


###Использование:

1) переход на localhost:8080

2) загрузить .png файл (есть в папке examples)

3) произойдет перенаправление на страницу с результатом
