# Домашнее задание к занятию "3.3. Операционные системы, лекция 1"
## 1. Какой системный вызов делает команда cd? 

*   `strace -o trace.log /bin/bash -c cd /vagrant`, записали вывод в лог; `cd` использует системный вызов `chdir`:
    *   `chdir("/root")`
    
## 2. Используя strace выясните, где находится база данных file на основании которой она делает свои догадки.

*   `sudo strace -o trace3.log file /dev/sda`
*   `cat trace3/log` и из считанного находим:

    `openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
    fstat(3, {st_mode=S_IFREG|0644, st_size=5699248, ...}) = 0
    mmap(NULL, 5699248, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7fc7a2c78000
    close(3)                                = 0
    stat("/root/.magic.mgc", 0x7ffe6980abe0) = -1 ENOENT (No such file or directory)
    stat("/root/.magic", 0x7ffe6980abe0)    = -1 ENOENT (No such file or directory)
    openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
    stat("/etc/magic", {st_mode=S_IFREG|0644, st_size=111, ...}) = 0
    openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
    fstat(3, {st_mode=S_IFREG|0644, st_size=111, ...}) = 0
    read(3, "# Magic local data for file(1) c"..., 4096) = 111
    read(3, "", 4096)                       = 0
    close(3)                                = 0
    openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
    fstat(3, {st_mode=S_IFREG|0644, st_size=5811536, ...}) = 0
    mmap(NULL, 5811536, PROT_READ|PROT_WRITE, MAP_PRIVATE, 3, 0) = 0x7fc7a26ed000
    close(3)     
    `
    
*   По выведенному результату можно видеть, что команда ищет данные из нескольких источников, но в конечном итоге `file` обратился к `/usr/share/misc/magic.mgc` за поиском формата файла

## 3. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе)

*   Просмотрим удаленные файлы `lsof | grep deleted` (делаю в своей ОС, в vagrant пусто). Из большого списка выбрала следующие:

`skypeforl  1678  1714            myuser  txt       REG              259,6 133765488    2374705 /usr/share/skypeforlinux/skypeforlinux (deleted)
skypeforl  1678  1714            myuser    3r      REG              259,6  10528096    2374637 /usr/share/skypeforlinux/icudtl.dat (deleted)
skypeforl  1678  1714            myuser    4r      REG              259,6    172330    2374709 /usr/share/skypeforlinux/v8_context_snapshot.bin (deleted)
`

*   Вторая колонка в выводе результата говорит нам о расположении файлового дескриптора (`1678`). Найдем полный путь до него:

`$ ls -l /proc/1678/fd | grep "v8_context_snapshot.bin"`


`lr-x------ 1 myuser myuser 64 мая 30 23:09 4 -> /usr/share/skypeforlinux/v8_context_snapshot.bin (deleted)
lr-x------ 1 myuser myuser 64 мая 30 23:09 78 -> /usr/share/skypeforlinux/v8_context_snapshot.bin (deleted)
`
*   Девятая колонка сообщает нам полный путь до файлового дескриптора, он будет выглядеть так (возьмем первую строчку): `/proc/1678/fd/4`

*   Обнулить файл можно, выполнив команду `truncate -s 0 /proc/1678/fd/4`

## 4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

*   Зомби-процессы не используют никаких системных ресурсов, но каждый использует очень маленький объем системной памяти для хранения своего дескриптора процесса.
    
*   Однако каждый процесс-зомби сохраняет свой идентификатор процесса (PID). 
    Системы Linux имеют конечное число идентификаторов процессов — 32767 по умолчанию в 32-разрядных системах. 
    Если зомби накапливаются с очень высокой скоростью — весь пул доступных PID в конечном итоге будет назначен процессам зомби, предотвращая запуск других процессов.
    
## 5. На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты? 

`# /sbin/opensnoop-bpfcc `

    *   PID    COMM               FD ERR PATH
    *   792    vminfo              4   0 /var/run/utmp
    *   580    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
    *   580    dbus-daemon        18   0 /usr/share/dbus-1/system-services
    *   580    dbus-daemon        -1   2 /lib/dbus-1/system-services`
    *   580    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/`

## 6. Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.

*   `uname` использует системный вызов `uname(2)` для получения информации, относящейся к ядру
*   `UNAME(2)  uname` - get name and information about current kernel
*   Также можно узнать версию ядра и релиз ОС: `Part of the utsname information is also accessible  via  /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}.`

## 7. Чем отличается последовательность команд через `;` и через `&&` в bash? 

*   `;` задает последовательность команд, а `&&` - логический оператор `и`
*   
В указанном примере:
*   root@netology1:~# test -d /tmp/some_dir; echo Hi 
*   Hi            
    > в данном примере сначала выполнится команда `test -d /tmp/some_dir` (проверяет, существует ли файл `some_dir` и что он является директорией), затем, независимо от результатов её выполнения, выполнится команда `echo Hi`
        
*   root@netology1:~# test -d /tmp/some_dir && echo Hi
*   root@netology1:~#
    > в данном примере команда `echo Hi` запустится только в том случае, если команда `test -d /tmp/some_dir` выполнится успешно.
    > учитывая, что проверка на существование директории вернет `false`, `echo Hi` выполнено не будет

### Есть ли смысл использовать в bash &&, если применить set -e?

*   `set` - команда, которая используется для указания и определения значений переменных окружения
*   опция `-e` - позволяет немедленно прекратить работу команды, если результат её выполнения отличается от 0 (0 - нормальный результат, true)
*   фактически, использование `set -e test -d /tmp/some_dir echo Hi` вернет тот же результат, что и с использованием `&&`, 
в простых конструкциях не вижу смысла использовать её. 
    
## 8. Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?

>>  `-e  Exit immediately if a command exits with a non-zero status.`
    > Немедленный выход, если команда завершается с ненулевым статусом.

>>  `-u  Treat unset variables as an error when substituting.`
    > Обработка неустановленных переменных при попытке подстановки как ошибку.    

>> `-x  Print commands and their arguments as they are executed.`
    > Печатает команды и их аргументы, по мере их выполнения. 
   
>> `-o  option-name опция, позволяет совместно работать с переменными.`
> `pipefail      the return value of a pipeline is the status of
                        the last command to exit with a non-zero status,
                        or zero if no command exited with a non-zero status`
    возвращает значение конвейерной функции - статус последней выполнившейся команды с ненулевым статусом или 0, 
    если ни одна команда не вышла с ненулевым статусом

*   Предполагаю, что использование в сценариях подобной команды и аргументов позволит отлаживать его работу, ведь в случае
возникновения ошибки, можно будет увидеть, на каком шаге она возникла и какие команды привели к появлению ошибки
       
## 9. Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе.

 `~$ ps -o stat`

    STAT
    Ss
    R+

*   `S` - прерывистый сон (ожидание завершения события)
*   `s` - является лидером сеанса
*   `R` - работает или запускается (в очереди выполнения)
*   `+` - находится в группе процессов переднего плана