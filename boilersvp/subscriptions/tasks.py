from huey import crontab
from huey.contrib.djhuey import periodic_task


@periodic_task(crontab(minute='*/5'))
def say_hello():
    print('Hello!')
