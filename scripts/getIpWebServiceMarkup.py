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
