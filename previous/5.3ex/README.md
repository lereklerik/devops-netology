# Домашнее задание к занятию "5.3. Контейнеризация на примере Docker"

## Задача 1

    Посмотрите на сценарий ниже и ответьте на вопрос: "Подходит ли в этом сценарии использование докера? 
    Или лучше подойдет виртуальная машина, физическая машина? Или возможны разные варианты?"
    
    Детально опишите и обоснуйте свой выбор.
    
    --
    
    Сценарий:
    
    Высоконагруженное монолитное java веб-приложение;
    Go-микросервис для генерации отчетов;
    Nodejs веб-приложение;
    Мобильное приложение c версиями для Android и iOS;
    База данных postgresql используемая, как кэш;
    Шина данных на базе Apache Kafka;
    Очередь для Logstash на базе Redis;
    Elastic stack для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
    Мониторинг-стек на базе prometheus и grafana;
    Mongodb, как основное хранилище данных для java-приложения;
    Jenkins-сервер.

| Сценарий                                        | Что подходит          |   Примечание      |
|:-----------------------------------------------:|:---------------------:|:-----------------:|
|Высоконагруженное монолитное java веб-приложение | Физическая машина     | Вся аппаратная часть будет находиться в нашем распоряжении, что позволит модернизировать сервер при первой необходимости. Более быстрый отклик на запросы, отказоустойчивость и более высокая производительность - всё это необходимо для ресурсозатратных Java-приложений.  |
|Go-микросервис для генерации отчетов             | Докер                 | Нам требуется сервис, который бы: 1. Быстро формировал отчеты 2. Был инкапсулирован от остальных программ и приложений. Это легко можно реализовать в контейнере   |
|Nodejs веб-приложение                            | Докер                 | Веб-приложение вполне может быть контейнеризировано |
|Мобильное приложение c версиями для Android и iOS| Виртуальный сервер    | Учитывая, что оно мобильное, требуется интерфейс, для чего докер не подходит               
|База данных postgresql используемая, как кэш     | Виртуальный сервер/докер | Не могу определиться с выбором, т.к. ориентируюсь также на опыт. Докер используем с БД, т.к. у нас postgresql необходим для работы развернутых приложений в контейнере. Однако, кэш может находиться в виртуальной машине, если к нему требуется доступ из разных систем.|
|Шина данных на базе Apache Kafka                 | Виртуальная машина    | Kafka организовывает поток данных между сервисами, событиями. Собирает логи и агрегирует записи. Я бы предпочла поставить Kafk'y на виртуалку, т.к. агрегация данных, сбор метрик может осуществляться между различными приложениями. Значит Kafka не должна быть закрыта совсем от всех, а доступ к метрикам можно получать извне. |
|Очередь для Logstash на базе Redis               | Физическая машина     | Для очереди обычно требуется высокая производительность, поэтому выберем физический сервер |
|Elastic stack для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana| Виртуальная машина + докер | На примере работы: развернули некоторые приложения для мониторинга и отчетности на виртуальном сервере. Прикрутили вывод логов продуктивного сервера пром.системы по нашим задачам. ELK, logstash, kibana полностью развернуты в докере. Не знаю, насколько это правильно, т.к. мне досталось по наследству, но проблем не возникает |
|Мониторинг-стек на базе prometheus и grafana     | Докер                 | Учитывая, что системы не ресурсозатратные, быстро разворачиваются, выбор докера очевиден |
|Mongodb, как основное хранилище данных для java-приложения               | Виртуальная машина | Использовалось на работе на виртуальной машине. Сейчас не используем. Нам нужно хранение данных, объем их может варьироваться. На физических серверах использование Mongodb было бы неоправданным, может съесть много ресурсов|
| Jenkins-сервер                                  | Докер                 | Очевидное решение зайти на hub.docker.com и скачать контейнер с Jenkins, который потом так просто настроить под свои нужды. Зачем придумывать что-то ещё?)|


## Задача 2

Сценарий выполнения задачи:

    *   создайте свой репозиторий на докерхаб;
    *   выберете любой образ, который содержит апачи веб-сервер;
    *   создайте свой форк образа;
    *   реализуйте функциональность: запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```html
<html>
    <head>Hey, Netology</head>
    <body>
        <h1>I’m kinda DevOps now</h1>
    </body>
</html>
```
    *   Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на докерхаб-репо.

* В качестве такого веб-сервера выбрала [HTTPD](https://hub.docker.com/_/httpd?tab=description&page=1&ordering=last_updated)
* В директории создала `index.html` с заданным кодом, изменив только апостроф в h1 (кодировка не воспринималась), добавив h2 для теста:
```shell
WorkFolder/docker-projects/test-httpd/public-html$ cat index.html
```
```html
<html>
    <head>Hey, Netology</head>
    <body>
        <h1>I'm kinda DevOps now</h1>
    <h2>test using dockerfile</h2>
    </body>
</html>
```            
* Создала Dockerfile:
```shell
WorkFolder/docker-projects/test-httpd$ cat Dockerfile 
FROM httpd:2.4
COPY ./public-html/ /usr/local/apache2/htdocs/
```

* Запустила образ:
```shell
$ docker build -t my-apache2 .
$ docker run -dit --name netology-httpd -p 8080:80 my-apache2
```
* Получили следующее:
```shell
WorkFolder/docker-projects/test-httpd# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
my-apache2          latest              964d8004fbc6        16 minutes ago      138MB
httpd               2.4                 f34528d8e714        29 hours ago        138MB
httpd               latest              f34528d8e714        29 hours ago        138MB
hello-world         latest              d1165f221234        6 months ago        13.3kB
WorkFolder/docker-projects/test-httpd# docker ps
CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS              PORTS                  NAMES
52f48d154c1f        my-apache2          "httpd-foreground"   16 minutes ago      Up 16 minutes       0.0.0.0:8080->80/tcp   netology-httpd
```
* Наш файл в контейнере:
```shell
WorkFolder/docker-projects/test-httpd# docker exec -ti netology-httpd bash
/usr/local/apache2# cd /usr/local/apache2/htdocs/
/usr/local/apache2/htdocs# cat index.html 
<html>
    <head>Hey, Netology</head>
    <body>
        <h1>I'm kinda DevOps now</h1>
	<h2>test using dockerfile</h2>
    </body>
</html>
root@52f48d154c1f:/usr/local/apache2/htdocs# 
```
* Проверим вывод [index.html](../../pictures/01_httpd_indexhtml.png)
* Создала репозиторий на `docker hub` [netology-httpd](https://hub.docker.com/r/lereklerik/netology-httpd)
* Связала тег с образом:
```shell
WorkFolder/docker-projects/test-httpd# docker tag 964d8004fbc6 lereklerik/netology-httpd:latest
WorkFolder/docker-projects/test-httpd# docker images
REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
lereklerik/netology-httpd   latest              964d8004fbc6        20 minutes ago      138MB
my-apache2                  latest              964d8004fbc6        20 minutes ago      138MB
httpd                       2.4                 f34528d8e714        29 hours ago        138MB
httpd                       latest              f34528d8e714        29 hours ago        138MB
hello-world                 latest              d1165f221234        6 months ago        13.3kB
WorkFolder/docker-projects/test-httpd# docker push lereklerik/netology-httpd
The push refers to repository [docker.io/lereklerik/netology-httpd]
ef303f953464: Pushed 
a5762756330a: Mounted from library/httpd 
d76ec8837f01: Mounted from library/httpd 
3453c54913b8: Mounted from library/httpd 
2136d1b3a4af: Mounted from library/httpd 
d000633a5681: Mounted from library/httpd 
latest: digest: sha256:4d54b43060c141b771923a62aebfb648c02cde0a096cc4420c1d0d4e574fd3f0 size: 1573
```
* Ссылка на теги образа: [tags](https://hub.docker.com/r/lereklerik/netology-httpd/tags?page=1&ordering=last_updated)
* или pull: [docker pull lereklerik/netology-httpd:latest](docker pull lereklerik/netology-httpd:latest)

## Задание 3

    -   Запустите первый контейнер из образа centos c любым тэгом в фоновом режиме, 
        подключив папку info из текущей рабочей директории на хостовой машине в /share/info контейнера;
    -   Запустите второй контейнер из образа debian:latest в фоновом режиме, подключив папку info из текущей рабочей директории 
        на хостовой машине в /info контейнера;
    -   Подключитесь к первому контейнеру с помощью exec и создайте текстовый файл 
        любого содержания в /share/info ;
    -   Добавьте еще один файл в папку info на хостовой машине;
    -   Подключитесь во второй контейнер и отобразите листинг и содержание файлов в /info контейнера.

* Предварительно создала папку info в рабочей директории. Комментарии действий за решеточками:
```shell
# проверим состояние образов
root@PAVILION:/home/lerekler/WorkFolder/docker-projects/test-debian# docker images
REPOSITORY                  TAG                 IMAGE ID            CREATED             SIZE
my-apache2                  latest              964d8004fbc6        2 hours ago         138MB
lereklerik/netology-httpd   latest              964d8004fbc6        2 hours ago         138MB
httpd                       2.4                 f34528d8e714        31 hours ago        138MB
httpd                       latest              f34528d8e714        31 hours ago        138MB
hello-world                 latest              d1165f221234        6 months ago        13.3kB
#
# заберем 7-й centos:
#
root@PAVILION:/home/lerekler/WorkFolder/docker-projects# docker pull centos:7
7: Pulling from library/centos
2d473b07cdd5: Pull complete 
Digest: sha256:0f4ec88e21daf75124b8a9e5ca03c37a5e937e0e108a255d890492430789b60e
Status: Downloaded newer image for centos:7
#
# и последнюю версию debian:
#
root@PAVILION:/home/lerekler/WorkFolder/docker-projects# docker pull debian:latest
latest: Pulling from library/debian
955615a668ce: Pull complete 
Digest: sha256:08db48d59c0a91afb802ebafc921be3154e200c452e4d0b19634b426b03e0e25
Status: Downloaded newer image for debian:latest
root@PAVILION:/home/lerekler/WorkFolder/docker-projects# docker run -dit --name netology-centos -v /info:/share/info -d centos
1f9c29c302fa27c99a57795a44849cb127a7b7fcb04decaa35951cbca21e3ff2
root@PAVILION:/home/lerekler/WorkFolder/docker-projects# docker run -dit --name netology-debian -v /info:/info -d debian
ed0d0e4e99a12f9aa8727d3cb19347422c714a0a52fa408bc3312aa4a1682866
root@PAVILION:/home/lerekler/WorkFolder/docker-projects# docker ps
CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS              PORTS                  NAMES
ed0d0e4e99a1        debian              "bash"               3 seconds ago       Up 3 seconds                               netology-debian
1f9c29c302fa        centos              "/bin/bash"          17 seconds ago      Up 16 seconds                              netology-centos
52f48d154c1f        my-apache2          "httpd-foreground"   3 hours ago         Up 3 hours          0.0.0.0:8080->80/tcp   netology-httpd
#
# запустим первый образ с centos:
#
root@PAVILION:/home/lerekler/WorkFolder/docker-projects# docker run -dit --name netology-centos -v /home/lerekler/WorkFolder/docker-projects/info:/share/info -d centos
57e04b45cdc806fdb6956b4f8b3be778445d2a6380ef7186ce133a68314efa29
#
# запустим второй образ с debian:
#
root@PAVILION:/home/lerekler/WorkFolder/docker-projects/info# docker run -dit --name netology-debian -v /home/lerekler/WorkFolder/docker-projects/info:/info -d debian
2c584295e85e57b95ecaac368f0e08f22abde9f698cb34bcb507a1e91ba8aeb8
#
# зайдем в первый контейнер и создадим файл
#
root@PAVILION:/home/lerekler/WorkFolder/docker-projects# docker exec -ti netology-centos bash
[root@57e04b45cdc8 /]# cd share/info/
[root@57e04b45cdc8 info]# ls -l
total 0
[root@57e04b45cdc8 info]# touch testcentos
[root@57e04b45cdc8 info]# ls
testcentos
[root@57e04b45cdc8 info]# 
```
* Создала файл `hosttest.file` в папке /info на своем хосте, при этом, в ней уже отображается файл, созданный в первом контейнере:
```shell
lerekler@PAVILION:~/WorkFolder/docker-projects/info$ ls -l
итого 4
-rw-rw-r-- 1 lerekler lerekler 15 сен  4 17:58 hosttest.file
-rw-r--r-- 1 root     root      0 сен  4 18:07 testcentos
#
# зайдем во второй контейнер и проверим файлы
#
root@PAVILION:/home/lerekler/WorkFolder/docker-projects# docker exec -ti netology-centos bash
root@2c584295e85e:/# cd info/
root@2c584295e85e:/info# ls -l
total 4
-rw-rw-r-- 1 1000 1000 15 Sep  4 14:58 hosttest.file
-rw-r--r-- 1 root root  0 Sep  4 15:07 testcentos
```