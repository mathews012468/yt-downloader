from email.mime import audio
from selenium import webdriver
import json
from pprint import pprint
import urllib.parse
import subprocess


def reformat_link(url):
    """
    Delete range, rn, and rbuf parameters from a video playback link
    This gives the whole video instead of just the snippet determined
    by range and rbuf.

    url: str?
    return: str?
    """
    if url is None:
        return
    
    parsed_url = urllib.parse.urlparse(url)
    query_dict = urllib.parse.parse_qs(parsed_url.query)

    #rewrite each value as a string instead of a list
    #this makes converting back to a query string 
    #more consistent with the original parameters
    query_dict = {key: value[0] for key, value in query_dict.items()}

    #delete problematic parameters to get whole video instead of snippet
    query_dict.pop("range")
    query_dict.pop("rn")
    query_dict.pop("rbuf")

    query_string = urllib.parse.urlencode(query_dict)
    #everything is the same as the original link except the query_string
    return urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, query_string, parsed_url.fragment))

def get_network_activity(youtube_url):
    """
    Get all network activity from a youtube video
    youtube_url: str
    return: list
    """
    #stack overflow answer that showed me how to get network requests from selenium: https://stackoverflow.com/a/65538568
    chrome_options = webdriver.ChromeOptions()
    chrome_options.set_capability(
                            "goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"}
                        )
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(youtube_url)

    #all network activity, including the video source links
    log_entries = driver.get_log("performance")
    driver.close()
    return log_entries

def get_audio_and_video_from_network(log_entries):
    """
    Find audio and video links from browser performance logs

    log_entries: list
    return: str?, str?
    """
    # # to save the log entries for later analysis
    # with open("youtube_logs.txt", "w") as f:
    #     for entry in log_entries:
    #         f.write(entry["message"])
    #         f.write("\n")

    #the following code assumes the videoplayback links for the actual video
    #are the first ones that appear in network
    #this appears to always be the case, but of course it's a big assumption
    video_link = None
    audio_link = None
    for entry in log_entries:
        try:
            obj_serialized: str = entry["message"]
            obj = json.loads(obj_serialized)
            url = obj["message"]["params"]["request"]["url"]
        except KeyError:
            #if any of the above keys fail, move on to the next entry
            continue
        
        #if it's not one of the links fetching video, move on to next entry
        #there is always a possiblility that this includes the ad links
        #install adblock on whatever machine I deploy this on to avoid the ads
        #ublock origin is currently working for me
        if "videoplayback" not in url:
            continue

        #videoplayback urls have parameters mime=audio/webm, video/webm
        query_params = urllib.parse.urlparse(url).query
        mime_type = urllib.parse.parse_qs(query_params)["mime"]
        #parse_qs puts values in a list, so we want the first item
        if "audio" in mime_type[0]: 
            audio_link = url
        elif "video" in mime_type[0]:
            video_link = url

        #this means we found both links, so we can exit
        if audio_link is not None and video_link is not None:
            break
    
    return audio_link, video_link


def get_audio_and_video_links(youtube_url):
    """
    Get links to source audio and video from a youtube video

    youtube_url: str
    return: str?, str? 
    """

    log_entries = get_network_activity(youtube_url)
    audio_link, video_link = get_audio_and_video_from_network(log_entries)
    
    #reformat gets rid of parameters limiting video to just a snippet
    #this allows us to get the entire video
    return reformat_link(audio_link), reformat_link(video_link)


def main():
    url = "https://www.youtube.com/watch?v=uAPUkgeiFVY"
    audio_link, video_link = get_audio_and_video_links(url)

    print(audio_link, video_link, sep="\n\n")

    #download audio and video using above links
    subprocess.run(["curl", "-o", "youtubeFiles/audio.webm", audio_link, "-o", "youtubeFiles/video.webm", video_link])

    #combine them using ffmpeg
    #I adapted this command from https://superuser.com/a/277667, under the heading "Copying the audio without re-encoding"
    subprocess.run(["ffmpeg", "-i", "youtubeFiles/audio.webm", "-i", "youtubeFiles/video.webm", "-c", "copy", "-y", "youtubeFiles/output.webm"])

if __name__ == "__main__":
    main()