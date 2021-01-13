#Some functions for XTueb_load
#By Awiteb
import os, platform
from time import sleep
import datetime
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
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

        
    def search(self,searchText :str, max_result = 10, track = True):

        """Soundcloud search function using scraping

        Args:
            searchText (str): The text you want to search for in soundcloud
            max_result (int, optional): How many result you want. Defaults to 10.
            track (bool, optional): It is true if you want to search for a track, False to playlist. Defaults to True.

        Returns:
                Print the result using the print_data() function below
        """

        def get_num_from_str(txt):
            """
            A function that extracts numbers from text and puts it into one number, the function is designed 
            for a specific type of text and it is not practical (it must be developed for use in other uses)

            Args:
                txt (str): Text is in this structure، (text 77 text)

            Returns:
                int: The number in the text
            """
            res = '' #اننشاء متغير لحفظ النتاج فيه
            lst_of_num = [i for i in txt if i.isnumeric()] #جمع الارقام في لستة
            for num in lst_of_num: #اخذ من اللستة رقم رقم
                res += num #تخزين الاراقم في المتغير
            return int(res) #اراجع المتغير 

        def get_url():
            if track: #اذا كان البحث عن تراك
                url = f"https://soundcloud.com/search/sounds?q={searchText}" #اضاافة نص البحث في رابط البحث عن تراك
            else: #اذ كان البحث عن قائمة تشغيل
                url = f"https://soundcloud.com/search/sets?q={searchText}" #اضاافة نص البحث في رابط البحث عن قائمة تشغيل
            return url #ارجاع الرابط
        
        def get_li_tags():
            """Scraping

            Returns:
                list: get all data of track / playlist
            """
            browser_options = Options() #انشاء متغير اعدادات المتصفح
            #browser_options.add_argument('--headless') #اخفاء المتصفح
            global browser #جعل متغير المتصفح عام
            browser = webdriver.Firefox(executable_path='./venv/driver/geckodriver',options=browser_options) #تشغيل المتصفح
            browser.get(get_url()) #اخذ رابط الصغحة من الدالة
            sleep(5) #الانتظار حتى تفتح الصفحة ويتم تشغيل السكربتات
            li_tags = [] #انشاء لستة لحفظ النتائج فيها

            while len(li_tags) < max_result: #طالمة عدد النتائج المستخرجة اقل من عدد النتائج المطلوبة
                html = browser.page_source #حفظ سورس الصفحة في متغير
                soup = BS(html,'lxml')
                if soup.find('div',class_="searchList__empty") != None: #يتم انشاء تاق اذا لم يكن هناك نتائج (هنا اقوله اذا انه متواجد افعل الاتي)
                    print(f"Sorry, '{searchText}' was not found in Soundcloud") #اطبع لم يتم العثور على بحثك
                    browser.quit() #اغلق المتصفح
                    return None
                results_on_the_page = get_num_from_str(soup.find('div',class_='resultCounts sc-type-h3 sc-type-light').text) #جلب نص عدد النتائج واستخراجه عبر دالة استخراج الرقم
            
                if max_result >  results_on_the_page - 2: #اذ كان عدد النتائج المطلوبة اكثر من النتائج الموجود بالصفحة
                    print('Sorry, the number of results you want more than the available items')
                    browser.quit() #اغلق المتصفح
                    return None
                else: # اذا كان اقل
                    result = soup.findAll('li',class_='searchList__item', limit=max_result) # سحب النتائج (في بداية الصفحة بدون النزول يكون موجود 10 عناصر فيتم سحبة قبل النزول)
                    for res in result:
                        if res.find('div',class_='blockedTrackMessage') == None or res.find('span',class_="waveform__emptyMessage") == None or res.find('span',class_="g-geoblocked-icon") == None: #بعض الاخطاء ان وجدت لاتضيف النتيجة
                            li_tags.append(res)
                        else:
                            continue
                    if max_result > 10:
                        for i in range(5): #تكرار النزول 10 مرات
                            browser.find_element_by_tag_name('html').send_keys(Keys.PAGE_DOWN) #النزول بالصفحة
            
            if not track: #اذا كان البحث عن قائمة تشغيل
                browser.quit() #اغلق المتصفح لاننا لانحتاجه تحت
            return li_tags #ارجع النتائج


        def get_track_count(li):
            """Fetch number of tracks inside the playlist

            Returns:
                int: Number of tracks
            """
            #اذا كانت عدد العناصر في قائمة التشغيل اقل من 8 لن يكون هناك نص فيه عدد التراك
            try:
                tracks = get_num_from_str(li.find('a',class_='compactTrackList__moreLink sc-link-light sc-border-light').text) #اذ لم يوجد النص الذي فيه عدد التراك
            except AttributeError:
                tracks = len(li.find('ul',class_='compactTrackList__list sc-list-nostyle sc-clearfix').findAll('li',class_='compactTrackList__item')) #اجلب عدد العناصر الخارجية
            return tracks

        def save_result():
            """
            Returns:
                list: A list of dictionaries
            """
            result_list = [] #انشاء لستة لحفظ النتائج
            res = get_li_tags()
            if res == None:
                return None
            for li_tag in res: #نتيجة نتيجة من النتائج
                result_dict = {} #قاموس لتخزين النتائج ثم ادخالها الى اللستة

                url_and_title = li_tag.find('div',class_ = 'soundTitle__usernameTitleContainer').findAll('a')[1] #اخذ التاق الذي يوجد فيه الرابط والعنوان
                like = li_tag.find(class_ = 'sc-button-like sc-button sc-button-small sc-button-responsive').text #اخذ عدد الاليكات
                if like == 'Like': #اذا لم يكن موجود ولا لايك
                    like = 0 #لايك يساوي صفر
                else:
                    pass

                title = url_and_title.find('span').text.strip() #اخذ العنوان
                url = 'https://soundcloud.com'+url_and_title['href'] #اخذ الرابط
                username = li_tag.find('span',class_="soundTitle__usernameText").text.strip() #اخذ اسم المستخدم
                
                if track: #اذا كان البحث عن تراك
                    browser.get(url) #فتح المتصفح على الاغنية
                    sleep(0.5) #الانتظار نص ثانية
                    soup = BS(browser.page_source,'lxml') #سحب سورس الصفحة
                    try:
                        duration = soup.find('div',class_='playbackTimeline__duration').find('span').text.strip('Duration: ') #اخذ وقت المقطع 
                    except: #اذا حدث خطأ
                        duration = None #اعطأ قيمة فارغة للوقت
                    result_dict['duration'] = duration #حفظ الوقت في الدكشنري
                else: #اذ كان البحث عن قائمة تشغيل
                    total_track = get_track_count(li_tag) #جلب عدد التراكات
                    result_dict['tracks'] = total_track #حفظ عدد التراكات
                    
                result_dict['url'] = url #حفظ الرابط في الدكشنري
                result_dict['title'] = title #حفظ العنوان في الدكشنري
                result_dict['username'] = username #حفظ اسم المستخدم في الدكشنري
                result_dict['like'] = like #حفظ عدد الايكات في الدكشنري
                result_list.append(result_dict) #اضافة الدكشنري الى اللستة

            browser.quit() #اغلاق المتصفح اذا كان شغال 
            return result_list #ارجاع اللستة داخلها مجموعة من الدكشنري
        
        #الدالة الوحيدة التي يتم تشغيلها في البحث هي دالة الطباعة ويتم تشغيل جميع الدوال بداخلها
        def print_data():
            start = datetime.datetime.now() #اخذ وقت بداية البحث
            res = save_result()
            if res != None:
                for data in res: #اخذ البيانات من دالة حفظ البيانات
                    print(f"\n{'-'*70}",end='')
                    if track:
                        print(f"""
                        \rTitle: {data['title']}
                        \rDuration: {data['duration']}
                        \rUserName: {data['username']}
                        \rLike: {data['like']}
                        \rUrl: {data['url']}""",end='')
                    else:
                        print(f"""
                        \rTitle: {data['title']}
                        \rUserName: {data['username']}
                        \rTracks: {data['tracks']}
                        \rLike: {data['like']}
                        \rUrl: {data['url']}""",end='')
                print(f"\n{'-'*70}")

                end = datetime.datetime.now() #اخذ وقت نهاية البحث
                if track:
                    search_type = 'track'
                else:
                    search_type = 'playlist'
                print(f"The search was performed for {len(res)} {search_type} in {str(end - start)[:7]}s")
            else:
                pass
        print_data()

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