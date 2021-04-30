from bs4 import BeautifulSoup
import requests

indeed_result = requests.get(
    "https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&l=%EC%84%9C%EC%9A%B8&limit=50")

indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')

pagination = indeed_soup.find('div', {'class': 'pagination'})
pages = pagination('a')

print(pages)
