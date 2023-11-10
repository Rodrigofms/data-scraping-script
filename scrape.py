"""Importação das bibliotecas necessárias"""
import pprint
import requests
from bs4 import BeautifulSoup


res = requests.get("https://news.ycombinator.com/news", timeout=10)
res2 = requests.get("https://news.ycombinator.com/news?p=2", timeout=10)
soup = BeautifulSoup(res.text, "html.parser")
soup2 = BeautifulSoup(res2.text, "html.parser")


links = soup.select(".titleline > a")
subtext = soup.select(".subtext")
links2 = soup2.select(".titleline > a")
subtext2 = soup2.select(".subtext")

mega_links = links + links2
mega_subtext = subtext + subtext2


def sort_news(hnlist):
    """Organiza os posts por pontos"""
    return sorted(hnlist, key=lambda k: k["votes"], reverse=True)


def custom_news(link, sub):
    """Customiza para retornar com apenas os posts com no mínimo 100 pontos"""
    hn = []
    for index, item in enumerate(link):
        title = item.getText()
        href = item.get("href", None)
        vote = sub[index].select(".score")
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points >= 100:
                hn.append({"title": title, "link": href, "votes": points})
    return sort_news(hn)


pprint.pprint(custom_news(mega_links, mega_subtext))
