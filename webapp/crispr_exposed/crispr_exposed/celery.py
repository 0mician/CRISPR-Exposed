import os
import configparser

from celery import Celery

app = Celery('crispr', include=['crispr.tasks'])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, os.path.join('crispr_exposed', 'config.ini')))

USER = config['Celery']['USER']
PASSWD = config['Celery']['PASSWORD']
HOST = config['Celery']['HOST']
URL = 'amqp://' + USER + ':' + PASSWD + '@localhost:5672/' + HOST

# Optional configuration, see the application user guide.
app.conf.update(
    BROKER_URL = URL,     ## broker
    CELERY_RESULT_BACKEND='rpc://',    ##result backend ##'djcelery.backends.database.DatabaseBackend'#'djcelery.backends.cache:CacheBackend',
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TIMEZONE = 'Europe/Brussels',
    CELERY_ENABLE_UTC = True,
)
