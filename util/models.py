import uuid
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# User tables
# User tables all use the email as the primary key

# HR (Human Resource) table
class HR(db.Model, UserMixin):
    HR_Email = db.Column(db.String(50), primary_key=True)
    HR_Name = db.Column(db.String(50), nullable=False)
    HR_Password = db.Column(db.String(50), nullable=False)
    HR_Company_ID = db.Column(db.Integer, db.ForeignKey('company.Company_ID'), nullable=False)

    def __repr__(self):
        return '<HR %r>' % self.HR_Email
    
class User(db.Model, UserMixin):
    User_Email = db.Column(db.String(50), primary_key=True)
    User_Name = db.Column(db.String(50), nullable=False)
    User_Password = db.Column(db.String(50), nullable=False)
    applied_jobs = db.relationship('Job', secondary='job_application')
    User_Info_ID = db.Column(db.Integer, db.ForeignKey('personal_info.Info_ID'), nullable=False)
    personal_info = db.relationship('Personal_Info', backref='user', uselist=False)
    
    def __repr__(self):
        return '<User %r>' % self.User_Email
    
# Company table, Company can be created by Company Registration
class Company(db.Model):
    Company_ID = db.Column(db.String(255), primary_key=True)
    Company_Name = db.Column(db.String(255), nullable=False)
    Company_Location = db.Column(db.String(255))
    Company_Description = db.Column(db.Text)

# Personal Info Table
class Personal_Info(db.Model):
    __tablename__ = 'personal_info'
    Info_ID = db.Column(db.Integer, primary_key=True)
    Info_Salary = db.Column(db.Integer, nullable=True) # expected salary
    Info_Education = db.Column(db.String(255), nullable=True) # education
    Info_Experience = db.Column(db.Integer, nullable=True) # years of experience
    Info_Skills = db.Column(db.String(1024), nullable=True) # skills

# Job table
class Job(db.Model):
    Job_ID = db.Column(db.Integer, primary_key=True)
    Job_Title = db.Column(db.String(255), nullable=False)
    Job_Description = db.Column(db.Text)
    Job_Salary = db.Column(db.Integer, nullable=True)
    Job_Company_ID = db.Column(db.Integer, db.ForeignKey('company.Company_ID'), nullable=False)
    Job_HR_Email = db.Column(db.String(50), db.ForeignKey('hr.HR_Email'), nullable=False)
    applicants_list = db.relationship('User', secondary='job_application')

job_application = db.Table('job_application',
    db.Column('job_id', db.Integer, db.ForeignKey('job.Job_ID')),
    db.Column('user_email', db.String(50), db.ForeignKey('user.User_Email'))
)
