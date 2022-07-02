from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired

class RegisterForm(FlaskForm):
    username = StringField(label='Name',validators=[DataRequired()])
    registernumber = StringField(label='Registration Number',validators=[DataRequired()])
    emailaddress = StringField(label='Email Address ',validators=[Email(),DataRequired()])
    HostelBlock = StringField(label='Hostel Block',validators=[DataRequired()])
    Password1 = PasswordField(label='Password',validators=[Length(min=6),DataRequired()])
    Password2 = PasswordField(label='Confirm Password',validators=[EqualTo('Password1')])
    submit = SubmitField(label='Create account')

class LoginForm(FlaskForm):
    emailaddress = StringField(label='Email Address',validators=[DataRequired()])
    Password = PasswordField(label='Password',validators=[DataRequired()])
    submit = SubmitField(label='Login')

class vLoginForm(FlaskForm):
    vendorname=StringField(label='Name',validators=[DataRequired()])
    Password=PasswordField(label='Password',validators=[DataRequired()])
    submit = SubmitField(label='Login')

class MyCart1(FlaskForm):
    submit=SubmitField(label='Add to cart')
class MyCart2(FlaskForm):
    submit=SubmitField(label='Add to cart')
class MyCart3(FlaskForm):
    submit=SubmitField(label='Add to cart')
class MyCart4(FlaskForm):
    submit=SubmitField(label='Add to cart')