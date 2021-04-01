from flask import current_app, render_template
from src.extensions import mail, celery_logger, log

from src.extensions import celery
from src.environment.user import User
from src.environment.alerts import DailyReport
from flask_mail import Message


@celery.task(bind=True, name="daily_report")
def daily_report_task(self):
    """Background task to send an email with Flask-Mail."""
    for user in User.find_all():
        for portfolio in user.portfolios:
            alert = portfolio.daily_report
            open_positions = [
                position for position in portfolio.positions if position.open
            ]
            if alert and alert.is_active and alert.is_triggered and open_positions:
                celery_logger.info("Condition satisfied, preparing email.")
                # send_email.apply_async(args=[alert.generate_email()])
