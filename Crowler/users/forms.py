from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from Crowler.models import User

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Hasło',validators=[DataRequired()])
    submit = SubmitField('Zaloguj się!')

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Nazwa użytkownika',validators=[DataRequired()])
    password = PasswordField('Hasło',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Powtórz hasło',validators=[DataRequired()])
    submit = SubmitField('Utwórz konto!')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Your username has been registered already!')
