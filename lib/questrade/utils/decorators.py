import functools
from typing import Callable
from flask import session, flash, redirect, url_for, request, current_app


def requires_questrade_access(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN', ''):
            flash('You need to be an administrator to access this page.', 'danger')
            return redirect(url_for('portfolio.portfolio_list'))
        return f(*args, **kwargs)
    return decorated_function