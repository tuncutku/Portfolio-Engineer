import logging
import click
from faker import Faker
import random

log = logging.getLogger(__name__)


faker = Faker()

fake_users = [
    {"username": "user_default", "role": "default"},
    {"username": "user_poster", "role": "poster"},
    {"username": "admin", "role": "admin"},
]
fake_roles = ["default", "poster", "admin"]


def register(app):
    @app.cli.command("create-user")
    @click.argument("username")
    @click.argument("password")
    def create_user(username, password):
        # user = User()
        # user.username = username
        # user.set_password(password)
        # try:
        #     db.session.add(user)
        #     db.session.commit()
        #     click.echo('User {0} Added.'.format(username))
        # except Exception as e:
        #     log.error("Fail to add new user: %s Error: %s" % (username, e))
        #     db.session.rollback()
        pass

    @app.cli.command("create-admin")
    @click.argument("username")
    @click.argument("password")
    def create_admin(username, password):
        # admin_role = Role.query.filter_by(name='admin').scalar()
        # user = User()
        # user.username = username
        # user.set_password(password)
        # user.roles.append(admin_role)
        # try:
        #     db.session.add(user)
        #     db.session.commit()
        #     click.echo('User {0} Added.'.format(username))
        # except Exception as e:
        #     log.error("Fail to add new user: %s Error: %s" % (username, e))
        #     db.session.rollback()
        pass

    @app.cli.command("list-users")
    def list_users():
        # try:
        #     users = User.query.all()
        #     for user in users:
        #         click.echo('{0}'.format(user.username))
        # except Exception as e:
        #     log.error("Fail to list users Error: %s" % e)
        #     db.session.rollback()
        pass
