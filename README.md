# Devops-netology exercise
* Recorded ignoring files in git

###1. Игнорирование локальных директорий с названием ".terraform"
`**/.terraform/*`

###2. Игнорирование файлов, оканчивающихся на ".tfstate" или содержащих это название
    `*.tfstate`
    `*.tfstate.*`

###3. Игнорирование файла crash.log
`crash.log`

###4. Игнорирование всех файлов, заканчивающихся на ".tfavs". В .gitignore к таким файлам есть дополнения, что они содержат информацию о паролях, ключах или другую секретную информацию
`*.tfvars`

###5. Игнорирования файлов переопределения, которые называются "ovveride.tf" или "ovveride.tf.json", или заканчиваются на "_ovveride.tf" или "_ovveride.tf.json"
    `override.tf`
    `override.tf.json`
    `*_override.tf`
    `*_override.tf.json`
 
Для включения файлов-override необходимо добавлять их с использованием "отрицаемого" символа "!"
К примеру, включить файл override:  `!example_override.tf`

Пример для игнорирования файлов при использовании команды: `terraform plan -out=tfplan`

    `*tfplan*`

###6. Игнорирование конфигурационных файлов:
    `.terraformrc`
    `terraform.rc`
