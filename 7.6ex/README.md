# Домашнее задание к занятию "7.6. Написание собственных провайдеров для Terraform."

## Задание 1 

### Найдите, где перечислены все доступные resource и data_source, приложите ссылку на эти строки в коде на гитхабе.

1. [Datasource](https://github.com/hashicorp/terraform-provider-aws/blob/6076d5a60ec814b243bc45170d67cb268a39d927/internal/provider/provider.go#L338)
2. [Resource](https://github.com/hashicorp/terraform-provider-aws/blob/6076d5a60ec814b243bc45170d67cb268a39d927/internal/provider/provider.go#L709)


### Для создания очереди сообщений SQS используется ресурс `aws_sqs_queue` у которого есть параметр `name`.
##### С каким другим параметром конфликтует name? Приложите строчку кода, в которой это указано.

----------------------------------------------------
* name_prefix [queue.go](https://github.com/hashicorp/terraform-provider-aws/blob/6076d5a60ec814b243bc45170d67cb268a39d927/internal/service/sqs/queue.go#L97)

##### Какая максимальная длина имени?

* На сайте это можно увидеть в виде предупреждения: [name_restrict](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sqs_queue#name)
* Исходя из этого, стала искать и по репозиторию. Однако, в ветке `main` это было сделать проблематично, нашла в `master`: [validators.go](https://github.com/hashicorp/terraform-provider-aws/blob/b8b7fee0e5cf4b469d8d4d2a2dc01ed13654a03a/aws/validators.go#L1035)
* 

----------------------------------------------------
##### Какому регулярному выражению должно подчиняться имя?

----------------------------------------------------
* В ветке `main`:
  * [resourceQueueCustomizeDiff](https://github.com/hashicorp/terraform-provider-aws/blob/6076d5a60ec814b243bc45170d67cb268a39d927/internal/service/sqs/queue.go#L413)
  * `^[a-zA-Z0-9_-]{1,80}$`
  * Здесь учтена сразу длина наименования. 
  * Имена очередей должны состоять только из прописных и строчных букв, цифр, знаков подчеркивания и дефисов, и должны иметь длину от 1 до 80 символов.
* В ветке `master`:
  * [validators.go](https://github.com/hashicorp/terraform-provider-aws/blob/b8b7fee0e5cf4b469d8d4d2a2dc01ed13654a03a/aws/validators.go#L1041)
  * `^[0-9A-Za-z-_]+(\.fifo)?$`
  * Имена очередей должны состоять только из прописных и строчных букв, цифр, знаков подчеркивания и дефисов. Для очереди FIFO (first-in-first-out) имя должно заканчиваться суффиксом `.fifo`.