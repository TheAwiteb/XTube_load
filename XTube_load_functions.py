#Some functions for XTueb_load
#By Awiteb
from pytube import YouTube, Playlist
from youtubesearchpython import SearchVideos,SearchPlaylists
import os
from colorama import init, Fore, Back
init(autoreset=True)

class _vid_():
    def __init__(self,Input):
        self.input =Input
#https://www.youtube.com/watch?v=PfSAavDGjWE&list=PLgcjCT1pz7y1uOCDJtoYe3X7xB9dMDAEO
#https://www.youtube.com/watch?v=QgcdG2L8A1A&list=PLgcjCT1pz7y1uOCDJtoYe3X7xB9dMDAEO&index=6
#https://www.youtube.com/playlist?list=PLgcjCT1pz7y1uOCDJtoYe3X7xB9dMDAEO
    def checkInput(self):
        """Function to check the type of entry

        Returns:
            str: input type (str or video or playlist link)
        """
        if "youtu.be" in self.input or "youtube.com" in self.input or "youtube.be" in self.input or "youtu.com" in self.input:
            if "playlist?list=PL" in self.input:
                inputType = "playList"
                self.link = self.input
            elif "watch?v=" in self.input and "&list=PL" in self.input:
                if "&index=" in self.input:
                    url = "https://www.youtube.com/playlist?list="+self.input[self.input.index("&list=PL") +6:self.input.index("&index=")]
                else:
                    url = "https://www.youtube.com/playlist?list="+self.input[self.input.index("&list=PL") +6:]
                inputType = "playList"
                self.link = url
            else:
                inputType = "youtube"
                self.link = self.input
        elif ".com" not in self.input or '.be' not in self.input and 'youtube' not in self.input or 'youtu' not in self.input:
            inputType = "string"
            self.link = self.input
        return inputType


    def print_video(self):
        """Print search results from videos or playlists
        """
        while True:
            try:
                numOFresults = int(input(f"{Fore.CYAN}How many results you want:\033[39m "))
            except ValueError:
                print(f"{Fore.RED}Sorry, please enter the number of results in numbers.!")
                continue
            vidORlist = input(f"{Fore.CYAN}Search for a video or playlist (v/p):\033[39m ")
            if vidORlist == 'v':
                result = SearchVideos(self.link,mode='dict',max_results=numOFresults).result()['search_result']
            elif vidORlist == 'p':
                result = SearchPlaylists(self.link,mode='dict',max_results=numOFresults).result()['search_result']
            else:
                print(f"{Fore.RED}Please choose 'v' or 'p'..")
                continue
            if len(result) != 0:
                if vidORlist == 'v':
                    for video in result:
                        print(
                        f'''
{'-'*30}{int(video['index'])+1}{'-'*30}
    Title: {video['title']}
    Link: {video['link']}
    Duration: {video['duration']}
    ''',end='')
                    break
                else:
                    for list in result:
                        print(
                            f'''
{'-' * 30}{int(list['index'])+1}{'-' * 30}
    Title: {list['title']}
    Link: {list['link']}
    count of videos: {list['count']}
    ''', end='')
                    break
            else:
                print(f"{Fore.RED}\nSorry, no results were found for your search..!")
                break



    def checkLink(self):
        """Verify the validity of the link and return the value in self.linkStatus
        """
        try:
            yt = pytube.YouTube(self.link)
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
            return video
            print(f"The video quality is selected at {self.quality}")

    def checkName(self,path):
        """A function to check the file path and add a number next to it if it exists, store the value, and review it

        Args:
            path (str): The path to where the file was downloaded
        """
        if os.path.lexists(path.strip('/')+'/'+self.name+self.extension):
                for i in range(999999999999999):
                    if os.path.lexists(path.strip('/')+'/'+self.name+str(i+1)+self.extension):
                        pass
                    else:
                        self.name = self.name+str(i+1)
                        break
        else:
            pass
