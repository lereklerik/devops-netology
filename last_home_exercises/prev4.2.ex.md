# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## 1. Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```
#####   1.1. Какое значение будет присвоено переменной `c`?
#####   1.2. Как получить для переменной `c` значение 12?
#####   1.3. Как получить для переменной `c` значение 3?

*   Мы не сможем неявно присвоить переменной `c` какое-либо однозначное значение без преобразования слагаемых к какому-то типу:
```shell
>>> a = 1
>>> b = '2'
>>> c = a + b
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```
*   Если мы преобразуем переменную `a` к строке, то в переменную `c` запишется результат конкатенации строк '1' и '2' (`a` и `b` соответственно), что в конечном итоге запишет в `c`значение **12**: 
```shell
>>> c = str(a) + b
>>> c
12
```
*  Если мы преобразуем переменную `b` к типу `int`, то в переменную `c` запишется результат сложения чисел `1 + 2`: 
```shell
>>> c = a + int(b)
>>> c
3
```

## 2. Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений: 
```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```
## Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

*   Проверим изменения в локальном репозитории: [git status](../pictures/4.2_py.png)
```shell
На ветке main
Ваша ветка опережает «gitlab/main» на 34 коммита.
  (используйте «git push», чтобы опубликовать ваши локальные коммиты)

Изменения, которые будут включены в коммит:
  (используйте «git reset HEAD <файл>…», чтобы убрать из индекса)

	изменено:      prev4.2.ex.md
	удалено:       first.txt
	удалено:       has_been_moved.txt
	скопировано:   prev4.2.ex.md -> last_home_exercises/prev4.1ex.md
	удалено:       last_home_exercises/test.txt

Изменения, которые не в индексе для коммита:
  (используйте «git add <файл>…», чтобы добавить файл в индекс)
  (используйте «git checkout -- <файл>…», чтобы отменить изменения
   в рабочем каталоге)

	изменено:      prev4.2.ex.md
```

*   Проанализировав скрипт, поняла, что в моем случае придется проверять ещё и кириллицу в статусах, т.к. `git` у меня для ленивых, и все пишет на русском.
*   Также, `git` отслеживает не только модифицируемые файлы, а еще и удаленные, новые или перемещаемые. В целом, мой вариант учел все такие ситуации.
*   Учитывая, что нет смысла выводить данные в таком же виде, что выводит нам `git status`, позволила себе несколько усложнить скрипт, добавив сбор данных по файлам в словарь, который в итоге и вывожу в консоли
*   Скрипт [script_vim](../pictures/4.2.2_py.png):
```python
#!/usr/bin/env  python3

import os

bash_command = ["cd ~/gitProjects/devops-netology", "git status"]
path_of_gitDir = bash_command[0][3:]
result_os = os.popen(' && '.join(bash_command)).read()
print("Проверяемая директория:" + path_of_gitDir)
if result_os:
    print("------Файлы-------")
    file_dict = {}
    for result in result_os.split('\n'):
        result = result.strip('\t')
        if (result.startswith("изменено:") or result.startswith("modified:")) \
            or (result.startswith("новый файл:") or result.startswith("new file:")) \
                or (result.startswith("удалено:") or result.startswith("deleted:")) \
                or (result.startswith("скопировано:") or result.startswith("renamed:")):
            key, value = list(result.split(":"))
            value = str(value).lstrip(' ')
            tmp_set = set()
            tmp_set.add(value)
            if file_dict.get(key) is None:
                file_dict.setdefault(key, tmp_set)
            else:
                prev_set = set(file_dict.get(key))
                tmp_set.update(prev_set)
                file_dict[key] = tmp_set

    for k, v in file_dict.items():
        print(f'{k}:')
        for elem in v:
            print(f'*   {elem}')
else:
    print("Измененных файлов не найдено")
```
*   Выдали права на чтение, запустили файл:
```shell
ler@PAVILION:~/gitProjects/devops-netology$ (main)/home/lerekler/test.py 
Проверяемая директория:~/gitProjects/devops-netology
------Файлы-------
изменено:
*   next_home_exercises/getChgFiles.py
*   prev4.2.ex.md
удалено:
*   first.txt
*   last_home_exercises/test.txt
*   has_been_moved.txt
скопировано:
*   prev4.2.ex.md -> last_home_exercises/prev4.1ex.md
новый файл:
*   next_home_exercises/getChgFiles.py
*   pictures/4.2.2_py.png
*   pictures/4.2_py.png
```    
*   Как видно, предыдущий файл README.md с прошлой домашней работы я перекладываю в другую папку и переименовываю
*   Сам скрипт присутствует в проекте [getChgFiles](../scripts/getChgFiles.py)

P.S. Python только стала изучать, по стилистике и коду могут быть провалы, т.к. в основном программирую на Java, но стараюсь

## 3. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями

* Учитывая, что репозиторий могут ввести любой, необходимо будет убрать `~` из команды перехода к директории
* Помимо этого требуется проверить, что путь существует и вообще является путем, здесь также воспользуемся модулем `os.path`
* Для передачи пути используем модуль `sys`
* Сбор наименований измененных файлов в словарь вынесем в отдельный метод `get_file_dict()`
* Скрипт [getChgFilesOtherDirectory](../scripts/getChgFilesOtherDirectory.py):

```python
#!/usr/bin/env  python3

import os
import sys

dir_path = sys.argv[1]

### метод сбора файлов
def get_file_dict():
    global file_dict
    file_dict = {}
    for result in result_os.split('\n'):
        result = result.strip('\t')
        if (result.startswith("изменено:") or result.startswith("modified:")) \
                or (result.startswith("новый файл:") or result.startswith("new file:")) \
                or (result.startswith("удалено:") or result.startswith("deleted:")) \
                or (result.startswith("скопировано:") or result.startswith("renamed:")):
            key, value = list(result.split(":"))
            value = str(value).lstrip(' ')
            tmp_set = set()
            tmp_set.add(value)
            if file_dict.get(key) is None:
                file_dict.setdefault(key, tmp_set)
            else:
                prev_set = set(file_dict.get(key))
                tmp_set.update(prev_set)
                file_dict[key] = tmp_set
    return file_dict
### проверка введенного значения пути
if not dir_path.startswith("/"):
    dir_path = "/" + dir_path

if os.path.exists(dir_path):
    bash_command = [f"cd {dir_path}", "git status"]
    path_of_gitDir = bash_command[0][3:]
    result_os = os.popen(' && '.join(bash_command)).read()
    print("Проверяемая директория:" + path_of_gitDir)
    if result_os:
        file_dict = dict(get_file_dict())
        if not file_dict:
            print("Измененных файлов не найдено")
        else:
            print("------Файлы-------")
            for k, v in file_dict.items():
                print(f'{k}:')
                for elem in v:
                    print(f'*   {elem}')
    else:
        print("Измененных файлов не найдено")
else:
    print("Путь не найден")
```
* Проверим работу скрипта. Запустим из `/home/user/Documents` с параметром - путь до папки, в которой отсутствует **git**-репозиторий:
```shell
ler@PAVILION:~/Documents$ ./getChgFilesOtherDirectory /usr/local/bin
fatal: not a git repository (or any of the parent directories): .git
Проверяемая директория:/usr/local/bin
Измененных файлов не найдено
```
* Проверим с неправильным путем:
```shell
ler@PAVILION:~/Documents$ ./getChgFilesOtherDirectory .home/lerekler/gitProjects/libgit
Путь не найден
```
* Протестируем с репозиторием, в котором веду этот проект: 
```shell
ler@PAVILION:~/Documents$ ./getChgFilesOtherDirectory home/lerekler/gitProjects/devops-netology
Проверяемая директория:/home/lerekler/gitProjects/devops-netology
------Файлы-------
изменено:
*   scripts/getChgFilesOtherDirectory.py
*   scripts/getChgFiles.py
*   prev4.2.ex.md
удалено:
*   first.txt
*   last_home_exercises/test.txt
*   has_been_moved.txt
скопировано:
*   prev4.2.ex.md -> last_home_exercises/prev4.1ex.md
новый файл:
*   scripts/getChgFilesOtherDirectory.py
*   scripts/getChgFiles.py
*   pictures/4.2_py.png
*   pictures/4.2.2_py.png
```
* Протестируем с тестовым **git**-репозиторием. Сначала просто просмотрим состояние:
```shell
ler@PAVILION:~/gitProjects/gitNetology$ (master)git status
На ветке master
Изменения, которые будут включены в коммит:
  (используйте «git reset HEAD <файл>…», чтобы убрать из индекса)

	изменено:      contributing.md

Изменения, которые не в индексе для коммита:
  (используйте «git add <файл>…», чтобы добавить файл в индекс)
  (используйте «git checkout -- <файл>…», чтобы отменить изменения
   в рабочем каталоге)

	изменено:      contributing.md
```
* Теперь запустим скрипт:
```shell
ler@PAVILION:~/Documents$ ./getChgFilesOtherDirectory home/lerekler/gitProjects/gitNetology
Проверяемая директория:/home/lerekler/gitProjects/gitNetology
------Файлы-------
изменено:
*   contributing.md
```

Вроде работает =)

## 4. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.

* Думать пришлось много, работа с файлами не самая тривиальная оказалась... 
* Первое, что необходимо было учесть: данные по сервису будут перезаписаны, значит как-то надо грамотно описать перезапись словаря в файле. Это было самым сложным, т.к. стандартные реализации нагугленные предлагали заменять строку с `replace` или самостоятельно создавать новый файл, в который нужно перезаписывать содержимое текущего с заменой нужной строки
* Второе, что я поняла, что если писать все самостоятельно, без использования сторонних библиотек, то выглядит громоздко и непонятно. 
* Третье - если хост не будет найден, вылетит **exception**, а его надо обработать.
* Четвертое - вынесла некоторые реализации в отдельные функции. К примеру, это было необходимо при открытии файла на чтение, т.к. при манипуляции с файлом неоднократное открытие файла с разными модификаторами приводит не к тем результатам, которых от них ожидаешь
* В итоге получился такой скрипт ([getIpWebService](../scripts/getIpWebService.py)):
```python
#!/usr/bin/env python3

import socket
import os
import sys
import fileinput

file_name = 'dictionary_service'      # вынесла переменную с наименованием файла выше, в функции она будет использована как глобальная


def search_word_in_file(source_file, dns_check, ip_check):      # метод, который возвращает определенную цифру в результате, в зависимости от того, что он найдет в файле. 
    result = -1                                                 # как раз в этом методе мы открываем файл только на чтение, если он создан, и просто анализируем наличие данных в нем                                    
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


def write_webservices(key, value, mod):   # вынесла реализацию записи/добавления строчки в файл в отдельный метод, чтобы не повторять её в условиях основного блока программы 
    global file_name
    target_file = open(file_name, mod)
    target_file.write(f"{key}:{value}\n")
    print(f'<{check_dns_service}> - <{current_ip}>')
    target_file.close()


def get_ip_of_dns(check_dns):           # обработка метода получения ip-адреса сервиса
    tmp_ip = ""
    try:
        tmp_ip = socket.gethostbyname(socket.getfqdn(check_dns))
    except socket.gaierror:
        pass
        print("Проверьте корректность имени сервиса:", sys.exc_info()[0])
    return tmp_ip


check_dns_service = input("Введите имя сервиса: ")    # в целом, можно было бы использовать sys.argv[1], но хотелось попробовать и другой вариант ввода
current_ip = get_ip_of_dns(check_dns_service)         # получаем IP-адрес сервиса

if current_ip:
    result_check = search_word_in_file(file_name, check_dns_service, current_ip)    # получаем результат анализа чтения файла
    if result_check < 0:                                                            # файл не создан, создаем его и добавляем нужные данные
        write_webservices(check_dns_service, current_ip, 'w+')
    elif result_check == 0:                                                         # файл создан, но выбранный сервис не найден, добавляем нужные данные
        write_webservices(check_dns_service, current_ip, 'a+')
    elif result_check == 2:                                                         # файл создан, но по выбранному сервису записан другой IP-адрес
        with fileinput.FileInput(file_name, inplace=True, backup='.bak') as file:   # воспользуемся модулем fileinput, создадим backup нашего файла, в который перезапишем несовпадающий ip выбранного сервиса
            for line in file:
                web_address, ip = line.strip().split(':')
                check_iter = (check_dns_service == web_address and current_ip != ip)
                print(f'{web_address}:{current_ip}' if check_iter else f'{web_address}:{ip}')
        os.unlink(file_name + '.bak')
    else:
        print(f'<{check_dns_service}> - <{current_ip}>')                            # при условии, что сервис найден в файле и ip не менялся, лишний раз файл на чтение не открываю, вывожу найденные значения выше 
```

* Посмотрим в действии. Скрипт положила в отдельную папку, которая пока не содержит в себе нужный нам файл [screen_ls](../pictures/4.2.4_2py.png):
```shell
ler@PAVILION:~/WorkFolder/scripts$ ls -l
итого 52
-rw-rw-r-- 1 lerekler lerekler   56 июл 17 20:36 '~'
-rw-rw-r-- 1 lerekler lerekler  120 июл 15 23:30  check.log
-rw-rw-r-- 1 lerekler lerekler 9273 июл 15 22:22  curl.log
-rw-rw-r-- 1 lerekler lerekler   79 июл 16 23:07  error.log
-rwxrw-r-- 1 lerekler lerekler  109 июл 15 22:21  ex4.1_01.sh
-rwxrw-r-- 1 lerekler lerekler  392 июл 16 22:45  ex4.1_02.sh
-rwxrw-r-- 1 lerekler lerekler  683 июл 16 22:40  ex4.1_03.sh
-rw-rw-r-- 1 lerekler lerekler 4815 июл 16 22:55  file.log
-rwxrwxr-x 1 lerekler lerekler 2109 авг  1 12:26  getIpWebService.py
-rw-rw-r-- 1 lerekler lerekler   76 июл 18 11:49  test
```
* Запустим скрипт:
```shell
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: www.google.com
<www.google.com> - <74.125.131.103>
```
* Проверим наличие файла и его содержимое:
```shell
ler@PAVILION:~/WorkFolder/scripts$ ls -l
итого 56
...
**-rwxrwxr-x 1 lerekler lerekler 2109 авг  1 12:26  getIpWebService.py**
...
ler@PAVILION:~/WorkFolder/scripts$ cat dictionary_service 
www.google.com:74.125.131.103
```
* Все появилось и записалось. Найдем несколько других сервисов и дополним наш файл. Также проверим работу при неправильно введенном имени сервиса:
```shell
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: driva.google.com
Проверьте корректность имени сервиса: <class 'socket.gaierror'>
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: drive.google.com
<drive.google.com> - <173.194.222.194>
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: mail.google.com
<mail.google.com> - <66.102.12.19>
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: bikepower.ddns.net
<bikepower.ddns.net> - <46.138.247.252>
```
* Я проверяла каждую итерацию, но выложу полный вариант:
```shell
ler@PAVILION:~/WorkFolder/scripts$ cat dictionary_service 
www.google.com:74.125.131.103
drive.google.com:173.194.222.194
mail.google.com:66.102.12.19
bikepower.ddns.net:46.138.247.252
```
* Теперь проверим перезапись адреса:
```shell
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: mail.google.com
[ERROR]<mail.google.com> IP mismatch: <66.102.12.19><173.194.222.17>
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: drive.google.com
<drive.google.com> - <173.194.222.194>
```
* Содержимое файла:
```shell
ler@PAVILION:~/WorkFolder/scripts$ cat dictionary_service 
www.google.com:74.125.131.103
drive.google.com:173.194.222.194
mail.google.com:173.194.222.17
bikepower.ddns.net:46.138.247.252
```

* И еще пару раз:
```shell
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: www.google.com
<www.google.com> - <74.125.131.103>
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: www.chebyrashka.ru
<www.chebyrashka.ru> - <194.58.112.166>
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: www.google.com
<www.google.com> - <74.125.131.103>
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: drive.google.com
[ERROR]<drive.google.com> IP mismatch: <173.194.222.194><173.194.221.194>
ler@PAVILION:~/WorkFolder/scripts$ ./getIpWebService.py 
Введите имя сервиса: www.google.com
[ERROR]<www.google.com> IP mismatch: <74.125.131.103><74.125.131.106>
```
* Наш файл:
```shell
ler@PAVILION:~/WorkFolder/scripts$ cat dictionary_service 
www.google.com:74.125.131.106
drive.google.com:173.194.221.194
mail.google.com:173.194.222.17
bikepower.ddns.net:46.138.247.252
www.chebyrashka.ru:194.58.112.166
```
