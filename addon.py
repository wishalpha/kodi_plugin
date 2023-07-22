# coding: utf-8
import sys
from urllib import urlencode
from urllib import quote
from urlparse import parse_qsl

from bs4 import BeautifulSoup as BS
from requests import get
import xbmcgui
import xbmcplugin
import xbmc

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

CATEGORIES = ["Movies", "TVshows","Comics","Entertainment","Search" ]
engines =['wujinvod','pianku','feifan','shandian','liangzi','tiankong','guangsu','wolong']

def get_user_input():  
    kb = xbmc.Keyboard('', 'Please enter the video title')
    kb.doModal() # Onscreen keyboard appears
    if not kb.isConfirmed():
        return
    query = kb.getText() # User input
    return query

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))
def get_home():
    return CATEGORIES
def retrive_video_info(url,engin):
    video={}
    if engin == 'feifan':
        response=get(url)
        content=BS(response.content,'html.parser')
        infos=content.find('div',class_='right').find_all('p')
        for i, info in enumerate(infos):
            if i==0:
                title=info.text.strip().split(' ')[-1]
            elif i == 3:
                status=info.text.strip().split(' ')[-1]
            elif i == 4:
                genre=info.text.strip().split(' ')[-1]
            elif i== 7:
                year = info.text.strip().split(' ')[-1]
            elif i==8:
                region=info.text.strip().split(' ')[-1]
            elif i==9:
                lang = info.text.strip().split(' ')[-1]
        thumb=content.find('div',class_='left').find('img')['src'].strip()
        intro=content.find('div',class_='vod_content').find('p').text.strip() 
        lists=content.find_all('div',class_='playlist')
        
        links=[]
        for li in lists[0].findChildren('li',recursive=False)[:-1]:
            v_url=li.find('a')['href'].strip()
            # v_response=get(v_url)
            # v_content=BS(v_response.content,'html.parser')
            # v_link=v_content.find('video',class_='art-video')['src'].strip()
            links.append(v_url)
        links_m3u8=[]
        for li in lists[1].find_all('li')[:-1]:
            links_m3u8.append(li.find('a')['href'].strip())
    elif engin == 'wujinvod':
        response=get(url)
        content=BS(response.content,'html.parser')
        title=content.find('h1').text.strip()
        region=None
        lang = None
        status=None
        genre=None 
        year=None
        thumb=content.find('img',class_='lazyload')['data-original'].strip()
        intro=content.find('span',class_='detail-content').text.strip() 
        lists=content.find_all('ul',class_='stui-content__playlist')
        links_m3u8=[]
        links=[]
        for li in lists[1].find_all('li'):
            v_url='https://wjvod.com'+li.find('a')['href'].strip()
            #xbmc.log('check the url '+v_url)
            v_response=get(v_url)
            v_content=BS(v_response.content,'html.parser')
            #v_link=v_content.find('div',class_='stui-player__video').find('script').text.strip().split('http')[-1].split('index.m3u8')[0].replace('\\','')
            v_link=v_content.find('div',class_='stui-player__video').find('script').string
            v_link=''.join(v_link).split('http')[-1].split('index.m3u8')[0].replace('\\','')
            #xbmc.log('get the url '+v_link)
            links.append('http'+v_link+'index.m3u8')
            links_m3u8.append('http'+v_link+'index.m3u8')      
        #for li in lists[1].find_all('li')[:-1]:
            #links_m3u8.append(li.find('a')['href'].strip())
    elif engin == 'pianku':
        response=get(url)
        content=BS(response.content,'html.parser')
        #xbmc.log('***************'+url)
        #xbmc.log(str(content))
        region=None
        lang = None
        status=None
        genre=None   
        year=content.find('span',class_='year').text.strip()
        title=content.find('h1').text.strip()
        thumb=content.find('div',class_='img').find('img')['src'].strip()
        intro=content.find('p',class_='sqjj_a').text.strip() 

        source=[]
        ul=content.find('ul',class_='py-tabs').find_all('li')
        for li in ul:
            source.append(li.text.strip())
        index = xbmcgui.Dialog().contextmenu(list=source)
        
        lists=content.find('div',class_='bd').find_all('player')[index]
        
        links=[]
        links_m3u8=[]
        for li in lists.find_all('li'):
            v_url='https://www.pkmkv.com'+li.find('a')['href'].strip()
            v_response=get(v_url)
            v_content=BS(v_response.content,'html.parser')
            v_link=v_content.find('div',id='video').find('script').text.strip().split('http')[-1].split('m3u8')[0].replace('\\','')
            links.append('http'+v_link+'m3u8')
            links_m3u8.append('http'+v_link+'m3u8')
        
        
    elif engin == 'shandian':
        response=get(url)
        content=BS(response.content,'html.parser')
        infos=content.find('div',class_='vodinfobox').find('ul').find_all('li')
        for i, info in enumerate(infos):
            if i == 3:
                genre=info.find('span').text.strip()
            elif i== 6:
                year = info.find('span').text.strip()
            elif i==4:
                region=info.find('span').text.strip()
            elif i==5:
                lang = info.find('span').text.strip()
        title=content.find('h2').text.strip() 
        status=content.find('div',class_='vodh').find('span').text.strip() 
        thumb=content.find('img',class_='lazy')['src'].strip()
        intro=content.find('div',class_='vodplayinfo').text.strip() 
        lists=content.find_all('input',title='sdyun')
        m3u8=content.find_all('input',title='sdm3u8')
        links_m3u8=[]
        links=[]
        for li in m3u8:
            links_m3u8.append(li['value'].strip())
            links.append(li['value'].strip())
    elif engin == 'liangzi':
        response=get(url)
        content=BS(response.content,'html.parser')
        infos=content.find('div',class_='right').find_all('p')
        for i, info in enumerate(infos):
            if i==0:
                title=info.text.strip()
            elif i == 3:
                status=info.text.strip()
            elif i == 4:
                genre=info.text.strip()
            elif i== 7:
                year = info.text.strip()
            elif i==8:
                region=info.text.strip()
            elif i==9:
                lang = info.text.strip()
        thumb=content.find('div',class_='left').find('img')['src'].strip()
        intro=content.find('div',class_='vod_content').find('p').text.strip() 
        lists=content.find_all('div',class_='playlist')
        
        links=[]
        for li in lists[0].findChildren('li',recursive=False)[:-1]:
            v_url=li.find('a')['href'].strip()
            # v_response=get(v_url)
            # v_content=BS(v_response.content,'html.parser')
            # v_link=v_content.find('video',class_='art-video')['src'].strip()
            links.append(v_url)
        links_m3u8=[]
        for li in lists[1].find_all('li')[:-1]:
            links_m3u8.append(li.find('a')['href'].strip())
    elif engin == 'tiankong':
        response=get(url)
        content=BS(response.content,'html.parser')
        infos=content.find('div',class_='vodinfobox').find('ul').find_all('li')
        for i, info in enumerate(infos):
            if i == 3:
                genre=info.find('span').text.strip()
            elif i== 6:
                year = info.find('span').text.strip()
            elif i==4:
                region=info.find('span').text.strip()
            elif i==5:
                lang = info.find('span').text.strip()
        title=content.find('h2').text.strip() 
        status=content.find('div',class_='vodh').find('span').text.strip() 
        thumb=content.find('img',class_='lazy')['src'].strip()
        intro=content.find('div',class_='vodplayinfo').text.strip() 
        lists=content.find_all('div',class_='vodplayinfo')

        links=[]
        for li in lists[1].find('ul').find_all('li'):
            links.append(li.find('input')['value'].strip())
        links_m3u8=[]
        for li in lists[2].find('ul').find_all('li'):
            links_m3u8.append(li.find('input')['value'].strip())
    elif engin == 'guangsu':
        response=get(url)
        content=BS(response.content,'html.parser')
        infos=content.find('div',class_='dy-deta').find_all('p')
        for i, info in enumerate(infos):
            if i==0:
                title=info.text.strip()
            elif i == 5:
                status=info.text.strip()
            elif i == 6:
                genre=info.text.strip()
            elif i== 4:
                year = info.text.strip()
            elif i==2:
                region=info.text.strip()
            elif i==3:
                lang = info.text.strip()
        thumb=content.find('div',class_='dy-photo').find('img')['src'].strip()
        intro=content.find('p',class_='dy-moreIns').text.strip() 
        lists=content.find_all('ul',class_='dy-collect-list')
        
        links=[]
        for li in lists[0].find_all('li'):
            v_url=li.find('a')['href'].strip()
            # v_response=get(v_url)
            # v_content=BS(v_response.content,'html.parser')
            # v_link=v_content.find('video',class_='dplayer-video')['src'].strip()
            links.append(v_url)
        links_m3u8=[]
        for li in lists[1].find_all('li'):
            links_m3u8.append(li.find('a')['href'].strip())
    elif engin == 'wolong':
        response=get(url)
        content=BS(response.content,'html.parser')
        infos=content.find('div',class_='right').find_all('p')
        for i, info in enumerate(infos):
            if i==0:
                title=info.text.strip()
            elif i == 12:
                status=info.text.strip()
            elif i == 2:
                genre=info.text.strip()
            elif i== 6:
                year = info.text.strip()
            elif i==7:
                region=info.text.strip()
            elif i==8:
                lang = info.text.strip()
        thumb=content.find('div',class_='left').find('img')['src'].strip()
        intro=content.find('div',class_='content').find('div').text.strip() 
        lists=content.find_all('li',class_='text-style')
        
        links=[]
        links_m3u8=[]
        for li in lists:
            v_url=li.find_all('a')[-1]['href'].strip()
            links_m3u8.append(v_url) 
            links.append(v_url)       
    

    video['title']=title
    video['status']=status
    video['genre']=genre
    video['year']=year
    video['region']=region
    video['lang']=lang
    video['thumb']=thumb
    video['intro']=intro
    video['link']=[links,links_m3u8]

    return video

def get_episode_list(e_url,engin):
        
        video_info=retrive_video_info(e_url,engin)

        source=['links','m3u8']
        index = xbmcgui.Dialog().contextmenu(list=source)

       
        return video_info,index
    
def get_video_list(url,engin):
        videos = []
        _next=url
        if engin == 'feifan':
            prefix='http://ffzy5.tv'
            response=get(url)
            content=BS(response.content,'html.parser')
            v_lists=content.find('ul',class_='videoContent').find_all('li')
            for v_list in v_lists:
                t_url=prefix+'/index.php/vod/detail/id/'+v_list.find('a',class_='address')['href'].strip().split('/')[-1]
                videos.append([v_list.find('a',class_='videoName').text.strip(),
                    t_url])
            try:
                _next=prefix+content.find('a',title='下一页')['href'].strip()
            except:
                _next=url
        elif engin == 'wujinvod':
            response=get(url)
            content=BS(response.content,'html.parser')
            v_lists=content.find_all('a',class_='stui-vodlist__thumb')
            for v_list in v_lists:
                t_url='https://www.wjvod.com'+v_list['href'].strip()
                v_info={'title':v_list['title'].strip(),
                        'thumb':v_list['data-original'].strip()
                        }
                videos.append([v_info,t_url])
            try:
                _next=content.find('ul',class_='stui-page').find_all('li')[-2].find('a')['href']
            except:
                _next=url
        elif engin == 'pianku':
            response=get(url)
            #xbmc.log('check url '+url)
            content=BS(response.content,'html.parser')
            img_lists=content.find_all('div',class_='li-img')
            v_lists=content.find_all('div',class_='li-bottom')  
            for img_list,v_list in zip(img_lists,v_lists):
                t_url='https://www.pkmkv.com'+img_list.find('a')['href'].strip()
                infos=v_list.find('div',class_='tag').text.strip()
                v_info={'title':img_list.find('a')['title'].strip(),
                        'thumb':img_list.find('a').find('img')['src'].strip(),
                        'genre':infos.split('/')[2],
                        'year':infos.split('/')[0],
                        'region':infos.split('/')[1],
                        'lang':infos.split('/')[3],
                        'score':v_list.find('h3').find('span').text.strip()
                        }
                videos.append([v_info,t_url])
            try:
                _next='https://www.pkmkv.com'+content.find('a',class_='a1')['href']
            except:
                _next=url
        elif engin == 'shandian':
            response=get(url)
            content=BS(response.content,'html.parser')
            v_lists=content.find_all('span',class_='xing_vb4')
            for v_list in v_lists:
                t_url='https://shandianzy.com/index.php/vod/detail/id/'+v_list.find('a')['href'].strip().split('/')[-1]
                videos.append([v_list.text.strip(),t_url])
            try:
                _next='https://shandianzy.com'+content.find('a',title='下一页')['href'].strip()
            except:
                _next=url
        elif engin == 'liangzi':
            prefix='http://lzizy.net'
            response=get(url)
            content=BS(response.content,'html.parser')
            v_lists=content.find_all('a',class_='videoName')
            for v_list in v_lists:
                t_url=prefix+'/index.php/vod/detail/id/'+v_list['href'].strip().split('/')[-1]
                videos.append([v_list.text.strip(),t_url])
            try:
                _next=prefix+content.find('a',title='下一页')['href'].strip()
            except:
                _next=url
        elif engin == 'tiankong':
            prefix='http://tkzy1.com'
            response=get(url)
            content=BS(response.content,'html.parser')
            v_lists=content.find_all('span',class_='xing_vb4')
            for v_list in v_lists:
                t_url=prefix+'/vod/detail/id/'+v_list.find('a')['href'].strip().split('id/')[-1]
                videos.append([v_list.text.strip(),t_url])
            try:
                _next=prefix+content.find('a',title='下一页')['href'].strip()
            except:
                _next=url
        elif engin == 'guangsu':
            response=get(url)
            content=BS(response.content,'html.parser')
            v_lists=content.find_all('td',class_='yp')
            for v_list in v_lists:
                t_url='https://www.guangsuzy.com/index.php/vod/detail/id/'+v_list.find('a')['href'].strip().split('id/')[-1]
                videos.append([v_list.text.strip(),t_url])
            try:
                _next='https://www.guangsuzy.com'+content.find('li',class_='next').find('a')['href'].strip()
            except:
                _next=url
        elif engin == 'wolong':
            prefix='https://www.wolongzyw.com'
            response=get(url)
            content=BS(response.content,'html.parser')
            v_lists=content.find_all('a',class_='videoName')
            for v_list in v_lists:
                t_url=prefix+'/index.php/vod/detail/id/'+v_list['href'].strip().split('/')[-1]
                videos.append([v_list.text.strip(),t_url])
            try:
                _next=prefix+content.find('ol',class_='pagination').find_all('li')[-1].find('a')['href'].strip()
            except:
                _next=url
       
        return videos,_next,engin

def get_videos(category):
    index = xbmcgui.Dialog().contextmenu(list=engines)
    if index == -1:
        index=0
    if engines[index] == 'feifan':
        if category == "Movies":
            cat=['All--全部','action--动作片','Comedy--喜剧片','SciFi--科幻片','Horor--恐怖片','Romance--爱情片','Drama--剧情片','War--战争片','Documentary--记录片']
            page=[1,6,7,9,10,8,11,12,20]
            genre= xbmcgui.Dialog().contextmenu(list=cat)
            url = "http://ffzy5.tv/index.php/vod/type/id/{}/page/1.html".format(page[genre]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            cat=['All--全部','Mainland--国产剧','US-EU--欧美剧','Hongkong--香港剧','Koren--韩国片','Taiwan--台湾片','Japan--日本片','World--海外片','Tailand--泰国片']
            page=[2,13,16,14,15,21,22,23,24]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = "http://ffzy5.tv/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            cat=['All--全部','Mainland--国产动漫','JP_KR--日韩动漫','US_EU--欧美动漫','HK_TW--港台动漫','World--海外动漫']
            page=[4,29,30,31,32,33]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = "http://ffzy5.tv/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            cat=['All--全部','Mainland--大陆综艺','US-EU--港台综艺','Hongkong--日韩综艺','Koren--欧美综艺']
            page=[3,25,26,27,28]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = "http://ffzy5.tv/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            query = get_user_input() # User input via onscreen keyboard
            if not query:
                return get_videos(category) # Return empty list if query is blank
            url = "http://ffzy5.tv/index.php/vod/search/page/1/wd/{}.html".format(quote(query)) # Change this to a valid url for search results that you want to scrape
            return get_video_list(url,engines[index])
    elif engines[index] == 'pianku':
        if category == "Movies":
            page=[ '','动作','喜剧','爱情','科幻','恐怖','剧情','战争','纪录','悬疑','犯罪','奇幻','冒险','儿童','动画','歌舞','音乐','惊悚',
                 '丧尸','传记','西部','灾难','古装','武侠','家庭','短片','校园','文艺','运动','青春','励志','人性','美食','女性','治愈','历史']
            genre= xbmcgui.Dialog().contextmenu(list=['全部']+page[1:])
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
         
            region=['','大陆','香港','台湾','美国','法国','英国','日本','韩国','德国','泰国','法国','印度','丹麦','瑞典','荷兰','加拿大',
                    '俄罗斯','丹麦意大利','比利时','西班牙','澳大利亚','其他']
            r=xbmcgui.Dialog().contextmenu(list=['全部']+region[1:])
            year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = "https://www.pkmkv.com/ms/1-{}-{}-{}-----1---{}.html".format(region[r],sorting[s],page[genre],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            page=[ '','动作','喜剧','爱情','科幻','恐怖','剧情','战争','纪录','悬疑','犯罪','奇幻','冒险','儿童','动画','歌舞','音乐','惊悚',
                 '丧尸','传记','西部','灾难','古装','武侠','家庭','短片','校园','文艺','运动','青春','励志','人性','美食','女性','治愈','历史']
            genre= xbmcgui.Dialog().contextmenu(list=['全部']+page[1:])
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
         
            region=['','大陆','香港','台湾','美国','法国','英国','日本','韩国','德国','泰国','法国','印度','丹麦','瑞典','荷兰','加拿大',
                    '俄罗斯','丹麦意大利','比利时','西班牙','澳大利亚','其他']
            r=xbmcgui.Dialog().contextmenu(list=['全部']+region[1:])
            year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = "https://www.pkmkv.com/ms/2-{}-{}-{}-----1---{}.html".format(region[r],sorting[s],page[genre],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            page=[ '','剧情','萌系','科幻','日常','战斗','战争','热血','机战','游戏','搞笑','恋爱','后宫','百合','基腐','冒险','儿童','歌舞',
                  '音乐','奇幻','恐怖','惊悚','犯罪','悬疑','西部','灾难','古装','武侠','泡面','校园','运动','体育','青春','美食','治愈','致郁','励志','历史','其他']
            genre= xbmcgui.Dialog().contextmenu(list=['全部']+page[1:])
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
         
            region=['','大陆','香港','台湾','美国','法国','英国','日本','韩国','德国','泰国','法国','印度','丹麦','瑞典','荷兰','加拿大',
                    '俄罗斯','丹麦意大利','比利时','西班牙','澳大利亚','其他']
            r=xbmcgui.Dialog().contextmenu(list=['全部']+region[1:])
            year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = "https://www.pkmkv.com/ms/4-{}-{}-{}-----1---{}.html".format(region[r],sorting[s],page[genre],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            page=[ '','真人秀','脱口秀','选秀','情感','喜剧','访谈','播报','旅游','音乐','美食','纪实','曲艺','生活','游戏','财经','求职','体育','MV纪录']
            genre= xbmcgui.Dialog().contextmenu(list=['全部']+page[1:])
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
         
            region=['','大陆','香港','台湾','美国','法国','英国','日本','韩国','德国','泰国','法国','印度','丹麦','瑞典','荷兰','加拿大',
                    '俄罗斯','丹麦意大利','比利时','西班牙','澳大利亚','其他']
            r=xbmcgui.Dialog().contextmenu(list=['全部']+region[1:])
            year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
            y=xbmcgui.Dialog().contextmenu(list=year)
            url = "https://www.pkmkv.com/ms/3-{}-{}-{}-----1---{}.html".format(region[r],sorting[s],page[genre],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            page=[ '','动作','喜剧','爱情','科幻','恐怖','剧情','战争','纪录','悬疑','犯罪','奇幻','冒险','儿童','动画','歌舞','音乐','惊悚',
                 '丧尸','传记','西部','灾难','古装','武侠','家庭','短片','校园','文艺','运动','青春','励志','人性','美食','女性','治愈','历史']
            genre= xbmcgui.Dialog().contextmenu(list=['全部']+page[1:])
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
         
            region=['','大陆','香港','台湾','美国','法国','英国','日本','韩国','德国','泰国','法国','印度','丹麦','瑞典','荷兰','加拿大',
                    '俄罗斯','丹麦意大利','比利时','西班牙','澳大利亚','其他']
            r=xbmcgui.Dialog().contextmenu(list=['全部']+region[1:])
            year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = "https://www.pkmkv.com/ms/1-{}-{}-{}-----1---{}.html".format(region[r],sorting[s],page[genre],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
    elif engines[index] == 'wujinvod':
        if category == "Movies":
            cat=['all--全部','action--动作片','Comedy--喜剧片','Romance--爱情片','SciFi--科幻片',
                 'Horor--恐怖片','Drama--剧情片','War--战争片','Documentary--记录片','Misery--悬疑片',
                 'Crime--犯罪片','Fantacy--奇幻片','Shaws--邵氏片']
            page=['',5,6,7,8,9,10,11,22,34,35,36,37]
            genre= xbmcgui.Dialog().contextmenu(list=cat)
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
            region=['','中国大陆','中国香港','中国台湾','美国','法国','英国','日本','韩国','德国','泰国','印度','其他']
            r=xbmcgui.Dialog().contextmenu(list=['全部']+region[1:])
            year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011',]
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = "https://www.wjvod.com/vodshow/{}-{}-{}------1---{}.html".format(page[genre],region[r],sorting[s],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            cat=['all--全部','Mainland--国产剧','Hongkong--香港剧','Taiwan--台湾剧','Japan--日本剧','Koren--韩国剧','US_EU--欧美剧','World--海外剧']
            page=[2,12,13,14,15,16,17,18]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            cat2=['time','hits','score']
            sorting=xbmcgui.Dialog().contextmenu(list=cat2)
            if region == -1:
                region == -2
            url = "https://www.wjvod.com/vodshow/{}--{}------1---.html".format(page[region],cat2[sorting]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            cat=['all--全部','Mainland--国产动漫','JP_KR--日韩动漫','US_EU--欧美动漫','Animation--动漫电影']
            page=[4,28,30,31,33]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            cat2=['time','hits','score']
            sorting=xbmcgui.Dialog().contextmenu(list=cat2)
            if region == -1:
                region == -2
            url = "https://www.wjvod.com/vodshow/{}--{}------1---.html".format(page[region],cat2[sorting]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            cat=['all--全部','Mainland--大陆综艺','HK_TW--港台综艺','JP_KR--日韩综艺','US_EU--欧美综艺']
            page=[3,23,24,25,26]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            cat2=['time','hits','score']
            sorting=xbmcgui.Dialog().contextmenu(list=cat2)
            if region == -1:
                region == -2
            url = "https://www.wjvod.com/vodshow/{}--{}------1---.html".format(page[region],cat2[sorting]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            query = get_user_input() # User input via onscreen keyboard
            if not query:
                return get_videos(category) # Return empty list if query is blank
            url = "https://www.wjvod.com/vodsearch/{}----------1---.html".format(quote(query)) # Change this to a valid url for search results that you want to scrape
            return get_video_list(url,engines[index])
    elif engines[index] == 'shandian':
        if category == "Movies":
            cat=['All--全部','action--动作片','Comedy--喜剧片','Romance--爱情片',
                 'SciFi--科幻片','Horor--恐怖片','Drama--剧情片','War--战争片','Documentary--记录片',
                 'Misery--悬疑片','Crime--犯罪片','Advanture--冒险片','Animation--动画片','Thriller--惊悚片',
                 'Fantaci--奇幻片']
            page=[1,6,7,9,10,8,11,12,20,21,22,38,39,40,43]
            genre= xbmcgui.Dialog().contextmenu(list=cat)
            url = "https://shandianzy.com/index.php/vod/type/id/{}/page/1.html".format(page[genre]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            cat=['All--全部','Mainland--国产剧','US-EU--欧美剧','Koren--韩国片','Japan--日本片','Hongkong--香港剧','Taiwan--台湾片','Tailand--泰国片','World--海外片']
            page=[2,13,14,15,16,17,18,19,23]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 2
            url = "https://shandianzy.com/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            cat=['All--全部','Mainland--国产动漫','JP_KR--日韩动漫','US_EU--欧美动漫','HK_TW--港台动漫','World--海外动漫']
            page=[4,29,30,31,44,45]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = "https://shandianzy.com/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            cat=['All--全部','Mainland--大陆综艺','Hongkong--日韩综艺','US-EU--港台综艺','Koren--欧美综艺','Shows--演唱会']
            page=[3,25,26,27,28,47]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = "https://shandianzy.com/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            cat=['All--全部','Mainland--国产剧','US-EU--欧美剧','Koren--韩国片','Japan--日本片','Hongkong--香港剧','Taiwan--台湾片','Tailand--泰国片','World--海外片']
            page=[2,13,14,15,16,17,18,19,23]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 2
            url = "https://shandianzy.com/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
    elif engines[index] == 'liangzi':
        prefix='http://lzizy.net'
        if category == "Movies":
            cat=['All--全部','action--动作片','Comedy--喜剧片','Romance--爱情片',
                 'SciFi--科幻片','Horor--恐怖片','Drama--剧情片','War--战争片','Documentary--记录片']
            page=[1,6,7,8,9,10,11,12,20]
            genre= xbmcgui.Dialog().contextmenu(list=cat)
            url = prefix+"/index.php/vod/type/id/{}/page/1.html".format(page[genre]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            cat=['All--全部','Mainland--国产剧','US-EU--欧美剧','Koren--韩国片','Japan--日本片',
                 'Hongkong--香港剧','Taiwan--台湾片','Tailand--泰国片','World--海外片','Shorts--短剧']
            page=[2,13,16,15,22,14,21,24,23,46]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 2
            url = prefix+"/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            cat=['All--全部','Mainland--国产动漫','JP_KR--日韩动漫','US_EU--欧美动漫','HK_TW--港台动漫','World--海外动漫']
            page=[4,29,30,31,32,33]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = prefix+"/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            cat=['All--全部','Mainland--大陆综艺','Hongkong--日韩综艺','US-EU--港台综艺','Koren--欧美综艺']
            page=[3,25,27,26,28]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url =prefix+"/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            query = get_user_input() # User input via onscreen keyboard
            if not query:
                return get_videos(category) # Return empty list if query is blank
            url = prefix+"/index.php/vod/search/page/1/wd/{}.html".format(quote(query)) # Change this to a valid url for search results that you want to scrape
            return get_video_list(url,engines[index])
    elif engines[index] == 'tiankong':
        prefix='http://tkzy1.com/'
        if category == "Movies":
            cat=['All--全部','action--动作片','Comedy--喜剧片','Romance--爱情片',
                 'SciFi--科幻片','Horor--恐怖片','Drama--剧情片','War--战争片','Documentary--记录片',
                 'Thriller--悬疑片','Crime--犯罪片','Disaser--灾难片','Animation--动画片',
                 'Fantaci--奇幻片']
            page=[1,6,12,7,8,9,10,11,2,40,21,39,20,38]
            genre= xbmcgui.Dialog().contextmenu(list=cat)
            url = prefix+"vod/type/id/{}/page/1.html".format(page[genre]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            cat=['All--全部','Mainland--国产剧','US-EU--欧美剧','Koren--韩国片','Japan--日本片',
                 'Hongkong--香港剧','Taiwan--台湾片','Tailand--泰国片']
            page=[3,22,4,23,36,5,30,35]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 2
            url =prefix+"vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            cat=['All--全部','Mainland--国产动漫','JP_KR--日韩动漫','US_EU--欧美动漫','World--海外动漫']
            page=[24,31,32,33,34]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = prefix+"vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            cat=['All--全部','Mainland--大陆综艺','Hongkong--日韩综艺','US-EU--港台综艺','Koren--欧美综艺']
            page=[25,26,28,27,29]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = prefix+"vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            query = get_user_input() # User input via onscreen keyboard
            if not query:
                return get_videos(category) # Return empty list if query is blank
            url = prefix+"vod/search/page/1/wd/{}.html".format(quote(query)) # Change this to a valid url for search results that you want to scrape
            return get_video_list(url,engines[index])
    elif engines[index] == 'guangsu':
        prefix='https://www.guangsuzy.com/'
        if category == "Movies":
            cat=['All--全部','action--动作片','Comedy--喜剧片','Romance--爱情片',
                 'SciFi--科幻片','Horor--恐怖片','Drama--剧情片','War--战争片','Documentary--记录片',
                 'Animation--动画片']
            page=[1,6,7,8,9,11,10,12,24,20]
            genre= xbmcgui.Dialog().contextmenu(list=cat)
            url = prefix+"index.php/vod/type/id/{}/page/1.html".format(page[genre]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            cat=['All--全部','Mainland--国产剧','US-EU--欧美剧','Koren--韩国片','Japan--日本片',
                 'Hongkong--香港剧','Taiwan--台湾片','Tailand--泰国片']
            page=[2,13,14,16,21,15,22,23]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 2
            url =prefix+"index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            #cat=['All--全部','Mainland--国产动漫','JP_KR--日韩动漫','US_EU--欧美动漫','World--海外动漫']
            #page=[24,31,32,33,34]
            #region= xbmcgui.Dialog().contextmenu(list=cat)
            region=4
            if region == -1:
                region == 1
            url = prefix+"index.php/vod/type/id/{}/page/1.html".format(region) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            #cat=['All--全部','Mainland--大陆综艺','Hongkong--日韩综艺','US-EU--港台综艺','Koren--欧美综艺']
            #page=[25,26,28,27,29]
            #region= xbmcgui.Dialog().contextmenu(list=cat)
            region=3
            if region == -1:
                region == 1
            url = prefix+"index.php/vod/type/id/{}/page/1.html".format(region) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            query = get_user_input() # User input via onscreen keyboard
            if not query:
                return get_videos(category) # Return empty list if query is blank
            url = prefix+"index.php/vod/search/page/1/wd/{}.html".format(quote(query)) # Change this to a valid url for search results that you want to scrape
            return get_video_list(url,engines[index])
    elif engines[index] == 'wolong':
        prefix='https://www.wolongzyw.com/'
        if category == "Movies":
            cat=['All--全部','action--动作片','Comedy--喜剧片','Romance--爱情片',
                 'SciFi--科幻片','Horor--恐怖片','Drama--剧情片','War--战争片','Documentary--记录片',
                 'Thriller--惊悚片','Crime--犯罪片','Family--灾难片','Animation--动画片',
                 'Misery--悬疑片','History--历史片','History Fiction--古装片']
            page=[1,5,6,7,8,9,10,11,22,39,46,42,24,45,44,43]
            genre= xbmcgui.Dialog().contextmenu(list=cat)
            url = prefix+"index.php/vod/type/id/{}/page/1.html".format(page[genre]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            cat=['All--全部','Mainland--国产剧','US-EU--欧美剧','Koren--韩国剧','Japan--日本剧',
                 'Hongkong--香港剧','Taiwan--台湾剧','Tailand--泰国剧','World--泰国剧']
            page=[2,12,15,14,17,13,16,33,18]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 2
            url =prefix+"index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            cat=['All--全部','Mainland--国产动漫','JP_KR--日韩动漫','US_EU--欧美动漫']
            page=[4,25,27,26]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = prefix+"index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            cat=['All--全部','Mainland--大陆综艺','Hongkong--日韩综艺','US-EU--港台综艺','Koren--欧美综艺']
            page=[3,32,31,30,37]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = prefix+"index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            query = get_user_input() # User input via onscreen keyboard
            if not query:
                return get_videos(category) # Return empty list if query is blank
            url = prefix+"index.php/vod/search/page/1/wd/{}.html".format(quote(query)) # Change this to a valid url for search results that you want to scrape
            return get_video_list(url,engines[index])

def home_list():
    categories = get_home()
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        url = get_url(action='searching', category=category)

        is_folder = True

        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)


def list_videos(category):
    
    videos,_next,engin = get_videos(category)
    for i,video in enumerate(videos):
        
        if engin == 'wujinvod':
            list_item = xbmcgui.ListItem(label=video[0]['title'])
            list_item.setInfo('video', {'title': video[0]['title'] })
            list_item.setArt({'thumb': video[0]['thumb'], 'icon': video[0]['thumb'], 'fanart': video[0]['thumb']})
        elif engin == 'pianku':
            list_item = xbmcgui.ListItem(label=video[0]['title'])
            list_item.setInfo('video', {'title': video[0]['title'], 'genre': video[0]['genre'], 'country': video[0]['region'],
                                       'rating': float(video[0]['score'])})
            list_item.setArt({'thumb': video[0]['thumb'], 'icon': video[0]['thumb'], 'fanart': video[0]['thumb']})
        else :
            list_item = xbmcgui.ListItem(label=video[0])
        url = get_url(action='listing', eposide=video[1],engin=engin)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    xbmcplugin.addDirectoryItem(_handle, get_url(action='listing_next', url=_next,engin=engin), xbmcgui.ListItem(label='Next-下一页'), True)
    xbmcplugin.endOfDirectory(_handle)
def list_videos_next (url,engin):

    videos,_next,engin = get_video_list(url,engin)
    for i,video in enumerate(videos):
        if engin == 'wujinvod':
            list_item = xbmcgui.ListItem(label=video[0]['title'])
            list_item.setInfo('video', {'title': video['title']})
            list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        elif engin == 'pianku':
            list_item = xbmcgui.ListItem(label=video[0]['title'])
            list_item.setInfo('video', {'title': video[0]['title'], 'genre': video[0]['genre'], 'country': video[0]['region'],
                                       'rating': float(video[0]['score'])})
            list_item.setArt({'thumb': video[0]['thumb'], 'icon': video[0]['thumb'], 'fanart': video[0]['thumb']})
        else :
            list_item = xbmcgui.ListItem(label=video[0])
        url = get_url(action='listing', eposide=video[1],engin=engin)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addDirectoryItem(_handle, get_url(action='listing_next', url=_next,engin=engin), xbmcgui.ListItem(label='Next-下一页'), True)
    xbmcplugin.endOfDirectory(_handle)

def list_episode(e_url,engin):

    # Get the list of videos in the category.
    video,index = get_episode_list(e_url,engin)
    # Iterate through videos.
    
    i=1
    for link in video['link'][1]:
        list_item = xbmcgui.ListItem(label='Episode:'+str(i)+'----第'+str(i)+'集')
        list_item.setInfo('video', {'title': 'Episode:'+str(i)+'----第'+str(i)+'集', 'genre': video['genre'], 'plot': video['intro']})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', video=link)
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        i+=1
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)
def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'searching':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_episode(params['eposide'],params['engin'])
        elif params['action'] == 'listing_next':
            # Display the list of videos in a provided category.
            list_videos_next(params['url'],params['engin'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        home_list()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
