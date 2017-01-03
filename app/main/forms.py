from flask_wtf import FlaskForm  
from wtforms import TextField,SubmitField,PasswordField  
from wtforms.validators import DataRequired,Length,Regexp,EqualTo 
from wtforms import ValidationError
from ..models import User
  
class NameForm(FlaskForm):  
    name=TextField('what is your name?',validators=[DataRequired()])  
    password=PasswordField('what is your password?',validators=[DataRequired()])
    login=SubmitField('login')
    logout=SubmitField('logout')

class RegisterForm(FlaskForm):
    name=TextField('Name',validators=[DataRequired(),Length(1,32),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'name is invalid')])
    registe=SubmitField('Registe')
    password1=PasswordField('passsword',validators=[DataRequired(),EqualTo('password2','passwords must match')])
    password2=PasswordField('password confirm')

    def validate_name(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('name exists')
