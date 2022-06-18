# ac-clip
AC clip server


## Quick Started

### Start Server

#### 1. cocker-compose
```shell
$ docker-compose up -d
```

#### 2. clip_server

```shell
$ python -m clip_server flows/flow-transformers.yml
```


### Client Query

#### 1. GRPC

```python
from clip_client import Client

c = Client('grpc://0.0.0.0:51000')

r = c.encode(['First do it', 'then do it right', 'then do it better'])
print(r.shape)  # [3, 512]
```

#### 2. HTTP

```python
import requests

res = requests.post(
    'http://0.0.0.0:51001',
    json=['First do it', 'then do it right', 'then do it better']
)
print(len(res.json()))  # 3
```
