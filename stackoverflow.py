from bs4 import BeautifulSoup
import requests

URL = "https://stackoverflow.com/jobs?q=python"


def extract_pn():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find('div', {'class': 's-pagination'})
    pages = pagination('a')
    pn = []
    for page in pages:
        pn.append(page.find('span').string)
    last_page = int(pn[-2])
    return last_page


def extract_job_info(job_row):
    title = job_row.find('h2', {'class': 'mb4'}).find('a')['title']
    company = job_row.find('h3').find('span').get_text(strip=True)
    location = company = job_row.find('h3').find('span', {'class':
                                                          'fc-black-500'}).get_text(strip=True)
    link = 'https://stackoverflow.com' + \
        job_row.find('h2', {'class': 'mb4'}).find('a')['href']
    return {'title': title, 'company': company, 'location': location, 'link': link}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping StackOverflow Page: {page+1}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, 'html.parser')
        job_data = soup('div', {'class': 'grid--cell fl1'})
        for job_row in job_data:
            job = extract_job_info(job_row)
            jobs.append(job)
    return jobs


def get_so_jobs():
    last_page = extract_pn()
    jobs = extract_jobs(last_page)
    print(f"Total: {len(jobs)} jobs")
    return jobs
