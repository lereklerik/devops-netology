# Домашнее задание к занятию "4.1. Командная оболочка Bash: Практические навыки"

## 1. Есть скрипт:
```shell
a=1
b=2
c=a+b
d=$a+$b
e=$(($a+$b))
```
## Какие значения переменным `c`,`d`,`e` будут присвоены? Почему?

*   значением переменной `c` является `a+b`
*   значением переменной `d` является `a+b`
*   значением переменной `e` является `3`

```shell
~$ a=1      # переменной a неявно присвоено числовое значение 1, т.е. a - строка с целым числом
~$ b=2      # переменной b неявно присвоено числовое значение 2, т.е. b - строка с целым числом
~$ c=a+b    # переменной c неявно присвоено строковое значение 'a+b', c - строка с символьными значениями
~$ echo $c
a+b
~$ d=$a+$b  # переменной d передали по ссылке значения a и b, 
            # однако арифметическая операция не интерпретируется как сложения без конструкции $(())
            # таким образом, оболочка воспринимает это как строку
~$ echo $d
1+2
~$ e=$(($a+$b)) ## переменной e передали конструкцию, которая позволяет определить математическую операцию сложения a и b,
                ## значения которых оболочкой интерпретируются как числовые
~$ echo $e
3
```

## 2. На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным. В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:
```shell
while ((1==1)
do
curl https://localhost:4757
if (($? != 0))
then
date >> curl.log
fi
done
```
*   Думаю, что нужно добавить закрывающую скобку у `while`:

```shell
while ((1==1)) # вот тут =)
do
curl https://localhost:4757
if (($? != 0))
then
date >> curl.log
fi
done
```
*   Протестируем на своем ПК с использованием `vagrant` и `vault`:
*   Напишем скрипт. Стучаться будем к `0.0.0.0:8200`:
```shell
~/WorkFolder$ mkdir scripts; cd scripts; vim ex4.1_01.sh
~/WorkFolder$ cat ex4.1_01.sh
#!/bin/bash
while ((1==1))
do
curl http://0.0.0.0:8200
if (($? != 0))
then
date >> curl.log
fi
sleep 10
done
~/WorkFolder/scripts$ chmod u+x ex4.1_01.sh
```
*   Запустим скрипт:
```shell
:~/WorkFolder/scripts$ ./ex4.1_01.sh 
curl: (56) Recv failure: Соединение разорвано другой стороной
curl: (56) Recv failure: Соединение разорвано другой стороной
curl: (56) Recv failure: Соединение разорвано другой стороной
curl: (56) Recv failure: Соединение разорвано другой стороной
curl: (56) Recv failure: Соединение разорвано другой стороной
```
*   В это время поднимем сервер `vault` с доступом к UI по адресу `http://0.0.0.0:8200`:
```shell
vagrant@vagrant:~$ vault server -dev -dev-listen-address="0.0.0.0:8200"
==> Vault server configuration:

             Api Address: http://0.0.0.0:8200
                     Cgo: disabled
         Cluster Address: https://0.0.0.0:8201
              Go Version: go1.15.13
              Listener 1: tcp (addr: "0.0.0.0:8200", cluster address: "0.0.0.0:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level: info
                   Mlock: supported: true, enabled: false
           Recovery Mode: false
                 Storage: inmem
                 Version: Vault v1.7.3
             Version Sha: 5d517c864c8f10385bf65627891bc7ef55f5e827

==> Vault server started! Log data will stream in below:
```
*   Вывод работы скрипта изменился:
```shell
~/WorkFolder/scripts$ ./ex4.1_01.sh 
curl: (56) Recv failure: Соединение разорвано другой стороной
curl: (56) Recv failure: Соединение разорвано другой стороной
<a href="/ui/">Temporary Redirect</a>.

<a href="/ui/">Temporary Redirect</a>.

<a href="/ui/">Temporary Redirect</a>.

<a href="/ui/">Temporary Redirect</a>.
```
*   `curl.log` (из-за `sleep` проверяем каждые 10 сек):
```shell
:~/WorkFolder/scripts$ tail curl.log
Чт июл 15 22:20:58 MSK 2021
Чт июл 15 22:21:23 MSK 2021
Чт июл 15 22:21:33 MSK 2021
Чт июл 15 22:21:43 MSK 2021
Чт июл 15 22:21:53 MSK 2021
Чт июл 15 22:22:03 MSK 2021
Чт июл 15 22:22:13 MSK 2021
Чт июл 15 22:22:23 MSK 2021
Чт июл 15 22:22:33 MSK 2021
Чт июл 15 22:22:43 MSK 2021
```    
*   Скрин:
[screenshot1](pictures/script1.png)

## 3. Необходимо написать скрипт, который проверяет доступность трёх IP: 192.168.0.1, 173.194.222.113, 87.250.250.242 по 80 порту и записывает результат в файл log. Проверять доступность необходимо пять раз для каждого узла.

*   Мой хост находится в первой подсети: `192.168.1.1`
```shell
$ ip route show
default via 192.168.1.1 dev wlo1 proto dhcp metric 600 
169.254.0.0/16 dev wlo1 scope link metric 1000 
192.168.1.0/24 dev wlo1 proto kernel scope link src 192.168.1.4 metric 600
```    

*   Поэтому для чистоты эксперимента заменила первый адрес из задания на него.
*   Скрипт:
```shell
#!/bin/bash
server_address_array=("192.168.1.1" "173.194.222.113" "87.250.250.242")
for (( i=0; i <${#server_address_array[@]}; i++ ))
do
n=5	                                      # добавила итератор, начальное значение = 5
echo "http://${server_address_array[$i]}" # в bash выводим проверяемое значение адреса (учитывая, что их немного, оставила так)
	while (($n > 0))                      # цикл будет выполняться до тех пор, пока каждый адрес не проанализируется 5 раз
	do
		echo "$( date +"%y-%m-%d %T" ); iteration $n; addr=http://${server_address_array[$i]}:">>file.log # в лог записываем информацию по дате запуска команды, номеру итерации и адресу сервера
		curl -I -s http://${server_address_array[$i]}&>>file.log                                          # а также, получаемый ответ по результату выполнения команды
		let "n -= 1"                      # уменьшаем значение итерируемой переменной в цикле
	done
done
```
*   Выдадим права на исполнение и запустим скрипт:
```shell
$ chmod u+x ex4.1_02.sh 
$ ./ex4.1_02.sh 
http://192.168.1.1
http://173.194.222.113
http://87.250.250.242

```
*   Скрипт отработал, посмотрим лог:
```shell
~/WorkFolder/scripts$ cat file.log 
$ cat file.log 
21-07-16 22:55:35; iteration 5; addr=http://192.168.1.1:
HTTP/1.1 200 OK
Server: 
Accept-Ranges: bytes
Connection: close
Content-Type: text/html; charset=utf-8
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self' 'unsafe-inline' 'unsafe-eval' data:
Cache-Control: no-cache,no-store
Pragma: no-cache
Content-Length: 38750
Set-Cookie: _TESTCOOKIESUPPORT=1; PATH=/; HttpOnly
X-Frame-Options: DENY

21-07-16 22:55:36; iteration 4; addr=http://192.168.1.1:
HTTP/1.1 200 OK
Server: 
Accept-Ranges: bytes
Connection: close
Content-Type: text/html; charset=utf-8
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self' 'unsafe-inline' 'unsafe-eval' data:
Cache-Control: no-cache,no-store
Pragma: no-cache
Content-Length: 38750
Set-Cookie: _TESTCOOKIESUPPORT=1; PATH=/; HttpOnly
X-Frame-Options: DENY

21-07-16 22:55:36; iteration 3; addr=http://192.168.1.1:
HTTP/1.1 200 OK
Server: 
Accept-Ranges: bytes
Connection: close
Content-Type: text/html; charset=utf-8
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self' 'unsafe-inline' 'unsafe-eval' data:
Cache-Control: no-cache,no-store
Pragma: no-cache
Content-Length: 38750
Set-Cookie: _TESTCOOKIESUPPORT=1; PATH=/; HttpOnly
X-Frame-Options: DENY

21-07-16 22:55:36; iteration 2; addr=http://192.168.1.1:
HTTP/1.1 200 OK
Server: 
Accept-Ranges: bytes
Connection: close
Content-Type: text/html; charset=utf-8
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self' 'unsafe-inline' 'unsafe-eval' data:
Cache-Control: no-cache,no-store
Pragma: no-cache
Content-Length: 38750
Set-Cookie: _TESTCOOKIESUPPORT=1; PATH=/; HttpOnly
X-Frame-Options: DENY

21-07-16 22:55:36; iteration 1; addr=http://192.168.1.1:
HTTP/1.1 200 OK
Server: 
Accept-Ranges: bytes
Connection: close
Content-Type: text/html; charset=utf-8
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self' 'unsafe-inline' 'unsafe-eval' data:
Cache-Control: no-cache,no-store
Pragma: no-cache
Content-Length: 38750
Set-Cookie: _TESTCOOKIESUPPORT=1; PATH=/; HttpOnly
X-Frame-Options: DENY

21-07-16 22:55:36; iteration 5; addr=http://173.194.222.113:
HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Type: text/html; charset=UTF-8
Date: Fri, 16 Jul 2021 19:55:36 GMT
Expires: Sun, 15 Aug 2021 19:55:36 GMT
Cache-Control: public, max-age=2592000
Server: gws
Content-Length: 219
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN

21-07-16 22:55:36; iteration 4; addr=http://173.194.222.113:
HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Type: text/html; charset=UTF-8
Date: Fri, 16 Jul 2021 19:55:36 GMT
Expires: Sun, 15 Aug 2021 19:55:36 GMT
Cache-Control: public, max-age=2592000
Server: gws
Content-Length: 219
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN

21-07-16 22:55:36; iteration 3; addr=http://173.194.222.113:
HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Type: text/html; charset=UTF-8
Date: Fri, 16 Jul 2021 19:55:36 GMT
Expires: Sun, 15 Aug 2021 19:55:36 GMT
Cache-Control: public, max-age=2592000
Server: gws
Content-Length: 219
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN

21-07-16 22:55:36; iteration 2; addr=http://173.194.222.113:
HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Type: text/html; charset=UTF-8
Date: Fri, 16 Jul 2021 19:55:36 GMT
Expires: Sun, 15 Aug 2021 19:55:36 GMT
Cache-Control: public, max-age=2592000
Server: gws
Content-Length: 219
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN

21-07-16 22:55:36; iteration 1; addr=http://173.194.222.113:
HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Type: text/html; charset=UTF-8
Date: Fri, 16 Jul 2021 19:55:36 GMT
Expires: Sun, 15 Aug 2021 19:55:36 GMT
Cache-Control: public, max-age=2592000
Server: gws
Content-Length: 219
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN

21-07-16 22:55:36; iteration 5; addr=http://87.250.250.242:
HTTP/1.1 406 Not acceptable
Connection: Close
Content-Length: 0

21-07-16 22:55:36; iteration 4; addr=http://87.250.250.242:
HTTP/1.1 406 Not acceptable
Connection: Close
Content-Length: 0

21-07-16 22:55:36; iteration 3; addr=http://87.250.250.242:
HTTP/1.1 406 Not acceptable
Connection: Close
Content-Length: 0

21-07-16 22:55:36; iteration 2; addr=http://87.250.250.242:
HTTP/1.1 406 Not acceptable
Connection: Close
Content-Length: 0

21-07-16 22:55:36; iteration 1; addr=http://87.250.250.242:
HTTP/1.1 406 Not acceptable
Connection: Close
Content-Length: 0
```

## 4. Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается

*   Продолжим с `192.168.1.1`. Скрипт обновленный:
```shell
#!/bin/bash
server_address_array=("192.168.1.1" "173.194.222.113" "87.250.250.242")
declare -i tmpcheck=0                             # переменная для передачи состояния соединения первому циклу
declare -i http_status                            # переменная для хранения значения статуса ответа сервера
for (( i=0; i <${#server_address_array[@]}; i++ ))
do
n=5	                                              # итератор
echo "http://${server_address_array[$i]}"         # выводим на консоль адрес
	while (($n > 0))
	do
		http_status=$( curl -I http://${server_address_array[$i]} 2>/dev/null | head -n 1 | cut -d$' ' -f2 )  # записываем числовой http-ответ от сервера, к которому обращаемся
		echo "http_status=$http_status"                                                                       # для наглядности выводим его в консоль
		declare -i answ=$(($http_status/100))		                                                          # проверяем, к какому сотне относится наш ответ от сервера (2xx: Success (успешно)
		if  [ "$answ" -ne 2 ];                                                                                # если ответ не относится к 2-й сотне, то переходим к прерыванию работы скрипта
		then
			echo "$( date ); http status: $http_status; ip: http://${server_address_array[$i]}">>error.log    # в лог пишем дату, текущий http-статус ответа и адрес
			tmpcheck=1                                                                                        # переменной для передачи состояния присваиваем значение 1 
			break                                                                                             # прерываем цикл
		fi	
		let "n -= 1"                  
	done
if [ "$tmpcheck" -eq 1 ]    # во внешнем цикле проверяем, если значение переменной равно 1, значит ответ от сервера был отличным от Success, проваливаемся внутрь условия 
then break                  # прерываем цикл
fi
done
```

*   Выдадим права на исполнение и запустим скрипт:
```shell
$ chmod u+x ex4.1_03.sh 
$ ./ex4.1_03.sh 
http://192.168.1.1
http_status=200
http_status=200
http_status=200
http_status=200
http_status=200
http://173.194.222.113
http_status=301
```
*   Проверим лог:
```shell
$ cat error.log 
Пт июл 16 23:07:05 MSK 2021; http status: 301; ip: http://173.194.222.113
```