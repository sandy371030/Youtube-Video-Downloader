from pytube import Playlist, YouTube
from collections import defaultdict

import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty


def playlist(url):

    pl=Playlist(url)
    x = []
    for l in pl.video_urls:
        yt = YouTube(l)
        x.append(yt.title)
    return x,pl


def get_video(yt):

    streams = yt.streams.filter(progressive=True)
    streams_dict = defaultdict(list)
    j = 0
    for stream in streams:
        j += 1
        streams_dict[str(j)].append(stream.resolution)
        streams_dict[str(j)].append(stream.itag)

    resolution_list = []
    for iter, res in streams_dict.items(): 
        y = iter+". "+res[0]
        resolution_list.append(y)

    return (streams_dict, resolution_list)


def get_caption(yt):

    captions = yt.captions
    caption_dict = defaultdict(list)

    if not captions: return ["No Caption available"]

    else:
        i = 0
        for caption in captions:
            i += 1
            caption_dict[str(i)].append(caption.name)
            caption_dict[str(i)].append(caption.code)

        caption_list = []
        for iter, lang in caption_dict.items():
            x = iter+". "+lang[0]
            caption_list.append(x)

    return (caption_dict, caption_list)


def download_caption(yt, selected_caption):

    yt = YouTube(yt)
    caption_dict = get_caption(yt)[0]
    caption = yt.captions[caption_dict[selected_caption.split(".")[0]][1]]
    title = ''.join(i for i in yt.title if i.isalnum() or i.isspace())
    file = open(title+".srt", "w", encoding="utf-8")
    file.write(caption.generate_srt_captions())
    file.close()


def download_video(yt, selected_resolution):

    yt = YouTube(yt)
    streams_dict = get_video(yt)[0]
    stream = yt.streams.get_by_itag(streams_dict[selected_resolution.split(".")[0]][1])
    stream.download()


class Main(Screen):

    def single(self, url):

        try:
            yt = YouTube(url)
            self.manager.get_screen("b").title = yt.title
            self.manager.get_screen("b").invi = url
            self.manager.get_screen("b").img_link = yt.thumbnail_url
            self.manager.get_screen("b").cap_list = get_caption(yt)[1]
            self.manager.get_screen("b").res_list = get_video(yt)[1]

        except:
            self.manager.get_screen("b").title = "Invalid URL"
    

    def play(self , url):
        
        try:
            lst ,url_list = playlist(url)
            yt = YouTube(url_list[0])
            self.manager.get_screen("c").title = yt.title
            self.manager.get_screen("c").invi = url
            self.manager.get_screen("c").img_link = yt.thumbnail_url
            self.manager.get_screen("c").cap_list = get_caption(yt)[1]
            self.manager.get_screen("c").res_list = get_video(yt)[1]
            self.manager.get_screen("c").vdo_list = lst
        
        except:
            self.manager.get_screen("c").title = "Invalid URL"
    



class Single(Screen):

    title = StringProperty('')
    invi = StringProperty('')
    img_link = StringProperty('')
    cap_list = ListProperty([])
    res_list = ListProperty([])


    def download(self, yt_url, selected_resolution, selected_caption):
        
        download_caption(yt_url, selected_caption)
        download_video(yt_url, selected_resolution)


class Album(Screen):

    title = StringProperty('')
    invi = StringProperty('')
    img_link = StringProperty('')
    cap_list = ListProperty([])
    res_list = ListProperty([])
    vdo_list = ListProperty([])
    
    def all(self,url):
        p = Playlist(url)
        for video in p.videos:
            video.streams.first().download()
        

    def download(self, url, title, selected_resolution, selected_caption):

        lst ,url_list = playlist(url)
        idx = lst.index(title)
        selected_vdo = url_list[idx]

        download_caption(selected_vdo, selected_caption)
        download_video(selected_vdo, selected_resolution)
    
     
        
class Winmanager(ScreenManager):
    pass


kv = Builder.load_file("main.kv")


class YoutubeDownloaderApp(App):
    def build(self):
        return kv



if __name__== "__main__" :
    YoutubeDownloaderApp().run()  