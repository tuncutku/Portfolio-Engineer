from src import create_app
from celery import Celery

from celery.schedules import crontab


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["RESULT_BACKEND"],
    )
    celery.conf.update(app.config)
    celery.conf.beat_schedule = {
        "periodic_task-every-minute": {
            "task": "periodic_task",
            "schedule": crontab(minute="*"),
        }
    }
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


flask_app = create_app("config.DevConfig")
celery = make_celery(flask_app)
