recorded ignoring files in git
#### added new line
# Devops-netology exercise

### 1. Игнорирование локальных директорий с названием ".terraform"
`**/.terraform/*`

### 2. Игнорирование файлов, оканчивающихся на ".tfstate" или содержащих это название
 `*.tfstate`
 `*.tfstate.*`

### 3. Игнорирование файла crash.log
`crash.log`

### 4. Игнорирование всех файлов, заканчивающихся на ".tfavs". В ".gitignore" к таким файлам есть дополнения, что они содержат информацию о паролях, ключах или другую секретную информацию
`*.tfvars`

### 5. Игнорирования файлов переопределения, которые называются "ovveride.tf" или "ovveride.tf.json", или заканчиваются на "_ovveride.tf" или "_ovveride.tf.json"
`override.tf`
`override.tf.json`
`*_override.tf`
`*_override.tf.json`
 
Для включения файлов-override необходимо добавлять их с использованием "отрицаемого" символа "!"
К примеру, включить файл override:  `!example_override.tf`

Пример для игнорирования файлов при использовании команды: `terraform plan -out=tfplan`

`*tfplan*`

### 6. Игнорирование конфигурационных файлов:
`.terraformrc`
`terraform.rc`

# Репозитории
 * github: https://github.com/lereklerik/devops-netology
 * gitlab: https://gitlab.com/tulyakova.v.e/devops-netology
 * bitbucket: https://bitbucket.org/lerekler/devops-netology/src/main/

# Домашнее задание к занятию "2.3. Ветвления в Git"
## Network graph in github
 * https://github.com/lereklerik/devops-netology/network
 * скрин терминала: https://ibb.co/XxZwGGw

# Домашнее задание к занятию "2.4. Инструменты Git"
## 1. Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea
### Команда 
```git show aefea```

-----------------------------
```
commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545
Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
Date:   Thu Jun 18 10:29:58 2020 -0400

    Update CHANGELOG.md

diff --git a/CHANGELOG.md b/CHANGELOG.md
index 86d70e3e0..588d807b1 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -27,6 +27,7 @@ BUG FIXES:
 * backend/s3: Prefer AWS shared configuration over EC2 metadata credentials by default ([#25134](https://github.com/hashicorp/terraform/issues/25134))
 * backend/s3: Prefer ECS credentials over EC2 metadata credentials by default ([#25134](https://github.com/hashicorp/terraform/issues/25134))
 * backend/s3: Remove hardcoded AWS Provider messaging ([#25134](https://github.com/hashicorp/terraform/issues/25134))
+* command: Fix bug with global `-v`/`-version`/`--version` flags introduced in 0.13.0beta2 [GH-25277]
 * command/0.13upgrade: Fix `0.13upgrade` usage help text to include options ([#25127](https://github.com/hashicorp/terraform/issues/25127))
 * command/0.13upgrade: Do not add source for builtin provider ([#25215](https://github.com/hashicorp/terraform/issues/25215))
 * command/apply: Fix bug which caused Terraform to silently exit on Windows when using absolute plan path ([#25233](https://github.com/hashicorp/terraform/issues/25233))
```
```хэш aefead2207ef7e2aa5dc81a34aedf0cad4c32545```
## 2. Какому тегу соответствует коммит 85024d3?
### Команда 
```git show 85024d3```

-----------------------------
```
commit 85024d3100126de36331c6982bfaac02cdab9e76 (tag: v0.12.23)
Author: tf-release-bot <terraform@hashicorp.com>
Date:   Thu Mar 5 20:56:10 2020 +0000

    v0.12.23
```
```тег v0.12.23```
## 3. Сколько родителей у коммита b8d720? Напишите их хеши
### 2 родителя
Команда 
``` git show -s --pretty=%P b8d720```

```
56cd7859e05c36c06b56d013b55a252d0bb7e158 9ea88f22fc6269854151c571162c5bcf958bee2b
```
---
P.S. Нашла также команду посложнее, пыталась разобрать. Вывод тот же

Команда 
``` 
git cat-file -p b8d720 | awk 'NR > 1 {if(/^parent/){print $2; next}{exit}}'

-----------------------------
56cd7859e05c36c06b56d013b55a252d0bb7e158
9ea88f22fc6269854151c571162c5bcf958bee2b
```

## 4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24
### Команда 
``` git log --left-right --oneline v0.12.23...v0.12.24 ```

```
> 33ff1c03b (tag: v0.12.24) v0.12.24
> b14b74c49 [Website] vmc provider links
> 3f235065b Update CHANGELOG.md
> 6ae64e247 registry: Fix panic when server is unreachable
> 5c619ca1b website: Remove links to the getting started guide's old location
> 06275647e Update CHANGELOG.md
> d5f9411f5 command: Fix bug when using terraform login on Windows
> 4b6d06cc5 Update CHANGELOG.md
> dd01a3507 Update CHANGELOG.md
> 225466bc3 Cleanup after v0.12.23 release
```
Команда 
``` git log --left-right --oneline v0.12.24...v0.12.23 ``` не выводит ничего
## 5. Найдите коммит в котором была создана функция func providerSource
### Команда 
```git log -S 'func providerSource('```

```-----------------------------
commit 8c928e83589d90a031f811fae52a81be7153e82f
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Thu Apr 2 18:04:39 2020 -0700

    main: Consult local directories as potential mirrors of providers
```
Выполнив команду ```git log -p 8c928e83589d90a031f811fae52a81be7153e82f```
найдем название файла (```provider_source.go```), в который добавили функцию:
```
diff --git a/provider_source.go b/provider_source.go
new file mode 100644
index 000000000..9524e0985
--- /dev/null
+++ b/provider_source.go
@@ -0,0 +1,89 @@
```
commit 8c928e83589d90a031f811fae52a81be7153e82f
## 6. Найдите все коммиты в которых была изменена функция globalPluginDirs
### Команда 
```git log -S "func globalPluginDirs()" --oneline```

```-----------------------------
8364383c3 Push plugin discovery down into command package
```
Изначально пыталась найти изменения следующим образом:
```git grep globalPluginDirs```
```
-----------------------------
commands.go:            GlobalPluginDirs: globalPluginDirs(),
commands.go:    helperPlugins := pluginDiscovery.FindPlugins("credentials", globalPluginDirs())
internal/command/cliconfig/config_unix.go:              // FIXME: homeDir gets called from globalPluginDirs during init, before
plugins.go:// globalPluginDirs returns directories that should be searched for
plugins.go:func globalPluginDirs() []string {
```
Затем уточнила запрос:
```git grep -p "globalPluginDirs()" *.go```

```
commands.go=func initCommands(
commands.go:            GlobalPluginDirs: globalPluginDirs(),
commands.go=func credentialsSource(config *cliconfig.Config) (auth.CredentialsSource, error) {
commands.go:    helperPlugins := pluginDiscovery.FindPlugins("credentials", globalPluginDirs())
plugins.go=import (
plugins.go:func globalPluginDirs() []string {
```
Но это не возвращает хэши коммитов.

Искала даже так:
```git log --oneline $(grep -p "func globalPluginDirs(")```

или так:
```git grep "globalPluginDirs()" $(git rev-list --all)```

но возвращает невалидный результат

## 7.Кто автор функции synchronizedWriters?
### Файл в репозитории не найден, значит был удален.
Сначала смотрю историю по работе с файлом с grep:

```git grep -p synchronizedWriters $(git rev-list --all)```

```
c1f2a48829b7d4d341e095d522d21db1c57ef551:synchronized_writers.go=type synchronizedWriter struct {
c1f2a48829b7d4d341e095d522d21db1c57ef551:synchronized_writers.go:// synchronizedWriters takes a set of writers and returns wrappers that ensure
c1f2a48829b7d4d341e095d522d21db1c57ef551:synchronized_writers.go:func synchronizedWriters(targets ...io.Writer) []io.Writer {
2b5effc739b04db8aef4c2d907c2a554215146a8:main.go=func copyOutput(r io.Reader, doneCh chan<- struct{}) {
2b5effc739b04db8aef4c2d907c2a554215146a8:main.go:               wrapped := synchronizedWriters(stdout, stderr)
```

Понимаем, что в ```synchronized_writers.go``` описана функция, а в ```main.go``` она вызывается.
Значит будем искать историю по  ```synchronized_writers.go ```

Команда ```git log --full-history --oneline -- synchronized_writers.go```

```-----------------------------
1338502c7 Merge pull request #26924 from remilapeyre/concurrent-locks-pg
85b9bdea9 backend/azure: azure state refreshes outside of grabbing the lock #26561
cb041053e Merge with master
7e11b9792 Merge remote-tracking branch 'origin/master' into validate-ignore-empty-provider
dcf0dba6f Merge pull request #27081 from hashicorp/jbardin/staticcheck
bdfea50cc remove unused
bcc5dffea provider/terraform: import terraform provider back into core
527b7af79 Merge pull request #14956 from fatmcgav/openstack_sort_headers
ac105b5b1 Merge branch 'master' of github.com:UKCloud/terraform
aae44290c merge master
8aac6c29a Merge pull request #2 from hashicorp/master
9d79fdd78 Merge branch 'master' into master
73dbded87 Merge pull request #13585 from augabet/bump_govcloudair
30c3e72dd Merge pull request #14540 from BWITS/aws_appautoscaling_policy
51b1c7b08 Merge pull request #14089 from hashicorp/b-aws-waf-rule
7b05d7f05 Merge pull request #12414 from jmcarp/govcloud-cloudwatchlogs-tags
a59e1183d Merge pull request #14210 from fatmcgav/provider_openstack_fix_floatingip_association_deletion
081e72f9f Merge pull request #14185 from hashicorp/liz/tfe-variables
827a541b0 Removing contributor comment from CHANGELOG as it was in the wrong section
50f8b9407 Merge branch 'master' into cloud_router
5ac311e2a main: synchronize writes to VT100-faker on Windows
```


```5ac311e2a``` - первый хэш коммита с искомой функций.
Посмотрим вывод по файлу в коммите командой
```git show 5ac311e2a -- synchronized_writers.go```

```
commit 5ac311e2a91e381e2f52234668b49ba670aa0fe5
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Wed May 3 16:25:41 2017 -0700

    main: synchronize writes to VT100-faker on Windows
{...}
diff --git a/synchronized_writers.go b/synchronized_writers.go
new file mode 100644
index 000000000..2533d1316
--- /dev/null
+++ b/synchronized_writers.go
@@ -0,0 +1,31 @@
+package main
+
+import (
+       "io"
+       "sync"
+)
+
+type synchronizedWriter struct {
+       io.Writer
+       mutex *sync.Mutex
+}
+
+// synchronizedWriters takes a set of writers and returns wrappers that ensure
+// that only one write can be outstanding at a time across the whole set.
+func synchronizedWriters(targets ...io.Writer) []io.Writer {
+       mutex := &sync.Mutex{}
+       ret := make([]io.Writer, len(targets))
+       for i, target := range targets {
+               ret[i] = &synchronizedWriter{
+                       Writer: target,
+                       mutex:  mutex,
+               }
+       }
+       return ret
+}
+
+func (w *synchronizedWriter) Write(p []byte) (int, error) {
+       w.mutex.Lock()
+       defer w.mutex.Unlock()
+       return w.Writer.Write(p)
+}
```

Автором функции, таким образом, является ```Martin Atkins <mart@degeneration.co.uk>```


# Домашнее задание к занятию "3.1 Работа в терминале (лекция 1)"

## Какие ресурсы выделены по-умолчанию?

* Оперативная память: 1024 MB
* 1 CPU
* 64 GB HDD

## Как добавить оперативной памяти или ресурсов процессора виртуальной машине?

`config.vm.provider "virtualbox" do |v|
  v.memory = 1024
  v.cpus = 2
end`

## Какой переменной можно задать длину журнала history, и на какой строчке manual это описывается?
* HISTFILESIZE
* Строка 2083: *2083:       specified by the value of HISTFILESIZE.  If HISTFILESIZE is unset, or set to null, a non-numeric value, or a numeric value less than zero, the history file is not truncated.*

## Что делает директива ignoreboth в bash?

* A value of `ignoreboth` is shorthand for `ignorespace` and `ignoredups` . `ignoreboth `- сокращение от команд `ignorespace` и `ignoredups`.
* `ignoredups`  causes lines matching the previous history entry to not be saved - директива позволяет не сохранять строки, соответствующие предыдущей записи в истории
* If the list of values includes `ignorespace`, lines which begin with a space character are not saved in the history list - директива позволяет не сохранять строки в истории, начинающиеся с символа пробела

## В каких сценариях использования применимы скобки {} и на какой строчке man bash это описано?

Строка `135`:       `! case  coproc  do done elif else esac fi for function if in select then until while { } time [[ ]]`

## Основываясь на предыдущем вопросе, как создать однократным вызовом touch 100000 файлов? А получилось ли создать 300000?

*   Команда `touch file{n..m}` позволяет создать заданное количество файлов, автоматически генерируя их имена.
*   При выполнении команды `touch file{0..99999}` терминал выдает ошибку:

` touch filetest{0..99999}
bash: /usr/bin/touch: Слишком длинный список аргументов`
* Аналогичное поведение при изменении конечного числа на 299999.
* Число аргументов команды `touch` ограничено только максимальным количеством символов в командной строке

## Что делает конструкция `[[ -d /tmp ]]` ?

    Условные выражения используются составной командой [[ и
    командой test и [, встроенными командами для проверки атрибутов файлов,
    выполнения строковыех и арифметических сравнений. Test и [
    команды определяют свое поведение в зависимости от количества
    аргументов; 

     -d file
              Проверяет, существует ли файл file или он является каталогом.
    
    В данном случае проверяет, является ли каталогом /tmp

## Добейтесь в выводе type -a bash

*   Скрин экрана: <https://ibb.co/Ss05BSW>

## Чем отличается планирование команд с помощью batch и at?
Программа `at` является частью набора, состоящего из четырех программ: `at, batch, atq и atrm`:

    at выполняет задачи в назначенное время.
    atq выводит список ожидающих выполнения задач для каждого пользователя; в случае использования суперпользователем, выводятся все ожидающие выполнения задачи.
    atrm удаляет задачи, заданные идентификаторами.
    batch выполняет задачи во время периодов низкой загруженности системы

# Домашнее задание к занятию "3.2. Работа в терминале, лекция 2"
## Какого типа команда cd? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа.

*   Команда `cd` - одна из основных команд навигации; Она позволяет сменить текущую директорию на домашнюю, или на указанную директорию:
`cd <dir>`
`cd <path/dir>`
    
*   Команда меняет директорию ((C)hange (D)irectory), не вмешиваясь в процессы управления файлами. 
*   `cd` является встроенной командой оболочки (bash), и не является, строго говоря, утилитой. Т.е. она меняет текущую папку только для оболочки.
*   Если бы команда `cd` была встроенной утилитой, выполняя передвижения по каталогам, затрагивающие процессы управления файлами системы, то её можно было бы отнести к другому типу команд

## Какая альтернатива без pipe команде grep <some_string> <some_file> | wc -l? 

*   `grep -c <some_string> <some_file>`

## Какой процесс с PID 1 является родителем для всех процессов в вашей виртуальной машине Ubuntu 20.04?

* systemd

## Как будет выглядеть команда, которая перенаправит вывод stderr ls на другую сессию терминала?

*   `ls 2> /dev/pts/X`, где X - другая сессия терминала

## Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример

*   `command < filename > newFileName`, если известно имя файла, которому передаем результат работы команды
*   `command < filename >> newFileName`, создаст новый файл, которому передаем результат работы команды

## Получится ли вывести находясь в графическом режиме данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?
*   Выполнив команду в графическом режиме `echo "Hello, world!" > /dev/ttyX` мы сможем наблюдать результат её выполнения в эмуляторе TTY только если в TTY был выполнен login; Порядок действий:
    *   Вызываем эмулятор TTY Ctrl + Alt + F1..6
    *   Логинимся
    *   Выходим из терминала Ctrl + Alt + F7 (у меня так)
    *   Вводим команду, указанную выше, в PTY (`echo "Hello, world!" > /dev/tty1` в моем случае)
    *   Открываем раннее запущенный эмулятор TTY, наблюдаем `Hello, world!`
*   Если логин не был произведен в эмуляторе TTY, то в PTY будет ошибка:

`$ echo "!" > /dev/tty1
bash: /dev/tty1: Отказано в доступе`

## Выполните команду bash 5>&1. К чему она приведет? Что будет, если вы выполните echo netology > /proc/$$/fd/5? Почему так происходит?

*   `bash 5>&1` - Перенаправляется bash с дескриптором 5 в 1, т.е. вывод в файл с дескриптором 5 передается в файл с дескриптором 1.
*   `echo netology > /proc/$$/fd/5` возвращает нам следующее:
`vagrant@vagrant:~$ echo netology > /proc/$$/fd/5
netology
`
    
*   т.к. вывод дескриптора 5 мы направили в bash с дескриптором 1, результат выводится через bash, 
    в который по умолчанию выводится результат выполнения команд, если не указано иное


## Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? 
#### Напоминаем: по умолчанию через pipe передается только stdout команды слева от | на stdin команды справа. Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе.

*   Учитывая, что в предыдущем задании мы добавили 5-й промежуточный файловый дескриптор, его и используем:

`vagrant@vagrant:~$ echo "stdout" 2>&1 1>&5 | echo "stderr" 5>&1
stderr
stdout
`

## Что выведет команда `cat /proc/$$/environ` ? Как еще можно получить аналогичный по содержанию вывод?

*   `cat /proc/$$/environ` выводит сплошным абзацем набор переменных окружения
*   `env` также выводит переменные окружения, только построчно

## Используя man, опишите что доступно по адресам /proc/<PID>/cmdline, /proc/<PID>/exe.

*   ` /proc/[pid]/cmdline` - Это доступный только для чтения файл содержит полную командную строку для процесса, `pid` которого мы передаем
    если только процесс не является зомби. В последнем случае в этом файле ничего нет: то есть чтение этого файла вернет 0 символов. 
    Аргументы командной строки появляются в этом файле как набор строк, разделенных нулевыми байтами ('\ 0'), 
    с последующим нулевым байтом после последней строки.
    
*   `proc/<PID>/exe` - *В Linux 2.2* и более поздних версиях этот файл представляет собой символическую ссылку, 
    содержащую фактический путь к исполняемой команде. 
    Эту символическую ссылку можно разыменовать обычным образом; 
    Можно ввести `/ proc / [pid] / exe`, чтобы запустить еще одну копию того же исполняемого файла, который запускается процессом [pid]. 
    Если имя пути было отключено, символическая ссылка будет содержать строку «(удалено)», добавленную к исходному имени пути. 
    В многопоточном процессе содержимое этой символической ссылки недоступно, если основной поток уже завершен (обычно путем вызова pthread_exit (3)). 
    *В Linux 2.0* и более ранних версиях `/ proc / [pid] / exe ` является указателем на исполняемый двоичный файл 
    и отображается как символическая ссылка. Вызов readlink (2) для этого файла в Linux 2.0 возвращает строку в формате:
    `[устройство]: индексный дескриптор`
    
## Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью /proc/cpuinfo

*   `grep "sse" /proc/cpuinfo` - из общего списка находим, что старшая версия (самая ранняя) - `sse`, а самая последняя поддерживаемая - `sse4_2`

`flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good nopl nonstop_tsc cpuid extd_apicid aperfmperf pni pclmulqdq monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw skinit wdt tce topoext perfctr_core perfctr_nb bpext perfctr_llc mwaitx cpb hw_pstate sme ssbd sev ibpb vmmcall fsgsbase bmi1 avx2 smep bmi2 rdseed adx smap clflushopt sha_ni xsaveopt xsavec xgetbv1 xsaves clzero irperf xsaveerptr arat npt lbrv svm_lock nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold avic v_vmsave_vmload vgif overflow_recov succor smca`

## При открытии нового окна терминала и vagrant ssh создается новая сессия и выделяется pty. Это можно подтвердить командой tty, которая упоминалась в лекции 3.2. Однако:

`vagrant@netology1:~$ ssh localhost 'tty'
not a tty`

## Почитайте, почему так происходит, и как изменить поведение.

*   Оболочка, используемая Vagrant по умолчанию `config.ssh.shell (string)` вызывается с флагом `bash -l`
*   bash вызывается как интерактивная оболочка входа с флагом `-l` авторизации, 
    т.е. сначала читает и выполняет команды из файла `/ etc / profile`, если этот файл существует
    
*   После прочтения этого файла он ищет`~ / .bash_profile, ~ / .bash_login`, затем `~ / .profile`, 
    и выполняет команды из первого, доступного для чтения.
    
*   Поскольку Vagrant работает под root'ом, то таковым файлом будет `/root/.profile`
*   В Ubuntu `/root/.profile` содержит команду `mesg n`, которая запрещает доступ на запись к терминалу:
    *   `mesg` — UNIX-утилита, управляет доступом на запись для терминала данного пользователя. 
    *   Обычно используется для разрешения или запрета другим пользователям писать на терминал данного пользователя.
    *   Может запускать с параметрами:
    -   `y` - Разрешить другим пользователям доступ на запись к вашему терминалу.
    -   `n` - Запретить доступ на запись к вашему терминалу.
    
*Если не заботиться о безопасности использования Vagrant, то можно просто удалить `mesg n` из командной строки `.profile`. 
Однако, более правильным решением будет изменить запуск оболочки в `config.ssh.shell (string)`. Пример найденной конфигурации:*

`config.ssh.shell = "bash -c 'BASH_ENV=/etc/profile exec bash'"`

## Узнайте что делает команда tee и почему в отличие от sudo echo команда с sudo tee будет работать.

*   `tee` - выводит stdout программы и записывает его в файл
*   `echo` - команда, предназначенная для отображения строки текста. 
    Команда echo выводит текст (выводит текст на стандартное устройство вывода)
    
В примере `sudo echo string > /root/new_file` sudo не выполняет перенаправление вывода, поэтому возникает ошибка ограничения прав
В примере `echo string | sudo tee /root/new_file` команда `tee` получит вывод команды `echo`, повысит права на `sudo` и запишет данные в файл.