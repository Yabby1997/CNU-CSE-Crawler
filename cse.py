import requests
from bs4 import BeautifulSoup
import json
import os

notice_url = 'https://computer.cnu.ac.kr/computer/notice/project.do?mode=list&&articleLimit=10&article.offset='
notice_selector = 'tr > td.b-td-left > div > a'

data = {}

for i in range(5):
	offset = 10 * i
	req = requests.get(notice_url + str(offset))
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	notices = soup.select(notice_selector)	
	for notice in notices:
		title = notice.get('title')
		print(title)

