import zhipuai

zhipuai.api_key = ""

prompt = \
"""
Given a job applicant information and a list of job, find the best job for the applicant, and tell me the best 5 IDs.
For example, if you think the job with ID 1, ID 3, ID 5, ID 6 and ID 11 are the best, then you can return in the format &[1, 3, 5, 6, 11&]. Please only return in the given format.
Personal Information:
Salary: 10086
Education: Phd@家里蹲大学
Experience: 100000000
Skills: Eat a lot
Job Information:
Job 1:
Job Title: Happy Monster
Job Description: Be a Happy Monster
Job Salary: 4001234567
Job 2:
Job Title: CSC3002 Student
Job Description: Go learn C++
Job Salary: 0.5
Job 3:
Job Title: CSC3170 Student
Job Description: Go taking CSC3170
Job Salary: 0
"""

response = zhipuai.model_api.sse_invoke(
    model="chatglm_turbo",
    prompt=[
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "I am a AI assistant"},
        {"role": "user", "content": "I am a job search platform manager, I need your help in recommanding some jobs to the applicants"},
        {"role": "assistant", "content": "Please give me the information of applicants and jobs"},
        {"role": "user", "content": prompt},
    ],
    temperature=0.95,
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