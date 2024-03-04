# Redis start (linux):
sudo service redis-server start
# Celery run:
celery -A project.celery worker --loglevel=info -P eventlet