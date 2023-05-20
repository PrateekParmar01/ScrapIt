from bs4 import BeautifulSoup
import time
import requests
import csv

print("Put some skills your are not familiar with")
unfamiliar_skills = input('>')
print(f"Filtering Out {unfamiliar_skills}")
seen=set()
def find_jobs():
  csv.register_dialect('escaped', escapechar='\\', doublequote=True, quoting=csv.QUOTE_ALL)
  html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=&cboWorkExp1=0').text
  soup = BeautifulSoup(html_text, 'lxml')
  jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
  filename = f"{unfamiliar_skills} jobs in TimesJob.csv"
  with open(filename, "w", newline='') as myfile:
    spamWriter = csv.writer(myfile, dialect='excel')
    spamWriter.writerow(["Company","Skills","More Info"])
    for job in jobs:
      published_date = job.find('span', class_ = 'sim-posted').span.text
      if 'few' in published_date:
        company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ','')
        skills = job.find('span', class_='srp-skills').text.replace(' ','')
        more_info = job.header.h2.a['href']
        if unfamiliar_skills not in skills:
          l=[str(company_name.strip()), str(skills.strip()), str(more_info.strip())]
          if l[1] not in seen:
                spamWriter.writerow(l)
                seen.add(l[1])
          print(f"Company Name : {company_name.strip()}")
          print(f"Skills : {skills.strip()}")
          print(f"More Info : {more_info}\n")


if __name__ =='__main__':
  # while True:
    find_jobs()
    # print(f"Waiting {time_wait } minutes....")
    # time.sleep(time_wait * 60)
