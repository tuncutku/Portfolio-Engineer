"""
Run using the command:

celery -A celery_worker.celery worker --loglevel=info
celery -A celery_worker.celery beat --loglevel=info

"""

import os
from dotenv import load_dotenv

from src import create_app, make_celery


load_dotenv()

flask_app = create_app(os.getenv("FLASK_CONFIG"))
celery = make_celery(flask_app)
