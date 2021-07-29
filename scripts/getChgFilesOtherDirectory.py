#!/usr/bin/env  python3

import os
import sys

dir_path = sys.argv[1]


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
