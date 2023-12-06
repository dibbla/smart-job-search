import csv
from faker import Faker
import requests
import os

fake = Faker()

def login_hr(email, password):
    session = requests.Session()
    login_data = {
        'User_Email': email,  # Use 'User_Email' instead of 'HR_Email'
        'User_Password': password,  # Use 'User_Password' instead of 'HR_Password'
    }
    r = session.post('http://localhost:5000/login', data=login_data, allow_redirects=True)
    return session

def logout_hr(session):
    r = session.post('http://localhost:5000/logout')

def post_job(session):
    job_info = {
        'Job_Title': fake.job(),
        'Job_Description': fake.text(),
        'Job_Salary': fake.random_int(1000, 10000),
    }
    r = session.post('http://localhost:5000/post_position', data=job_info)

if __name__ == "__main__":
    # read hr csv
    local_path = os.path.dirname(__file__)
    hr_csv = os.path.join(local_path, 'hr.csv')
    with open(hr_csv, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        hr_data = [row for row in reader]

    # login hr, post job, and logout for each HR
    for hr in hr_data:
        session = login_hr(hr['HR_Email'], hr['HR_Password'])
        for i in range(5):
            post_job(session)
        logout_hr(session)
