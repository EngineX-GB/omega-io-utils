import os
import requests
import re
import sys

class DataDto:

    def __init__(self, link, outputFileName, strategyMode):
        self.link = link
        self.outputFileName = outputFileName
        self.strategyMode = strategyMode

    def getLink(self):
        return self.link

    def getOutputFileName(self):
        return self.outputFileName

    def getStrategyMode(self):
        return self.strategyMode

    def getRecord(self):
        return ((self.outputFileName + "|" + self.strategyMode + "|" + self.link))



def extractData(url : str, mode : str):
    source = requests.get(url)
    file_pattern = r'<source\s+src="([^"]+)"'
    file_matches = re.findall(file_pattern, source.text)
    file = ""
    title = ""
    if file_matches:
        file = file_matches[0]

    title_pattern = r'<title>(.*?)</title>'
    title_matches = re.findall(title_pattern, source.text)
    if title_matches:
        title = title_matches[0]

    if title is not None and file is not None:

        new_title = title.replace("\"", "") .replace("\'", "").replace(" ", "_")
        processed_title_pattern = r'[^0-9a-zA-Z_-]'
        processed_title= re.sub(processed_title_pattern, '-', new_title)
        print("[DEBUG] Preparing DataDTO for asset : " + file)
        return DataDto(file, processed_title, mode)
def extractUrlPageLinks(url: str):
    url_list = []
    source = requests.get(url)
    if "Sorry, but you are looking for something that isn't here." in source.text:
        print ("Page does not exist.[ " + url + " ]. Exiting")
        return []
    # Regular expression to capture <h2><a> tag and extract url, title and text.
    pattern = r'<h2><a href="(.*?)" rel="bookmark" title="(.*?)">(.*?)</a></h2>'

    matches = re.findall(pattern, source.text)

    for match in matches:
        _url, _title, _text = match
        url_list.append(_url)
    return url_list


def writeInputFile(dataDtoList: set, feed_file_name : str):
    os.makedirs("../feeds", exist_ok=True)
    f = open("../feeds/" + feed_file_name, 'w', encoding='UTF-8')
    pattern = r'[^0-9a-zA-Z_-]'
    for dto in dataDtoList:
        f.write(dto.getRecord() + "\n")
    f.close()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("[ERROR] Incorrect number of arguments. Current length is "+ str(len(sys.argv)))
        print("[INFO] Example command : ")
        print("[INFO] python model4.py <hostname> <name search> <strategyMode> <feed_file_name>")
        print("[INFO] e.g: python model4.py \"http://url.com\" \"joe bloggs\" \"SINGLE\" \"input.txt\"")

        sys.exit(1)
    hostname = sys.argv[1]                   # including the "?page=" query param
    search_query = sys.argv[2].replace(" ", "+")              # search query
    strategyMode = sys.argv[3].upper()  # MULTI_FILE
    feed_file_name = sys.argv[4]        # output feed file name (to be placed in ../feeds folder
    totalList = []

    startPage = hostname + "/page/1/?s=" + search_query
    print("[INFO] Starting URL : " + startPage)

    for i in range(25,26):
        linkData = extractUrlPageLinks(hostname + "/page/" + str(i) + "/?s=" + search_query)
        if len(linkData) == 0:
            break
        else:
            for j in linkData:
                totalList.append(j)

    distinct_url_list = set(totalList)

    # for each link collected, then get the asset/ media link

    assetLinksList = []

    for url in distinct_url_list:
        print("[INFO] Extracting link for [" + url + "]")
        assetLinksList.append(extractData(url, strategyMode))

    writeInputFile(assetLinksList, feed_file_name)
