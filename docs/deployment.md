# 部署

## Docker

```bash
docker build -t dramaforge .
docker run -p 8000:8000 dramaforge
```

## Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml
```

## Helm

```bash
helm install dramaforge helm/
```

## 可复用要点

- 零依赖意味着 Docker 镜像只用 `python:3.11-slim`，无重型依赖层
- HTTP 服务用 stdlib `ThreadingHTTPServer`，天然适合容器化
