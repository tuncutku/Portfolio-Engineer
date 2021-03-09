from flask import current_app, render_template
from src.extensions import mail, celery_logger, log

from src.extensions import celery
from src.environment.user import User
from flask_mail import Message


@celery.task(bind=True, ignore_result=True, default_retry_delay=300, max_retries=5)
def send_async_email(self, email_data):
    """Background task to send an email with Flask-Mail."""

    celery_logger.info("Sending email.")
    app = current_app._get_current_object()
    msg = Message(
        subject="aaa",
        recipients=["tuncutku10@gmail.com"],
    )
    msg.body = render_template("email/daily_report.txt", email=email_data["email"])
    msg.html = render_template("email/daily_report.html", email=email_data["email"])
    celery_logger.info("Sending email.")
    # with app.app_context():
    #     mail.send(msg)


@celery.task(bind=True, name="periodic_report")
def periodic_report(self):

    for user in User.find_all():
        for portfolio in user.portfolios:
            for alert in portfolio.alerts:

                pass

    print("Hi! from periodic_task")
    logger.info("Hello! from periodic task")
