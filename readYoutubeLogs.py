import json
from pprint import pprint

#if an ad shows, are any of the video playbacks the actual video?
with open("youtube_logs.txt") as f:
    for entry in f:
        jsonEntry = json.loads(entry)
        try:
            url = jsonEntry["message"]["params"]["request"]["url"]
        except KeyError:
            continue

        if "videoplayback" in url:
            print(url)