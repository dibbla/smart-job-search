import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import CompanyRegistrationForm, HRRegistrationForm, UserRegistrationForm, AdminRegistrationForm, LoginForm, \
    PostPositionForm
from .models import db, Company, Admin, HR, User, Personal_Info, Job, job_application
from. smart_search import perform_smart_search

main_routes = Blueprint('main_routes', __name__)

# Main page
@main_routes.route('/')
def index():
    # print(HR.query.all())
    # print(User.query.all())
    # print(Company.query.all())
    # print(Admin.query.all())
    print(session.get('user_id'), session.get('user_type'))
    return render_template('index.html')

@main_routes.route('/smart_search', methods=['GET'])
def smart_search():
    # Check if the 'search' parameter is present
    if 'search' in request.args:
        # Perform the search logic
        print("Search triggered!")

        user_email = session.get('user_id')
        user = User.query.filter_by(User_Email=user_email).first()

        if user:
            personal_info = Personal_Info.query.get(user.User_Info_ID)
            
            if personal_info:
                print(f"User's Personal Info: {personal_info.Info_Salary}, \
                      {personal_info.Info_Education}, {personal_info.Info_Experience}, \
                        {personal_info.Info_Skills}") # debug
            
            # get all the job information
            jobs = Job.query.all()
            print(jobs, type(jobs))
            print(jobs[0].Job_Title)

            search_result = perform_smart_search(personal_info, jobs, max_result=5)
            print("DEBUG: search_result in smart search", search_result)

            # Convert the list to a string using a comma as a delimiter
            search_result_str = ','.join(map(str, search_result))
            return redirect(url_for('main_routes.smart_search_result', search_result=search_result_str))

    return render_template('smart_search.html')

@main_routes.route('/smart_search_result', methods=['GET'])
def smart_search_result():
    # Check if the 'search_result' parameter is present
    if 'search_result' in request.args:
        # Perform the search logic
        print("Search result triggered!")

        search_result = request.args.get('search_result')
        print("DEBUG: search_result", search_result, type(search_result))

        # Parse the string back into a list using a comma as a delimiter
        search_result = request.args.get('search_result').split(',')
        # Convert the list elements back to integers
        search_result = list(map(int, search_result))

        print("DEBUG: search_result decoded", search_result, type(search_result))
        
        # search results is a list of job ids
        job_data = []
        for job_id in search_result:
            print(job_id)
            # query the job information
            job = Job.query.get(job_id)
            company = Company.query.get(job.Job_Company_ID)
            job_info = {
                'job': job,
                'company': company
            }
            job_data.append(job_info)

        print(job_data)

        return render_template('smart_search_result.html', jobs=job_data)

    return render_template('smart_search_result.html')

# display all the jobs
@main_routes.route('/jobs')
def jobs():
    jobs = Job.query.all()

    # Fetch company information for each job
    job_data = []
    for job in jobs:
        company = Company.query.get(job.Job_Company_ID)
        job_info = {
            'job': job,
            'company': company
        }
        job_data.append(job_info)

    print(job_data)

    return render_template('jobs.html', jobs=job_data)

# display all the jobs
@main_routes.route('/admin_hr_jobs/<string:hr_email>')
def admin_hr_jobs(hr_email):
    jobs = Job.query.filter_by(Job_HR_Email=hr_email).all() 

    # Fetch company information for each job
    job_data = []
    for job in jobs:
        company = Company.query.get(job.Job_Company_ID)
        job_info = {
            'job': job,
            'company': company
        }
        job_data.append(job_info)

    print(job_data)

    return render_template('admin_hr_jobs.html', jobs=job_data)

@main_routes.route('/company_info/<company_id>')
def company_info(company_id):
    # Fetch company information based on company_id
    company = Company.query.get(company_id)

    return render_template('company_info.html', company=company)

@main_routes.route('/admin_company_info/<company_id>')
def admin_company_info(company_id):
    # Fetch company information based on company_id
    company = Company.query.get(company_id)

    return render_template('admin_company_info.html', company=company)

# Admin Dashboard
@main_routes.route('/admin_dashboard')
def admin_dashboard():
    # Check if the user is logged in
    if 'user_id' not in session or session['user_type'] != 'admin':
        print('You are not logged in.')
        flash('You need to log in to access the user dashboard.', 'danger')
        return redirect(url_for('main_routes.login'))
    
    return render_template('admin_dashboard.html')

# display all the users
@main_routes.route('/users')
def users():
    users = User.query.all()

    # Fetch basic info for each user
    user_data = []
    for user in users:
        user_info = {
            'user': user
        }
        user_data.append(user_info)
    print(user_data)
    return render_template('users.html', users = user_data)

# display all the hrs
@main_routes.route('/hrs')
def hrs():
    hrs = HR.query.all()

    # Fetch basic info for each user
    hr_data = []
    for hr in hrs:
        company = Company.query.get(hr.HR_Company_ID)
        hr_info = {
            'hr': hr,
            'company': company
        }
        hr_data.append(hr_info)
    print(hr_data)
    return render_template('hrs.html', hrs = hr_data)

# display all the companies
@main_routes.route('/companies')
def companies():
    companies = Company.query.all()

    # Fetch basic info for each user
    company_data = []
    for company in companies:
        # company_info = {
        #     'name': company.Company_Name,
        #     'location': company.Company_Location,
        #     'description': company.Company_Description
        # }
        company_data.append(company)
    # print(company_data)
    return render_template('companies.html', companies = company_data)

@main_routes.route('/delete_user/<string:user_email>')
def delete_user(user_email):
    # Check if the user is logged in and is an admin
    if 'user_id' not in session or session['user_type'] != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('main_routes.index'))

    # Get the User to delete
    # job = Job.query.filter_by(Job_ID=job_id, Job_HR_Email=hr.HR_Email).first()
    user = User.query.filter_by(User_Email=user_email).first()

    if user:
        # Delete the job from the database
        db.session.delete(user)
        db.session.commit()
        print('User deleted successfully.\n', User.query.all())
        flash('User deleted successfully.', 'success')
    else:
        print('User not found or you do not have permission to delete it.')
        flash('User not found or you do not have permission to delete it.', 'danger')

    return redirect(url_for('main_routes.users'))

@main_routes.route('/delete_hr/<string:hr_email>')
def delete_hr(hr_email):
    # Check if the user is logged in and is an admin
    if 'user_id' not in session or session['user_type'] != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('main_routes.index'))

    # Get the User to delete
    # job = Job.query.filter_by(Job_ID=job_id, Job_HR_Email=hr.HR_Email).first()
    hr = HR.query.filter_by(HR_Email=hr_email).first()

    if hr:
        # Delete all the job posted by this hr from the database
        # Get all jobs posted by the HR
        jobs = Job.query.filter_by(Job_HR_Email=hr_email).all()  
        for job in jobs:
            db.session.delete(job)
            db.session.commit()
        db.session.delete(hr)
        db.session.commit()
        print('HR deleted successfully.\n', HR.query.all())
        flash('HR deleted successfully.', 'success')
    else:
        print('HR not found or you do not have permission to delete it.')
        flash('HR not found or you do not have permission to delete it.', 'danger')

    return redirect(url_for('main_routes.hrs'))

@main_routes.route('/delete_company/<string:company_id>')
def delete_company(company_id):
    # Check if the user is logged in and is an admin
    if 'user_id' not in session or session['user_type'] != 'admin':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('main_routes.index'))

    # Get the Company to delete
    # job = Job.query.filter_by(Job_ID=job_id, Job_HR_Email=hr.HR_Email).first()
    company = Company.query.filter_by(Company_ID=company_id).first()

    if company:
        # Delete all the HRs work for this company from the database
        hrs = HR.query.filter_by(HR_Company_ID=company_id).all()
        for hr in hrs:
            # Delete all jobs posted by the HR
            jobs = Job.query.filter_by(Job_HR_Email=hr.HR_Email).all()  
            for job in jobs:
                db.session.delete(job)
                db.session.commit()
            db.session.delete(hr)
            db.session.commit()
        db.session.delete(company)
        db.session.commit()
        print('Company deleted successfully.\n', Company.query.all())
        flash('Company deleted successfully.', 'success')
    else:
        print('Company not found or you do not have permission to delete it.')
        flash('Company not found or you do not have permission to delete it.', 'danger')

    return redirect(url_for('main_routes.companies'))

# dashboard page
# In dash board, HR can see and delete the jobs posted by him/her
# In dash board, user can see and apply the jobs
@main_routes.route('/hr_dashboard')
def hr_dashboard():
    # Check if the user is logged in and is an HR
    if 'user_id' not in session or (session['user_type'] != 'hr' and session['user_type'] != 'admin'):
        flash('You are not authorized to access this page.', 'danger')
        print('You are not authorized to access this page.')
        return redirect(url_for('main_routes.index'))

    # Get the HR information
    hr = HR.query.filter_by(HR_Email=session['user_id']).first()

    # Get all jobs posted by the HR
    jobs = Job.query.filter_by(Job_HR_Email=hr.HR_Email).all()

    # Create a dictionary to store applicants for each job
    applicants_dict = {}

    for job in jobs:
        applicants = db.session.query(User).join(job_application).filter(job_application.c.job_id == job.Job_ID).all()
        applicants_dict[job.Job_ID] = applicants

    return render_template('hr_dashboard.html', jobs=jobs)

@main_routes.route('/delete_job/<int:job_id>')
def delete_job(job_id):
    # Check if the user is logged in and is an HR
    if 'user_id' not in session or session['user_type'] != 'hr':
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('main_routes.index'))

    # Get the HR information
    hr = HR.query.filter_by(HR_Email=session['user_id']).first()

    # Get the job to delete
    job = Job.query.filter_by(Job_ID=job_id, Job_HR_Email=hr.HR_Email).first()

    if job:
        # Delete the job from the database
        db.session.delete(job)
        db.session.commit()
        print('Job deleted successfully.\n', Job.query.all())
        flash('Job deleted successfully.', 'success')
    else:
        print('Job not found or you do not have permission to delete it.')
        flash('Job not found or you do not have permission to delete it.', 'danger')

    return redirect(url_for('main_routes.hr_dashboard'))

@main_routes.route('/post_position', methods=['GET', 'POST'])
def post_position():
    # check user authentication
    if 'user_id' not in session:
        flash('You are not logged in.', 'danger')
        print('You are not logged in.')
        return redirect(url_for('main_routes.login'))
    if session['user_type'] != 'hr':
        flash('You are not a HR.', 'danger')
        print('You are not a HR.')
        return redirect(url_for('main_routes.index'))
    
    # get the HR information
    hr = HR.query.filter_by(HR_Email=session['user_id']).first()
    if hr is None:
        flash('You are not logged in.', 'danger')
        print('You are not logged in.')
        return redirect(url_for('main_routes.login'))
    
    # get the company information
    company = Company.query.filter_by(Company_ID=hr.HR_Company_ID).first()
    if company is None:
        flash('You are not logged in.', 'danger')
        print('You are not logged in.')
        return redirect(url_for('main_routes.login'))
    
    # post a job and add it to the database
    form = PostPositionForm()
    if form.validate_on_submit():
        # create a job id with uuid
        job_id = uuid.uuid4().int & (1<<32)-1
        print(job_id)
        new_job = Job(
            Job_ID=job_id,
            Job_Title=form.Job_Title.data,
            Job_Description=form.Job_Description.data,
            Job_Salary=form.Job_Salary.data,
            Job_Company_ID=company.Company_ID,
            Job_HR_Email=hr.HR_Email
        )
        db.session.add(new_job)
        db.session.commit()
        print('Job posted successfully.\n', Job.query.all())
        return redirect(url_for('main_routes.hr_dashboard'))
    
    return render_template('post_position.html', form=form)

# In your routes.py
@main_routes.route('/view_personal_info/<string:user_email>')
def view_personal_info(user_email):
    # Fetch the user based on the provided email
    user = User.query.filter_by(User_Email=user_email).first()

    if user:
        # Render a template to display the user's personal information
        return render_template('view_personal_info.html', user=user)
    else:
        flash('User not found.', 'danger')
        return redirect(url_for('main_routes.hr_dashboard'))

@main_routes.route('/apply_job/<int:job_id>')
def apply_job(job_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('You need to log in to apply for jobs.', 'danger')
        return redirect(url_for('main_routes.login'))

    # Get the user information
    user = User.query.filter_by(User_Email=session['user_id']).first()

    # Get the job to apply for
    job = Job.query.get(job_id)

    # Check if the user has already applied to this job
    if job and user and job not in user.applied_jobs:
        user.applied_jobs.append(job)
        db.session.commit()
        flash('Application submitted successfully.', 'success')
    else:
        flash('You have already applied to this job.', 'danger')

    return redirect(url_for('main_routes.jobs'))

@main_routes.route('/user_dashboard')
def user_dashboard():
    # Check if the user is logged in
    if 'user_id' not in session or (session['user_type'] != 'user' and session['user_type']!= 'admin'):
        print('You are not logged in.')
        flash('You need to log in to access the user dashboard.', 'danger')
        return redirect(url_for('main_routes.login'))

    # Get the user information
    user = User.query.filter_by(User_Email=session['user_id']).first()

    return render_template('user_dashboard.html', user=user)

@main_routes.route('/update_personal_info', methods=['GET', 'POST'])
def update_personal_info():
    # Check if the user is logged in
    if 'user_id' not in session or session['user_type'] != 'user':
        flash('You need to log in to update personal information.', 'danger')
        print('You need to log in to update personal information.')
        return redirect(url_for('main_routes.login'))

    # Get the user information
    user = User.query.filter_by(User_Email=session['user_id']).first()
    personal_info = Personal_Info.query.get(user.User_Info_ID)

    if request.method == 'POST':
        # Update the personal information based on the form data
        personal_info.Info_Salary = request.form.get('salary')
        personal_info.Info_Education = request.form.get('education')
        personal_info.Info_Experience = request.form.get('experience')
        personal_info.Info_Skills = request.form.get('skills')

        # Commit changes to the database
        db.session.commit()
        flash('Personal information updated successfully.', 'success')

    return render_template('update_personal_info.html', user=user, personal_info=personal_info)

# Register page
@main_routes.route('/register_company', methods=['GET', 'POST'])
def register_company():
    form = CompanyRegistrationForm()

    if form.validate_on_submit():
        # Check if the company already exists
        existing_company = Company.query.filter_by(Company_ID=form.Company_ID.data).first()

        if existing_company:
            flash('Company ID already exists. Please provide a unique Company ID.', 'danger')
        else:
            # Register the new company
            new_company = Company(
                Company_ID=form.Company_ID.data,
                Company_Name=form.Company_Name.data,
                Company_Location=form.Company_Location.data,
                Company_Description=form.Company_Description.data
            )
            db.session.add(new_company)
            db.session.commit()

            flash('Company registration successful.', 'success')
            print('Company registration successful.')
            return redirect(url_for('main_routes.index'))

    return render_template('register_company.html', form=form)

# Register page
@main_routes.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    # loggin check
    if 'user_id' in session:
        flash('You are already logged in.', 'danger')
        print('You are already logged in.')
        return redirect(url_for('main_routes.index'))
    
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        # Check if the admin already exists
        existing_admin = is_email_conflict(form.Admin_Email.data)

        if existing_admin:
            flash('Admin email already exists. Please provide a unique Admin Email.', 'danger')
            print('Admin email already exists. Please provide a unique Admin Email.')
            return redirect(url_for('main_routes.index'))
        else:
            # Register the new admin
            hashed_password = generate_password_hash(form.Admin_Password.data, method='pbkdf2:sha256', salt_length=8)
            print("New admin...")
            new_admin = Admin(
                Admin_Email=form.Admin_Email.data,
                Admin_Name=form.Admin_Name.data,
                Admin_Password=hashed_password
            )
            db.session.add(new_admin)
            db.session.commit()

            flash('Admin registration successful.', 'success')
            print('Admin registration successful.')
            return redirect(url_for('main_routes.index'))
    flash('Admin Invalid submit')
    return render_template('register_admin.html', form=form)

# Registration pages
@main_routes.route('/register_hr', methods=['GET', 'POST'])
def register_hr():
    # loggin check
    if 'user_id' in session:
        flash('You are already logged in.', 'danger')
        print('You are already logged in.')
        return redirect(url_for('main_routes.index'))

    form = HRRegistrationForm()
    if form.validate_on_submit():
        # Check if the HR already exists
        existing_hr = is_email_conflict(form.HR_Email.data)
        if existing_hr:
            flash('HR email already exists. Please provide a unique HR Email.', 'danger')
            print('HR email already exists. Please provide a unique HR Email.')
            return redirect(url_for('main_routes.register_hr'))

        # Check if the company exists
        existing_company = Company.query.filter_by(Company_ID=form.Company_ID.data).first()
        if not existing_company:
            flash('Company ID does not exist. Please provide a valid Company ID.', 'danger')
            print('Company ID does not exist. Please provide a valid Company ID.')
            return redirect(url_for('main_routes.register_company'))
        
        hashed_password = generate_password_hash(form.HR_Password.data, method='pbkdf2:sha256', salt_length=8)

        # generate a new HR id
        new_hr = HR(
            HR_Name=form.HR_Name.data,
            HR_Email=form.HR_Email.data,
            HR_Company_ID=form.Company_ID.data,
            HR_Password=hashed_password
        )
        db.session.add(new_hr)
        db.session.commit()
        print('HR registration successful.\n', HR.query.all()) # debug
        return redirect(url_for('main_routes.index'))

    return render_template('register_hr.html', form=form)

@main_routes.route('/register_user', methods=['GET', 'POST'])
def register_user():
    # loggin check
    if 'user_id' in session:
        flash('You are already logged in.', 'danger')
        print('You are already logged in.')
        return redirect(url_for('main_routes.index'))
    
    form = UserRegistrationForm()
    if form.validate_on_submit():
        print(form.User_Name.data, form.User_Email.data, form.User_Password.data)
        # Check if the user already exists
        existing_user = is_email_conflict(form.User_Email.data)

        if existing_user:
            flash('User email already exists. Please provide a unique User Email.', 'danger')
            print('User email already exists. Please provide a unique User Email.')
            return redirect(url_for('main_routes.register_user'))
        
        hashed_password = generate_password_hash(form.User_Password.data, method='pbkdf2:sha256', salt_length=8)

        # generate a new User id for personal information
        personal_info_id = len(User.query.all()) + 1
        new_personal_info = Personal_Info(
            Info_ID=personal_info_id,
            Info_Salary=0
        )
        db.session.add(new_personal_info)
        db.session.commit()

        # add the new user
        new_user = User(
            User_Name=form.User_Name.data,
            User_Email=form.User_Email.data,
            User_Password=hashed_password,
            User_Info_ID=personal_info_id
        )
        db.session.add(new_user)
        db.session.commit()
        print('User registration successful.\n', User.query.all())
        return redirect(url_for('main_routes.index'))
    
    return render_template('register_user.html', form=form)

# Login page
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(User_Email=form.User_Email.data).first()
        if user is None:
            user = HR.query.filter_by(HR_Email=form.User_Email.data).first()
            if user is None:
                user = Admin.query.filter_by(Admin_Email=form.User_Email.data).first()
        print("User is:", user)
        # if user and isinstance(user, Admin):
        #     if check_password_hash(user.Admin_Password, form.User_Password.data):
        #         session['user_id'] = user.Admin_Email
        #         session['user_type'] = 'admin'
        #         flash('Logged in successfully.', 'success')
        #         print('Logged in successfully.')
        #         print(session['user_id'], session['user_type'])
        #         return redirect(url_for('main_routes.index'))          

        try:
            if user and check_password_hash(user.User_Password, form.User_Password.data):
                session['user_id'] = user.User_Email
                session['user_type'] = 'user' if isinstance(user, User) else 'hr'
                flash('Logged in successfully.', 'success')
                print('Logged in successfully.')
                print(session['user_id'], session['user_type'])
                return redirect(url_for('main_routes.index'))
        except:
            try:
                if user and check_password_hash(user.HR_Password, form.User_Password.data):
                    session['user_id'] = user.HR_Email
                    session['user_type'] = 'user' if isinstance(user, User) else 'hr'
                    flash('Logged in successfully.', 'success')
                    print('Logged in successfully.')
                    print(session['user_id'], session['user_type'])
                    return redirect(url_for('main_routes.index'))
            except:
                if check_password_hash(user.Admin_Password, form.User_Password.data):
                    session['user_id'] = user.Admin_Email
                    session['user_type'] = 'admin'
                    flash('Logged in successfully.', 'success')
                    print('Logged in successfully.')
                    print(session['user_id'], session['user_type'])
                    return redirect(url_for('main_routes.index'))
        else:
            print(HR.query.all())
            print(User.query.all())
            print('Logged in NOT successfully.')
            flash('Invalid email or password.', 'danger')
    else:
        print("Error:", form)
    
    return render_template('login.html', form=form)

@main_routes.route('/logout')
def logout():
    if 'user_id' not in session:
        flash('You are not logged in.', 'danger')
        print('You are not logged in.')
        return redirect(url_for('main_routes.login'))
    # Clear user information from the session
    session.pop('user_id', None)
    session.pop('user_type', None)
    flash('Logged out successfully.', 'success')
    print('Logged out successfully.')
    return redirect(url_for('main_routes.index'))

# regitser email conflict check
def is_email_conflict(User_Email):
    # check if the email is already registered
    existing_user = User.query.filter_by(User_Email=User_Email).first()
    if existing_user:
        return True
    existing_hr = HR.query.filter_by(HR_Email=User_Email).first()
    if existing_hr:
        return True
    existing_admin = Admin.query.filter_by(Admin_Email=User_Email).first()
    if existing_admin:
        return True
    return False