# Домашнее задание к занятию "3.5. Файловые системы"

## 1. Узнайте о `sparse` (разряженных) файлах

    *   Разреженные – это специальные файлы, которые с большей эффективностью используют файловую систему, 
        они не позволяют ФС занимать свободное дисковое пространство носителя, когда разделы не заполнены. 
        То есть, «пустое место» будет задействовано только при необходимости. Пустая информация в виде нулей, 
        будет хранится в блоке метаданных ФС. Поэтому, разреженные файлы изначально занимают меньший объем носителя, 
        чем их реальный объем.

Поэкспериментируем:
```shell
# создадим разреженный файл, размером 20 Мб 
# (возможно, можно было бы экспериментировать с бОльшим размером, далее было бы нагляднее)
vagrant@vagrant:~$ truncate -s20M file-sparse
vagrant@vagrant:~$ file file-sparse 
file-sparse: data
vagrant@vagrant:~$ du -h --apparent-size file-sparse 
20M	file-sparse
#
# после того, как создали разреженный файл, видим, что размер под него сразу задан
#
vagrant@vagrant:~$ stat file-sparse 
  File: file-sparse
  Size: 20971520  	Blocks: 0          IO Block: 4096   regular file
Device: fd00h/64768d	Inode: 2883656     Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/ vagrant)   Gid: ( 1000/ vagrant)
Access: 2021-06-15 17:19:31.049758375 +0000
Modify: 2021-06-15 17:18:37.497757832 +0000
Change: 2021-06-15 17:18:37.497757832 +0000
 Birth: -
vagrant@vagrant:~$ touch test_file_new
#
# а вот обычный пустой файл ничего весит
#
vagrant@vagrant:~$ stat test_file_new 
  File: test_file_new
  Size: 0         	Blocks: 0          IO Block: 4096   regular empty file
Device: fd00h/64768d	Inode: 2883660     Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/ vagrant)   Gid: ( 1000/ vagrant)
Access: 2021-06-15 17:23:21.657760713 +0000
Modify: 2021-06-15 17:23:21.657760713 +0000
Change: 2021-06-15 17:23:21.657760713 +0000
 Birth: -
#
# добавим ему немного данных размером в 15 кб
#
vagrant@vagrant:~$ echo 'test test test' >>test_file_new 
vagrant@vagrant:~$ stat test_file_new 
  File: test_file_new
  Size: 15        	Blocks: 8          IO Block: 4096   regular file
Device: fd00h/64768d	Inode: 2883660     Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/ vagrant)   Gid: ( 1000/ vagrant)
Access: 2021-06-15 17:23:45.693760957 +0000
Modify: 2021-06-15 17:24:00.085761103 +0000
Change: 2021-06-15 17:24:00.085761103 +0000
 Birth: -
vagrant@vagrant:~$ ls -lsh test_file_new 
4.0K -rw-rw-r-- 1 vagrant vagrant 15 Jun 15 17:24 test_file_new
#
# и такую же операцию провернем с разреженным, его размер также увеличился на 15 кб
#
vagrant@vagrant:~$ echo 'test test test' >>file-sparse 
vagrant@vagrant:~$ stat file-sparse 
  File: file-sparse
  Size: 20971535  	Blocks: 8          IO Block: 4096   regular file
Device: fd00h/64768d	Inode: 2883656     Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/ vagrant)   Gid: ( 1000/ vagrant)
Access: 2021-06-15 17:29:12.489764270 +0000
Modify: 2021-06-15 17:28:30.305763842 +0000
Change: 2021-06-15 17:28:30.305763842 +0000
 Birth: -
```

*   Среди обсуждаемых проблем и вопросов о `sparse`, наткнулась на то, что объемные файлы 
    очень долго "просматриваются", если мы хотим их прочитать (с начала или конца). 
    Поэтому решила сравнить просмотр файлов с конца, сколько займет это по времени в наносекундах
```shell
# разреженный файл - проход занял 0,63 секунды (627084645 наносекунд)
# конечно, с более объемным файлом было бы нагляднее
vagrant@vagrant:~$ date +%T.%N; tail -n 20 file-sparse; date +%T.%N
17:39:12.708901821
test test test
17:39:13.335986466
# обычный файл - проход занял 0,0039 секунды (3918743 наносекунд)
vagrant@vagrant:~$ date +%T.%N; tail -n 20 test_file_new; date +%T.%N
17:39:22.109751296
test test test
17:39:22.113670039
```    
* Время существенно увеличилось при просмотре файлов, казалось бы, с одинаковым содержимым. 
  Просмотр нулевых байтов занимает много времени

## 2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?

*   У объекта в файловой системе (далее -- ФС) есть первичный идентификатор - `inode`, и это *не имя файла*.
*   В рамках одной ФС может быть создано более одного файла с одним и тем же `inode` и разными именами. Например:

```shell
# создадим файл
vagrant@vagrant:~$ touch test_file
# проверим число ссылок на него
vagrant@vagrant:~$ stat --format=%h test_file 
1
# создадим ещё одну жесткую ссылку на файл
vagrant@vagrant:~$ ln test_file test_hl_tf
# уточним число ссылок на файл, их стало две
vagrant@vagrant:~$ stat --format=%h test_file 
2
# посмотрим первичные идентификаторы, на которые ссылаются наши файлы
vagrant@vagrant:~$ stat --format=%i test_file; stat --format=%i test_hl_tf 
2883655
2883655
# уточним права доступа
vagrant@vagrant:~$ ls -ilh | grep "test_"
2883655 -rw-rw-r-- 2 vagrant vagrant    0 Jun 15 15:48 test_file
2883655 -rw-rw-r-- 2 vagrant vagrant    0 Jun 15 15:48 test_hl_tf
# скорректируем права доступа для test_hl_tf и ещё раз проверим их
vagrant@vagrant:~$ sudo chmod 0755 test_hl_tf
vagrant@vagrant:~$ ls -ilh | grep "test_"
2883655 -rwxr-xr-x 2 vagrant vagrant    0 Jun 15 15:48 test_file
2883655 -rwxr-xr-x 2 vagrant vagrant    0 Jun 15 15:48 test_hl_tf
```
*   Таким образом, владелец и права доступа не могут быть разными у объекта и жестких ссылок на него.
*   Если мы удалим оригинальный `test_file`, то объект все равно продолжит существование на ФС, т.к.
    на него присутствует жесткая ссылка:
    
```shell
vagrant@vagrant:~$ rm test_file 
vagrant@vagrant:~$ stat --format=%h,inode=%i test_hl_tf 
1,inode=2883655
```
*   Каждая из жестких ссылок -- это отдельный файл, но ведут они к одному участку жесткого диска. 
    Файл можно перемещать между каталогами, и все ссылки останутся рабочими, поскольку для них неважно имя.

## 3. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile. Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.

*   После изменения конфигурации выведем список устройств:
```shell
root@vagrant:/home/vagrant# lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                    8:0    0   64G  0 disk 
├─sda1                 8:1    0  512M  0 part /boot/efi
├─sda2                 8:2    0    1K  0 part 
└─sda5                 8:5    0 63.5G  0 part 
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
sdb                    8:16   0  2.5G  0 disk 
sdc                    8:32   0  2.5G  0 disk 
```
## 4. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.

*   Перейдем в интерактивный режим `fdisk`:
```shell
root@vagrant:/home/vagrant# fdisk /dev/sdb

Welcome to fdisk (util-linux 2.34).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0x8f716b04.
```
*   Создадим новую таблицу разделов MBR:
```shell
Command (m for help): o
Created a new DOS disklabel with disk identifier 0xba58eeb4.
```
*   Создадим разделы:
```shell
Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-5242879, default 2048): 2048
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2G

Created a new partition 1 of type 'Linux' and of size 2 GiB.
Command (m for help): n       
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (2-4, default 2): 2
First sector (4196352-5242879, default 4196352): 4196352
Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879): 5242879

Created a new partition 2 of type 'Linux' and of size 511 MiB.
```
*   Посмотрим, что в итоге:
```shell

Command (m for help): p
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xba58eeb4
# разделы создались
Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 4196351 4194304    2G 83 Linux
/dev/sdb2       4196352 5242879 1046528  511M 83 Linux
```

## 5. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.

*   Перенесем:
```shell
root@vagrant:/# sfdisk -d /dev/sdb | sfdisk --force /dev/sdc
Checking that no-one is using this disk right now ... OK

Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Created a new DOS disklabel with disk identifier 0xba58eeb4.
/dev/sdc1: Created a new partition 1 of type 'Linux' and of size 2 GiB.
/dev/sdc2: Created a new partition 2 of type 'Linux' and of size 511 MiB.
/dev/sdc3: Done.

New situation:
Disklabel type: dos
Disk identifier: 0xba58eeb4

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 4196351 4194304    2G 83 Linux
/dev/sdc2       4196352 5242879 1046528  511M 83 Linux

The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```
*   Посмотрим результат:
```shell
root@vagrant:/# lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda                    8:0    0   64G  0 disk 
├─sda1                 8:1    0  512M  0 part /boot/efi
├─sda2                 8:2    0    1K  0 part 
└─sda5                 8:5    0 63.5G  0 part 
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]
sdb                    8:16   0  2.5G  0 disk 
├─sdb1                 8:17   0    2G  0 part 
└─sdb2                 8:18   0  511M  0 part 
sdc                    8:32   0  2.5G  0 disk 
├─sdc1                 8:33   0    2G  0 part 
└─sdc2                 8:34   0  511M  0 part
```
*   И немного подробнее:
```shell
...
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xba58eeb4

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 4196351 4194304    2G 83 Linux
/dev/sdb2       4196352 5242879 1046528  511M 83 Linux


Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xba58eeb4

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 4196351 4194304    2G 83 Linux
/dev/sdc2       4196352 5242879 1046528  511M 83 Linux
...
```

## 6. Соберите `mdadm RAID1` на паре разделов 2 Гб.

*   Соберем с `mdadm` с подробным `--verbose` описанием происходящего
```shell
root@vagrant:/# mdadm --create --verbose /dev/md1 --level=1 -n 2 /dev/sdb1 /dev/sdc1
mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
mdadm: size set to 2094080K
Continue creating array? y
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md1 started.
```
* Результат:
```shell
root@vagrant:/# cat /proc/mdstat
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10] 
md1 : active raid1 sdc1[1] sdb1[0]
      2094080 blocks super 1.2 [2/2] [UU]
```
## 7. Соберите `mdadm RAID0` на второй паре маленьких разделов.

```shell
root@vagrant:/# mdadm --create --verbose /dev/md0 --level=1 -n 2 /dev/sdb2 /dev/sdc2
mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
mdadm: size set to 522240K
Continue creating array? y
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md0 started.
```
*   Результат:
```shell
root@vagrant:/# cat /proc/mdstat
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10] 
md0 : active raid1 sdc2[1] sdb2[0]
      522240 blocks super 1.2 [2/2] [UU]
      
md1 : active raid1 sdc1[1] sdb1[0]
      2094080 blocks super 1.2 [2/2] [UU]
```

## 8. Создайте 2 независимых PV на получившихся md-устройствах.

*   Создадим с командой `pvcreate`:
```shell
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
root@vagrant:/# pvcreate /dev/md0 /dev/md1
  Physical volume "/dev/md0" successfully created.
  Physical volume "/dev/md1" successfully created.
```
*   Посмотрим, что получилось вкратце с `pvscan`:
```shell
root@vagrant:/# pvscan
  PV /dev/sda5   VG vgvagrant       lvm2 [<63.50 GiB / 0    free]
  PV /dev/md0                       lvm2 [510.00 MiB]
  PV /dev/md1                       lvm2 [<2.00 GiB]
  Total: 3 [65.99 GiB] / in use: 1 [<63.50 GiB] / in no VG: 2 [<2.50 GiB]
```
*   И подробнее с `pvdisplay`:
```shell
root@vagrant:/# pvdisplay
  --- Physical volume ---
  PV Name               /dev/sda5
  VG Name               vgvagrant
  PV Size               <63.50 GiB / not usable 0   
  Allocatable           yes (but full)
  PE Size               4.00 MiB
  Total PE              16255
  Free PE               0
  Allocated PE          16255
  PV UUID               OCbATH-NO0a-4yCv-lVyW-UOYQ-uFJm-DPdN8c
   
  "/dev/md0" is a new physical volume of "510.00 MiB"
  --- NEW Physical volume ---
  PV Name               /dev/md0
  VG Name               
  PV Size               510.00 MiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               vDcCXR-HLjJ-bdWC-t90n-SWut-5NCv-XMrmsk
   
  "/dev/md1" is a new physical volume of "<2.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/md1
  VG Name               
  PV Size               <2.00 GiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               1s3iI0-AD2x-n6t9-MzlF-voI5-aNmr-lkcSQI

```
## 9. Создайте общую volume-group на этих двух PV.

*   С помощью `vgcreate` создадим общую группу томов `vol_gr1`:
```shell
root@vagrant:/# vgcreate vol_gr1 /dev/md0 /dev/md1
  Volume group "vol_gr1" successfully created
```
*   Результат c `vgdisplay`:
```shell
root@vagrant:/# vgdisplay
  --- Volume group ---
  VG Name               vgvagrant
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  3
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <63.50 GiB
  PE Size               4.00 MiB
  Total PE              16255
  Alloc PE / Size       16255 / <63.50 GiB
  Free  PE / Size       0 / 0   
  VG UUID               VE2d8u-Iecl-8hpG-Migd-wvgP-pWW8-GIXH5V
   
  --- Volume group ---
  VG Name               vol_gr1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               2.49 GiB
  PE Size               4.00 MiB
  Total PE              638
  Alloc PE / Size       0 / 0   
  Free  PE / Size       638 / 2.49 GiB
  VG UUID               izRKZ3-0FmL-mPrT-Zd7V-asdd-2ltX-ne6R2a
```

## 10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

*   Создадим с `lvcreate`:
```shell
root@vagrant:/# lvcreate -L 100M vol_gr1 /dev/md0
  Logical volume "lvol0" created.
```
*   Посмотрим результат с `lvdisplay`:
```shell
root@vagrant:/# lvdisplay
  --- Logical volume ---
  LV Path                /dev/vgvagrant/root
  LV Name                root
  VG Name                vgvagrant
  LV UUID                MQQRbn-9xpd-nWNN-Fuq3-UH8Z-1AIp-AVmolp
  LV Write Access        read/write
  LV Creation host, time vagrant, 2020-12-23 07:45:37 +0000
  LV Status              available
  # open                 1
  LV Size                <62.54 GiB
  Current LE             16010
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
   
  --- Logical volume ---
  LV Path                /dev/vgvagrant/swap_1
  LV Name                swap_1
  VG Name                vgvagrant
  LV UUID                bv9Pja-jeKa-32O7-Oodb-HnFk-z9D6-uX0W4s
  LV Write Access        read/write
  LV Creation host, time vagrant, 2020-12-23 07:45:37 +0000
  LV Status              available
  # open                 2
  LV Size                980.00 MiB
  Current LE             245
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:1
   
  --- Logical volume ---
  LV Path                /dev/vol_gr1/lvol0
  LV Name                lvol0
  VG Name                vol_gr1
  LV UUID                Obrxq7-YvKk-60Dv-KkrX-inhs-qSEl-TCPShb
  LV Write Access        read/write
  LV Creation host, time vagrant, 2021-06-15 19:31:18 +0000
  LV Status              available
  # open                 0
  LV Size                100.00 MiB
  Current LE             25
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:2
```
## 11. Создайте `mkfs.ext4` ФС на получившемся LV.
```shell
root@vagrant:/# mkfs.ext4 /dev/vol_gr1/lvol0 
mke2fs 1.45.5 (07-Jan-2020)
Creating filesystem with 25600 4k blocks and 25600 inodes

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done
```

## 12. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`

*   Смонтируем раздел:
```shell
root@vagrant:/# mkdir /tmp/new
root@vagrant:/# mount /dev/vol_gr1/lvol0 /tmp/new
root@vagrant:/# ls /tmp/new/
lost+found
```
## 13. Поместите туда тестовый файл, например wget `https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`
```shell
root@vagrant:/# wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
--2021-06-15 19:41:20--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 20897241 (20M) [application/octet-stream]
Saving to: ‘/tmp/new/test.gz’

/tmp/new/test.gz                                            100%[==========>]  19.93M  2.09MB/s    in 9.9s    

2021-06-15 19:41:30 (2.01 MB/s) - ‘/tmp/new/test.gz’ saved [20897241/20897241]
```

## 14. Прикрепите вывод `lsblk`
```shell
root@vagrant:/# lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1 
└─sdb2                 8:18   0  511M  0 part  
  └─md0                9:0    0  510M  0 raid1 
    └─vol_gr1-lvol0  253:2    0  100M  0 lvm   /tmp/new
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1 
└─sdc2                 8:34   0  511M  0 part  
  └─md0                9:0    0  510M  0 raid1 
    └─vol_gr1-lvol0  253:2    0  100M  0 lvm   /tmp/new
```
## 15. Протестируйте целостность файла
```shell
# выполнено
root@vagrant:/# gzip -t /tmp/new/test.gz && echo $?
0
```

## 16. Используя `pvmove`, переместите содержимое PV с RAID0 на RAID1.
```shell
# у нас два PV-устройства, второе указывать необязательно в таком случае:
root@vagrant:/# pvmove /dev/md0
  /dev/md0: Moved: 84.00%
  /dev/md0: Moved: 100.00%
root@vagrant:/# lsblk
NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0   64G  0 disk  
├─sda1                 8:1    0  512M  0 part  /boot/efi
├─sda2                 8:2    0    1K  0 part  
└─sda5                 8:5    0 63.5G  0 part  
  ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]
sdb                    8:16   0  2.5G  0 disk  
├─sdb1                 8:17   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1 
│   └─vol_gr1-lvol0  253:2    0  100M  0 lvm   /tmp/new
└─sdb2                 8:18   0  511M  0 part  
  └─md0                9:0    0  510M  0 raid1 
sdc                    8:32   0  2.5G  0 disk  
├─sdc1                 8:33   0    2G  0 part  
│ └─md1                9:1    0    2G  0 raid1 
│   └─vol_gr1-lvol0  253:2    0  100M  0 lvm   /tmp/new
└─sdc2                 8:34   0  511M  0 part  
  └─md0                9:0    0  510M  0 raid1
```
## 17. Сделайте `--fail` на устройство в вашем RAID1 md.

```shell
root@vagrant:/# mdadm --fail /dev/md1 /dev/sdb1
mdadm: set /dev/sdb1 faulty in /dev/md1
```
*   Видим, что статус `faulty`:
```shell
root@vagrant:/# mdadm -D /dev/md1
/dev/md1:
           Version : 1.2
     Creation Time : Tue Jun 15 19:10:21 2021
        Raid Level : raid1
        Array Size : 2094080 (2045.00 MiB 2144.34 MB)
     Used Dev Size : 2094080 (2045.00 MiB 2144.34 MB)
      Raid Devices : 2
     Total Devices : 2
       Persistence : Superblock is persistent

       Update Time : Tue Jun 15 19:53:02 2021
             State : clean, degraded 
    Active Devices : 1
   Working Devices : 1
    Failed Devices : 1
     Spare Devices : 0

Consistency Policy : resync

              Name : vagrant:1  (local to host vagrant)
              UUID : c53ccdc9:6b3d78b1:b4683d2f:4b757429
            Events : 22

    Number   Major   Minor   RaidDevice State
       -       0        0        0      removed
       1       8       33        1      active sync   /dev/sdc1

       0       8       17        -      faulty   /dev/sdb1

```
## 18. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.

*   Disk failure on sdb1, disabling device:
```shell
root@vagrant:/# dmesg | grep md1
[ 3585.246413] md/raid1:md1: not clean -- starting background reconstruction
[ 3585.246415] md/raid1:md1: active with 2 out of 2 mirrors
[ 3585.246438] md1: detected capacity change from 0 to 2144337920
[ 3585.248606] md: resync of RAID array md1
[ 3595.755458] md: md1: resync done.
[ 5925.200642] md: delaying data-check of md1 until md0 has finished (they share one or more physical units)
[ 5927.836022] md: data-check of RAID array md1
[ 5938.295196] md: md1: data-check done.
[ 6145.529912] md/raid1:md1: Disk failure on sdb1, disabling device.
               md/raid1:md1: Operation continuing on 1 devices.
```

## 19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:
```shell
root@vagrant:/# gzip -t /tmp/new/test.gz && echo $?
0
# по-прежнему доступен
```

## 20. Погасите тестовый хост, `vagrant destroy`.

```shell
$ vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
```