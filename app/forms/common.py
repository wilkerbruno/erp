from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

class BaseForm(FlaskForm):
    """Formulário base com campos comuns"""
    pass

# Outros formulários podem ser adicionados aqui posteriormente