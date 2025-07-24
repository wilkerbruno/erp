from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(message='Campo obrigatorio'),
        Length(min=3, max=50)
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Campo obrigatorio'),
        Length(min=3)
    ])
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')
