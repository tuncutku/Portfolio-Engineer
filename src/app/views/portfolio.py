from flask import Blueprint, request, session, url_for, render_template, redirect
from src.app.models import User
from src.app.models.utils import UserError


user_blueprint = Blueprint('portfolio', __name__)


@user_blueprint.route('/list', methods=['GET', 'POST'])
def register_user():
    # if request.method == 'POST':
    #     email = request.form['email']
    #     password = request.form['password']

    #     try:
    #         if User.register_user(email, password):
    #             session['email'] = email
    #             return redirect(url_for('.portfolio'))
    #     except UserError as e:
    #         return e.message
    return render_template("users/register.html")  # Send the user an error if their login was invalid