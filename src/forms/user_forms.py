from flask_wtf import FlaskForm as Form
from wtforms import PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from src.environment.user_activities.user import User


class RegisterForm(Form):
    email = EmailField("Email address", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired(), Length(min=4)])
    confirm = PasswordField("Confirm Password", [DataRequired(), EqualTo("password")])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()

        # Is the email already being used
        if user:
            self.email.errors.append("User with that email address already exists")
            return False

        return True


class LoginForm(Form):
    email = EmailField(u"Email address", [DataRequired(), Email()])
    password = PasswordField(u"Password", [DataRequired()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        def authenticate(email: str, password: str) -> User:
            user = User.query.filter_by(email=email).first()
            if not user:
                return None
            # Do the passwords match
            if not user.check_password(password):
                return None
            return user

        if not authenticate(self.email.data, self.password.data):
            self.email.errors.append("Invalid email or password")
            return False
        return True