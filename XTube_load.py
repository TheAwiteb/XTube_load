from XTube_load_functions import _vid_
import pytube
import os, platform



print('''
Developed by: Awiteb
GitHub: Awiteb
Email: Awiteb@hotmail.com''')
print("\nYou can download a single YouTube clip\nor playlist or search on YouTube\nEnter the link for the playlist, video, or text to search for")

while True:
    userInput = input("\n=> ")
    v = _vid_(userInput)
    userInputType = v.checkInput()
    if userInputType == "string":
        v.print_video()
        continue

    elif userInputType == "youtube":
        dataCollection = False
        typeVoice = False
        v.checkLink()
        if v.linkStatus == True:
            yt = pytube.YouTube(userInput)
            print("Video[1]\nAudio[2]\nElse to cancel")
            downloadMethod = input("Choose the download method: ")

            if downloadMethod == '1':
                typeVoice = False
                print('1080p[1]\n720p[2]\n480p[3]\n360p[4]\nElse if no one working')

                while True:
                    vidQuality = input("Choose the video quality: ")
                    if vidQuality == '1':
                        quality = '1080p'
                        video = v.selectQuality(quality)
                        if v.quality != None:
                            dataCollection = True
                            break
                    elif vidQuality == '2':
                        quality = '720p'
                        video = v.selectQuality(quality)
                        if v.quality != None:
                            dataCollection = True
                            break
                    elif vidQuality == '3':
                        quality = '480p'
                        video = v.selectQuality(quality)
                        if v.quality != None:
                            dataCollection = True
                            break
                    elif vidQuality == '4':
                        quality = '360p'
                        video = v.selectQuality(quality)
                        if v.quality != None:
                            dataCollection = True
                            break
                    else:
                        video = yt.streams.filter(type = 'video', audio_codec = 'mp4a.40.2').first()
                        v.quality = str(video)[46:50]
                        dataCollection = True
                        break

            elif downloadMethod == '2':
                typeVoice = True
                video = yt.streams.filter(mime_type="audio/mp4", type="audio").first()
                dataCollection = True
            else:
                pass

            if typeVoice:
                v.extension = '.mp3'
                v.quality = None
            else:
                v.extension = '.mp4'


            if dataCollection:
                print(f"Title is '{yt.title.replace(' ','_')}'")
                v.name = input("Enter file name (Press enter to make the title the name of file): ").replace(' ','_')
                if v.name == '':
                    v.name = yt.title.replace(' ','_')
                else:
                    pass

                while True:
                    if platform.system() != 'Windows':
                        DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
                    else:
                        DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

                    path = input("Enter the path to place the video in: ").replace('\\','/')
                    if path == '':
                        path = DESKTOP
                        break
                    else:
                        if os.path.lexists(path):
                            if os.path.isdir(path):
                                break
                            else:
                                print("Sorry, but the path you entered is not a directory")
                        else:
                            print("Sorry, the path does not exist. Please enter a valid path to complete the download.!")

                minutes = yt.length // 60
                seconds = yt.length % 60
                hours = minutes // 60
                v.size = video.filesize / 1000000
                v.duration = f"{hours}:{minutes}:{int(seconds)}"
                v.path = f"{path}/{v.name}{v.extension}"
                v.checkName(v.path)

                print(f"""
       File name: {v.name}
       Duration: {v.duration}
       Quality: {v.quality}
       size: {v.size:.2f} MB
       Link: {v.link}
       Path: {v.path}
       """)

                while True:
                    sureDownload = input("\nAre you sure you want to continue downloading? y/n: ")
                    if sureDownload == 'y':
                        video.download(path, filename = v.name)
                        if typeVoice:
                            os.rename(path+'/'+v.name+'.mp4', v.path)
                            print("Done, Download successful..!")
                            break
                        else:
                            print("Done, Download successful..!")
                            break
                    elif sureDownload == 'n':
                        break
                    else:
                        print("Write 'y' to complete downloading or 'n' to cancel..!")

    elif userInputType == "playList":
        print("\n\nSorry, But there is a problem currently and it is not possible to download a playlist \ncurrently (the problem will be addressed later)")


    break
