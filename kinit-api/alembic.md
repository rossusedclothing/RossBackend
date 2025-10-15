`迁移dev 环境的数据库 `
```base
alembic --name dev stamp head
python.exe .\main.py  migrate --env  dev
```

 