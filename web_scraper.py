import requests
from bs4 import BeautifulSoup

def checkIfExsits(title):
    url = 'https://en.wikipedia.org/api/rest_v1/page/html/' + title
    title_code = requests.get(url).status_code
    if title_code == 200:
        return True
    else:
        return False


def getAllUrl(title):

    url = 'https://en.wikipedia.org/api/rest_v1/page/html/' + title

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    linklist = set()

    for link in soup.find_all("a", href=True):
        #cut a tag down to link
        link = str(link)
        linkstart = link.find('href="') + 6
        linkend = link.find('"', linkstart)
        link = link[linkstart: linkend]
        #filter only wiki links and no general wiki pages ':'
        if (link[:2] == './') and link.find(":") == -1:
            #remove all hashes and on page links
            if link.find('#') != -1:
                link = link[:link.find('#')]
            linklist.add(link[2:])
    return linklist

# ll = getAllUrl("Flour")
# print(ll)
# if("Mixer_(cooking)" in ll):
#     print("Found it")


def getAllBackLinks(title):
    #Code partly from https://www.mediawiki.org/wiki/API:Backlinks
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action":"query",
        "format":"json",
        "list":"backlinks",
        "bltitle":"{}".format(title),
        "bllimit": "max"
    }

    res = S.get(url=URL, params=PARAMS)
    DATA = res.json()

    backlinks = []

    for page in DATA["query"]["backlinks"]:
        backlinks.append(page["title"])
    
    return backlinks








def getAllUrlOld(urls):

    url = 'https://en.wikipedia.org/' + urls

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    linklist = set()

    for link in soup.find_all("a", href=True):
        #cut a tag down to link
        link = str(link)
        linkstart = link.find('href="') + 6
        linkend = link.find('"', linkstart)
        link = link[linkstart: linkend]
        #filter only wiki links and no general wiki pages ':'
        if (link[:5] == '/wiki') and link.find(":") == -1:
            #remove all hashes and on page links
            if link.find('#') != -1:
                link = link[:link.find('#')]
            linklist.add(link)
    return linklist



