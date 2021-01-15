from XTube_load_functions import *
from pytube import YouTube, Playlist
import os
from colorama import init, Fore, Back
from sclib import SoundcloudAPI
from time import sleep
init(autoreset=True)
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,


print(f"{Fore.YELLOW}\n{'-'*30}|",end='')
print(f'''{Fore.YELLOW}
 Developed by: Awiteb         |
 GitHub: Awiteb               |
 Email: Awiteb@hotmail.com    |''')
print(f"{Fore.YELLOW}{'-'*30}|")
print("'-h' to help!")

while True: #loop of projram
    print(f"{Fore.MAGENTA}\n𝚙𝚛𝚎𝚜𝚜 𝚎𝚗𝚝𝚎𝚛 𝚝𝚘 𝚚𝚞𝚒𝚝.\033[39m")
    userInput = input(f"{Fore.CYAN}└➤ \033[39m") # حقل ادخال البيانات
    if userInput == "":
        break
    elif userInput == '-h':
        print("""
            \rYou can do with the tool:
            \r  Search in:
            \r      YouTube -> video/playlist      Max -> 20
            \r      SoundCloud -> track/playlist   Max -> 20
            \r
            \r  Download from:
            \r      YouTube -> video/playlist
            \r      SoundCloud -> track/playlist
            \r
            \r  Commands:
            \r      -h -> Show this message  
            \r      -clear -> Clear the window
            \r
            \rJust enter the link to download, or text to search 
            \rThe source code: https://github.com/Awiteb/XTube_load """)
        continue
    elif userInput == '-clear':
        if get_operating_system == "Windows":
            os.system('cls')
        else:
            os.system('clear')
        continue
    userInputType, url = checkInput(userInput) #تخزين نوع الادخال في متغير
    if userInputType == "string": #اذا كان النوع نص
        while True:
            soundcloudORyoutube = input(f"{Fore.CYAN}\nSearch in Soundcloud or YouTube (s,y): \033[39m").lower()
            while soundcloudORyoutube == 'y' or soundcloudORyoutube == 's':
                try:
                    maxResult = int(input(f"{Fore.CYAN}\nHow many results you want: \033[39m"))
                    if maxResult > 20:
                        print(f"{Fore.RED}Sorry, only 20 items will be searched, because 20 is the maximum.!")
                        maxResult = 20 #اجبار المستخدم على 20 نتيجة لعدم البحث لوقت طويل
                    break
                except ValueError:
                    print(f"{Fore.RED}Sorry, please enter the number of results in numbers.!")
            else:
                print(f"{Fore.RED}Sorry, enter 's' or 'y'")
                continue
            
            def singleORlist(soundcloudORyoutube:str):
                if soundcloudORyoutube == 'y':
                    callType = "video"
                    abbreviation = 'v'
                else:
                    callType = "track"
                    abbreviation = 't'
                while True:
                    singleORlist = input(f"{Fore.CYAN}Search for a {callType} or playlist ({abbreviation}/p):\033[39m ")
                    if singleORlist == abbreviation:
                        return True
                    elif singleORlist == 'p':
                        return False
                    else:
                        print(f"{Fore.RED}\nSorry, enter '{abbreviation}' or 'p'")
            if soundcloudORyoutube == 'y':
                Youtube().print_video(userInput,maxResult,singleORlist('y'))
                break
            elif soundcloudORyoutube == 's':
                Soundcloud_dl().search(searchText= userInput, max_result=maxResult, track=singleORlist('s'))
                break
            else:
                print(f"{Fore.RED}Sorry, enter 'y' or 's'")
        continue #ارجع الى بداية اللوب
    elif userInputType == "youtube": #اذا كان النوع رابط يوتيوب
        dataCollection = False
        v = Youtube() # تعريف اوبجكت
        v.link = url
        v.checkLink()
        if v.linkStatus == True: # اذا كان الرابط فعال
            yt = YouTube(v.link) #انشاء كائن واعطائه الرابط
            print("Video[1]\nAudio[2]\nElse to cancel")
            downloadMethod = input(f"{Fore.CYAN}Choose the download method:\033[39m ") #اختيار تنزيل فديو او صوت

            if downloadMethod == '1': #اذا كان الاختيار فديو
                typeVoice = False #الفويس بفولس
                print('1080p[1]\n720p[2]\n480p[3]\n360p[4]\nElse if no one working')

                while True: #وايل اختيار الجودة
                    vidQuality = input(f"{Fore.CYAN}Choose the video quality:\033[39m ")
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
                continue

            if typeVoice: #اذا كان التنزيل صوت
                v.extension = '.mp3' #الامتداد 
                v.quality = None #ولايوجد له جودة
            else: #اذ لم يكن
                v.extension = '.mp4' #الامتداد

            if dataCollection: #اذا كانت البيانات كاملة(غالبا ماتكون كاملة وهاذا الشرط فقط لتفادي المشاكل)
                print(f"Title is '{yt.title}'") #طباعة عنوان المقطع
                v.name = input(f"{Fore.CYAN}\nEnter file name (Press enter to make the title the name of file):\033[39m ").replace(' ','_') #اذ كنت ترغب بتغير الاسم
                while True: #وايل وضع مسار للملف
                    path = input(f"{Fore.CYAN}\nEnter the path to place the video in (Press Enter to download to the desktop):\033[39m ").replace('\\','/').rstrip('/') #اخذ المسار
                    path = checkPath(path)
                    if path == None:
                        print(f"{Fore.RED}Sorry, the path does not exist. Please enter a valid path to complete the download.!")
                        continue
                    else:
                        if v.name == '':
                            v.name = checkName(path,yt.title.replace(' ','_'),v.extension)
                        else:
                            v.name = checkName(path, v.name, v.extension)
                        v.path = f"{path}/{v.name}{v.extension}"
                        break

                minutes = yt.length // 60 #تخزين عدد دقائق الفديو
                seconds = yt.length % 60 #تخزين عدد ثواني الفديو
                hours = minutes // 60 #تخزين عدد ساعات الفديو
                v.size = video.filesize / 1000000 #تخزين حجم الفديو بالميجابايت
                v.duration = f"{hours}:{minutes}:{int(seconds)}" #تخزين مدة المقطع

                print(f"""
                \r  File name: {Fore.BLUE}{v.name}\033[39m
                \r  Duration: {Fore.BLUE}{v.duration}\033[39m
                \r  Quality: {Fore.BLUE}{v.quality}\033[39m
                \r  size: {Fore.BLUE}{v.size:.2f} MB\033[39m
                \r  Link: {Fore.BLUE}{v.link}\033[39m
                \r  Path: {Fore.BLUE}{v.path}\033[39m
                            """) #طباعة معلومات الفديو للموافقة عليها او الغاء العملية

                while True: #وايل التاكد من الرغبة بتحميل الفديو
                    sureDownload = input(f"{Fore.CYAN}\nAre you sure you want to continue downloading? y/n:\033[39m ")
                    if sureDownload == 'y': #اذا كانت الاجابة نعم
                        mp4fileName = checkName(path,'XTUBE_LOAD','.mp4')
                        video.download(path, filename = mp4fileName) #تحميل
                        os.rename(path+'/'+mp4fileName+'.mp4', f"{path}/{v.name}{v.extension}") #تغير امتاد الصوت الى صوت (ملاحظة المكتبة تحمل الصوت بامتداد فديو مرئي ويتم تغيره هنا)
                        print(f"{Fore.YELLOW}Done, Download successful..!")
                        break #الخروج من الوايل
                    elif sureDownload == 'n': # اذا كانت الاجالة لا
                        break #الخروج من الوايل
                    else: #غير ذالك اطبع اختار نعم ام لا
                        print("Write 'y' to complete downloading or 'n' to cancel..!")

        else: #اذ لم يكن الرابط فعال
            print(f"{Fore.RED}Sorry, the link is not valid (try again)")
    elif userInputType == "playList": #اذا كان النوع قائمة تشغيل
        try:
            pl = Playlist(url)
            stateUrl = True
        except:
            stateUrl = False
        
        if stateUrl:
            print("Video[1]\nAudio[2]\nElse to cancel")
            downloadMethod = input(f"{Fore.CYAN}Choose the download method:\033[39m ") #اختيار تنزيل فديو او صوت
            if downloadMethod == '1':
                typeVoice = False #الفويس بفولس
                extension = '.mp4'
                print('1080p[1]\n720p[2]\n480p[3]\n360p[4]')
                print("\nNOTE: A random quality will be chosen if the video does not support the quality you chose")
                while True:
                    vidQuality = input(f"{Fore.CYAN}Choose the video quality:\033[39m")
                    if vidQuality == '1':
                        quality = '1080p'
                        break
                    elif vidQuality == '2':
                        quality = '720p'
                        break
                    elif vidQuality == '3':
                        quality = '480p'
                        break
                    elif vidQuality == '4':
                        quality = '360p'
                        break
                    else:
                        print(f"{Fore.RED}Please choose one of the above qualities.!")
            elif downloadMethod == '2':
                typeVoice = True
                extension = '.mp3'
            else:
                continue
            userFileName = input(f"{Fore.CYAN}\nEnter file name (Press enter to make the video title the name of file):\033[39m ").replace(' ','_')
            while True: #وايل وضع مسار للملف
                path = input(f"{Fore.CYAN}\nEnter the path to place the video in (Press Enter to download to the desktop):\033[39m ").replace('\\','/') #اخذ المسار
                path = checkPath(path)
                if path == None:
                    print(f"{Fore.RED}Sorry, the path cannot be reached!")
                    continue
                else:
                    break
            
            maxResultOnPlaylist = pl.__len__()
            print(f"\n{maxResultOnPlaylist} video in playlist => Title: {pl.title}")
            while True:
                try:
                    maxResult = input(f"{Fore.CYAN}How many track do you want to download (Press enter to select all): \033[39m")
                    if maxResult == '':
                        maxResult = maxResultOnPlaylist
                    else:
                        maxResult = int(maxResult)
                    if maxResult > maxResultOnPlaylist:
                        print(f"{Fore.RED}Sorry, the number of results you want is more than the results in the playlist.!")
                        continue
                    else:
                        break
                except ValueError:
                    print(f"{Fore.RED}Sorry, please enter the number of videos with numbers only.!")
                    continue

            for vidUrl in pl.video_urls[:maxResult]:
                try:
                    yt = YouTube(vidUrl)
                except Exception as e:
                    print(f"{Fore.RED}Sorry, {e}.!")
                    continue
                if userFileName == '':
                    fileName = checkName(path,yt.title,extension).replace('  ','_')
                else:
                    fileName = checkName(path,userFileName,extension)
                
                if typeVoice:
                    video = yt.streams.filter(mime_type="audio/mp4", type="audio").first()
                else:
                    video = yt.streams.filter(res=quality, type = 'video', audio_codec = 'mp4a.40.2').first()       
                    if video == None:
                        video = yt.streams.filter(type = 'video', audio_codec = 'mp4a.40.2').first()    
                    else:
                        pass
                
                mp4fileName = checkName(path,'XTUBE_LOAD','.mp4')
                video.download(output_path=path, filename=mp4fileName)
                sleep(.6)
                os.rename(path+'/'+mp4fileName+'.mp4', f"{path}/{fileName}{extension}") #تغير امتاد الصوت الى صوت (ملاحظة المكتبة تحمل الصوت بامتداد فديو مرئي ويتم تغيره هنا)
                print(f"{Fore.YELLOW}Done, Download {fileName}{extension}")
        else:
            print(f"{Fore.RED}Sorry, the link is not valid (try again)")
    elif userInputType == "soundTrack": #اذا كان النوع تراك ساوندكلاود
        fileName = input(f"{Fore.CYAN}\nEnter file name (Press enter to make the sound title name of file):\033[39m ") #اذ كنت ترغب بتغير الاسم
        while True: #وايل وضع مسار للملف
            path = input(f"{Fore.CYAN}\nEnter the path to place the video in (Press Enter to download to the desktop):\033[39m ").replace('\\','/').rstrip('/') #اخذ المسار
            path = checkPath(path)
            if path == None:
                print(f"{Fore.RED}Sorry, the path does not exist. Please enter a valid path to complete the download.!")
            else:
                if fileName != '':
                    fileName = checkName(path, fileName, '.mp3')
                else:
                    pass
                break
        downloadState = Soundcloud_dl().download(url,path,fileName)
        if downloadState:
            pass
        else:
            print(f"{Fore.RED}Sorry, the link is not valid (try again)")
    elif userInputType == "soundList": #اذا كان نوع قائمة تشغيل في ساوندكلاود
        try:
            pl = SoundcloudAPI().resolve(url)
            stateUrl = True
        except:
            stateUrl = False
        
        if stateUrl:
            userFileName = input(f"{Fore.CYAN}\nEnter file name (Press enter to make the track title the name of file):\033[39m ").replace(' ','_')
            while True:
                path = input(f"{Fore.CYAN}\nEnter the path to place the track in (Press Enter to download to the desktop):\033[39m ").replace('\\','/').rstrip('/') #اخذ المسار
                path = checkPath(path)
                if path == None:
                    print(f"{Fore.RED}Sorry, the path does not exist. Please enter a valid path to complete the download.!")
                    continue
                else:
                    break
            maxResultOnPlaylist = pl.track_count
            print(f"\n{maxResultOnPlaylist} tracks in playlist => Title: {pl.title}")
            while True:
                try:
                    maxResult = input(f"{Fore.CYAN}How many track do you want to download (Press enter to select all): \033[39m")
                    if maxResult == '':
                        maxResult = maxResultOnPlaylist
                    else:
                        maxResult = int(maxResult)
                    if maxResult > maxResultOnPlaylist:
                        print(f"{Fore.RED}Sorry, the number of results you want is more than the results in the playlist.!")
                        continue
                    else:
                        break
                except ValueError:
                    print(f"{Fore.RED}Sorry, please enter the number of track with numbers only.!")
                    continue
            for trackUrl in pl.tracks[:maxResult]:
                fileName = checkName(path, userFileName, '.mp3')
                try:
                    Soundcloud_dl().download(trackUrl.permalink_url,path,fileName)
                except:
                    print(f"{Fore.RED}Sorry, can't download {fileName}")
        else:
            print(f"{Fore.RED}Sorry, the link is not valid (try again)")
