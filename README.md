
## SMLS

Стегоанализ изображений с помощью CatboostClassfier и SPAM feature selection.

### Запуск: 

1) pip3 install -r requirements.txt

2) sudo service rabbitmq-server start

3) python3 -m workers.consumer

4) python3 -m workers.server


### Использование:

1) переход на localhost:8080

2) загрузить .png файл (есть в папке examples)

3) произойдет перенаправление на страницу с результатом


### Самостоятельное обучение модели

1) wget https://www.dropbox.com/s/jha7kf0lrwde31u/train.zip

2) распаковать архив в папку mlbuild

3) python3 -m mlbuild.build

4) результат - файл mlbuild/catboost.obj
