# take in a file with just URL links.
# script will resolve the links and populate the final feed.

import os
import urllib
import requests
import re
import sys

from DataDto import DataDto

def parseLink (url):
    url = url.strip('\n')
    print("Examining url : " + str(url.strip('\n')))
    source = requests.get(url)
    match = re.search(r'<title>(.*?)</title>', source.text, re.IGNORECASE | re.DOTALL)
    title = None
    channel = None
    if match:
        title = match.group(1).strip()
    else:
        title = None
    channelRegex = re.search(r'\'video_uploader_name\' : \'(.*?)\'', source.text, re.IGNORECASE | re.DOTALL)
    if channelRegex:
        channel = channelRegex.group(1).strip()
    else:
        channel = None
    if channel == None or title == None:
        print ("Channel = " + str(channel) +", title = " + str(title))
        return None
    else:
        title = title.replace("\"", "") .replace("\'", "").replace(" ", "_")
        pattern = r'[^0-9a-zA-Z_-]'
        title = re.sub(pattern, '-', title)
        outputFilename = str(channel) + "_" + str(title)
        return DataDto(url, outputFilename, "MULTI_FILE")

if __name__ == "__main__":
    feedlines = list()
    file = open("input.txt", 'r')
    lines = file.readlines()
    for line in lines:
        dto = parseLink(line)
        if dto is not None:
            feedlines.append(dto.getRecord())
    file.close()

    feedfile = open("../feeds/feeds.txt", 'w')
    for f in feedlines:
        feedfile.write(f + "\n")
    feedfile.close()
