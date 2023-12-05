import os
import requests
import random
import csv
from faker import Faker

fake = Faker()

def generate_fake_company():
    return {
        'Company_ID': fake.unique.uuid4(),
        'Company_Name': fake.company(),
        'Company_Location': fake.address(),
        'Company_Description': fake.text(),
    }

def generate_fake_hr(company_id):
    pass_word = fake.password()
    return {
        'HR_Name': fake.name(),
        'HR_Email': fake.email(),
        'HR_Password': pass_word,
        'Confirm_Password': pass_word,
        'Company_ID': company_id,
    }

def generate_fake_user():
    pass_word = fake.password()
    return {
        'User_Name': fake.name(),
        'User_Email': fake.email(),
        'User_Password': pass_word,
        'Confirm_Password': pass_word,
    }

def test(company_num, hr_num, user_num):
    company_data = []
    hr_data = []
    user_data = []

    for _ in range(company_num):
        company = generate_fake_company()
        company_data.append(company)
        r = requests.post('http://localhost:5000/register_company', data=company)
        company_id = company['Company_ID']

        for _ in range(hr_num):
            hr = generate_fake_hr(company_id)
            hr_data.append(hr)
            r = requests.post('http://localhost:5000/register_hr', data=hr)

    for _ in range(user_num):
        user = generate_fake_user()
        user_data.append(user)
        r = requests.post('http://localhost:5000/register_user', data=user)

    # dump into csv
    local_path = os.path.dirname(__file__)
    dump_to_csv(os.path.join(local_path, 'company.csv'), company_data)
    dump_to_csv(os.path.join(local_path, 'hr.csv'), hr_data)
    dump_to_csv(os.path.join(local_path, 'user.csv'), user_data)

def dump_to_csv(file_name, data):
    keys = data[0].keys()
    with open(file_name, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Example usage
test(3, 2, 5)
