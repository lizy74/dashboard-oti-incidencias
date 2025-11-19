from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from app.models import Usuario

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    nombre_completo = StringField('Nombre Completo', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Usuario.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class SolicitanteIncidenteForm(FlaskForm):
    titulo = StringField('Título del Incidente', validators=[DataRequired()])
    descripcion = TextAreaField('Descripción Detallada', validators=[DataRequired()])
    documento = FileField('Adjuntar Documento (PDF, PNG, JPG)', validators=[
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], '¡Solo se permiten imágenes y PDFs!')
    ])
    submit = SubmitField('Enviar Incidente')
