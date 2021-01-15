#Some functions for XTueb_load
#By Awiteb
import os, platform
import requests
from sclib import SoundcloudAPI
from pytube import YouTube, Playlist
from youtubesearchpython import SearchVideos,SearchPlaylists
from colorama import init, Fore, Back

init(autoreset=True)



def checkName(path, fileName, extension):
    def infinity():
        i = 0
        while True:
            i += 1
            yield i
    if os.path.lexists(f"{path}/{fileName}{extension}"):
        for num in infinity():
            if os.path.lexists(f"{path}/{fileName}{num}{extension}"):
                continue
            else:
                return f"{fileName}{num}"
    else:
        return fileName

def get_operating_system():
    return platform.system()
def checkPath(path:str):

    if path == '': #اذ لم يتم ادخال ايشي
        if get_operating_system() == 'Windows': #اذا كان نظام التشغيل ويندوز
            DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') #هاذا هو مسار سطح المكتب
        else: #اذا كان نظام التشغيل لينكس او يونكس
            DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')#هاذا مسار سطح المكتب في اللينكس واليونكس
        path = DESKTOP #حفظ المسار هو سطح المكتب
    else:
        if os.path.lexists(path):
            if os.path.isdir(path):
                pass
            else:
                path = None
        else:
            path = None
    return path
    



def checkInput(userInput:str):
    if "https://" in userInput and ".com" in userInput:
        if "soundcloud.com" in userInput:
            if "/sets/" in userInput:
                inputType = "soundList"
                url = userInput
            else:
                inputType = "soundTrack"
                url = userInput
        elif "youtu.be" in userInput or "youtube.com" in userInput or "youtube.be" in userInput or "youtu.com" in userInput:
            if "playlist?list=PL" in userInput:
                inputType = "playList"
                url = userInput
            elif "watch?v=" in userInput and "&list=PL" in userInput:
                if "&index=" in userInput:
                    url = "https://www.youtube.com/playlist?list="+userInput[userInput.index("&list=PL") +6:userInput.index("&index=")]
                else:
                    url = "https://www.youtube.com/playlist?list="+userInput[userInput.index("&list=PL") +6:]
                inputType = "playList"
            else:
                inputType = "youtube"
                url = userInput
        else:
            url = None
    else:
        inputType = "string"
        url = ''
    return inputType, url


class Youtube():
    def __init__(self):
        self.name = None
        self.extension = None
        self.link = None

    def print_video(self,searchText:str,maxResult:int,vidORlist:bool):
        """Print search results from videos or playlists
        """

        if vidORlist:
            result = SearchVideos(searchText,mode='dict',max_results=maxResult).result()['search_result']
        else:
            result = SearchPlaylists(searchText,mode='dict',max_results=maxResult).result()['search_result']
        while True:
            if len(result) != 0:
                if vidORlist:
                    for video in result:
                        print(f'''
                        \r{'-'*30}{int(video['index'])+1}{'-'*30}
                        \r Title: {video['title']}
                        \r Link: {video['link']}
                        \r Duration: {video['duration']}
                        \r''',end='')
                    break
                else:
                    for lst in result:
                        print(f'''
                        \r{'-' * 30}{int(lst['index'])+1}{'-' * 30}
                        \r Title: {lst['title']}
                        \r Link: {lst['link']}
                        \r count of videos: {lst['count']}
                        \r''', end='')
                    break
            else:
                print(f"{Fore.RED}\nSorry, no results were found for your search..!")
                break



    def checkLink(self):
        """Verify the validity of the link and return the value in self.linkStatus
        """
        try:
            yt = YouTube(self.link)
            self.yt = yt
            self.linkStatus = True
        except:
            self.linkStatus = False


    def selectQuality(self,quality):
        """[summary]

        Args:
            quality (str): The quality of the video to be downloaded

        Returns:
            [Stream or None]: the first result of this query or None if the result doesn’t contain any streams.
        """
        Q_ = self.yt.streams.filter(res = quality, type = 'video', audio_codec = 'mp4a.40.2')
        if len(Q_) == 0:
            print(f"{Fore.RED}Sorry, this quality is not available..! (Choose agin.!)")
            self.quality = None
        elif len(Q_) >= 1:
            video = Q_.first()
            self.quality = quality
            print(f"The video quality is selected at {self.quality}")
            return video

class Soundcloud_dl():
    
    def __init__(self):
        pass

    def search(self,searchText :str, max_result :int, track = bool):

        def get_url() -> str:
            if track:
                url = f'''https://api-v2.soundcloud.com/search/tracks?q={searchText}&sc_a_id=c4feedeb-6e15-4c64-9bbb-b84644b60f49&variant_ids=&facet=genre&user_
                        id=59504-178307-437384-398340&client_id=8vRJNEvP8SeU3H4B4T60iRfxyibSmQQm&limit=20&offset=0&linked_partitioning=1&app_version=1610545850&app_locale=en'''
            else:
                url = f'''https://api-v2.soundcloud.com/search/playlists_without_albums?q={searchText}&sc_a_id=c4feedeb-6e15-4c64-9bbb-b84644b60f49&variant_ids=&facet=genre&user_
                        id=59504-178307-437384-398340&client_id=8vRJNEvP8SeU3H4B4T60iRfxyibSmQQm&limit=20&offset=0&linked_partitioning=1&app_version=1610545850&app_locale=en'''
            return url
        
        def get_data() -> dict:
            try:
                self.internet_error = False
                return requests.get(get_url()).json()
            except Exception as e:
                print(f"{Fore.RED}\nInternet error")
                self.internet_error = True
        
        def get_duration(milliseconds) -> str:
            full_duration = milliseconds / 1000 #milliseconds to seconds
            seconds = int(full_duration % 60)
            minutes = int(full_duration // 60)
            hours = int(minutes // 60)
            return f"{hours}:{minutes}:{seconds}"

        def save_result() -> list:
            data = get_data()
            if not self.internet_error:
                results = []
                for res in data['collection'][:max_result]:
                    result = {}
                    result['title'] = res['title']
                    result['like'] = res['user']['likes_count']
                    result['username'] = res['user']['username']
                    result['link'] = res['permalink_url']
                    if track:
                        result['duration'] = get_duration(res['duration'])
                    else:
                        result['tracks'] = res['track_count']
                        result['tracks_titles'] = ''
                        for i in [res['tracks'][i]['title'] for i in range(3) if i != (len(res['tracks']) -1)]:
                            result['tracks_titles'] += f"\t{i}\n"
                        result['tracks_titles'].rstrip('\n')
                    results.append(result)
                return results
            else:
                return None
        
        def print_result():
            results = save_result()
            if not self.internet_error:
                if len(results) > max_result:
                    print(type(results))
                    results = results[:max_result]
                else:
                    pass
                if len(results) != 0:
                    for result in results:
                        print(f"""\r{'-'*35}
                        \r  Title: {Fore.BLUE}{result['title']}\033[39m
                        \r  {'Duration' if track else 'Tracks'}: {Fore.BLUE}{result['duration'] if track else result['tracks']}\033[39m
                        \r  Like: {Fore.BLUE}{result['like']}\033[39m
                        \r  Username: {Fore.BLUE}{result['username']}\033[39m
                        \r  Link: {Fore.BLUE}{result['link']}\033[39m"
                        \r  {'' if track else 'Some track title:'}\n{Fore.GREEN}{'' if track else result['tracks_titles']}\033[39m""")
                    print('-'*35,end=' ')
                elif max_result == 0:
                    pass
                else:
                    print(f"{Fore.RED}\nSorry, There are no results for '{searchText}'")
            else:
                pass
        print_result()

    def download(self,url,path,fileName):
        try:
            track = SoundcloudAPI().resolve(url)
        except:
            return False
        if fileName == '':
            fileName = checkName(path,track.title,'.mp3')
        else:
            pass
        with open(f"{path}/{fileName}.mp3",'wb+') as f:
            track.write_mp3_to(f)
            print(f"{Fore.YELLOW}Done, Download {fileName}\033[39m")
            return True