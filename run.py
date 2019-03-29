from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import requests
import json
topic_home = {}
topic_python = {}
url = 'https://www.familug.org/search/'
labels = ['', 'label/Python', 'label/Command', 'label/sysadmin']
json_file = {"details": []}
for label in labels:
    # Xu ly trang home
    if label == '':
        ses_page =requests.session()
        req_page = ses_page.get(urljoin(url, label))
        soup_page = bs(req_page.text, 'html5lib')
        home_topics = soup_page.find_all('h3', class_=True)
        n = 0
        for topic in home_topics:
            if n == 10:
                break
            else:
                title_home_topic = str(topic.a.contents)[2:-2]
                link_home_topic = topic.a['href']
                json_home = {"tag": "home", "title": str(title_home_topic), "link": str(link_home_topic)}
                json_file['details'].append(json_home)
                n += 1
    else:
        # Xu ly cac trang co label
        link_page = ''
        while True:
            try:
                ses = requests.session()
                req = ses.get('https://www.familug.org/search/{}{}'.format(label, link_page))
                a = 'https://www.familug.org/search/{}{}'.format(label, link_page)
                soup = bs(req.text, 'html5lib')
                topics_main = soup.find_all('h3', class_=True)
                for topic_main in topics_main:
                    title = str(topic_main.a.contents)[2:-2]
                    link = topic_main.a['href']
                    if label[6:] == 'Python':
                        json_python = {"tag": "python", "title": str(title), "link": str(link)}
                        json_file['details'].append(json_python)
                    elif label[6:] == 'Command':
                        json_command = {"tag": "command", "title": str(title), "link": str(link)}
                        json_file['details'].append(json_command)
                    elif label[6:] == 'sysadmin':
                        json_sysadmin = {"tag": "sysadmin", "title": str(title), "link": str(link)}
                        json_file['details'].append(json_sysadmin)
                select_page = soup.find('a', class_='blog-pager-older-link')
                page = str(select_page['href'])
                next_page = page[(page.index('?')):]
                link_page = next_page
            except TypeError:
                break
with open('familug.json', 'w', encoding='utf-8') as f:
    json.dump(json_file, f, ensure_ascii=False, indent=4)