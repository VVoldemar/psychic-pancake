## Шаблон для третьего ДЗ по ИПР

Условие дз доступно по [ссылке](https://github.com/Nikfilk2030/missing_semester_hse_cs/blob/main/2026/amcs/year_1/hw_3/README.md)

## Запуск через Compose

```sh
sudo docker build --network=host -t hw3-counter:local .
cp .env.example .env
sudo docker compose up -d --no-build --wait --wait-timeout 90
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

## Проверка Compose с SQLite

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

## Проверка Redis

```sh
sudo docker compose up -d --no-build --wait --wait-timeout 90 2>&1 | tee level8.log
sudo docker compose ps | tee -a level8.log
curl -sS --max-time 5 -w '\nHTTP %{http_code}\n' http://127.0.0.1:8080/ | tee -a level8.log
curl -sS --max-time 5 -w '\nHTTP %{http_code}\n' -X POST http://127.0.0.1:8080/increment | tee -a level8.log
curl -sS --max-time 5 -w '\nHTTP %{http_code}\n' -X POST http://127.0.0.1:8080/increment | tee -a level8.log
curl -sS --max-time 5 -w '\nHTTP %{http_code}\n' -X POST http://127.0.0.1:8080/increment | tee -a level8.log

sudo docker compose down 2>&1 | tee -a level8.log
sudo docker compose up -d --no-build --wait --wait-timeout 90 2>&1 | tee -a level8.log
curl -sS --max-time 5 -w '\nHTTP %{http_code}\n' http://127.0.0.1:8080/ | tee -a level8.log

sudo docker compose stop redis 2>&1 | tee -a level8.log
curl -sS --max-time 5 -w '\nHTTP %{http_code}\n' http://127.0.0.1:8080/healthz | tee -a level8.log
curl -sS --max-time 5 -w '\nHTTP %{http_code}\n' http://127.0.0.1:8080/readyz | tee -a level8.log
curl -sS --max-time 5 -w '\nHTTP %{http_code}\n' -X POST http://127.0.0.1:8080/increment | tee -a level8.log

sudo docker compose start --wait --wait-timeout 90 redis 2>&1 | tee -a level8.log
curl -sS --max-time 5 -w '\nHTTP %{http_code}\n' http://127.0.0.1:8080/ | tee -a level8.log
curl -sS --max-time 5 -w '\nHTTP %{http_code}\n' -X POST http://127.0.0.1:8080/increment | tee -a level8.log
sudo docker compose logs --no-color app redis 2>&1 | tee -a level8.log
```

```text
Image redis:7.4-alpine Pulling
 4a603bc2424c Pulling fs layer 0B
 4f4fb700ef54 Pulling fs layer 0B
 6c0bde7286d0 Pulling fs layer 0B
 ad83137ff0b2 Pulling fs layer 0B
 0e50696bc150 Pulling fs layer 0B
 f55179448640 Pulling fs layer 0B
 710f3da1112f Pulling fs layer 0B
 dfed3a5d50b9 Downloading 24.69kB
 dfed3a5d50b9 Download complete 0B
 5864e364268f Download complete 0B
 4a603bc2424c Download complete 0B
 6c0bde7286d0 Download complete 0B
 4f4fb700ef54 Download complete 0B
 0e50696bc150 Download complete 0B
 ad83137ff0b2 Download complete 0B
 f55179448640 Downloading 1.049MB
 f55179448640 Downloading 1.049MB
 f55179448640 Downloading 1.049MB
 f55179448640 Downloading 1.049MB
 f55179448640 Downloading 2.097MB
 f55179448640 Downloading 2.097MB
 f55179448640 Downloading 3.146MB
 f55179448640 Downloading 3.146MB
 f55179448640 Downloading 3.146MB
 f55179448640 Downloading 5.243MB
 f55179448640 Downloading 5.243MB
 f55179448640 Downloading 5.243MB
 f55179448640 Downloading 7.34MB
 f55179448640 Downloading 7.34MB
 f55179448640 Downloading 7.34MB
 f55179448640 Downloading 7.34MB
 f55179448640 Downloading 9.437MB
 f55179448640 Downloading 9.437MB
 f55179448640 Downloading 10.49MB
 f55179448640 Downloading 11.53MB
 f55179448640 Downloading 12.42MB
 f55179448640 Download complete 0B
 710f3da1112f Downloading 1.049MB
 710f3da1112f Downloading 1.049MB
 710f3da1112f Downloading 2.097MB
 710f3da1112f Downloading 2.097MB
 710f3da1112f Downloading 2.097MB
 710f3da1112f Downloading 2.097MB
 710f3da1112f Download complete 0B
 710f3da1112f Extracting 1B
 710f3da1112f Extracting 1B
 6c0bde7286d0 Pull complete 0B
 710f3da1112f Pull complete 0B
 ad83137ff0b2 Extracting 1B
 ad83137ff0b2 Pull complete 0B
 f55179448640 Extracting 1B
 f55179448640 Extracting 1B
 f55179448640 Extracting 1B
 f55179448640 Extracting 1B
 4a603bc2424c Pull complete 0B
 4f4fb700ef54 Pull complete 0B
 0e50696bc150 Pull complete 0B
 f55179448640 Pull complete 0B
 Image redis:7.4-alpine Pulled
 Volume hw_3_template_redis-data Creating
 Volume hw_3_template_redis-data Created
 Container hw_3_template-redis-1 Creating
 Container hw_3_template-redis-1 Created
 Container hw_3_template-app-1 Recreate
 Container hw_3_template-app-1 Recreated
 Container hw_3_template-redis-1 Starting
 Container hw_3_template-redis-1 Started
 Container hw_3_template-redis-1 Waiting
 Container hw_3_template-redis-1 Healthy
 Container hw_3_template-app-1 Starting
 Container hw_3_template-app-1 Started
 Container hw_3_template-redis-1 Waiting
 Container hw_3_template-app-1 Waiting
 Container hw_3_template-redis-1 Healthy
 Container hw_3_template-app-1 Healthy
NAME                    IMAGE               COMMAND                  SERVICE   CREATED         STATUS                   PORTS
hw_3_template-app-1     hw3-counter:local   "python app.py"          app       9 seconds ago   Up 5 seconds (healthy)   127.0.0.1:8080->8000/tcp
hw_3_template-redis-1   redis:7.4-alpine    "docker-entrypoint.s…"   redis     9 seconds ago   Up 9 seconds (healthy)   6379/tcp
{"greeting": "hello world", "count": 0, "hostname": "e9bec4e90c75", "storage": "redis"}
HTTP 200
{"greeting": "hello world", "count": 1, "hostname": "e9bec4e90c75", "storage": "redis"}
HTTP 200
{"greeting": "hello world", "count": 2, "hostname": "e9bec4e90c75", "storage": "redis"}
HTTP 200
{"greeting": "hello world", "count": 3, "hostname": "e9bec4e90c75", "storage": "redis"}
HTTP 200
 Container hw_3_template-app-1 Stopping
 Container hw_3_template-app-1 Stopped
 Container hw_3_template-app-1 Removing
 Container hw_3_template-app-1 Removed
 Container hw_3_template-redis-1 Stopping
 Container hw_3_template-redis-1 Stopped
 Container hw_3_template-redis-1 Removing
 Container hw_3_template-redis-1 Removed
 Network hw_3_template_default Removing
 Network hw_3_template_default Removed
 Network hw_3_template_default Creating
 Network hw_3_template_default Created
 Container hw_3_template-redis-1 Creating
 Container hw_3_template-redis-1 Created
 Container hw_3_template-app-1 Creating
 Container hw_3_template-app-1 Created
 Container hw_3_template-redis-1 Starting
 Container hw_3_template-redis-1 Started
 Container hw_3_template-redis-1 Waiting
 Container hw_3_template-redis-1 Healthy
 Container hw_3_template-app-1 Starting
 Container hw_3_template-app-1 Started
 Container hw_3_template-app-1 Waiting
 Container hw_3_template-redis-1 Waiting
 Container hw_3_template-redis-1 Healthy
 Container hw_3_template-app-1 Healthy
{"greeting": "hello world", "count": 3, "hostname": "7d2cbbc7fa93", "storage": "redis"}
HTTP 200
 Container hw_3_template-redis-1 Stopping
 Container hw_3_template-redis-1 Stopped
{"status": "alive"}
HTTP 200
{"error": "storage_unavailable"}
HTTP 503
{"error": "storage_unavailable"}
HTTP 503
 Container hw_3_template-redis-1 Starting
 Container hw_3_template-redis-1 Started
 Container hw_3_template-redis-1 Waiting
 Container hw_3_template-redis-1 Healthy
{"greeting": "hello world", "count": 3, "hostname": "7d2cbbc7fa93", "storage": "redis"}
HTTP 200
{"greeting": "hello world", "count": 4, "hostname": "7d2cbbc7fa93", "storage": "redis"}
HTTP 200
```
