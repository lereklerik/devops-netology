# Домашнее задание к занятию "3.9. Элементы безопасности информационных систем"

## 1. Установите Hashicorp Vault в виртуальной машине Vagrant/VirtualBox. 

*   Настройка `vault`:
```shell
vagrant@vagrant:~$ export VAULT_ADDR='http://0.0.0.0:8200'
vagrant@vagrant:~$ echo "+VyM1V32HXEwZI/LqQu6m6TNmZCrnQq604rYuv/9/FA=" > unseal.key
vagrant@vagrant:~$ export VAULT_DEV_ROOT_TOKEN_ID=s.zhUkRAh7VdwEDl2n9hl5EGFR
vagrant@vagrant:~$ vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.7.3
Storage Type    inmem
Cluster Name    vault-cluster-542d0cb6
Cluster ID      d4d692b4-7e8c-c604-cfb3-2f931a4bf099
HA Enabled      false
```
## 2. Запустить Vault-сервер в dev-режиме (дополнив ключ -dev упомянутым выше -dev-listen-address, если хотите увидеть UI).

*   Работа из браузера:
    *   [screenshot1](../../pictures/vault_starting.png)
    *   [screenshot2](../../pictures/vault_starting2.png)
 
---------------------------------------------------------
### *Однако с 0.0.0.0:8200 у меня не подписывался промежуточный сертификат. Поэтому от UI было принято решение отказаться*

---------------------------------------------------------
```shell
# Новый запуск без участия UI
vagrant@vagrant:~$ vault server -dev
==> Vault server configuration:

             Api Address: http://127.0.0.1:8200
                     Cgo: disabled
         Cluster Address: https://127.0.0.1:8201
              Go Version: go1.15.13
              Listener 1: tcp (addr: "127.0.0.1:8200", cluster address: "127.0.0.1:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level: info
                   Mlock: supported: true, enabled: false
           Recovery Mode: false
                 Storage: inmem
                 Version: Vault v1.7.3
             Version Sha: 5d517c864c8f10385bf65627891bc7ef55f5e827

-----
WARNING! dev mode is enabled! In this mode, Vault runs entirely in-memory
and starts unsealed with a single unseal key. The root token is already
authenticated to the CLI, so you can immediately begin using Vault.

You may need to set the following environment variable:

    $ export VAULT_ADDR='http://127.0.0.1:8200'

The unseal key and root token are displayed below in case you want to
seal/unseal the Vault or re-authenticate.

Unseal Key: +H7rCaU8QBQZZ6SwoNLcGPAXTnwOxQs/OBBwAHG66Yo=
Root Token: s.ST2sz0jAvxdyzqVQ1Efa6mvs

Development mode should NOT be used in production installations!
```

```shell
# Настраиваем переменные, проверяем статус сервера
vagrant@vagrant:~$ export VAULT_ADDR='http://127.0.0.1:8200'
vagrant@vagrant:~$ echo "+H7rCaU8QBQZZ6SwoNLcGPAXTnwOxQs/OBBwAHG66Yo=" > unseal.key
vagrant@vagrant:~$ export VAULT_DEV_ROOT_TOKEN_ID=s.ST2sz0jAvxdyzqVQ1Efa6mvs
vagrant@vagrant:~$ vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.7.3
Storage Type    inmem
Cluster Name    vault-cluster-8ae1cb4f
Cluster ID      dea006eb-2fba-5617-c618-bda73464b752
HA Enabled      false

```

## 3. Используя PKI Secrets Engine, создайте Root CA и Intermediate CA. Обратите внимание на дополнительные материалы по созданию CA в Vault, если с изначальной инструкцией возникнут сложности.
*   Создадим корневой сертификат
```shell
vagrant@vagrant:~$ vault secrets enable pki
Success! Enabled the pki secrets engine at: pki/
vagrant@vagrant:~$ vault secrets tune -max-lease-ttl=87600h pki
Success! Tuned the secrets engine at: pki/
vagrant@vagrant:~$ vault write -field=certificate pki/root/generate/internal \
>         common_name="example.com" \
>         ttl=87600h > CA_cert.crt
vagrant@vagrant:~$ vault write pki/config/urls \
>         issuing_certificates="$VAULT_ADDR/v1/pki/ca" \
>         crl_distribution_points="$VAULT_ADDR/v1/pki/crl"
Success! Data written to: pki/config/urls

vagrant@vagrant:~$ vault write pki/roles/example-dot-com \
>     allowed_domains=my-website.com \
>     allow_subdomains=true \
>     max_ttl=72h
Success! Data written to: pki/roles/example-dot-com
vagrant@vagrant:~$ vault write pki/issue/example-dot-com \
>     common_name=www.my-website.com
Key                 Value
---                 -----
certificate         -----BEGIN CERTIFICATE-----
MIIDxDCCAqygAwIBAgIUQzsJxqMV9JRBLyfgspBQhhKjhQ4wDQYJKoZIhvcNAQEL
CS1HN+ib+ZE=
-----END CERTIFICATE-----
expiration          1626521626
issuing_ca          -----BEGIN CERTIFICATE-----
MIIDNTCCAh2gAwIBAgIUZPQaRakae7ESMTHCzAFZvK4W+B8wDQYJKoZIhvcNAQE
5WAfQOWn1zcg
-----END CERTIFICATE-----
private_key         -----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA8//ETW/lflaY6RcMFy8MxUFrjoZMek5VJ/9/4aQaZZq6yDWm
kANIWTKndC0a/QO/Ow7BHf27vONaPA/AOubmILdXsXCtOPbzH97tQQM=
-----END RSA PRIVATE KEY-----
private_key_type    rsa
serial_number       43:3b:09:c6:a3:15:f4:94:41:2f:27:e0:b2:90:50:86:12:a3:85:0e
```

*   Создадим промежуточный сертификат
```shell
vagrant@vagrant:~$ vault secrets enable -path=pki_interm pki
Success! Enabled the pki secrets engine at: pki_interm/
vagrant@vagrant:~$ vault secrets tune -max-lease-ttl=43800h pki_interm
Success! Tuned the secrets engine at: pki_interm/
## запрос на сертификат
vagrant@vagrant:~$ vault write -format=json pki_interm/intermediate/generate/internal common_name="example.com Intermediate Authority" | jq -r '.data.csr' > pki_intermediate.csr

vagrant@vagrant:~$ vault write pki/root/sign-intermediate csr=@pki_intermediate.csr format=pem_bundle ttl=43800h
Key              Value
---              -----
certificate      -----BEGIN CERTIFICATE-----
MIIDpjCCAo6gAwIBAgIUL693u60vzfgK9iD441VEKSJTmdQwDQYJKoZIhvcNAQEL
-----END CERTIFICATE-----
expiration       1783945385
issuing_ca       -----BEGIN CERTIFICATE-----
MIIDNTCCAh2gAwIBAgIUZPQaRakae7ESMTHCzAFZvK4W+B8wDQYJKoZIhvcNAQEL
MEOg8qaNscmY8KaCLkcvOdy4bRhtUtz65T7/FExR8XysvXmi/w0yVTt+v/i8228C
5WAfQOWn1zcg
-----END CERTIFICATE-----
serial_number    2f:af:77:bb:ad:2f:cd:f8:0a:f6:20:f8:e3:55:44:29:22:53:99:d4

## Пропишем промежуточный сертификат
vagrant@vagrant:~$ vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr format=pem_bundle ttl="43800h" | jq -r '.data.certificate' > intermediate.cert.pem
vagrant@vagrant:~$ vault write pki_interm/intermediate/set-signed certificate=@intermediate.cert.pem
Success! Data written to: pki_interm/intermediate/set-signed

## Создадим роль для выдачи сертификатов
vagrant@vagrant:~$ vault write pki_interm/roles/example-dot-com allowed_domains="example.com" allow_subdomains=true max_ttl="720h"
Success! Data written to: pki_interm/roles/example-dot-com
## Запросим сертификаты
vagrant@vagrant:~$ vault write pki_interm/issue/example-dot-com common_name="test.example.com" ttl="24h"
Key                 Value
---                 -----
ca_chain            [-----BEGIN CERTIFICATE-----
MIIDpjCCAo6gAwIBAgIUV1jR2xDL18+zAGQfiIospz0bEXEwDQYJKoZIhvcNAQEL
JPAeLn+Ho3hITJQFYEDF7xDt4gxAtQZZkN5NUfR+YW+bBnbCyiMv72PfNpSNR/yD
wuF2/WN9kICwqdcYIQTmML87asP26/Nmwdo=
-----END CERTIFICATE-----]
certificate         -----BEGIN CERTIFICATE-----
MIIDZjCCAk6gAwIBAgIUSCkge42YRf1DsXFPMfJ2n4y8H9owDQYJKoZIhvcNAQEL
GMMc/qHscGYZEiW7l1ZrpMwLiSFlMbenf26i+USzk7iDhOqGadQtMfozNM5qrKBd
sr0FD+syqSjxvQ==
-----END CERTIFICATE-----
expiration          1626352128
issuing_ca          -----BEGIN CERTIFICATE-----
MIIDpjCCAo6gAwIBAgIUV1jR2xDL18+zAGQfiIospz0bEXEwDQYJKoZIhvcNAQEL
JPAeLn+Ho3hITJQFYEDF7xDt4gxAtQZZkN5NUfR+YW+bBnbCyiMv72PfNpSNR/yD
wuF2/WN9kICwqdcYIQTmML87asP26/Nmwdo=
-----END CERTIFICATE-----
private_key         -----BEGIN RSA PRIVATE KEY-----
MIIEpgIBAAKCAQEAtCrN06NTeOQVxap1We0QPsAtGjRm25CGYuSRZlbgH6v62px/
Xt+jVENzhaOULR4ziznA2DbKbRIRRUkANz+pq37rN20hEaBAxU3SOXSN2hiGHK5e
BYKDKTZ7H7B8flu5VHTCyc+lioEQYf6w2KYnVTdqYKeL7c/DvGCaBwu3
-----END RSA PRIVATE KEY-----
private_key_type    rsa
serial_number       48:29:20:7b:8d:98:45:fd:43:b1:71:4f:31:f2:76:9f:8c:bc:1f:da
```


## 4. Согласно этой же инструкции, подпишите Intermediate CA csr на сертификат для тестового домена (например, netology.example.com если действовали согласно инструкции).

*   Создадим центры сертификации:
```shell
vagrant@vagrant:~$ vault secrets enable -path=pki_netology pki
Success! Enabled the pki secrets engine at: pki_netology/
vagrant@vagrant:~$ vault secrets tune -max-lease-ttl=8760h pki_netology
Success! Tuned the secrets engine at: pki_netology/
vagrant@vagrant:~$ vault secrets enable -path=pki_intermediate pki
Success! Enabled the pki secrets engine at: pki_intermediate/
vagrant@vagrant:~$ vault secrets tune -max-lease-ttl=43800h pki_intermediate
Success! Tuned the secrets engine at: pki_intermediate/
```
*   Сгенерируем СА:
```shell
vagrant@vagrant:~$ vault write pki_netology/root/generate/internal common_name="Root Authority localhost" ttl="8760h" > CA_cert.crt
```
*   Создадим роль для корневого центра:
```shell
vagrant@vagrant:~$ vault write pki_netology/roles/devops-dot-un allowed_domains="example.com" allow_subdomains=true max_ttl="72h"
Success! Data written to: pki_netology/roles/devops-dot-un
```
*   Запросим сертификат:
```shell
vagrant@vagrant:~$ vault write pki_netology/issue/devops-dot-un common_name="netology.example.com"
Key                 Value
---                 -----
certificate         -----BEGIN CERTIFICATE-----
MIIDZDCCAkygAwIBAgIUMvT15rhAKZ1cK6lTEwzQyQAQTFQwDQYJKoZIhvcNAQEL
-----END CERTIFICATE-----
expiration          1626590091
issuing_ca          -----BEGIN CERTIFICATE-----
MIIDNzCCAh+gAwIBAgIUYUPn/3P2DUarDFxo5RFm2TyWO7gwDQYJKoZIhvcNAQEL
CWAkgd0/xxr6xmQ=
-----END CERTIFICATE-----
private_key         -----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAlgNzVWvdVaSkGLORESHVZ0TA8aLJ6sx23lKVCo4zIojyRouP
0ssTwiSOqV+Fi9WMQ3Z+37oudbMIaq+nKDVqfMu+uUp2YU0dBy1tWg==
-----END RSA PRIVATE KEY-----
private_key_type    rsa
serial_number       32:f4:f5:e6:b8:40:29:9d:5c:2b:a9:53:13:0c:d0:c9:00:10:4c:54
```
*   Создадим роль для промежуточного центра
```shell
vagrant@vagrant:~$ vault write pki_intermediate/roles/devops-dot-un allowed_domains="example.com" allow_subdomains=true max_ttl="720h"
Success! Data written to: pki_intermediate/roles/devops-dot-un
```
*   CRL:
```shell
vagrant@vagrant:~$ vault write pki_netology/config/urls issuing_certificates="http://localhost:8200/v1/pki/ca" crl_distribution_points="http://localhost:8200/v1/pki/crl"
Success! Data written to: pki_netology/config/urls
```
*   Сгенерируем запрос на промежуточный сертификат:
```shell
vagrant@vagrant:~$ vault write -format=json pki_intermediate/intermediate/generate/internal common_name="Intermediate Authority localhost" county="RU" organization="localOffice" | jq -r '.data.csr' > pki_intermediate.csr
```

*   Подпишем промежуточный сертификат корневым:
```shell
vagrant@vagrant:~$ vault write -format=json pki_netology/root/sign-intermediate csr=@pki_intermediate.csr format=pem_bundle ttl="43800h" | jq -r '.data.certificate' > intermediate.cert.pem
```
*   Добавим в `vault`:
```shell
vagrant@vagrant:~$ vault write pki_intermediate/intermediate/set-signed certificate=@intermediate.cert.pem
Success! Data written to: pki_intermediate/intermediate/set-signed
``` 
*   Сформируем цепочку + закрытый ключ:
```shell
vagrant@vagrant:~$ vault write pki_intermediate/issue/devops-dot-un common_name="netology.example.com" county="RU" organization="localOffice" ttl="24h"
Key                 Value
---                 -----
ca_chain            [-----BEGIN CERTIFICATE-----
MIIDsTCCApmgAwIBAgIUK2+hhiq3TWxmAFA6vJO0wTQe8R8wDQYJKoZIhvcNAQEL
woIpSO6HxwcOukRTinYFQariDpM3wcLGMZxYuplD6VDIc1Dy8Q==
-----END CERTIFICATE-----]
certificate         -----BEGIN CERTIFICATE-----
MIIDbDCCAlSgAwIBAgIUfrfCc7qKLGSH5ddTiMt5XDoz05owDQYJKoZIhvcNAQEL
+4xYdqTHHKmVjhc/umc60g==
-----END CERTIFICATE-----
expiration          1626417433
issuing_ca          -----BEGIN CERTIFICATE-----
MIIDsTCCApmgAwIBAgIUK2+hhiq3TWxmAFA6vJO0wTQe8R8wDQYJKoZIhvcNAQEL
woIpSO6HxwcOukRTinYFQariDpM3wcLGMZxYuplD6VDIc1Dy8Q==
-----END CERTIFICATE-----
private_key         -----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAmO2jOMYsm0CGbEquoT/pY+cQQRXHfU2qamXtFJUJUYXpIY3G
TOuI4w1l2KHR7JnVZ288v3sDXzd+cRbiWycCmlLJuw1ehnB3ZnV8
-----END RSA PRIVATE KEY-----
private_key_type    rsa
serial_number       7e:b7:c2:73:ba:8a:2c:64:87:e5:d7:53:88:cb:79:5c:3a:33:d3:9a
```

## 5. Поднимите на localhost nginx, сконфигурируйте default vhost для использования подписанного Vault Intermediate CA сертификата и выбранного вами домена. Сертификат из Vault подложить в nginx руками.

*   Создала каталог и два файла, скопировав результат подписи сертификата:
    *   Первый `chain.pem` - цепочка сертификатов, включающая корневой + промежуточный сертификаты
    
```shell
vagrant@vagrant:~$ cat chain.pem
-----BEGIN CERTIFICATE-----
MIIDbDCCAlSgAwIBAgIUfrfCc7qKLGSH5ddTiMt5XDoz05owDQYJKoZIhvcNAQEL
BQAwKzEpMCcGA1UEAxMgSW50ZXJtZWRpYXRlIEF1dGhvcml0eSBsb2NhbGhvc3Qw
HhcNMjEwNzE1MDYzNjQ0WhcNMjEwNzE2MDYzNzEzWjAfMR0wGwYDVQQDExRuZXRv
bG9neS5leGFtcGxlLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
AJjtozjGLJtAhmxKrqE/6WPnEEEVx31Nqmpl7RSVCVGF6SGNxn0Lyl19X8LpciiI
DRFoioluhdXlO5vtMko+CEYDnNNnfoJksPV/fnbZYQ4WUsuNtCItPp1E19swHtQn
rrZcqfVzy+U3cdQFN9gdZgOdXxkBQdELw+acHQrqxXu0DmuY9CvRpj1unnSLU/PF
Zlc3o9SC9hAxrxJ/7wGLNzPJIXl6k6lDv1Qc2w1755adSzJzPKQgMhAofszeAbJI
R+QK6CcEM4ogPp4DLyOIBC5OVcrP9MRgSpfTmy/5mjNYFNJVpiENw4FhMi4c6pRc
aSuFXf9I4cGbA1W5wPrANWkCAwEAAaOBkzCBkDAOBgNVHQ8BAf8EBAMCA6gwHQYD
VR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMB0GA1UdDgQWBBRDbFMiS7D9QwbK
FD275EItTjriKDAfBgNVHSMEGDAWgBQ8Xkyivd3TZhFKVmcRE3Mtvn1d3zAfBgNV
HREEGDAWghRuZXRvbG9neS5leGFtcGxlLmNvbTANBgkqhkiG9w0BAQsFAAOCAQEA
PdztySeknrcjpK3Q9GwTygUu2AJSyLJY57pT6nw5Ksz9yBjtaR2l34UtLujsC3Pv
bbholtsLrSTXtbR6pEblrlhDK0UeQTFx3aQam6pgAKLPfoU/VDuNAuedwKufc+u7
Qpqk1KdMPDjC4b0bLBwuSKYRNqhi6yuKEpn6pRKEvi8MvVATYITNMyMg0fhd61ox
4BO7poSzqBN1tTB5m6FkwNietIPm2YPy2Fq1nxfVrwoPTGvd4c6R55m3S6HuncHT
zRoi4/BaOSIxirQYuBkTsC6s0cGeV+b7nfr6GNd3eMQRXX0HIC1AR63RH+PJmRaJ
+4xYdqTHHKmVjhc/umc60g==
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIDsTCCApmgAwIBAgIUK2+hhiq3TWxmAFA6vJO0wTQe8R8wDQYJKoZIhvcNAQEL
BQAwIzEhMB8GA1UEAxMYUm9vdCBBdXRob3JpdHkgbG9jYWxob3N0MB4XDTIxMDcx
NTA2MzYxOVoXDTIyMDcxNTA2MzY0OVowKzEpMCcGA1UEAxMgSW50ZXJtZWRpYXRl
IEF1dGhvcml0eSBsb2NhbGhvc3QwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
AoIBAQClvi4/O1MWeG5VvnLqxb+EkJNlOAtalIkW1REqNHx1am9wl+nvlykxpy3J
/KxYMHYA5lHLHT4MPgB3nTLQn42iunztg9yzJuqj5PJ6rZkkRapR1Wi797eFBUxu
Lt4vJChLwoyNJUp+3+x95It3NcENuxfxzUycDwTBdkz72gP5ayyG4R5vLsqnaKwo
Pyoo1G00PUuDfkDVuw33dQ7sYH03smlPiLKU5FYKhPkwpkSGdWbA7gNzn5uiK5kH
8vXCQDpJLTeoBW6f6wyOtcHuRvz127GTvoIJZE7n0COs9u0nrfXjkxs6VHiXRPFG
KZaNi1YL/6hKeVYdt+eFtNBcjDpfAgMBAAGjgdQwgdEwDgYDVR0PAQH/BAQDAgEG
MA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFDxeTKK93dNmEUpWZxETcy2+fV3f
MB8GA1UdIwQYMBaAFBN4+S56wEK7546ZUh3naa7bs5h+MDsGCCsGAQUFBwEBBC8w
LTArBggrBgEFBQcwAoYfaHR0cDovL2xvY2FsaG9zdDo4MjAwL3YxL3BraS9jYTAx
BgNVHR8EKjAoMCagJKAihiBodHRwOi8vbG9jYWxob3N0OjgyMDAvdjEvcGtpL2Ny
bDANBgkqhkiG9w0BAQsFAAOCAQEAM7eqEGBNZuDYBAlWs88vpfw1CMwahacdiGuY
gzOG8hPZKTANocldPKDvjG4McSe7U9KTTELsGzDe/xB6d4RCWzBLwIE7NEUGK8fh
py0nEFLhACHYm7+jcY14sPh1uT5r74Ytk/x/n4AOQIvgFY6nh3c0cHCCqUvykMf9
GLL1bx5rSDu40+7HyYvsf5Q0Qpjlm4qBCCOdmD5RCR1bPScHDod+dLeE+KGb+gjK
cADurxRAIGXUnd9qm58Z0N3AYOCLTfI93qpy4i36gLql6uwbNGAAyBbcrxqaW+1M
woIpSO6HxwcOukRTinYFQariDpM3wcLGMZxYuplD6VDIc1Dy8Q==
-----END CERTIFICATE-----
```
   *   Второй `private.pem` - приватный ключ.

```shell
vagrant@vagrant:~$ cat private.pem
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAmO2jOMYsm0CGbEquoT/pY+cQQRXHfU2qamXtFJUJUYXpIY3G
fQvKXX1fwulyKIgNEWiKiW6F1eU7m+0ySj4IRgOc02d+gmSw9X9+dtlhDhZSy420
Ii0+nUTX2zAe1Ceutlyp9XPL5Tdx1AU32B1mA51fGQFB0QvD5pwdCurFe7QOa5j0
K9GmPW6edItT88VmVzej1IL2EDGvEn/vAYs3M8kheXqTqUO/VBzbDXvnlp1LMnM8
pCAyECh+zN4BskhH5AroJwQziiA+ngMvI4gELk5Vys/0xGBKl9ObL/maM1gU0lWm
IQ3DgWEyLhzqlFxpK4Vd/0jhwZsDVbnA+sA1aQIDAQABAoIBAEJqQg6wEkNCnJ5/
OKQTC5s1iFubx81lY3Nd3L6pkyhyjbLizacU7cf4YRRXKhrsKzC6RCA3faxNJ7wq
IUMY+aLegsdVFR4v+KJFwnh/I6VokICSg/6rw5utgElS9rCQo1HToIRWy+A6WhcI
RR54dgtv1xMW9qyA/Y0zk3FgUG/OMOH/oL5LWqLbP36+bbc6AgNLpRpUMLbRALIi
QIyqvnZgOrZeyayG7DfQRptCvtE6FnAfOvyGBraSn+7aUlTQLIt/sM/vcZjWEBXB
2eiKhu9VX6lH9CLrezb+AlWMr5OWpZIt/Oamdp5vZLSmLe1cm/CQOEn5FwiN4Ted
RLuglmECgYEAwNvVlDGgblfY7bLnsK4WCOwCzUOQH5QBRnvN4gOaYOW8SBIkDvI9
gcyNChIAjIo5RpclHHSfhaC621+6GgCW1jmdB4zZco9PqelWW7gYWoP685fjvQPi
GPCYBQJHFLIO01gfiSt8O4f0eJutheWk9XKzTmTXJ7zHteFs/8COhwUCgYEAyv8X
hTJxUolWtUooWxFgM97lZUW5sho9+gAsg1UoRMz0pPXsJlC78IMvoDySTwzQdUTs
6/dL1D1DYL8F/zIFedXsmzjvSWevx2HRnby9+R+g6CNrdV/AiSo8IeJeYJbe7lNE
9lTTTh0rJSUuO3lbUbZfZF2A4dl2xQyNsQwYOhUCgYAUoC4yYDBZPLntigGvap7e
q2cNTtl+FxUf1aPKNTpwfIFrb809b/jWBetblVtLrIi9nPKSHYLmBq+VQKKln0SC
erzpjs2+q8cIU/Uxb/nizFStcqQflee7ZRfNCVZSx0xAnB8bS3RI5ZxmvbeMJ2hB
+9djXfOIw27Ua9x9abmUhQKBgQCZ5JHcNMWcoOnPPo0hnSalrFGUWSvSTfq2UPNu
DV0d65N8i8OfuI0CZTHx9Hmm3Dwc60gCC9S87kTqT2codK+aEgfyFVOy/pxQN2RG
hRQwjT3bPx70OMcqNY6o0YhjCX2wiAg8B0q6aXqQCoPmKraEWBIxcIGItuhHsqCo
nFaxkQKBgFsXcqK/AtrM3zRQX6vvHjzaIQkvaTIO6ut6tlHq9MIguKCBw5xr/OVL
tVNQcbIrEDL5A9tkfaTp2OfRxL1Nr5rA+V0xqDgOZCfqQIoINJBAktd/UXEcRDoQ
TOuI4w1l2KHR7JnVZ288v3sDXzd+cRbiWycCmlLJuw1ehnB3ZnV8
-----END RSA PRIVATE KEY-----
```

*   В конфигурационном файле `/sited-available/default` можно указать не `.crt` и `.key`, а файлы с расширением `.pem`:     

```shell
    # SSL configuration
	#
	listen 443 ssl default_server;
	listen [::]:443 ssl default_server;
	ssl_certificate /etc/nginx/ssl/chain.pem;
	ssl_certificate_key /etc/nginx/ssl/private.pem;
	#
	# Note: You should disable gzip for SSL traffic.
	# See: https://bugs.debian.org/773332
```
*   Протестируем:
```shell
root@vagrant:/etc/nginx/sites-available# nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
*   И перезапустим `nginx`:
```shell
root@vagrant:/etc/nginx/sites-available# systemctl restart nginx
root@vagrant:/etc/nginx/sites-available# systemctl status nginx.service
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2021-07-14 15:51:34 UTC; 3s ago
       Docs: man:nginx(8)
    Process: 30594 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
    Process: 30605 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
   Main PID: 30606 (nginx)
      Tasks: 2 (limit: 1074)
     Memory: 2.6M
     CGroup: /system.slice/nginx.service
             ├─30606 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
             └─30607 nginx: worker process

Jul 14 15:51:34 vagrant systemd[1]: Starting A high performance web server and a reverse proxy server...
Jul 14 15:51:34 vagrant systemd[1]: Started A high performance web server and a reverse proxy server.
```
*   Выполним запрос к `localhost`:
```shell
root@vagrant:/etc/nginx/sites-available# curl https://localhost
curl: (60) SSL certificate problem: unable to get local issuer certificate
More details here: https://curl.haxx.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the web page mentioned above.
```
*   И переходим к пункту 6 =)

## 6. Модифицировав /etc/hosts и системный trust-store, добейтесь безошибочной с точки зрения HTTPS работы curl на ваш тестовый домен (отдающийся с localhost). Рекомендуется добавлять в доверенные сертификаты Intermediate CA. Root CA добавить было бы правильнее, но тогда при конфигурации nginx потребуется включить в цепочку Intermediate, что выходит за рамки лекции. Так же, пожалуйста, не добавляйте в доверенные сам сертификат хоста.
*   Меняем `/etc/hosts`:
```shell
root@vagrant:/etc/nginx/ssl# vim /etc/hosts
root@vagrant:/etc/nginx/ssl# cat /etc/hosts
127.0.0.1	localhost
127.0.1.1	vagrant.vm	vagrant
127.0.0.1	netology.example.com  example.com
# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```
*   Сформируем файл `.crt`, для этого извлечем все сертификаты с цепочкой CA:
```shell
agrant@vagrant:~$ openssl crl2pkcs7 -nocrl -certfile intermediate.cert.pem | openssl pkcs7 -print_certs -out netinter.crt
vagrant@vagrant:~$ cat netinter.crt
subject=CN = Intermediate Authority localhost

issuer=CN = Root Authority localhost

-----BEGIN CERTIFICATE-----
MIIDsTCCApmgAwIBAgIUK2+hhiq3TWxmAFA6vJO0wTQe8R8wDQYJKoZIhvcNAQEL
BQAwIzEhMB8GA1UEAxMYUm9vdCBBdXRob3JpdHkgbG9jYWxob3N0MB4XDTIxMDcx
NTA2MzYxOVoXDTIyMDcxNTA2MzY0OVowKzEpMCcGA1UEAxMgSW50ZXJtZWRpYXRl
-----END CERTIFICATE-----
```
*   Скопируем сертификат в `trust-store` и обновим системный каталог с ними:
```shell
vagrant@vagrant:~$ sudo cp netinter.crt /usr/local/share/ca-certificates/
vagrant@vagrant:~$ sudo update-ca-certificates
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
vagrant@vagrant:~$ sudo systemctl restart nginx
vagrant@vagrant:~$ sudo systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2021-07-15 10:32:26 UTC; 5s ago
       Docs: man:nginx(8)
    Process: 61327 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
    Process: 61339 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
   Main PID: 61340 (nginx)
      Tasks: 2 (limit: 1074)
     Memory: 2.6M
     CGroup: /system.slice/nginx.service
             ├─61340 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
             └─61341 nginx: worker process

Jul 15 10:32:26 vagrant systemd[1]: Starting A high performance web server and a reverse proxy server...
Jul 15 10:32:26 vagrant systemd[1]: Started A high performance web server and a reverse proxy server.
```
*   Выполним `curl`:
```shell
vagrant@vagrant:~$ curl -I -s https://netology.example.com
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Thu, 15 Jul 2021 10:32:41 GMT
Content-Type: text/html
Content-Length: 612
Last-Modified: Thu, 15 Jul 2021 06:25:18 GMT
Connection: keep-alive
ETag: "60efd4ce-264"
Accept-Ranges: bytes
```

*DONE! =)*

## 7. Ознакомьтесь с протоколом ACME и CA Let's encrypt. Если у вас есть во владении доменное имя с платным TLS-сертификатом, который возможно заменить на LE, или же без HTTPS вообще, попробуйте воспользоваться одним из предложенных клиентов, чтобы сделать веб-сайт безопасным (или перестать платить за коммерческий сертификат).

*   С протоколом `ACME` и CA `Let's enscrypt` знакомы, т.к. во владении есть домен [bikepower.ddns.net](https://bikepower.ddns.net/). Используем, в частности, как домашнее облако `nextcloud`
*   Сертификат устанавливали по рекомендациям с [losst](https://losst.ru/kak-poluchit-sertifikat-let-s-encrypt) ещё до начала моего обучения на курсе)
[cert_bikepower](../../pictures/bikepower.png)

