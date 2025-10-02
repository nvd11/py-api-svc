我部署了一个fastapi app 到k8s， 和一个相应的clusterip
```bash
gateman@tf-vpc0-subnet0-vm0:~$ kubectl get svc
NAME                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
clusterip-py-api-svc   ClusterIP   192.170.29.241   <none>        8000/TCP   18h
kubernetes             ClusterIP   192.170.16.1     <none>        443/TCP    27d
gateman@tf-vpc0-subnet0-vm0:~$ kubectl describe svc clusterip-py-api-svc
Name:                     clusterip-py-api-svc
Namespace:                default
Labels:                   <none>
Annotations:              cloud.google.com/neg: {"ingress":true}
Selector:                 app=py-api-svc
Type:                     ClusterIP
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       192.170.29.241
IPs:                      192.170.29.241
Port:                     <unset>  8000/TCP
TargetPort:               8000/TCP
Endpoints:                192.169.17.7:8000,192.169.19.8:8000,192.169.18.9:8000
Session Affinity:         None
Internal Traffic Policy:  Cluster
Events:                   <none>
gateman@tf-vpc0-subnet0-vm0:~$ kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP              NODE                                          NOMINATED NODE   READINESS GATES
dns-test                      1/1     Running   0          17h   192.169.19.7    gke-my-cluster1-my-node-pool1-5cad8c5c-4xw8   <none>           <none>
py-api-svc-6f44547c88-d59bl   1/1     Running   0          27m   192.169.17.7    gke-my-cluster1-my-node-pool1-f7d2eb2b-e0gi   <none>           <none>
py-api-svc-6f44547c88-gksk4   1/1     Running   0          27m   192.169.19.8    gke-my-cluster1-my-node-pool1-5cad8c5c-4xw8   <none>           <none>
py-api-svc-6f44547c88-n2rj6   1/1     Running   0          27m   192.169.18.9    gke-my-cluster1-my-node-pool1-8902d932-ab08   <none>           <none>
test-curl2                    1/1     Running   0          77m   192.169.21.17   gke-my-cluster1-my-node-pool1-5cad8c5c-lrwc   <none>           <none>
```

当我在dns-test 里测试curl cluster ip时， 是通的

```bash
gateman@tf-vpc0-subnet0-vm0:~$ kubectl exec -it dns-test -- /bin/sh
/home # curl -v http://clusterip-py-api-svc:8000/pyapi/
*   Trying 192.170.29.241:8000...
* Connected to clusterip-py-api-svc (192.170.29.241) port 8000 (#0)
> GET /pyapi/ HTTP/1.1
> Host: clusterip-py-api-svc:8000
> User-Agent: curl/7.81.0
> Accept: */*
> 
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< date: Thu, 02 Oct 2025 07:03:38 GMT
< server: uvicorn
< content-length: 32
< content-type: application/json
< 
* Connection #0 to host clusterip-py-api-svc left intact
{"message":"Hello, FastAPI222!"}/home #
```
检查了pod 的日志也有相应的debug输出
```bash
025-10-02 07:03:39.002 | INFO     | __main__:read_root:20 - Root endpoint accessed!
project_path is /app
INFO:     192.169.19.1:11708 - "GET /pyapi/ HTTP/1.1" 200 OK
2025-10-02 07:03:39.002 | INFO     | __main__:read_root:20 - Root endpoint accessed!
INFO:     192.169.19.1:11708 - "GET /pyapi/ HTTP/1.1" 200 OK

```


我在fastapi里i也配置了rootpath= /pyapi
```python
import src.configs.config

from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

app = FastAPI(root_path="/pyapi")

class RootPathRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not request.url.path.startswith(app.root_path):
            raise HTTPException(status_code=404, detail="Not Found")
        response = await call_next(request)
        return response

app.add_middleware(RootPathRedirectMiddleware)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed!")
    return {"message": "Hello, FastAPI222!"}
```

但是我不能用ingress 访问
```bash
gateman@tf-vpc0-subnet0-vm0:~$ curl -v http://34.117.190.168/pyapi/
*   Trying 34.117.190.168:80...
* Connected to 34.117.190.168 (34.117.190.168) port 80 (#0)
> GET /pyapi/ HTTP/1.1
> Host: 34.117.190.168
> User-Agent: curl/7.74.0
> Accept: */*
> 
* Empty reply from server
* Connection #0 to host 34.117.190.168 left intact
curl: (52) Empty reply from server
```
从py-api-svc里见不到相应的debug 信息， 应该没call进来

这是我的ingress 配置
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-py-api-svc
  labels:
    app: py-api-svc
spec:
  ingressClassName: "gce"
  rules:
  - http:
      paths:
      - path: /pyapi/
        pathType: Prefix
        backend:
          service:
            name: clusterip-py-api-svc
            port:
              number: 8000
      - path: /pyapi/api
        pathType: Prefix
        backend:
          service:
            name: clusterip-py-api-svc
            port:
              number: 8000
```

这是ingress部署后的信息
```bash
Name:             ingress-py-api-svc
Labels:           app=py-api-svc
Namespace:        default
Address:          34.117.190.168
Ingress Class:    gce
Default backend:  <default>
Rules:
  Host        Path  Backends
  ----        ----  --------
  *           
              /pyapi/      clusterip-py-api-svc:8000 (192.169.17.7:8000,192.169.19.8:8000,192.169.18.9:8000)
              /pyapi/api   clusterip-py-api-svc:8000 (192.169.17.7:8000,192.169.19.8:8000,192.169.18.9:8000)
Annotations:  ingress.kubernetes.io/backends:
                {"k8s1-77db6059-default-clusterip-py-api-svc-8000-8517ddcb":"HEALTHY","k8s1-77db6059-kube-system-default-http-backend-80-1bcaa49a":"HEALTH...
              ingress.kubernetes.io/forwarding-rule: k8s2-fr-1zguzzcn-default-ingress-py-api-svc-0pexkp5i
              ingress.kubernetes.io/target-proxy: k8s2-tp-1zguzzcn-default-ingress-py-api-svc-0pexkp5i
              ingress.kubernetes.io/url-map: k8s2-um-1zguzzcn-default-ingress-py-api-svc-0pexkp5i
Events:       <none>
gateman@tf-vpc0-subnet0-vm0:~$ 
``` 