Proceso
=======

```bash
docker build -t eventoL .
docker run -d -i --name="eventoL" --hostname="eventoL" -p 11000:80 -t eventoL:latest /bin/bash
```

Listo
-----
