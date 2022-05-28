# ac-clip
AC clip server


## Quick Started

### Start Server

```shell
$ python -m clip_server flows/flow-demo.yml
```


### Client Query

```python
from clip_client import Client

c = Client('grpc://0.0.0.0:51000')

r = c.encode(['First do it', 'then do it right', 'then do it better'])
print(r.shape)  # [3, 512]
```


## Transformers As Service

```shell
$ python -m clip_server flows/flow-transformers.yml
```
