# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 3
timeout = 120
keepalive = 5

# 로깅 설정
accesslog = "-"
errorlog = "-"
loglevel = "info"

# 워커 설정
worker_class = "sync"
max_requests = 1000
max_requests_jitter = 50

# 프로세스 이름
proc_name = "tastept_app"
