import re

import zhipuai
zhipuai.api_key = ""

def get_response(prompt):
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_turbo",
        prompt=[
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "I am a AI assistant"},
            {"role": "user", "content": "I am a job search platform manager, I need your help in recommanding some jobs to the applicants, I also need you to give me response in the given format. No other words are allowed."},
            {"role": "assistant", "content": "Please give me the information of applicants and jobs, and I will answer you with the best 5 job IDs in the given format, without any other words."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.00,
        top_p=0.7,
        incremental=True
    )

    r = ""
    for event in response.events():
        if event.event == "add":
            print(event.data)
            try:
                r += str(event.data)
            except:
                print("error", type(event.data))
                pass
        elif event.event == "error" or event.event == "interrupted":
            print(event.data)
        elif event.event == "finish":
            print(event.data)
            print(event.meta)
        else:
            print(event.data)
    print(r)
    return r

def extract_content(input_string):
    pattern = r'&\[(.*?)&\]'
    matches = re.findall(pattern, input_string)
    return matches

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

        # compare job_salary with info_salary
        if job_salary <= info_salary*0.75 or job_salary >= info_salary*1.25:
            continue

        jobs_list.append({
            'job_id': j.Job_ID,
            'job_title': job_title,
            'job_description': job_description,
            'job_salary': job_salary,
        })

    sorted_jobs_list = sorted(jobs_list, key=lambda x: x['job_salary'], reverse=True)
    max_prompted = 10
    if len(sorted_jobs_list) > max_prompted:
        jobs_list = sorted_jobs_list[:max_prompted]

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
    prompt_example = "For example, if you think the job with ID 1, ID 3, ID 5, ID 6 and ID 10 are the best, then you can return &[1, 3, 5, 6, 10&].\n"
    prompt_example += "Please only return in the given format.\n"
    
    prompt = prompt_start + prompt_example + prompt
    print('prompt:')
    print(prompt)
    print(len(jobs_list))

    # get response
    response = get_response(prompt)
    print('response:')
    print(response)


    result = extract_content(response)
    print('DEBUG::result:')
    print(result, type(result))
    result = eval(result[0])
    print(result, type(result))

    job_ids = []

    print('DEBUG::job_ids:')
    for i in range(len(result)):
        job_ids.append(jobs_list[result[i]-1]['job_id'])
        print(jobs_list[result[i]-1]['job_id'], jobs_list[result[i]-1]['job_title'])

    return job_ids