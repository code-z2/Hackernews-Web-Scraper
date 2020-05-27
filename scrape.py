import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')

soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select(".storylink")
links2 = soup2.select(".storylink")
subtext = soup.select(".subtext")
subtext2 = soup2.select(".subtext")

mega_link = links + links2
mega_subtext = subtext + subtext2

def sort_stories_by_vote(hnlist):
    return sorted(hnlist, key=lambda x:x['votes'], reverse=True)

def create_custom_hacker_news(item, subtext):
    hn = []
    for idx, item in enumerate(item):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    print(len(hn))

    return sort_stories_by_vote(hn)

pprint.pprint(create_custom_hacker_news(mega_link, mega_subtext))
