# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

## 1. Используя знания из лекции по systemd, создайте самостоятельно простой unit-файл для node_exporter

*   Необходимо было скачать архивы с `prometheus` и `node_exporter`:
```shell
$ wget https://github.com/prometheus/prometheus/releases/download/v2.27.1/prometheus-2.27.1.linux-amd64.tar.gz
$ tar xvf prometheus-2.27.1.linux-amd64.tar.gz
```

```shell  
$ wget https://github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.linux-amd64.tar.gz
$ tar xvfz node_exporter-1.1.2.linux-amd64.tar.gz
```    

*   Настраиваем `prometheus` и `node_exporter`. В `prometheus.yml` добавляем:
    
```yml
global:
    scrape_interval: 15s
scrape_configs:
  - job_name: 'node'
    file_sd_configs:
      - files:
         - 'targets.json'
    static_configs:
    - targets: ['localhost:9100']
```
        
    


*   Создаем targets.json:    
```json
[
  {
    "labels": {
      "job": "node"
    },
    "targets": [
      "localhost:9100"
    ]
  }
]
```

*   Инициализируем конфигурационный файл:
```commandline  
./prometheus --config.file=./prometheus.yml
```
    
*   Далее, создаем файл `.service`:
```shell
/lib/systemd/system$ sudo vi runscript.service
```
    
*   Его содержимое:
```shell
[Unit]
Description=My Script Service
After=multi-user.target
[Service]
Type=idle
ExecStart=/home/vagrant/node_exporter-1.1.2.linux-amd64/node_exporter
[Install]
WantedBy=multi-user.target
```
* Рестарт системы и просмотр статуса сервиса после её запуска:

```shell
vagrant@vagrant:~$ systemctl status runscript.service
```

     ● runscript.service - My Script Service
    Loaded: loaded (/lib/systemd/system/runscript.service; enabled; vendor preset: enabled)
    Active: active (running) since Thu 2021-06-03 20:06:08 UTC; 4min 10s ago
    Main PID: 789 (node_exporter)
    Tasks: 4 (limit: 1074)
    Memory: 12.6M
    CGroup: /system.slice/runscript.service
         └─789 /home/vagrant/node_exporter-1.1.2.linux-amd64/node_exporter


    | Jun 03 20:06:08 | vagrant | node_exporter[789]: | level=info |  ts=2021-06-03T20:06:08.302Z | caller=node_exporter.go:113 collec> |
    | Jun 03 20:06:08 | vagrant | node_exporter[789]: | level=info |  ts=2021-06-03T20:06:08.302Z | caller=node_exporter.go:113 collec> |
    | Jun 03 20:06:08 | vagrant | node_exporter[789]: | level=info |  ts=2021-06-03T20:06:08.302Z | caller=node_exporter.go:113 collec> |
    | Jun 03 20:06:08 | vagrant | node_exporter[789]: | level=info |  ts=2021-06-03T20:06:08.302Z | caller=node_exporter.go:113 collec> |
    | Jun 03 20:06:08 | vagrant | node_exporter[789]: | level=info |  ts=2021-06-03T20:06:08.302Z | caller=node_exporter.go:113 collec> |
    | Jun 03 20:06:08 | vagrant | node_exporter[789]: | level=info |  ts=2021-06-03T20:06:08.302Z | caller=node_exporter.go:113 collec> |
    | Jun 03 20:06:08 | vagrant | node_exporter[789]: | level=info |  ts=2021-06-03T20:06:08.302Z | caller=node_exporter.go:113 collec> |
    | Jun 03 20:06:08 | vagrant | node_exporter[789]: | level=info |  ts=2021-06-03T20:06:08.302Z | caller=node_exporter.go:113 collec> |
    | Jun 03 20:06:08 | vagrant | node_exporter[789]: | level=info |  ts=2021-06-03T20:06:08.302Z | caller=node_exporter.go:195 msg="L> |
    | Jun 03 20:06:08 | vagrant | node_exporter[789]: | level=info |  ts=2021-06-03T20:06:08.303Z | caller=tls_config.go:191 msg="TLS > |

    lines 1-19/19 (END)

###   Предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на systemctl cat cron)?

*   Создадим файл node_exporter в `/etc/default/`:
```shell
vagrant@vagrant:~$ cat /etc/default/node_exporter 
testVar='test_DevOps'
```    
*   И выдадим права на исполнение:
```shell
vagrant@vagrant:/etc/default$ sudo chmod u+x node_exporter
``` 

*   Добавим в runscript.service указание на наш файл 
```shell
[Unit]
Description=My Script Service
After=multi-user.target
[Service]
Type=idle
ExecStart=/home/vagrant/node_exporter-1.1.2.linux-amd64/node_exporter
EnvironmentFile=-/etc/default/node_exporter
[Install]
WantedBy=multi-user.target
```
*   После перезагрузки смотрим состояние сервиса и по PID находим заданные переменные окружения:
```shell
vagrant@vagrant:~$ systemctl status runscript.service
● runscript.service - My Script Service
     Loaded: loaded (/lib/systemd/system/runscript.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2021-06-08 20:28:21 UTC; 41s ago
   Main PID: 796 (node_exporter)
      Tasks: 3 (limit: 1074)
     Memory: 12.6M
     CGroup: /system.slice/runscript.service
             └─796 /home/vagrant/node_exporter-1.1.2.linux-amd64/node_exporter

Jun 08 20:28:21 vagrant node_exporter[796]: level=info ts=2021-06-08T20:28:21.401Z caller=node_exporter.go:113 collector=thermal_zone
Jun 08 20:28:21 vagrant node_exporter[796]: level=info ts=2021-06-08T20:28:21.401Z caller=node_exporter.go:113 collector=time
Jun 08 20:28:21 vagrant node_exporter[796]: level=info ts=2021-06-08T20:28:21.401Z caller=node_exporter.go:113 collector=timex
Jun 08 20:28:21 vagrant node_exporter[796]: level=info ts=2021-06-08T20:28:21.401Z caller=node_exporter.go:113 collector=udp_queues
Jun 08 20:28:21 vagrant node_exporter[796]: level=info ts=2021-06-08T20:28:21.401Z caller=node_exporter.go:113 collector=uname
Jun 08 20:28:21 vagrant node_exporter[796]: level=info ts=2021-06-08T20:28:21.401Z caller=node_exporter.go:113 collector=vmstat
Jun 08 20:28:21 vagrant node_exporter[796]: level=info ts=2021-06-08T20:28:21.401Z caller=node_exporter.go:113 collector=xfs
Jun 08 20:28:21 vagrant node_exporter[796]: level=info ts=2021-06-08T20:28:21.401Z caller=node_exporter.go:113 collector=zfs
Jun 08 20:28:21 vagrant node_exporter[796]: level=info ts=2021-06-08T20:28:21.401Z caller=node_exporter.go:195 msg="Listening on" address=:9100
Jun 08 20:28:21 vagrant node_exporter[796]: level=info ts=2021-06-08T20:28:21.402Z caller=tls_config.go:191 msg="TLS is disabled." http2=false
```
```shell
vagrant@vagrant:~$ sudo cat /proc/796/environ 
LANG=en_US.UTF-8LANGUAGE=en_US:PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/binINVOCATION_ID=13461c45557b41919f855dc37263df4e
JOURNAL_STREAM=9:24191testVar=test_DevOps
```
*   У нас появилась новая переменная окружения `test` со значением `test_DevOps`


### Обновление задания по замечанию

*   Сервис скорректировала:
```shell
vagrant@vagrant:/lib/systemd/system$ cat runscript.service 
[Unit]
Description=My Script Service
After=multi-user.target runscript.service
[Service]
Type=idle
EnvironmentFile=-/etc/default/node_exporter
ExecStart=/home/vagrant/node_exporter-1.1.2.linux-amd64/node_exporter $ARG1
Restart=Always
[Install]
WantedBy=multi-user.target
```
*   Скорректировала `/etc/default/node_exporter`:
```shell
vagrant@vagrant:/etc/default$ cat node_exporter 
#testVar='test_DevOps'
ARG1=--collector.cpu.info
```
*   Запускаю систему:
```shell
vagrant@vagrant:~$ sudo systemctl status runscript.service 
● runscript.service - My Script Service
     Loaded: loaded (/lib/systemd/system/runscript.service; enabled; vendor preset: enabled)
     Active: active (running) since Fri 2021-06-11 07:22:53 UTC; 3min 27s ago
   Main PID: 798 (node_exporter)
      Tasks: 4 (limit: 1074)
     Memory: 12.8M
     CGroup: /system.slice/runscript.service
             └─798 /home/vagrant/node_exporter-1.1.2.linux-amd64/node_exporter --collector.cpu.info

Jun 11 07:22:53 vagrant node_exporter[798]: level=info ts=2021-06-11T07:22:53.422Z caller=node_exporter.go:113 collector=thermal_zone
Jun 11 07:22:53 vagrant node_exporter[798]: level=info ts=2021-06-11T07:22:53.422Z caller=node_exporter.go:113 collector=time
Jun 11 07:22:53 vagrant node_exporter[798]: level=info ts=2021-06-11T07:22:53.422Z caller=node_exporter.go:113 collector=timex
Jun 11 07:22:53 vagrant node_exporter[798]: level=info ts=2021-06-11T07:22:53.422Z caller=node_exporter.go:113 collector=udp_queues
Jun 11 07:22:53 vagrant node_exporter[798]: level=info ts=2021-06-11T07:22:53.422Z caller=node_exporter.go:113 collector=uname
Jun 11 07:22:53 vagrant node_exporter[798]: level=info ts=2021-06-11T07:22:53.422Z caller=node_exporter.go:113 collector=vmstat
Jun 11 07:22:53 vagrant node_exporter[798]: level=info ts=2021-06-11T07:22:53.422Z caller=node_exporter.go:113 collector=xfs
Jun 11 07:22:53 vagrant node_exporter[798]: level=info ts=2021-06-11T07:22:53.422Z caller=node_exporter.go:113 collector=zfs
Jun 11 07:22:53 vagrant node_exporter[798]: level=info ts=2021-06-11T07:22:53.427Z caller=node_exporter.go:195 msg="Listening on" address=:9100
Jun 11 07:22:53 vagrant node_exporter[798]: level=info ts=2021-06-11T07:22:53.429Z caller=tls_config.go:191 msg="TLS is disabled." http2=false
```

## 2. Ознакомьтесь с опциями node_exporter и выводом /metrics по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.

        --collector.cpu            Enable the cpu collector (default: enabled). /* Собирает статистику использования процессора */                       
        --collector.cpufreq        Enable the cpufreq collector (default: enabled). /* Собирает статистику частоты процессора */
        --collector.diskstats      Enable the diskstats collector (default: enabled). /* Собирает статистику дискового ввода-вывода */
        --collector.edac           Enable the edac collector (default: enabled). /* Собирает статистику обнаружения и исправления ошибок*/
        --collector.filesystem     Enable the filesystem collector (default: enabled). /* Собирает статистику по файловой системе */
        --collector.meminfo        Enable the meminfo collector (default: enabled). /* Собирает статистику использования оперативной памяти */
        --collector.vmstat         Enable the vmstat collector (default: enabled). /* Собирает статистику процессов из /proc/vmstat */      
        --collector.schedstat      Enable the schedstat collector (default: enabled). /* Собирает статистику планировщика задач */

## 3. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.

*   Подключение к `localhost:19999` (Скриншоты экрана):
    > Для "показательной" нагрузки запускала `sysbench`:
    ```shell
    $ sysbench --num-threads=4 --test=cpu run
    ```

*   [![1 pic](//https://bikepower.ddns.net/index.php/s/2scywbX5opPiwMZ)](https://bikepower.ddns.net/index.php/s/2scywbX5opPiwMZ)
*   [![2 pic](//https://bikepower.ddns.net/index.php/s/kc447JkKSrXzNi2)](https://bikepower.ddns.net/index.php/s/kc447JkKSrXzNi2)
*   [![3 pic](//https://bikepower.ddns.net/index.php/s/fx6KaE2Ey9X89Xt)](https://bikepower.ddns.net/index.php/s/fx6KaE2Ey9X89Xt)
*   [![4 pic](//https://bikepower.ddns.net/index.php/s/prkkf2HL4ZsRNns)](https://bikepower.ddns.net/index.php/s/prkkf2HL4ZsRNns)


## 4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?

*   Т.к. на домашнем ПК установлен Linux Mint, проверить разницу в выводе `dmesg` можно элементарно. 
    Посмотрев результат выполнения просто команды `dmesg` выполняю поиск по слову `virtual`:

-   *vagrant*
```shell
vagrant@vagrant:~$ dmesg | grep virtual
[    0.001498] CPU MTRRs all blank - virtualized system.
[    0.038795] Booting paravirtualized kernel on KVM
[    0.176881] Performance Events: PMU not available due to virtualization, using software events only.
[    2.322434] systemd[1]: Detected virtualization oracle.
```
         Все диапазонные регистры памяти пустые, т.к. это виртуальная система;
         Происходит загрузка паравиртуализированного ядра в Kernel-based Virtual Machine;
         Модуль управления питания недоступен из-за виртуализации, используются event'ы ПО;
         systemd: обнаружена виртуализация oracle.

-   *Linux Mint (дом.ПК)*
```shell
~$ dmesg | grep virtual
[    0.027717] Booting paravirtualized kernel on bare hardware
...
```
         Загрузка ядра происходит на чистом железе

Таким образом, ОС осознает, что она виртуальная (:

## 5. Как настроен sysctl fs.nr_open на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (ulimit --help)?

```shell
vagrant@vagrant:~$ /sbin/sysctl -n fs.nr_open
1048576
```
        1048576 - максимально возможное количество открытых дексрипторов для ядра системы. 
        Если не менять его, то для пользователя задать значение больше этого числа не получится

```shell
vagrant@vagrant:/sbin$ ulimit -Sn
1024
```
--------------------------------------------
    мягкий лимит для пользователя, может быть увеличен в процессе работы (аналогично ulimit -n)
```shell
vagrant@vagrant:/sbin$ ulimit -Hn
1048576
```
--------------------------------------------
    жесткий лимит для пользователя, предел не может увеличиваться, только уменьшаться

Оба варианта не могут превысить системный лимит `fs.nr_open`

## 6. Запустите любой долгоживущий процесс (не ls, который отработает мгновенно, а, например, sleep 1h) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через nsenter. 

```shell
vagrant@vagrant:~$ sudo unshare -f --pid --mount-proc top
```
```shell
vagrant@vagrant:~$ ps aux | grep top
root        3622  0.0  0.4  11856  4580 pts/4    S+   18:49   0:00 sudo unshare -f --pid --mount-proc top
root        3624  0.0  0.0   8080   592 pts/4    S+   18:49   0:00 unshare -f --pid --mount-proc top
root        3625  0.0  0.3  11712  3824 pts/4    S+   18:49   0:00 top
vagrant     3681  0.0  0.0   8900   672 pts/7    S+   18:49   0:00 grep --color=auto top
```
```shell
vagrant@vagrant:~$ sudo nsenter --target 3625 --pid --mount
root@vagrant:/# vagrant
-bash: vagrant: command not found
root@vagrant:/# ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.3  11712  3824 pts/4    S+   18:49   0:00 top
root           2  0.0  0.3   9836  3940 pts/7    S    18:50   0:00 -bash
root          12  0.0  0.3  11492  3420 pts/7    R+   18:50   0:00 ps aux
```

## 7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (это важно, поведение в других ОС не проверялось). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов dmesg расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

*    Конструкция определяет функцию с названием `:`, которая вызывает саму себя, пока не исчерпает лимит на запуск процессов в системе.
*    Заменим `:` на слово:
```shell
func() {
      func | func &
};
func
```
*    Система бесконечно утверждает, что это fork-процесс:
```shell
-bash: fork: Resource temporarily unavailable
```
*   Но в конце концов "отходит" от этого состояния. С командой `dmesg` выводим сообщения. 
*   Судя по временному отрезку и результату вывода на экран, `cgroup` помог системе стабилизироваться:
```shell
[   12.157402] systemd-journald[357]: File /var/log/journal/324489e30d404746a187573936b5c7e9/user-1000.journal corrupted or uncleanly shut down, renaming and replacing.
[44054.775006] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-21.scope
```
*   `cgroup` - группа процессов в Linux, для которой механизмами ядра наложена изоляция и установлены ограничения 
    на некоторые вычислительные ресурсы (процессорные, сетевые, ресурсы памяти, ресурсы ввода-вывода). 
    Механизм позволяет образовывать иерархические группы процессов с заданными ресурсными свойствами и 
    обеспечивает программное управление ими.    
*   Таким образом, `cgroup` ограничивает создание процессов пользователя, т.к. "выдача" pid'ов процессам лимитирована
*   Ограничить количество процессов, создаваемых пользователем, определенным количеством, с помощью `ulimit -u`:
```shell
$ ulimit -u 100
```