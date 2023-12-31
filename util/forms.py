from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class CompanyRegistrationForm(FlaskForm):
    Company_ID = StringField('Company ID', validators=[DataRequired()])
    Company_Name = StringField('Company Name', validators=[DataRequired()])
    Company_Location = StringField('Company Location')
    Company_Description = TextAreaField('Company Description')
    Submit = SubmitField('Register Company')

class HRRegistrationForm(FlaskForm):
    HR_Name = StringField('Name', validators=[DataRequired()])
    HR_Email = StringField('Email', validators=[DataRequired(), Email()])
    HR_Password = PasswordField('Password', validators=[DataRequired()])
    Confirm_Password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('HR_Password')])
    Company_ID = StringField('Company ID', validators=[DataRequired()])
    Submit = SubmitField('Register')

class UserRegistrationForm(FlaskForm):
    User_Name = StringField('Name', validators=[DataRequired()])
    User_Email = StringField('Email', validators=[DataRequired(), Email()])
    User_Password = PasswordField('Password', validators=[DataRequired()])
    Confirm_Password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('User_Password')])
    Submit = SubmitField('Register')

class LoginForm(FlaskForm):
    User_Email = StringField('Email', validators=[DataRequired(), Email()])
    User_Password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostPositionForm(FlaskForm):
    Job_Title = StringField('Job Title', validators=[DataRequired()])
    Job_Description = TextAreaField('Job Description')
    Job_Salary = StringField('Salary', validators=[DataRequired()])
    Submit = SubmitField('Post Position')

class AdminRegistrationForm(FlaskForm):
    Admin_Name = StringField('Name', validators=[DataRequired()])
    Admin_Email = StringField('Email', validators=[DataRequired(), Email()])
    Admin_Password = PasswordField('Password', validators=[DataRequired()])
    Confirm_Password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Admin_Password')])
    Submit = SubmitField('Register')