#!/usr/bin/env python3

import socket
import os
import sys
import fileinput

file_name = 'dictionary_service'


def search_word_in_file(source_file, dns_check, ip_check):
    result = -1
    if not os.path.isfile(source_file):
        return result
    else:
        f = open(source_file, "r")
        for i in f:
            k, v = i.strip().split(':')
            if dns_check == k and v != ip_check:
                print(f'[ERROR]<{k}> IP mismatch: <{v}><{ip_check}>')
                result = 2
                break
            elif dns_check == k and v == ip_check:
                result = 1
                break
            else:
                result = 0
    f.close()
    return result


def write_webservices(key, value, mod):
    global file_name
    target_file = open(file_name, mod)
    target_file.write(f"{key}:{value}\n")
    print(f'<{check_dns_service}> - <{current_ip}>')
    target_file.close()


def get_ip_of_dns(check_dns):
    tmp_ip = ""
    try:
        tmp_ip = socket.gethostbyname(socket.getfqdn(check_dns))
    except socket.gaierror:
        pass
        print("Проверьте корректность имени сервиса:", sys.exc_info()[0])
    return tmp_ip


check_dns_service = input("Введите имя сервиса: ")
current_ip = get_ip_of_dns(check_dns_service)

if current_ip:
    result_check = search_word_in_file(file_name, check_dns_service, current_ip)
    if result_check < 0:
        write_webservices(check_dns_service, current_ip, 'w+')
    elif result_check == 0:
        write_webservices(check_dns_service, current_ip, 'a+')
    elif result_check == 2:
        with fileinput.FileInput(file_name, inplace=True, backup='.bak') as file:
            for line in file:
                web_address, ip = line.strip().split(':')
                check_iter = (check_dns_service == web_address and current_ip != ip)
                print(f'{web_address}:{current_ip}' if check_iter else f'{web_address}:{ip}')
        os.unlink(file_name + '.bak')
    else:
        print(f'<{check_dns_service}> - <{current_ip}>')
