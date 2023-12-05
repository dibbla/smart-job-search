import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import CompanyRegistrationForm, HRRegistrationForm, UserRegistrationForm, LoginForm, \
    PostPositionForm
from .models import db, Company, HR, User, Personal_Info, Job, job_application

main_routes = Blueprint('main_routes', __name__)
# Main page
@main_routes.route('/')
def index():
    return render_template('index.html')

# display all the jobs
@main_routes.route('/jobs')
def jobs():
    jobs = Job.query.all()
    print(jobs)
    return render_template('jobs.html', jobs=jobs)

# dashboard page
# In dash board, HR can see and delete the jobs posted by him/her
# In dash board, user can see and apply the jobs
@main_routes.route('/hr_dashboard')
def hr_dashboard():
    # Check if the user is logged in and is an HR
    if 'user_id' not in session or session['user_type'] != 'hr':
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

    return redirect(url_for('main_routes.index'))

@main_routes.route('/user_dashboard')
def user_dashboard():
    # Check if the user is logged in
    if 'user_id' not in session or session['user_type'] != 'user':
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
        existing_hr = HR.query.filter_by(HR_Email=form.HR_Email.data).first()
        if existing_hr:
            flash('HR ID already exists. Please provide a unique HR Email.', 'danger')
            print('HR ID already exists. Please provide a unique HR Email.')
            return redirect(url_for('main_routes.register_hr'))
        
        # Check if the user already exists
        existing_user = User.query.filter_by(User_Email=form.HR_Email.data).first()
        if existing_user:
            flash('HR ID already exists. Please provide a unique HR Email.', 'danger')
            print('HR ID already exists. Please provide a unique HR Email.')
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
        # Check if the user already exists
        existing_user = User.query.filter_by(User_Email=form.User_Email.data).first()
        if existing_user:
            flash('User ID already exists. Please provide a unique User Email.', 'danger')
            print('User ID already exists. Please provide a unique User Email.')
            return redirect(url_for('main_routes.register_user'))
        
        # check if the HR already exists
        existing_hr = HR.query.filter_by(HR_Email=form.User_Email.data).first()
        if existing_hr:
            flash('User ID already exists. Please provide a unique User Email.', 'danger')
            print('User ID already exists. Please provide a unique User Email.')
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
        print("User is:", user)
        try:
            if user and check_password_hash(user.User_Password, form.User_Password.data):
                session['user_id'] = user.User_Email
                session['user_type'] = 'user' if isinstance(user, User) else 'hr'
                flash('Logged in successfully.', 'success')
                print('Logged in successfully.')
                return redirect(url_for('main_routes.index'))
        except:
            if user and check_password_hash(user.HR_Password, form.User_Password.data):
                session['user_id'] = user.HR_Email
                session['user_type'] = 'user' if isinstance(user, User) else 'hr'
                flash('Logged in successfully.', 'success')
                print('Logged in successfully.')
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
