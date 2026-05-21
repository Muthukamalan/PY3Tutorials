# Fast API + Envoy

Envoy as reverse proxy

```sh
docker compose up --scale fastapi=3
curl -v localhost:8000/
```

```sh
.
├── app
│   ├── Dockerfile
│   └── main.py
├── envoy
│   └── envoy.yaml
├── compose.yaml
└── README.md
```