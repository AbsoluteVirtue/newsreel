import requests
import bs4


def get_rss(address):
    resource = requests.get(address)
    try:
        resource.raise_for_status()
    except Exception as exc:
        print("Error while downloading source page: {}".format(exc))
        return
    return bs4.BeautifulSoup(resource.text, "lxml")


def get_sslowdown_data():
    soup = get_rss("https://sslowdown.wordpress.com/feed/")
    articles = soup.select('item')
    data = {}
    for item in articles:
        url = item.link.next
        key = url[:(len(url) - 3)]
        data[key] = {}
        data[key]["title"] = item.title.text
        data[key]["date"] = item.pubdate.text
        data[key]["author"] = item.find('media:title', type="html").text
        data[key]["summary"] = item.find('content:encoded').text[:200]
        data[key]["text"] = item.find('content:encoded').text
        data[key]["source"] = item.find('content:encoded').a.attrs['href']
    return data
