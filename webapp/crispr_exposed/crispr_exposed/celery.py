from celery import Celery

app = Celery('crispr', include=['crispr.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    BROKER_URL = 'amqp://crispr:crispr2015@localhost:5672/crispr_host',     ## broker
    CELERY_RESULT_BACKEND='rpc://',    ##result backend ##'djcelery.backends.database.DatabaseBackend'#'djcelery.backends.cache:CacheBackend',
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TIMEZONE = 'Europe/Brussels',
    CELERY_ENABLE_UTC = True,
)
