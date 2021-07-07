# Домашнее задание к занятию "3.8. Компьютерные сети, лекция 3"
## 1. `ipvs`. Если при запросе на VIP сделать подряд несколько запросов (например, `for i in {1..50}; do curl -I -s 172.28.128.200>/dev/null; done `), ответы будут получены почти мгновенно. Тем не менее, в выводе `ipvsadm -Ln` еще некоторое время будут висеть активные `InActConn`. Почему так происходит?

```shell
# пока настраивала машины для второго задания, выполнила запрос к другому адресу
root@netology5:/home/vagrant# for i in {1..50}; do curl -I -s 192.168.1.100>/dev/null; done
root@netology5:/home/vagrant# ipvsadm -Ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
```
*   В `IPVS` есть концепция виртуального сервиса с собственным адресом – **VIP (Virtual IP).**    
*   В NAT режиме адрес VIP заменяется DST одного из “real” серверов, где отвечает приложение.    
*   Так как для возврата ответа клиенту требуется обратная трансляция, в NAT режиме ответ роутится через балансировщик.
	>NAT опирается на информацию от `сonntrack`, поэтому он может одинаково обрабатывать все пакеты из одного потока.
	
	>Firewall’ы с отслеживанием состояния, опираются на информацию от `сonntrack`, чтобы добавлять “ответный” трафик в белый список. 
	Это позволяет вам написать сетевую политику, которая говорит: *«разрешить моему pod’у подключаться к любому удаленному IP-адресу»* без необходимости писать политику для явного разрешения ответного трафика.

Однако у `conntrack` есть свои ограничения.
*   Таблица`conntrack`имеет настраиваемый максимальный размер, и, если она заполняется, 
    соединения обычно начинают отклоняться или прерываться. 
	Есть несколько сценариев, при которых стоит задуматься об использовании таблицы `conntrack`:
  
**Наиболее очевидный случай**, если ваш сервер обрабатывает чрезвычайно большое количество единовременно активных соединений. Например, если ваша таблица`conntrack`настроена на 128k записей, но у вас есть > 128k одновременных подключений;
    
**Немного менее очевидный случай**: если ваш сервер обрабатывает очень большое количество соединений в секунду. 
> Даже если соединения кратковременные, *они продолжают отслеживаться Linux в течение некоторого периода времени (по умолчанию 120с)*.

Например, если ваша таблица`conntrack`настроена на 128 тыс. записей и вы пытаетесь обработать 1100 подключений в секунду, они будут превышать размер таблицы `conntrack`, даже если соединения очень недолговечны (128k / 120с = 1092 соединений / с).


*Таким образом, из-за отслеживания Linux'ом соединений, их статус активен в течение некоторого времени*

# 2. На лекции мы познакомились отдельно с `ipvs` и отдельно с `keepalived`. Воспользовавшись этими знаниями, совместите технологии вместе (VIP должен подниматься демоном keepalived). Приложите конфигурационные файлы, которые у вас получились, и продемонстрируйте работу получившейся конструкции. Используйте для директора отдельный хост, не совмещая его с риалом! Подобная схема возможна, но выходит за рамки рассмотренного на лекции.

----------------------------------------------------------------------------------------------------------
*	*Изменила конфигурационный файл, т.к. приложенный не присваивал виртуальным машинам нужные ip-адреса.*
	
[Vagrantfile](https://bikepower.ddns.net/index.php/s/8w4EZTJtj6oYzaD)
<details>
<summary>Или под катом...</summary>
Vagrant.configure("2") do |config|
  config.vm.network "private_network", virtualbox__intnet: true, auto_config: false
  config.vm.box = "bento/ubuntu-20.04"

  config.vm.define "netology1" do |vb|
	vb.vm.provider "virtualbox" do |v|
	  v.memory = 512
	  v.cpus = 1
	end
	  vb.vm.provision "shell" do |s|
		s.inline = "hostname netology1;"\
		  "ip addr add 192.168.1.10/24 dev eth1;"\
		  "ip link set dev eth1 up;"\
		  "sudo apt-get update;"\
		  "sudo apt -y install nginx;"
	  end
  end
 
 config.vm.define "netology2" do |vb|
	vb.vm.provider "virtualbox" do |v|
	  v.memory = 512
	  v.cpus = 1
	end
	  vb.vm.provision "shell" do |s|
		s.inline = "hostname netology2;"\
		  "ip addr add 192.168.1.13/24 dev eth1;"\
		  "ip link set dev eth1 up;"\
		  "sudo apt-get update;"\
		  "sudo apt -y install nginx;"
	  end
  end
 
  config.vm.define "netology3" do |vb|
	vb.vm.provider "virtualbox" do |v|
	  v.memory = 512
	  v.cpus = 1
	end
	  vb.vm.provision "shell" do |s|
		s.inline = "hostname netology3;"\
		  "ip addr add 192.168.1.30/24 dev eth1;"\
		  "ip link set dev eth1 up;"\
		  "sudo apt-get update;"\
		  "sudo apt -y install nginx;"
	  end
  end

  config.vm.define "netology4" do |vb|
	vb.vm.provider "virtualbox" do |v|
	  v.memory = 512
	  v.cpus = 1
	end
	  vb.vm.provision "shell" do |s|
		s.inline = "hostname netology4;"\
		  "ip addr add 192.168.1.40/24 dev eth1;"\
		  "ip link set dev eth1 up;"\
		  "sudo apt-get update;"\
		  "sudo apt -y install nginx;"
	  end
  end
 
  config.vm.define "netology5" do |vb|
	vb.vm.provider "virtualbox" do |v|
	  v.memory = 512
	  v.cpus = 1
	end
	  vb.vm.provision "shell" do |s|
		s.inline = "hostname netology5;"\
		  "ip addr add 192.168.1.50/24 dev eth1;"\
		  "ip link set dev eth1 up;"\
		  "sudo apt-get update;"\
		  "sudo apt -y install nginx;"          
	  end
  end 
end
</details>

----------------------------------------------------------------------------------------------------------
*	Виртуальные машины:

1. [Клиент](https://bikepower.ddns.net/index.php/s/9qCr74aicTYBZgA) `netology5`, ip `192.168.1.50` 
1. `Балансировщики`:
   1. [Балансировщик1](https://bikepower.ddns.net/index.php/s/6zsfDsbE6m2tdxD) `netology1`, ip `192.168.1.10`
   2. [Балансировщик2](https://bikepower.ddns.net/index.php/s/m34dTgiSTCbZoaa) `netology3`, ip `192.168.1.30`
1. `nginx`:
	1. [nginx1](https://bikepower.ddns.net/index.php/s/iNywTSgz5g69HcW) `netology2`, ip `192.168.1.13`
	2. [nginx2](https://bikepower.ddns.net/index.php/s/57HpdyEw4AFgf2m) `netology4`, ip `192.168.1.40`

*	Сконфигурированные файлы по машинам: [machines](https://bikepower.ddns.net/index.php/s/kLMy7doLjXd9WBi)

----------------------------------------------------------------------------------------------------------

* Запрос с клиента к `nginx`
```shell
##--------------------------------------------------------------------------------------
## netology5 client
##--------------------------------------------------------------------------------------
vagrant@netology5:~$ curl -I -s 192.168.1.{13,40}:80 | grep HTTP
HTTP/1.1 200 OK
HTTP/1.1 200 OK
##--------------------------------------------------------------------------------------
```

*	Балансировщики:
*	ip `192.168.1.10`:
```shell
##--------------------------------------------------------------------------------------
## netology1 load balancer
##--------------------------------------------------------------------------------------
vagrant@netology1:~$ lsmod | grep -c ip_vs
0
vagrant@netology1:~# apt -y install ipvsadm; ipvsadm -Ln
Reading package lists... Done
Building dependency tree       
Reading state information... Done
Suggested packages:
  heartbeat keepalived ldirectord
The following NEW packages will be installed:
  ipvsadm
0 upgraded, 1 newly installed, 0 to remove and 135 not upgraded.
Need to get 40.2 kB of archives.
After this operation, 137 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu focal/main amd64 ipvsadm amd64 1:1.31-1 [40.2 kB]
Fetched 40.2 kB in 0s (157 kB/s)
Selecting previously unselected package ipvsadm.
(Reading database ... 41895 files and directories currently installed.)
Preparing to unpack .../ipvsadm_1%3a1.31-1_amd64.deb ...
Unpacking ipvsadm (1:1.31-1) ...
Setting up ipvsadm (1:1.31-1) ...
Processing triggers for man-db (2.9.1-1) ...
Processing triggers for systemd (245.4-4ubuntu3.3) ...
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
##--------------------------------------------------------------------------------------
```

*	ip `192.168.1.30`:
```shell
##--------------------------------------------------------------------------------------
## netology3 load balancer
##--------------------------------------------------------------------------------------
vagrant@netology3:~$ lsmod | grep -c ip_vs
0
root@netology3:/home/vagrant# apt -y install ipvsadm; ipvsadm -Ln
Reading package lists... Done
Building dependency tree       
Reading state information... Done
Suggested packages:
  heartbeat keepalived ldirectord
The following NEW packages will be installed:
  ipvsadm
0 upgraded, 1 newly installed, 0 to remove and 135 not upgraded.
Need to get 40.2 kB of archives.
After this operation, 137 kB of additional disk space will be used.
Get:1 http://archive.ubuntu.com/ubuntu focal/main amd64 ipvsadm amd64 1:1.31-1 [40.2 kB]
Fetched 40.2 kB in 0s (165 kB/s)
Selecting previously unselected package ipvsadm.
(Reading database ... 41895 files and directories currently installed.)
Preparing to unpack .../ipvsadm_1%3a1.31-1_amd64.deb ...
Unpacking ipvsadm (1:1.31-1) ...
Setting up ipvsadm (1:1.31-1) ...
Processing triggers for man-db (2.9.1-1) ...
Processing triggers for systemd (245.4-4ubuntu3.3) ...
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
##--------------------------------------------------------------------------------------
```
*	Выбираем общий `floating ip` для балансировщиков `192.168.1.100`
```shell
##--------------------------------------------------------------------------------------
# netology1 load balancer
##--------------------------------------------------------------------------------------
root@netology1:/home/vagrant# ipvsadm -A -t 192.168.1.100:80 -s rr
root@netology1:/home/vagrant# ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.13 -g -w 1
root@netology1:/home/vagrant# ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.40 -g -w 1
root@netology1:/home/vagrant# ipvsadm -Ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
TCP  192.168.1.100:80 rr
  -> 192.168.1.13:80              Route   1      0          0         
  -> 192.168.1.40:80              Route   1      0          0    

root@netology1:/home/vagrant# ip addr add 192.168.1.100/24 dev eth1 label eth1:100
root@netology1:/home/vagrant# ip -4 addr show eth1 | grep inet
    inet 192.168.1.10/24 scope global eth1
    inet 192.168.1.100/24 scope global secondary eth1:100
##--------------------------------------------------------------------------------------
## установим keepalived и пропишем конфигурационный файл:
##--------------------------------------------------------------------------------------
root@netology1:/home/vagrant# cat /etc/keepalived/keepalived.conf 
vrrp_script chk_nginx {
script "systemctl status nginx"
interval 2
}
vrrp_instance VI_1 {
state MASTER
interface eth1
virtual_router_id 33
priority 100 / 50
advert_int 1
authentication {
auth_type PASS
auth_pass netology_secret
}
virtual_ipaddress {
192.168.1.100/24 dev eth1
}
track_script {
chk_nginx
}
}

root@netology1:/home/vagrant# systemctl start keepalived
root@netology1:/home/vagrant# systemctl status keepalived
● keepalived.service - Keepalive Daemon (LVS and VRRP)
     Loaded: loaded (/lib/systemd/system/keepalived.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2021-07-05 19:32:46 UTC; 1min 29s ago
   Main PID: 24561 (keepalived)
      Tasks: 2 (limit: 470)
     Memory: 1.7M
     CGroup: /system.slice/keepalived.service
             ├─24561 /usr/sbin/keepalived --dont-fork
             └─24573 /usr/sbin/keepalived --dont-fork

Jul 05 19:32:47 netology1 Keepalived_vrrp[24573]: Registering Kernel netlink reflector
Jul 05 19:32:47 netology1 Keepalived_vrrp[24573]: Registering Kernel netlink command channel
Jul 05 19:32:47 netology1 Keepalived_vrrp[24573]: Opening file '/etc/keepalived/keepalived.conf'.
Jul 05 19:32:47 netology1 Keepalived_vrrp[24573]: WARNING - default user 'keepalived_script' for scr>
Jul 05 19:32:47 netology1 Keepalived_vrrp[24573]: (Line 13) Truncating auth_pass to 8 characters
Jul 05 19:32:47 netology1 Keepalived_vrrp[24573]: WARNING - script `systemctl` resolved by path sear>
Jul 05 19:32:47 netology1 Keepalived_vrrp[24573]: SECURITY VIOLATION - scripts are being executed bu>
Jul 05 19:32:47 netology1 Keepalived_vrrp[24573]: Registering gratuitous ARP shared channel
Jul 05 19:32:47 netology1 Keepalived_vrrp[24573]: VRRP_Script(chk_nginx) succeeded
Jul 05 19:32:47 netology1 Keepalived_vrrp[24573]: (VI_1) Entering BACKUP STATE
##--------------------------------------------------------------------------------------
```
```shell
##--------------------------------------------------------------------------------------
## netology3 load balancer
##--------------------------------------------------------------------------------------
root@netology3:/home/vagrant# ipvsadm -A -t 192.168.1.100:80 -s rr
root@netology3:/home/vagrant# ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.40 -g -w 1
root@netology3:/home/vagrant# ipvsadm -a -t 192.168.1.100:80 -r 192.168.1.13 -g -w 1
root@netology3:/home/vagrant# ipvsadm -Ln
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
TCP  192.168.1.100:80 rr
  -> 192.168.1.13:80              Route   1      0          0         
  -> 192.168.1.40:80              Route   1      0          0   

root@netology3:/home/vagrant# ip addr add 192.168.1.100/24 dev eth1 label eth1:100
root@netology3:/home/vagrant# ip -4 addr show eth1 | grep inet
    inet 192.168.1.30/24 scope global eth1
    inet 192.168.1.100/24 scope global secondary eth1:100  

##--------------------------------------------------------------------------------------
## установим keepalived и пропишем конфигурационный файл:
##--------------------------------------------------------------------------------------
root@netology3:/etc/keepalived# cat /etc/keepalived/keepalived.conf 
vrrp_script chk_nginx {
script "systemctl status nginx"
interval 2
}
vrrp_instance VI_1 {
state BACKUP
interface eth1
virtual_router_id 33
priority 100 / 50
advert_int 1
authentication {
auth_type PASS
auth_pass netology_secret
}
virtual_ipaddress {
192.168.1.100/24 dev eth1
}
track_script {
chk_nginx
}
}

root@netology3:/home/vagrant# systemctl start keepalived
root@netology3:/home/vagrant# systemctl status keepalived
● keepalived.service - Keepalive Daemon (LVS and VRRP)
     Loaded: loaded (/lib/systemd/system/keepalived.service; enabled; vend>
     Active: active (running) since Mon 2021-07-05 19:32:34 UTC; 23s ago
   Main PID: 24451 (keepalived)
      Tasks: 2 (limit: 470)
     Memory: 1.7M
     CGroup: /system.slice/keepalived.service
             ├─24451 /usr/sbin/keepalived --dont-fork
             └─24463 /usr/sbin/keepalived --dont-fork

Jul 05 19:32:34 netology3 Keepalived_vrrp[24463]: Opening file '/etc/keepa>
Jul 05 19:32:34 netology3 Keepalived_vrrp[24463]: WARNING - default user '>
Jul 05 19:32:34 netology3 Keepalived_vrrp[24463]: (Line 13) Truncating aut>
Jul 05 19:32:34 netology3 Keepalived_vrrp[24463]: WARNING - script `system>
Jul 05 19:32:34 netology3 Keepalived_vrrp[24463]: SECURITY VIOLATION - scr>
Jul 05 19:32:34 netology3 Keepalived_vrrp[24463]: Registering gratuitous A>
Jul 05 19:32:34 netology3 Keepalived_vrrp[24463]: VRRP_Script(chk_nginx) s>
Jul 05 19:32:34 netology3 Keepalived_vrrp[24463]: (VI_1) Entering BACKUP S>
Jul 05 19:32:45 netology3 Keepalived_vrrp[24463]: (VI_1) Backup received p>
Jul 05 19:32:46 netology3 Keepalived_vrrp[24463]: (VI_1) Entering MASTER S>
##--------------------------------------------------------------------------------------
```
*	Для `nginx` добавляем возможность обрабатывать пересланные балансировщиками пакеты:
```shell
##--------------------------------------------------------------------------------------
##netology2 real server
##--------------------------------------------------------------------------------------
root@netology2:/home/vagrant# ip addr add 192.168.1.100/24 dev lo label lo:100
root@netology2:/home/vagrant# ip -4 addr show lo | grep inet
    inet 127.0.0.1/8 scope host lo
    inet 192.168.1.100/24 scope global lo:100
##--------------------------------------------------------------------------------------
```
```shell
##--------------------------------------------------------------------------------------
## netology4 real server
##--------------------------------------------------------------------------------------
root@netology4:/home/vagrant# ip addr add 192.168.1.100/24 dev lo label lo:100
root@netology4:/home/vagrant# ip -4 addr show lo | grep inet
    inet 127.0.0.1/8 scope host lo
    inet 192.168.1.100/24 scope global lo:100
##--------------------------------------------------------------------------------------
```
*	Определяем режим отправки ответов на запросы ARP и ограничения для локального IP-адреса из IP-пакетов запроса ARP:
```shell
##--------------------------------------------------------------------------------------
##netology2 real server
##--------------------------------------------------------------------------------------
root@netology2:/home/vagrant# sysctl -w net.ipv4.conf.all.arp_announce=2
net.ipv4.conf.all.arp_announce = 2
root@netology2:/home/vagrant# sysctl -w net.ipv4.conf.all.arp_ignore=1
net.ipv4.conf.all.arp_ignore = 1
##--------------------------------------------------------------------------------------
```
```shell
##--------------------------------------------------------------------------------------
##netology4 real server
##--------------------------------------------------------------------------------------
root@netology4:/home/vagrant# sysctl -w net.ipv4.conf.all.arp_ignore=1
net.ipv4.conf.all.arp_ignore = 1
root@netology4:/home/vagrant# sysctl -w net.ipv4.conf.all.arp_announce=2
net.ipv4.conf.all.arp_announce = 2
##--------------------------------------------------------------------------------------
```

*	Выполним `arping` с клиента:
```shell
##--------------------------------------------------------------------------------------
##netology5 client
##--------------------------------------------------------------------------------------
root@netology5:/home/vagrant# arping -c1 -I eth1 192.168.1.100
ARPING 192.168.1.100
60 bytes from 08:00:27:05:04:cf (192.168.1.100): index=0 time=1.386 msec

--- 192.168.1.100 statistics ---
1 packets transmitted, 1 packets received,   0% unanswered (0 extra)
rtt min/avg/max/std-dev = 1.386/1.386/1.386/0.000 ms
##--------------------------------------------------------------------------------------
```
*	Затем запустим на клиенте `curl` в цикле:
```shell
##--------------------------------------------------------------------------------------
##netology5 client
##--------------------------------------------------------------------------------------
root@netology5:/home/vagrant# for i in {1..50}; do curl -I -s 192.168.1.100>/dev/null; done
##--------------------------------------------------------------------------------------
```

*	После завершения цикла по `curl` проверим статистику *netology1* (**MASTER**):
```shell
##--------------------------------------------------------------------------------------
## netology1 load balancer
##--------------------------------------------------------------------------------------
root@netology1:/proc/net# ipvsadm -Ln --stats
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port               Conns   InPkts  OutPkts  InBytes OutBytes
  -> RemoteAddress:Port
TCP  192.168.1.100:80                   61      183      150    10980    13200
  -> 192.168.1.13:80                    30       90       75     5400     6600
  -> 192.168.1.40:80                    31       93       75     5580     6600
##--------------------------------------------------------------------------------------
```

*	После завершения цикла по `curl` проверим статистику *netology3* (**BACKUP**):
```shell
##--------------------------------------------------------------------------------------
## netology3 load balancer
##--------------------------------------------------------------------------------------
root@netology3:/etc/keepalived# ipvsadm -Ln --stats
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port               Conns   InPkts  OutPkts  InBytes OutBytes
  -> RemoteAddress:Port
TCP  192.168.1.100:80                    0        0        0        0        0
  -> 192.168.1.13:80                     0        0        0        0        0
  -> 192.168.1.40:80                     0        0        0        0        0
##--------------------------------------------------------------------------------------
```

* После, экспериментируя, перезапускала службы. В результате, `keepalived` распределять нагрузку стал через **BACKUP**. 

* Запустила команду `curl` от клиента в цикле: 
```shell
##--------------------------------------------------------------------------------------
##netology5 client
##--------------------------------------------------------------------------------------
root@netology5:/home/vagrant# for i in {1..5}; do curl -I -s 192.168.1.100>/dev/null; done
##--------------------------------------------------------------------------------------
```
* С `tcpdump` проверила, что происходит на `nginx'ах`:

```shell
##--------------------------------------------------------------------------------------
## netology2 real server
##--------------------------------------------------------------------------------------
root@netology2:/home/vagrant# tcpdump -i eth1
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth1, link-type EN10MB (Ethernet), capture size 262144 bytes
20:21:24.878272 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:25.101376 ARP, Request who-has 192.168.1.13 tell 192.168.1.10, length 46
20:21:25.878617 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:26.125432 ARP, Request who-has 192.168.1.13 tell 192.168.1.10, length 46
20:21:26.879043 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:27.161933 ARP, Request who-has 192.168.1.40 tell 192.168.1.10, length 46
20:21:27.879548 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:28.173241 ARP, Request who-has 192.168.1.40 tell 192.168.1.10, length 46
20:21:28.879994 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:29.197179 ARP, Request who-has 192.168.1.40 tell 192.168.1.10, length 46
20:21:29.880248 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:30.236116 ARP, Request who-has 192.168.1.13 tell 192.168.1.10, length 46
20:21:30.880832 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:31.245615 ARP, Request who-has 192.168.1.13 tell 192.168.1.10, length 46
20:21:31.881302 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:32.269259 ARP, Request who-has 192.168.1.13 tell 192.168.1.10, length 46
20:21:32.881661 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:32.881661 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:33.881919 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:34.882432 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20

##--------------------------------------------------------------------------------------
```
```shell
##--------------------------------------------------------------------------------------
## netology4 real server
##--------------------------------------------------------------------------------------
root@netology4:/home/vagrant# tcpdump -i eth1
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth1, link-type EN10MB (Ethernet), capture size 262144 bytes
20:21:29.880899 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:30.236799 ARP, Request who-has 192.168.1.13 tell 192.168.1.10, length 46
20:21:30.881410 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:31.246223 ARP, Request who-has 192.168.1.13 tell 192.168.1.10, length 46
20:21:31.881910 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:32.269874 ARP, Request who-has 192.168.1.13 tell 192.168.1.10, length 46
20:21:32.882328 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:33.882550 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:34.883088 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
20:21:35.883406 IP 192.168.1.10 > vrrp.mcast.net: VRRPv2, Advertisement, vrid 33, prio 100, authtype simple, intvl 1s, length 20
##--------------------------------------------------------------------------------------
```

*	Статистика по балансировщикам:
```shell
##--------------------------------------------------------------------------------------
## netology1 load balancer
##--------------------------------------------------------------------------------------
root@netology1:/home/vagrant# ipvsadm -Ln --stats
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port               Conns   InPkts  OutPkts  InBytes OutBytes
  -> RemoteAddress:Port
TCP  192.168.1.100:80                    0        0        0        0        0
  -> 192.168.1.13:80                     0        0        0        0        0
  -> 192.168.1.40:80                     0        0        0        0        0
##--------------------------------------------------------------------------------------
```
```shell
##--------------------------------------------------------------------------------------
## netology3 load balancer
##--------------------------------------------------------------------------------------
root@netology3:/home/vagrant# ipvsadm -Ln --stats
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port               Conns   InPkts  OutPkts  InBytes OutBytes
  -> RemoteAddress:Port
TCP  192.168.1.100:80                   68      203        0    12180        0
  -> 192.168.1.13:80                    34      101        0     6060        0
  -> 192.168.1.40:80                    34      102        0     6120        0
##--------------------------------------------------------------------------------------
```
* Затем *netology3* по команде отправился в ребут. Повторив запросы с `curl` (for 1..5) и `tcpdump`, проверила работу оставшегося балансировщика:
```shell
##--------------------------------------------------------------------------------------
## netology1 load balancer
##--------------------------------------------------------------------------------------
root@netology1:/home/vagrant# ipvsadm -Ln --stats
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port               Conns   InPkts  OutPkts  InBytes OutBytes
  -> RemoteAddress:Port
TCP  192.168.1.100:80                    5       15        0      900        0
  -> 192.168.1.13:80                     3        9        0      540        0
  -> 192.168.1.40:80                     2        6        0      360        0
##--------------------------------------------------------------------------------------
```

## 3. В лекции мы использовали только 1 VIP адрес для балансировки. У такого подхода несколько отрицательных моментов, один из которых – невозможность активного использования нескольких хостов (1 адрес может только переехать с master на standby). Подумайте, сколько адресов оптимально использовать, если мы хотим без какой-либо деградации выдерживать потерю 1 из 3 хостов при входящем трафике 1.5 Гбит/с и физических линках хостов в 1 Гбит/с? Предполагается, что мы хотим задействовать 3 балансировщика в активном режиме (то есть не 2 адреса на 3 хоста, один из которых в обычное время простаивает).

>Попыталась нарисовать то, как представляю себе схему сети с тремя балансировщиками: [3ex](https://bikepower.ddns.net/index.php/s/6reHwzTnrJibbmx) 

*	Есть три балансировщика и три хоста;
*	Необходимо попарно определить, какие из балансировщиков будут взаимодействовать между собой; 
*	Таким образом, выделяются 3 VIP адреса, между которыми распределяется нагрузка на серверы (*на схеме MASTER - сплошные линии от балансировщиков, BACKUP - прерывистые*).
	 
| VIP				 | MASTER 	IP		| BACKUP  IP	 	| Server MASTER	| Server's BACKUP			|
:-------------------:|:----------------:|:-----------------:|:-------------:|:-------------------------:|
|192.168.2.115		 | 192.168.2.110 	|  192.168.2.111 	|**Server1**	|**Server2**	**Server3**	|
|192.168.2.116		 | 192.168.2.112 	|  192.168.2.110 	|**Server3**	|**Server1**	**Server2**	|
|192.168.2.117		 | 192.168.2.111 	|  192.168.2.112 	|**Server2**	|**Server1**	**Server3**	|

*	Все эти данные описаны в конфигурационных файлах в файле, что приложила к задаче (опустила задания значений `vrrp_script`, `track_script`);
*	На серверах прописаны балансировщики таким образом, чтоб они могли компенсировать потерю одного из них без потери соединения к серверу;
*	В идеале нужно добавить HAProxy для распределения трафика между балансировщиками. Однако, в теории я понимаю, как он работает, но отображать на схеме не рискнула.

*Таким образом, выделено три VIP адреса для балансировки нагрузки*	

