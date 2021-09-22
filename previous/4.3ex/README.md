# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

## 1. Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```json
{ "info" : "Sample JSON output from our service\t",
    "elements" :[
        { "name" : "1-2exercises",
        "type" : "server",
        "ip" : 7175 
        },
        { "name" : "second",
        "type" : "proxy",
        "ip : 71.78.22.43
        }
    ]
}
```
# Нужно найти и исправить все ошибки, которые допускает наш сервис

* Добавила недостающие кавычки в паре ключ-значения ip-address второго элемента массива:
```json
{ "info" : "Sample JSON output from our service\t",
    "elements" :[
        { "name" : "1-2exercises",
        "type" : "server",
        "ip" : 7175
        },
        { "name" : "second",
        "type" : "proxy",
        "ip" : "71.78.22.43"
        }
    ]
}
```
Хотя ip-адрес первого сервера меня тоже смущает)

## 2. В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.


* По замечаниям из предыдущей домашней работы убрала использование `global`, а также использовала работу с файлом с конструкцией `with`. 
* Скорее всего, код выглядит большим. Может нагроможденным, но мне хотелось унифицировать его, чтобы не было перечисленных сервисов, а пользователь вводил нужный для проверки.
* Первое, с чем столкнулась - разная обработка данных по `json` и `yaml`. С получением данных по ключу возникли основные сложности, с чем провозилась довольно долго.
* Также выделила отдельный файл с перечислением сервисов, которые были введены пользователем. По его содержимому и пробегаюсь в поисках повторно введенного сервиса.

#### Скрипт:
Сам скрипт: [service_markup_script](../../scripts/getIpWebServiceMarkup.py)
```python
#!/usr/bin/env python3

import socket
import os
import sys
import fileinput
import json
import yaml

# Задаем название файлам
file_name = 'dictionary_service'                        
# Определяем сервис для поиска ip
check_dns_service = input('Введите имя сервиса: ')


# Ищем ip
def get_ip_of_dns(check_dns):
    tmp_ip = ''
    try:
        tmp_ip = socket.gethostbyname(socket.getfqdn(check_dns))
    except socket.gaierror:
        pass
        print('Проверьте корректность имени сервиса:', sys.exc_info()[0])
    return tmp_ip


# Если ip найден, записываем его в переменную
current_ip = get_ip_of_dns(check_dns_service)


# Проверяем наличие файлов и сервисов с ip.
# Если сервис не найден, то добавим его в список services_list
# Если сервис найден, но ip не совпадает, то в дальнейшем необходимо вызвать 
# метод rewrite_webservices с обновленными значениями 
def check_service():
    check = 0
    if not os.path.isfile('services_list'):
        with open('services_list', 'a+') as services_file:
            services_file.write(check_dns_service)
        return check
    f = open('services_list', 'r+')
    for line in f:
        current_line = line.strip('\n')
        if current_line == check_dns_service:
            check = 1
            break
    if check == 0:
        f.write('\n' + check_dns_service)
    f.close()
    return check


# Метод, который записывает/добавляет данные в файлы
def write_webservices(src_filename, key, value, mod):
    with open(src_filename + '.json', mod) as file_json:
        json_data = json.dumps({key: value})
        file_json.write(json_data + '\n')
    with open(src_filename + '.yaml', mod) as file_yaml:
        yaml_data = yaml.dump([{key: value}])
        file_yaml.write(yaml_data + '\n')
    with open(src_filename, mod) as target_file:
        target_file.write(f'{key}:{value}\n')


# Метод, в котором происходит перезапись данных по сервисам, если ip не совпадает после последней проверки 
def rewrite_webservices(key, value):
    matches = False
    old_ip = ''
    with fileinput.FileInput(file_name, inplace=True, backup='.bak') as file:
        for line in file:
            web_address, ip = line.strip().split(':')
            check_iter = (key == web_address and value != ip)
            if check_iter:
                matches = True
                old_ip = ip
            print(f'{web_address}:{value}' if check_iter else f'{web_address}:{ip}')
    os.unlink(file_name + '.bak')
    if matches:
        print(f'[ERROR]<{key}> IP mismatch: <{old_ip}><{value}>')
    rewrite_json(key, value)    # отдельно выделила методы по перезаписи в json и yaml
    rewrite_yaml(key, value)


# перезапись в yaml 
# хотела сделать с fileinput, но не получилось, перешла на with и ручное создание нового файла
def rewrite_yaml(key, value):
    bak_yaml_name = file_name + '.yaml.bak'
    os.rename(file_name + '.yaml', bak_yaml_name)
    with open(bak_yaml_name, 'r') as file_yaml:
        data_loaded = yaml.safe_load(file_yaml)
        for tmp_dict in data_loaded:
            for y_key, y_value in tmp_dict.items():
                yaml_data = yaml.dump([{y_key: y_value}])
                if y_key == key and y_value != value:
                    yaml_data = yaml.dump([{y_key: value}])
                with open(file_name + '.yaml', 'a+', encoding='utf-8') as new_file_yaml:
                    new_file_yaml.write(yaml_data)
    os.remove(bak_yaml_name)


# перезапись в json с fileinput
def rewrite_json(key, value):
    with fileinput.FileInput(file_name + '.json', inplace=True, backup='.bak') as file_json:
        for line in file_json:
            prs_json = json.loads(line)
            for j_key, j_value in prs_json.items():
                json_data = json.dumps({j_key: j_value})
                if j_key == key and j_value != value:
                    json_data = json.dumps({j_key: value})
                print(json_data)
    os.unlink(file_name + '.json' + '.bak')


# здесь вызываются все необходимые методы по результатам проверки списка с сервисами
if current_ip:
    exists_service = check_service()
    if exists_service == 0:
        write_webservices(file_name, check_dns_service, current_ip, 'a+')
    else:
        rewrite_webservices(check_dns_service, current_ip)
    print(f'<{check_dns_service}> - <{current_ip}>')
```

#### Проверяем работу:

* Перед первым запуском папка пустая:
```shell
$ ls -l
итого 4
-rwxrwxr-x 1 lerekler lerekler 3528 авг 11 19:16 getIpWebServiceMarkup.py
$ 
```
* Запускаем скрипт:
```shell
$ ./getIpWebServiceMarkup.py 
Введите имя сервиса: www.google.com
<www.google.com> - <64.233.164.103>
```
* Наш каталог обновился:
```shell
$ ls -l
итого 20
-rw-rw-r-- 1 lerekler lerekler   30 авг 11 20:06 dictionary_service
-rw-rw-r-- 1 lerekler lerekler   37 авг 11 20:06 dictionary_service.json
-rw-rw-r-- 1 lerekler lerekler   36 авг 11 20:06 dictionary_service.yaml
-rwxrwxr-x 1 lerekler lerekler 3528 авг 11 19:16 getIpWebServiceMarkup.py
-rw-rw-r-- 1 lerekler lerekler   14 авг 11 20:06 services_list
```
* Посмотрим содержимое файлов:
```shell
$ echo 'simple === >'; cat dictionary_service ; echo 'json === >'; cat dictionary_service.json ; echo 'yaml === >'; cat dictionary_service.yaml 
simple === >
www.google.com:64.233.164.103
json === >
{"www.google.com": "64.233.164.103"}
yaml === >
- {www.google.com: 64.233.164.103}
```
* Добавим еще несколько сервисов:
```shell
$ ./getIpWebServiceMarkup.py 
Введите имя сервиса: drive.google.com
<drive.google.com> - <173.194.221.194>
$ ./getIpWebServiceMarkup.py 
Введите имя сервиса: mail.google.com
<mail.google.com> - <66.102.12.17>
$ ./getIpWebServiceMarkup.py 
Введите имя сервиса: www.yandex.ru
<www.yandex.ru> - <77.88.55.80>
$ ./getIpWebServiceMarkup.py 
Введите имя сервиса: www.mail.ru
<www.mail.ru> - <94.100.180.70>
```
* Проверим:
```shell
$ echo 'simple === >'; cat dictionary_service ; echo 'json === >'; cat dictionary_service.json ; echo 'yaml === >'; cat dictionary_service.yaml 
simple === >
www.google.com:64.233.164.103
drive.google.com:173.194.221.194
mail.google.com:66.102.12.17
www.yandex.ru:77.88.55.80
www.mail.ru:94.100.180.70
json === >
{"www.google.com": "64.233.164.103"}
{"drive.google.com": "173.194.221.194"}
{"mail.google.com": "66.102.12.17"}
{"www.yandex.ru": "77.88.55.80"}
{"www.mail.ru": "94.100.180.70"}
yaml === >
- {www.google.com: 64.233.164.103}

- {drive.google.com: 173.194.221.194}

- {mail.google.com: 66.102.12.17}

- {www.yandex.ru: 77.88.55.80}

- {www.mail.ru: 94.100.180.70}
```
* Теперь проверим некоторые сервисы повторно:
```shell
$ ./getIpWebServiceMarkup.py 
Введите имя сервиса: www.google.com
[ERROR]<www.google.com> IP mismatch: <64.233.164.103><74.125.131.105>
<www.google.com> - <74.125.131.105>
$ ./getIpWebServiceMarkup.py 
Введите имя сервиса: www.yandex.ru
<www.yandex.ru> - <77.88.55.80>
$ ./getIpWebServiceMarkup.py 
Введите имя сервиса: drive.google.com
<drive.google.com> - <173.194.221.194>
$ ./getIpWebServiceMarkup.py 
Введите имя сервиса: mail.google.com
[ERROR]<mail.google.com> IP mismatch: <66.102.12.17><173.194.222.17>
<mail.google.com> - <173.194.222.17>
$ ./getIpWebServiceMarkup.py 
Введите имя сервиса: www.mail.ru
<www.mail.ru> - <94.100.180.70>
```
* Содержимое файлов поменялось у тех сервисов, где `ip` не совпадает:
```shell
$ echo 'simple === >'; cat dictionary_service ; echo 'json === >'; cat dictionary_service.json ; echo 'yaml === >'; cat dictionary_service.yaml 
simple === >
www.google.com:74.125.131.105 # here
drive.google.com:173.194.221.194
mail.google.com:173.194.222.17 # here
www.yandex.ru:77.88.55.80
www.mail.ru:94.100.180.70
json === >
{"www.google.com": "74.125.131.105"} # here
{"drive.google.com": "173.194.221.194"}
{"mail.google.com": "173.194.222.17"} # here
{"www.yandex.ru": "77.88.55.80"}
{"www.mail.ru": "94.100.180.70"}
yaml === >
- {www.google.com: 74.125.131.105} # here
- {drive.google.com: 173.194.221.194}
- {mail.google.com: 173.194.222.17} # here
- {www.yandex.ru: 77.88.55.80}
- {www.mail.ru: 94.100.180.70}
```

* Ну а так выглядит список сервисов:
```shell
$ cat services_list 
www.google.com
drive.google.com
mail.google.com
www.yandex.ru
www.mail.ru
```

P.S. конечно, нужно бы добавить цикл, который прерывал работу скрипта по волшебному слову + конструкции `try-except`, но боюсь, что и так нагромоздила