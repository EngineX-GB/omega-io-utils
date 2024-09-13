from bs4 import BeautifulSoup
import requests
import re
import sys
import os

from DataDto import DataDto


def getLinks(channelname, content, parenturl, free):
    links = list()
    soup = BeautifulSoup(content, 'html.parser')
    videos = soup.findAll('li', attrs={'class': 'pcVideoListItem'})
    for v in videos:
        link = v.a['href']
        title = v.a['title']
        if free:
            freeblock = v.findAll('span', attrs={'class', 'phpFreeBlock'})
            if len(freeblock) > 0:
                title = title.replace("\"", "").replace("\'", "").replace(" ", "_")
                pattern = r'[^0-9a-zA-Z_-]'
                processed = re.sub(pattern, '-', title)
                links.append(DataDto(parenturl + link, channelname + "_"  +processed, "MULTI_FILE"))

        else:
            title = title.replace("\"", "").replace("\'", "").replace(" ", "_")
            pattern = r'[^0-9a-zA-Z_-]'
            processed = re.sub(pattern, '-', title)
            links.append(DataDto(parenturl + link, channelname + "_"  +processed, "MULTI_FILE"))

    return links

def writeInputFile(dataDtoList: set):
    os.makedirs("../feeds", exist_ok=True)
    f = open("../feeds/input.txt", 'w', encoding='UTF-8')
    pattern = r'[^0-9a-zA-Z_-]'
    for dto in dataDtoList:
        f.write(dto + "\n")
    f.close()


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("[ERROR] Length of arguments is 1")
        print("Example command : ")
        print("python model2.py <channel_name> <parentUrl> <full_url>")
        print("e.g.")
        print("python model2.py \"channelname\" \"http://www.url.com\" \"http://www.url.com/channel/videos\"")
        system.exit(1)

    max_pages = 2
    records = set()
    channel = sys.argv[1]
    parentUrl = sys.argv[2] # "https://www.url.com"
    isFree = False
    url = sys.argv[3] # "https://www.url.com/modl/<channel_name>/videos/upload"
    for i in range(1, max_pages):
        pageUrl = url+ "?page=" + str(i)
        res = requests.get(pageUrl)
        if "Error Page Not Found" in res.text:
            print("Page does not exist.[ " + pageUrl + " ]. Exiting")
            break
        lines = getLinks(channel, res.content, parentUrl, isFree)
        if len(lines) == 0:
            print("No links were identified for page " + str(i) + ". Terminating.")
            break
        for line in lines:
            records.add(line.getRecord())

    writeInputFile(records)