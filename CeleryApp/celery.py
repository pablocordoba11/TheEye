from celery import Celery
import os
from theEyeProject.settings import *



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "theEyeProject.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

app = Celery('CeleryApp',
             broker='amqp://guest:guest@localhost:5672//',
             include=['CeleryApp.task']
             )

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"]
)
if __name__ == '__main__':
    app.start()