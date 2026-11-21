## Шаблон для третьего ДЗ по ИПР

Условие дз доступно по [ссылке](https://github.com/Nikfilk2030/missing_semester_hse_cs/blob/main/2026/amcs/year_1/hw_3/README.md)

## Запуск через Compose

```sh
sudo docker build --network=host -t hw3-counter:local .
cp .env.example .env
sudo docker compose up -d --no-build
```

```sh
cat .env.example
```

```dotenv
HOST_PORT=8080
GREETING="hello world"
```

## Проверка 1 части

```sh
curl -fsS http://127.0.0.1:8080/ | tee level4-response.json
```

```sh
cat level4.log
```

```text
2026-11-24 10:05:20,359 listening port=8000 storage=sqlite
2026-11-24 10:05:35,324 http 172.17.0.1 "GET / HTTP/1.1" 200 -
2026-11-24 10:05:35,379 http 172.17.0.1 "POST /increment HTTP/1.1" 200 -
2026-11-24 10:05:35,387 http 172.17.0.1 "GET / HTTP/1.1" 200 -
```

## Проверка Compose

```console
$ curl -fsS --max-time 5 -X GET http://127.0.0.1:8080/
{"greeting": "hello world", "count": 0, "hostname": "3c97bcd4fed3", "storage": "sqlite"}
$ curl -fsS --max-time 5 -X POST http://127.0.0.1:8080/increment
{"greeting": "hello world", "count": 1, "hostname": "3c97bcd4fed3", "storage": "sqlite"}
$ docker compose logs --no-color app
app-1  | 2026-11-24 10:42:14,022 listening port=8000 storage=sqlite
app-1  | 2026-11-24 10:42:14,772 http 172.18.0.1 "GET /readyz HTTP/1.1" 200 -
app-1  | 2026-11-24 10:42:14,782 http 172.18.0.1 "GET / HTTP/1.1" 200 -
app-1  | 2026-11-24 10:42:15,035 http 172.18.0.1 "POST /increment HTTP/1.1" 200 -
$ docker compose down
 Container hw_3_template-app-1 Stopping
 Container hw_3_template-app-1 Stopped
 Container hw_3_template-app-1 Removing
 Container hw_3_template-app-1 Removed
 Network hw_3_template_default Removing
 Network hw_3_template_default Removed
$ docker compose up -d --no-build
 Network hw_3_template_default Creating
 Network hw_3_template_default Created
 Container hw_3_template-app-1 Creating
 Container hw_3_template-app-1 Created
 Container hw_3_template-app-1 Starting
 Container hw_3_template-app-1 Started
$ curl -fsS --max-time 5 -X GET http://127.0.0.1:8080/
{"greeting": "hello world", "count": 1, "hostname": "f36de142fcb3", "storage": "sqlite"}
$ docker compose logs --no-color app
app-1  | 2026-11-24 10:42:26,522 listening port=8000 storage=sqlite
app-1  | 2026-11-24 10:42:27,271 http 172.18.0.1 "GET /readyz HTTP/1.1" 200 -
app-1  | 2026-11-24 10:42:27,280 http 172.18.0.1 "GET / HTTP/1.1" 200 -
PASS: 0 -> 1 -> 1
```
