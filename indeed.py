from bs4 import BeautifulSoup
import requests


def extract_pn(url):
    result = requests.get(url)
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
    try:
        company = job_row.find('div', {'class': 'sjcl'}).find(
            'span', {'class': 'company'}).get_text(strip=True)
    except:
        company = None
    location = job_row.find('div', {'class': 'recJobLoc'})['data-rc-loc']
    link = 'https://kr.indeed.com'+job_row.find('h2').find('a')['href']
    return {'title': title, 'company': company, 'location': location, 'link': link}


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed Page: {page+1}")
        result = requests.get(f"{url}&start={page*50}")
        soup = BeautifulSoup(result.text, 'html.parser')
        job_data = soup('div', {'class': 'jobsearch-SerpJobCard'})

        for job_row in job_data:
            job = extract_job_info(job_row)
            jobs.append(job)
    return jobs


def get_indeed_jobs(word):
    url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and={word}&l=%EC%84%9C%EC%9A%B8&limit=50"
    last_page = extract_pn(url)
    jobs = extract_jobs(last_page, url)
    print(f"Total: {len(jobs)} jobs")
    return jobs
