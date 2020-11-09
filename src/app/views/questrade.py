from flask import Blueprint, request, session, url_for, render_template, redirect
from src.app.models import User
from src.app.models.utils import UserError


user_blueprint = Blueprint('questrade', __name__)


@portfolio_blueprint.route('/access_code', methods=['GET', 'POST'])
def insert_token():
    if request.method == 'POST':
        token = request.form['email']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.portfolio'))
        except UserError as e:
            return e.message
    # else 
    return render_template("portfolio/list.html")