from bs4 import BeautifulSoup
import requests

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&l=%EC%84%9C%EC%9A%B8&limit={LIMIT}"


def extract_pn():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find('div', {'class': 'pagination'})
    pages = pagination('a')
    pn = []
    for page in pages[:-1]:
        pn.append(int(page.string))

    last_page = pn[-1]
    return last_page


def extract_job_info(job_row):
    title = job_row.find('h2').find('a')['title']
    company = job_row.find('div', {'class': 'sjcl'}).find(
        'span', {'class': 'company'}).get_text(strip=True)
    location = job_row.find('div', {'class': 'recJobLoc'})['data-rc-loc']
    link = 'https://kr.indeed.com'+job_row.find('h2').find('a')['href']
    return {'title': title, 'company': company, 'location': location, 'link': link}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed Page: {page+1}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        job_data = soup('div', {'class': 'jobsearch-SerpJobCard'})

        for job_row in job_data:
            job = extract_job_info(job_row)
            jobs.append(job)
    return jobs


def get_indeed_jobs():
    last_page = extract_pn()
    jobs = extract_jobs(last_page)
    print(f"Total: {len(jobs)} jobs")
    return jobs
