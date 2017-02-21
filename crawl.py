import requests
import bs4
import datetime
from copy import deepcopy


def __get_image_from_source(url):
    """Hogs resources, too expensive to request each site's code and then parse it"""
    soup = __get_html(url)
    images = soup.select('img')
    checklist = ["gif", "png", "jpg"]
    if images:
        image_url = images[0].attrs['src']
        if image_url[-3:].lower() in checklist and image_url[:5].lower() != "http":
            return image_url
        else:
            return "http://ic.pics.livejournal.com/masio/8221809/287143/287143_original.gif"
    else:
        return "http://ic.pics.livejournal.com/masio/8221809/287143/287143_original.gif"


def __get_datetime(date):
    sliced_date = date[5:25]
    return datetime.datetime.strptime(sliced_date, '%d %b %Y %H:%M:%S')


def __build_post(text, source):
    return "{}<br><br>Original source: {}".format(text, source)


def __build_json_from_raw_data():
    raw_data = get_sslowdown_data()
    result = []
    entry = {}
    check_date = datetime.datetime(2017, 2, 15)
    for entry_key, entry_metadata in raw_data.items():
        entry_date = __get_datetime(entry_metadata["date"])
        if entry_date > check_date:
            entry["author"] = entry_metadata["author"]
            entry["date"] = entry_date
            entry["image"] = entry_metadata["image"]
            entry["summary"] = entry_metadata["summary"]
            entry["title"] = entry_metadata["title"]
            entry["text"] = __build_post(entry_metadata["text"], entry_metadata["source"])
            result.append(deepcopy(entry))
    return result


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
        text = item.find('content:encoded').text
        data[key]["text"] = text[:(len(text) - 4)]
        data[key]["source"] = item.find('content:encoded').a.attrs['href']
        data[key]["image"] = "http://ic.pics.livejournal.com/masio/8221809/287143/287143_original.gif"
    return data


# __build_json_from_raw_data()
