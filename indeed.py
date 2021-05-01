from bs4 import BeautifulSoup
import requests

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&l=%EC%84%9C%EC%9A%B8&limit={LIMIT}"


def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')

    pagination = soup.find('div', {'class': 'pagination'})
    pages = pagination('a')
    pn = []
    for page in pages[:-1]:
        pn.append(int(page.string))

    last_page = pn[-1]
    return last_page


def extract_indeed_jobs(last_page):
    jobs = []
    # for page in range(last_page):
    result = requests.get(f"{URL}&start={0*LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    job_data = soup('div', {'class': 'jobsearch-SerpJobCard'})

    for job_row in job_data:
        title = job_row.find('h2').find('a')['title']
        company = job_row.find('div', {'class': 'sjcl'}).find(
            'span', {'class': 'company'}).get_text(strip=True)
        try:
            location = job_row.find('div', {'class': 'sjcl'}).find(
                'span', {'class': 'location'}).get_text(strip=True)
        except AttributeError:
            location = ''
        link = 'https://kr.indeed.com'+job_row.find('h2').find('a')['href']
        print(link)
