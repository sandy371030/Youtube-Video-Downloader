#!/usr/bin/env python3
import re
import pyfiglet
from pytube import Playlist, YouTube
from collections import defaultdict


def get_video(yt):
    # Fetch All Progressive Streams:
    streams = yt.streams.filter(progressive=True)
    streams_dict = defaultdict(list)
    j = 0
    for stream in streams:
        j += 1
        streams_dict[str(j)].append(stream.resolution)
        streams_dict[str(j)].append(stream.itag)

    # Print The Available Video Resolution:
    for iter, res in streams_dict.items(): print(iter+".", res[0])

    # Based On Selected Resolution Download Will Begin...
    selected_resolution = str(input("SELECT ANY RESOLUTION FROM ABOVE LIST: "))
    stream = yt.streams.get_by_itag(streams_dict[selected_resolution][1])
    print("Downloading Please wait...")
    stream.download()
    print("Download Completed Successfully.")


def get_caption(yt):
    # Get The Title Of The Video:
    title = yt.title

    # Remove All The Characters Other Than AlphaNumerical:
    try:
        title = re.sub("[^a-zA-Z0-9]+"," ", title) # Using RegExp.
    except:
        title = ''.join(i for i in title if i.isalnum() or i.isspace()) # Without using RegExp.

    # Get All The Available Captions:
    captions = yt.captions
    caption_dict = defaultdict(list)

    if not captions: print("No Captions Available.")

    else:
        i = 0
        for caption in captions:
            i += 1
            caption_dict[str(i)].append(caption.name)
            caption_dict[str(i)].append(caption.code)

        # Print All Available Captions:
        for iter, lang in caption_dict.items(): print(iter+".",lang[0])

        # Based on Selected caption Download will begin...
        selected_caption = str(input("SELECT ANY CAPTIONS FROM ABOVE LIST: "))
        caption = yt.captions[caption_dict[selected_caption][1]]

        # Create A New File With The Name of Title And Write Selected Caption Data Into This File.
        file = open(title+".srt", "w", encoding="utf-8")
        file.write(caption.generate_srt_captions())
        file.close()


def single(video_url):
    yt = YouTube(video_url)
    get_caption(yt)
    get_video(yt)


def playlist(playlist_url):
    pl = Playlist(playlist_url)
    for url in pl.video_urls:
        single(url)


def main():
    
    try:
        # If Pyfiglet Module Is Installed Run This.
        banner = pyfiglet.figlet_format("YOUTUBE \nDOWNLOADER")
        print(banner)
    except:
        # Incase, If Pyfiglet Module Not Installed.
        print("Welcome to Youtube Downloader!")

    video_or_playlist = input("Do you want to download Single Video or Playlist?\n\t1. single Video \n\t2. Playlist\n")
    
    if video_or_playlist == "1":
        video_url = input("Enter Video URL: ")
        single(video_url)
        # single("https://youtu.be/H2vN2QXZGnc")

    elif video_or_playlist == "2": 
        playlist_url = input("Enter Playlist URL: ")
        playlist(playlist_url)
        # playlist("https://youtube.com/playlist?list=PLsyeobzWxl7rXr9qxVZPbaoU7uUqP7iPM")
    
    else:
        decision = input("You Selected an Invalid Option. Do You Want To \n1. Try Again \n\tor \n2.Exit:")
        if decision == "1":
            main()
        elif decision == "2":
            print("See You Later...")
            exit()
        else:
            print("Invalid Option. Bye!")
            exit()


main()
