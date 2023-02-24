import multiprocessing

bind = "0.0.0.0:8001"

workers = multiprocessing.cpu_count() * 2 + 1

# Increase worker timeout value to give upstream services time to respond.
# Value is aligned to apprise-api, see:
# https://github.com/caronc/apprise-api/blob/master/apprise_api/gunicorn.conf.py
timeout = 90

accesslog = "-"
errorlog = "-"
loglevel = "warning"
