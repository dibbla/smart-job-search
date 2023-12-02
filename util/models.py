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
    User_Info_ID = db.Column(db.Integer, db.ForeignKey('personal_info.Info_ID'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.User_Email
    
# Company table, Company can be created by Company Registration
class Company(db.Model):
    Company_ID = db.Column(db.Integer, primary_key=True)
    Company_Name = db.Column(db.String(255), nullable=False)
    Company_Location = db.Column(db.String(255))
    Company_Description = db.Column(db.Text)

# Personal Info Table
class Personal_Info(db.Model):
    __tablename__ = 'personal_info'
    Info_ID = db.Column(db.Integer, primary_key=True)
    Info_Salary = db.Column(db.Integer, nullable=True)