# Smart Job Search System
for CSC 3170 - Database Systems @CUHKSZ

## Set up
Install dependencies with `pip install Flask Flask-SQLAlchemy`.

Start Flask server with `python app.py`.

## Description

### Tables
- HR: stores HR information
  - HR_ID: primary key
  - HR_Name: name of HR
  - HR_Email: email of HR
  - HR_Phone: phone number of HR
  - HR_Company_ID: foreign key of Company_ID
  - HR_Password: password of HR

- Job: stores job information
  - Job_ID: primary key
  - Job_Name: name of job
  - Job_Company: company of job
  - Job_Salary: salary of job
  - Job_Education: education of job
  - Job_Location: location of job
  - Job_Description: description of job
  - Job_HR_ID: foreign key of HR_ID

- JobSeeker: stores job seeker information
  - JobSeeker_ID: primary key
  - JobSeeker_Name: name of job seeker
  - JobSeeker_Email: email of job seeker
  - JobSeeker_Phone: phone number of job seeker
  - JobSeeker_Password: password of job seeker
  - JobSeeker_Skill: skill of job seeker
  - JobSeeker_Experience: experience of job seeker
  - JobSeeker_Education: education of job seeker

- Application: stores application information
  - Application_ID: primary key
  - Application_Job_ID: foreign key of Job_ID
  - Application_JobSeeker_ID: foreign key of JobSeeker_ID
  - Application_Status: status of application

- Company: stores company information
  - Company_ID: primary key
  - Company_Name: name of company
  - Company_Location: location of company
  - Company_Description: description of company

## Team Members
- Yinggan Xu
- Minyi Sun
- Chi Xu
- Xingtong Yao
