def perform_smart_search(personal_info, jobs, max_result=5):
    # personal info
    info_salary = personal_info.Info_Salary
    info_education = personal_info.Info_Education
    info_experience = personal_info.Info_Experience
    info_skills = personal_info.Info_Skills

    # jobs
    jobs_list = []
    for j in jobs:
        job_title = j.Job_Title
        job_description = j.Job_Description
        job_salary = j.Job_Salary

        jobs_list.append({
            'job_id': j.Job_ID,
            'job_title': job_title,
            'job_description': job_description,
            'job_salary': job_salary,
        })

    # print
    print('info_salary: ', info_salary)
    print('info_education: ', info_education)
    print('info_experience: ', info_experience)
    print('info_skills: ', info_skills)
    print('jobs_list: ', jobs_list)

    # concat all text into a prompt
    prompt = ''
    personal_information = f"Personal Information:\nSalary: {info_salary}\nEducation: {info_education}\nExperience: {info_experience}\nSkills: {info_skills}\n"
    prompt += personal_information

    job_information = 'Job Information:\n'
    for i, job in enumerate(jobs_list):
        job_information += f"Job {i+1}:\nJob Title: {job['job_title']}\nJob Description: {job['job_description']}\nJob Salary: {job['job_salary']}\n"
    
    prompt += job_information

    prompt_start = "Given a job applicant information and a list of job, find the best job for the applicant, and tell me the best 5 IDs.\n"
    prompt_example = "For example, if you think the job with ID 1, ID 3, ID 5, ID 6 and ID 11 are the best, then you can return [1, 3, 5, 6, 11].\n"
    
    prompt = prompt_start + prompt_example + prompt
    print('prompt:')
    print(prompt)