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


def extractData(url: str, channelName:str, parentUrl : str, mode : str):
    dataDtoList = []
    source = requests.get(url)
    if "Error Page Not Found" in source.text:
        print ("Page does not exist.[ " + url + " ]. Exiting")
        return []
    results = re.findall("<a href=\"(/view_video.php\\?viewkey\\=[a-zA-Z0-9]+)\"\\stitle\\=(.*)\"\\sclass", source.text,
                         0)
    for result in results:
        title = result[1].replace("\"", "") .replace("\'", "").replace(" ", "_")
        pattern = r'[^0-9a-zA-Z_-]'
        processed= re.sub(pattern, '-', title)
        dataDtoList.append(DataDto(parentUrl + result[0], channelName + "\\" + channelName + "_" +processed, mode))
    return dataDtoList


def writeInputFile(dataDtoList: set, feed_file_name : str):
    os.makedirs("../feeds", exist_ok=True)
    f = open("../feeds/" + feed_file_name, 'w', encoding='UTF-8')
    pattern = r'[^0-9a-zA-Z_-]'
    for dto in dataDtoList:
        f.write(dto.getRecord() + "\n")
    f.close()


if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("[ERROR] Incorrect number of arguments. Current length is "+ str(len(sys.argv)))
        print("[INFO] Example command : ")
        print("[INFO] python model1.py <url> <channelname> <parentUrl> <strategyMode> <feed_file_name>")
        print("[INFO] e.g: python model1.py \"http://url.com/media\" \"channelName\" \"http://url.com\" \"MULTI_FILE\" \"input.txt\"")

        sys.exit(1)
    url = sys.argv[1]                   # not including the "?page=" query param
    channelName = sys.argv[2]           # the channel name
    parentUrl = sys.argv[3]             # .com domain
    strategyMode = sys.argv[4].upper()  # MULTI_FILE
    feed_file_name = sys.argv[5]        # output feed file name (to be placed in ../feeds folder
    totalList = []
    for i in range(1,5):
        linkData = extractData(url + "?page="+str(i), channelName, parentUrl, strategyMode)
        if len(linkData) == 0:
            break
        else:
            for j in linkData:
                totalList.append(j)
    filteredSet = set(totalList)
    writeInputFile(filteredSet, feed_file_name)
