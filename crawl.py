import requests
import bs4


def __get_html(url):
    resource = requests.get(url)
    try:
        resource.raise_for_status()
    except Exception as exc:
        print("Error while downloading source page: {}".format(exc))
        return
    return bs4.BeautifulSoup(resource.text, "lxml")


def get_sslowdown_data():
    soup = __get_html("https://sslowdown.wordpress.com/feed/")
    articles = soup.select('item')
    data = {}
    for item in articles:
        link = item.link.next
        key = link[:(len(link) - 3)]
        data[key] = {}
        data[key]["title"] = item.title.text
        data[key]["date"] = item.pubdate.text
        data[key]["author"] = item.find('media:title', type="html").text
        summary = item.find('content:encoded').text[:200]
        data[key]["summary"] = summary[:(len(summary) - 4)]
        data[key]["text"] = str(item.find('content:encoded').next)
        data[key]["source"] = item.find('content:encoded').a.attrs['href']
        data[key]["image"] = "http://ic.pics.livejournal.com/masio/8221809/287143/287143_original.gif"
    return data
