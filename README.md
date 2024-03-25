# Redis start (linux):
sudo service redis-server start

# Celery run (windows):
python -m celery -A project.celery worker --loglevel=info --pool=solo
celery -A project.celery worker --loglevel=info -P eventlet (monkeypatch I/O problem)

# Celery beat run:
celery -A project.celery beat --loglevel=info