# Acervo Edson - Backend

## Esse repositório contém:

1. Código fonte de um repositório de obras musicais e literárias
2. Instruções para execuções

## Esse repositório **não** contém:

1. Obras literárias
2. Obras musicais
3. Usuário e senhas

## Como executar

1. Instale o cliente docker para linha de comando.
   1. Se tiver usando Linux ou MACOS, utilize o colima para gerir as virtualizações
   2. Se tiver usando Windows, utilize o Rancher Desktop
3. Usar a seguinte linha de comando para executar a base de dados (na raiz do projeto):

```shell
docker-compose up -d
```

4. Executar o programa principal com:

```shell
python acervo.py
```

O programa estará executando no porto 9100.

5. (PENDING) Usar o programa POSTMAN com a collection localizada na raiz do projeto

## Parar programa

1. Onde foi executado a última linha de comando:

```
CTRL+C
```

2. Digitar na linha de comando (na raiz do projeto):

```shell
docker-compose down
```

3. (Opcional) Se quiser apagar os volumes associados, digite o seguinte comando:

```shell
docker volume rm acervo_edson_backend_mysql_data
```