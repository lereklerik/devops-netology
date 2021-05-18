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
