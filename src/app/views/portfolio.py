from flask import Blueprint, request, session, url_for, render_template, redirect

from src.app.models import User
from src.app.models.utils import UserError
from src.app.models.utils import requires_login


portfolio_blueprint = Blueprint('portfolio', __name__)


@portfolio_blueprint.route('/list', methods=['GET', 'POST', 'PUT', 'DELETE'])
@requires_login
def portfolio_list():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(email, password):
                session['email'] = email
                return redirect(url_for('.portfolio'))
        except UserError as e:
            return e.message
    
    
    
    # if the user needs to provide token to access Questrade account, render_template "provide Questrade token.html"
    if:
        render_template("portfolio/questrade_token")
    # else 
    return render_template("portfolio/list.html")


@portfolio_blueprint.route('/summary', methods=['GET', 'POST'])
@requires_login
def portfolio_summary():
    # if request.method == 'POST':
    #     email = request.form['email']
    #     password = request.form['password']

    #     try:
    #         if User.register_user(email, password):
    #             session['email'] = email
    #             return redirect(url_for('.portfolio'))
    #     except UserError as e:
    #         return e.message
    return render_template("portfolio/summary.html")