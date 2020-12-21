from XTube_load_functions import _vid_
from pytube import YouTube, Playlist
import os, platform
from colorama import init, Fore, Back
init(autoreset=True)
#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE,


print(f"{Fore.YELLOW}\n{'-'*30}|",end='')
print(f'''{Fore.YELLOW}
 Developed by: Awiteb         |
 GitHub: Awiteb               |
 Email: Awiteb@hotmail.com    |''')
print(f"{Fore.YELLOW}{'-'*30}|")
print("\nYou can download a single YouTube clip\nor playlist or search on YouTube\nEnter the link for the playlist, video, or text to search for")

while True: #loop of projram
    dataCollection = False
    userInput = input(f"{Fore.CYAN}\n=>\033[39m ") # حقل ادخال البيانات
    v = _vid_(userInput) # تعريف اوبجكت
    userInputType = v.checkInput() #تخزين نوع الادخال في متغير
    if userInputType == "string": #اذا كان النوع نص
        v.print_video() #اطبع مقاطع الفديو
        continue #ارجع الى بداية اللوب

    elif userInputType == "youtube": #اذا كان النوع رابط يوتيوب
        dataCollection = False
        v.checkLink()
        if v.linkStatus == True: # اذا كان الرابط فعال
            yt = pytube.YouTube(userInput) #انشاء كائن واعطائه الرابط
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
                break

            if typeVoice: #اذا كان التنزيل صوت
                v.extension = '.mp3' #الامتداد 
                v.quality = None #ولايوجد له جودة
            else: #اذ لم يكن
                v.extension = '.mp4' #الامتداد


            if dataCollection: #اذا كانت البيانات كاملة(غالبا ماتكون كاملة وهاذا الشرط فقط لتفادي المشاكل)
                print(f"Title is '{yt.title.replace(' ','_')}'") #طباعة عنوان المقطع
                v.name = input(f"{Fore.CYAN}\nEnter file name (Press enter to make the title the name of file):\033[39m ").replace(' ','_') #اذ كنت ترغب بتغير الاسم
                if v.name == '': #اذ لم تدخل شي 
                    v.name = yt.title.replace(' ','_') #وضع عنوان المقطع اسم للملف
                else: #اذا وضع اسم لاتفعل شي
                    pass

                while True: #وايل وضع مسار للملف
                    path = input(f"{Fore.CYAN}\nEnter the path to place the video in (Press Enter to download to the desktop):\033[39m ").replace('\\','/') #اخذ المسار
                    
                    if path == '': #اذ لم يتم ادخال ايشي
                        if platform.system() == 'Windows': #اذا كان نظام التشغيل ويندوز
                            DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') #هاذا هو مسار سطح المكتب
                        else: #اذا كان نظام التشغيل لينكس او يونكس
                            DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')#هاذا مسار سطح المكتب في اللينكس واليونكس
                        path = DESKTOP #حفظ المسار هو سطح المكتب

                        v.path = f"{path}/{v.name}{v.extension}" #حفظ المسار الكامل (مسار الحفظ، اسم الملف، امتداد الملف)
                        v.checkName(v.path) #ادخال المسار في دالة التحقق من الاسم (عمل الدالة اذ تشابه الاسم في المسار تزيد عليه رقم اذا لا تخرجه كما هو)
                        break #الخروج من الوايل
                    else:
                        if os.path.lexists(path): #اذا كان المسار موجود
                            if os.path.isdir(path): #التحقق اذا كان مجلد
                                v.path = f"{path}/{v.name}{v.extension}" #حفظ المسار الكامل (مسار الحفظ، اسم الملف، امتداد الملف)
                                v.checkName(v.path) #ادخال المسار في دالة التحقق من الاسم (عمل الدالة اذ تشابه الاسم في المسار تزيد عليه رقم اذا لا تخرجه كما هو)
                                break #الخروج من الوايل
                            else:
                                print(f"{Fore.RED}Sorry, but the path you entered is not a directory")
                        else:
                            print(f"{Fore.RED}Sorry, the path does not exist. Please enter a valid path to complete the download.!")
                    

                minutes = yt.length // 60 #تخزين عدد دقائق الفديو
                seconds = yt.length % 60 #تخزين عدد ثواني الفديو
                hours = minutes // 60 #تخزين عدد ساعات الفديو
                v.size = video.filesize / 1000000 #تخزين حجم الفديو بالميجابايت
                v.duration = f"{hours}:{minutes}:{int(seconds)}" #تخزين مدة المقطع

                print(f"""
                File name: {Fore.BLUE}{v.name}\033[39m
                Duration: {Fore.BLUE}{v.duration}\033[39m
                Quality: {Fore.BLUE}{v.quality}\033[39m
                size: {Fore.BLUE}{v.size:.2f} MB\033[39m
                Link: {Fore.BLUE}{v.link}\033[39m
                Path: {Fore.BLUE}{v.path}\033[39m
                            """) #طباعة معلومات الفديو للموافقة عليها او الغاء العملية

                while True: #وايل التاكد من الرغبة بتحميل الفديو
                    sureDownload = input(f"{Fore.CYAN}\nAre you sure you want to continue downloading? y/n:\033[39m ")
                    if sureDownload == 'y': #اذا كانت الاجابة نعم
                        video.download(path, filename = v.name) #تحميل
                        if typeVoice: #اذا كان المراد تحميله صوت
                            os.rename(path+'/'+v.name+'.mp4', v.path) #تغير امتاد الصوت الى صوت (ملاحظة المكتبة تحمل الصوت بامتداد فديو مرئي ويتم تغيره هنا)
                            print(f"{Fore.YELLOW}Done, Download successful..!")
                            break #الخروج من الوايل
                        else:
                            print(f"{Fore.YELLOW}Done, Download successful..!")
                            break #الخروج من الوايل
                    elif sureDownload == 'n': # اذا كانت الاجالة لا
                        break #الخروج من الوايل
                    else: #غير ذالك اطبع اختار نعم ام لا
                        print("Write 'y' to complete downloading or 'n' to cancel..!")

        else: #اذ لم يكن الرابط فعال
            print(f"{Fore.RED}Sorry, the link is not valid")
    elif userInputType == "playList": #اذا كان النوع قائمة تشغيل
        print(f"{Fore.RED}\n\nSorry, But there is a problem currently and it is not possible to download a playlist \ncurrently (the problem will be addressed later)")
        #حاليا ميزة التحميل من قائمة تشغيل ليست فعالة


    break #عند الانتهاء من كل شي الخروج من الوايل
    #ملاحظة يمكنك بناء الكود بدون وايل البرنامج ولكن تم استعمالها لاعادة طلب الادخال (اذ لم تفهم انظر الى سطر 22)
