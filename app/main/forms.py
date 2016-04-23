from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Required, EqualTo


class LoginForm(Form):
    name = StringField('name', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember me', default = False)
    submit = SubmitField('Log In')

class ModPassword(Form):
    oldpassword = PasswordField('old password', validators=[Required()])
    newpassword = PasswordField('new password', validators=[Required(), EqualTo('new2password', message='Passwords must match')])
    new2password = PasswordField('repeat new password', validators=[Required()])
    submit = SubmitField('comfirm')
