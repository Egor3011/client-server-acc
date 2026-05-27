# Deploy на чистый Ubuntu сервер

## 1) Что установить на сервере (если он "0")

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
```

После `usermod` выйди и зайди в SSH заново.

Проверка:

```bash
docker --version
docker compose version
```

## 2) Загрузка проекта и запуск

1. Загрузи проект на сервер (например в `/opt/acc-client`).
2. Перейди в корень проекта (там, где `docker-compose.yml`):

```bash
cd /opt/acc-client
docker compose up -d --build
```

## 3) Проверка

```bash
docker compose ps
docker compose logs -f backend
docker compose logs -f webapp
docker compose logs -f nginx
```

- Web UI: `http://<IP_сервера>/`
- API: `http://<IP_сервера>/api/servers`

## 4) Управление

```bash
docker compose pull
docker compose up -d --build
docker compose restart
docker compose down
```

## Важное замечание про WebSocket

Страница сервера подключается напрямую к `ws://<ip_сервера_из_списка>:8765`.
Поэтому каждый управляемый сервер должен быть доступен по этому IP и порту с машины пользователя (браузера).
