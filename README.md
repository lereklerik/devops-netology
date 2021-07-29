# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## 1. Есть скрипт:
```shell
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```
#####   1.1. Какое значение будет присвоено переменной `c`?
#####   1.2. Как получить для переменной `c` значение 12?
#####   1.3. Как получить для переменной `c` значение 3?

*   Мы не сможем неявно присвоить переменной `c` какое-либо однозначное значение без явного преобразования слагаемых к какому-то типу:
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
```shell
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

*   Проверим изменения в локальном репозитории: [git status](pictures/4.2_py.png)
```shell
На ветке main
Ваша ветка опережает «gitlab/main» на 34 коммита.
  (используйте «git push», чтобы опубликовать ваши локальные коммиты)

Изменения, которые будут включены в коммит:
  (используйте «git reset HEAD <файл>…», чтобы убрать из индекса)

	изменено:      README.md
	удалено:       first.txt
	удалено:       has_been_moved.txt
	скопировано:   README.md -> last_home_exercises/prev4.1ex.md
	удалено:       last_home_exercises/test.txt

Изменения, которые не в индексе для коммита:
  (используйте «git add <файл>…», чтобы добавить файл в индекс)
  (используйте «git checkout -- <файл>…», чтобы отменить изменения
   в рабочем каталоге)

	изменено:      README.md
```

*   Проанализировав скрипт, поняла, что в моем случае придется проверять ещё и кириллицу в статусах, т.к. `git` у меня для ленивых, и все пишет на русском.
*   Также, `git` отслеживает не только модифицируемые файлы, а еще и удаленные, новые или перемещаемые. В целом, мой вариант учел все такие ситуации.
*   Учитывая, что нет смысла выводить данные в таком же виде, что выводит нам `git status`, позволила себе несколько усложнить скрипт, добавив сбор данных по файлам в словарь, который в итоге и вывожу в консоли
*   Скрипт [script_vim](pictures/4.2.2_py.png):
```shell
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
lerekler@PAVILION:~/gitProjects/devops-netology$ (main)/home/lerekler/test.py 
Проверяемая директория:~/gitProjects/devops-netology
------Файлы-------
изменено:
*   next_home_exercises/getChgFiles.py
*   README.md
удалено:
*   first.txt
*   last_home_exercises/test.txt
*   has_been_moved.txt
скопировано:
*   README.md -> last_home_exercises/prev4.1ex.md
новый файл:
*   next_home_exercises/getChgFiles.py
*   pictures/4.2.2_py.png
*   pictures/4.2_py.png
```    
*   Как видно, предыдущий файл README.md с прошлой домашней работы я перекладываю в другую папку и переименовываю
*   Сам скрипт присутствует в проекте [getChgFiles](scripts/getChgFiles.py)

P.S. Python только стала изучать, по стилистике и коду могут быть провалы, т.к. в основном программирую на Java, но стараюсь

## 3. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями

* Учитывая, что репозиторий могут ввести любой, необходимо будет убрать `~` из команды перехода к директории
* Помимо этого требуется проверить, что путь существует и вообще является путем, здесь также воспользуемся модулем `os.path`
* Для передачи пути используем модуль `sys`
* Сбор наименований измененных файлов в словарь вынесем в отдельный метод `get_file_dict()`
* Скрипт [script3](pictures/4.2.3py.png):

```shell
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
lerekler@PAVILION:~/Documents$ ./getChgFilesOtherDirectory /usr/local/bin
fatal: not a git repository (or any of the parent directories): .git
Проверяемая директория:/usr/local/bin
Измененных файлов не найдено
```
* Проверим с неправильным путем:
```shell
lerekler@PAVILION:~/Documents$ ./getChgFilesOtherDirectory .home/lerekler/gitProjects/libgit
Путь не найден
```
* Протестируем с репозиторием, в котором веду этот проект: 
```shell
lerekler@PAVILION:~/Documents$ ./getChgFilesOtherDirectory home/lerekler/gitProjects/devops-netology
Проверяемая директория:/home/lerekler/gitProjects/devops-netology
------Файлы-------
изменено:
*   scripts/getChgFilesOtherDirectory.py
*   scripts/getChgFiles.py
*   README.md
удалено:
*   first.txt
*   last_home_exercises/test.txt
*   has_been_moved.txt
скопировано:
*   README.md -> last_home_exercises/prev4.1ex.md
новый файл:
*   scripts/getChgFilesOtherDirectory.py
*   scripts/getChgFiles.py
*   pictures/4.2_py.png
*   pictures/4.2.2_py.png
```
* Протестируем с тестовым **git**-репозиторием. Сначала просто просмотрим состояние:
```shell
lerekler@PAVILION:~/gitProjects/gitNetology$ (master)git status
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
lerekler@PAVILION:~/Documents$ ./getChgFilesOtherDirectory home/lerekler/gitProjects/gitNetology
Проверяемая директория:/home/lerekler/gitProjects/gitNetology
------Файлы-------
изменено:
*   contributing.md
```

Вроде работает =)

