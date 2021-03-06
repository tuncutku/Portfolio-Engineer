from celery.utils.log import get_task_logger

from src.extensions import celery


@celery.task(name="periodic_task")
def periodic_task():
    print("Hi! from periodic_task")
    logger.info("Hello! from periodic task")