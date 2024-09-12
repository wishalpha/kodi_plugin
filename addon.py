# coding: utf-8
import sys,os

try:
    from urllib import urlencode
    from urllib import quote,unquote
    from urlparse import parse_qsl
except ImportError:
    from urllib.parse import urlencode,quote,parse_qsl,unquote

import datetime
from bs4 import BeautifulSoup as BS
from requests import get
import xbmcgui
import xbmcplugin
import xbmc
import xbmcvfs

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

CATEGORIES = ["Movies", "TVshows","Comics","Entertainment","Search" ]
engines =['wujinvod','pianku','feifan','taopian','shandian','liangzi','tiankong','guangsu','wolong']
current_year = datetime.datetime.now().year
def get_user_input():  
    kb = xbmc.Keyboard('', 'Please enter the video title')
    kb.doModal() # Onscreen keyboard appears
    if not kb.isConfirmed():
        return
    query = kb.getText() # User input
    return query

def get_ip():  
    file_path='server_list'
    server_list = ['192.168.1.169','127.0.0.1','192.168.1.253']
    #with open(file_path, 'r') as file:
    #    for line in file:
    #        server_list.append(line.strip())
    ip_index= xbmcgui.Dialog().contextmenu(list=['new']+server_list)
    if ip_index == 0:
        kb = xbmc.Keyboard('192.168.1.', 'Please enter server ip')
        kb.doModal() # Onscreen keyboard appears
        if not kb.isConfirmed():
            return '192.168.1.169'
        query = kb.getText() # User input
    #    with open(file_path, 'a') as file:
    #        file.write(query+'\n')
        return query
    return server_list[ip_index-1]
def to_text (url_string):
    return unquote(url_string)
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
        for li in lists[-1].find_all('li'):
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
    elif engin == 'taopian':
        response=get(url)
        content=BS(response.content,'html.parser')
        title=content.find('span',class_='name').text.strip()
        region=None
        lang = None
        status=None
        genre=None 
        year=None
        thumb=content.find('img',class_='lazyload')['data-original'].strip()
        intro=content.find('pre',id='pretags').text.strip() 
        lists=content.find_all('input',class_='m3u8')
        links_m3u8=[]
        links=[]
        for li in lists:
            vlink=li['value'].strip()
            links.append(vlink)
            links_m3u8.append(vlink)      
        #for li in lists[1].find_all('li')[:-1]:
            #links_m3u8.append(li.find('a')['href'].strip())
    elif engin == 'pianku':
        prefix='https://www.pian-ku.com'
        response=get(url)
        content=BS(response.content,'html.parser')
        title=content.find('a',class_='vodlist_thumb')['title'].strip()
        region=None
        lang = None
        status=None
        genre=None 
        year=None
        thumb=prefix+content.find('a',class_='vodlist_thumb')['data-original'].strip()
        intro=content.find('div',class_='full_text').find('span').text.strip() 
        lists=content.find_all('ul',class_='content_playlist')
        y=xbmcgui.Dialog().contextmenu(list=['source: '+ str(x+1) for x in range(len(lists))])
        links_m3u8=[]
        links=[]
        for li in lists[y].find_all('li'):
            v_url=prefix+li.find('a')['href'].strip()
            #xbmc.log('check the url '+v_url)
            v_response=get(v_url)
            v_content=BS(v_response.content,'html.parser')
            #v_link=v_content.find('div',class_='stui-player__video').find('script').text.strip().split('http')[-1].split('index.m3u8')[0].replace('\\','')
            v_link=v_content.find('div',class_='player_video').find('script').string
            v_link=''.join(v_link).split('http')[-1].split('index.m3u8')[0].replace('\\','')
            #xbmc.log('get the url '+v_link)
            links.append('http'+v_link+'index.m3u8')
            links_m3u8.append('http'+v_link+'index.m3u8')      
        #for li in lists[1].find_all('li')[:-1]:
            #links_m3u8.append(li.find('a')['href'].strip())
    elif engin == 'pkmkv':
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
        
        lists=content.find('div',class_='bd').find_all('ul',class_='player')[index]
        
        links=[]
        links_m3u8=[]
        for li in lists.find_all('li'):
            v_url='https://www.pkmkv.com'+li.find('a')['href'].strip()
            v_response=get(v_url)
            v_content=BS(v_response.content,'html.parser')
            v_link=v_content.find('div',id='video').find('script').string
            v_link=''.join(v_link).split('http')[-1].split('index.m3u8')[0].replace('\\','')
            links.append('http'+v_link+'index.m3u8')
            links_m3u8.append('http'+v_link+'index.m3u8')
        
        
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

        #source=['links','m3u8']
        #index = xbmcgui.Dialog().contextmenu(list=source)
        index=1
       
        return video_info,index
    
def get_video_list(url,engin):
        videos = []
        _next=url
        if engin == 'feifan':
            prefix='http://ffzy1.tv'
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
        elif engin == 'taopian':
            prefix='https://www.taopianzy.com'
            response=get(url)
            content=BS(response.content,'html.parser')
            v_lists=content.find_all('span',class_='fontbule')
            for v_list in v_lists:
                t_url=prefix+v_list.find('a')['href'].strip()
                videos.append([v_list.find('a').text.strip(),
                    t_url])
            try:
                #_next=url.split('page=')[-1]+str(int(url.split('page=')[-1][0])+1)+url.split('page=')[-1][1:]
                _next=url[:-1]+str(int(url[-1])+1)
            except:
                _next=url
        elif engin == 'wujinvod':
            prefix='https://wjvod.com'
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
                _next=prefix+content.find('ul',class_='stui-page').find_all('li')[-2].find('a')['href'].strip()
            except:
                _next=url
        elif engin == 'pkmkv':
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
                _next='https://www.pkmkv.com'+content.find('a',class_='a1')['href'].strip()
            except:
                _next=url
        elif engin == 'pianku':
            prefix='https://www.pian-ku.com'
            response=get(url)
            #xbmc.log('check url '+url)
            content=BS(response.content,'html.parser')
            
            v_lists=content.find_all('a',class_='vodlist_thumb')  
            for v_list in v_lists:
                t_url=prefix+v_list['href'].strip()
                #infos=v_list.find('div',class_='tag').text.strip()
                v_info={'title':v_list['title'].strip(),
                        'thumb':prefix+v_list['data-original'].strip()
                        }
                videos.append([v_info,t_url])
            try:
                _next=prefix+content.find('ul',class_='page').find_all('li')[-2].find('a')['href'].strip()

            except:
                _next=url
        elif engin == 'shandian':
            prefix='https://shandianzy.com'
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

def get_videos(category,index):

    #index = xbmcgui.Dialog().contextmenu(list=engines)
    #if index == -1:
    #    index=0
    if engines[index] == 'feifan':
        prefix='http://ffzy1.tv'
        if category == "Movies":
            cat=['All--全部','action--动作片','Comedy--喜剧片','SciFi--科幻片','Horor--恐怖片','Romance--爱情片','Drama--剧情片','War--战争片','Documentary--记录片']
            page=[1,6,7,9,10,8,11,12,20]
            genre= xbmcgui.Dialog().contextmenu(list=cat)
            url = prefix+"/index.php/vod/type/id/{}/page/1.html".format(page[genre]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            cat=['All--全部','Mainland--国产剧','US-EU--欧美剧','Hongkong--香港剧','Koren--韩国片','Taiwan--台湾片','Japan--日本片','World--海外片','Tailand--泰国片']
            page=[2,13,16,14,15,21,22,23,24]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
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
            cat=['All--全部','Mainland--大陆综艺','US-EU--港台综艺','Hongkong--日韩综艺','Koren--欧美综艺']
            page=[3,25,26,27,28]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = prefix+"/index.php/vod/type/id/{}/page/1.html".format(page[region]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            query = get_user_input() # User input via onscreen keyboard
            if not query:
                return get_videos(category,index) # Return empty list if query is blank
            url = prefix+"/index.php/vod/search/page/1/wd/{}.html".format(quote(query)) # Change this to a valid url for search results that you want to scrape
            return get_video_list(url,engines[index])
    if engines[index] == 'taopian':
        prefix='https://www.taopianzy.com/'
        if category == "Movies":
            cat=['全部','战争片','奇幻片','科幻片','剧情片','惊悚片','恐怖片','爱情片','动作片','喜剧片','动画片','冒险片','悬疑片','纪录片']
            cat_id=['',235,233,234,222,223,226,227,228,229,230,231,128,18]
            cid= xbmcgui.Dialog().contextmenu(list=cat)
            area=['全部','中国','香港','台湾','美国','英国','法国','日本','韩国','泰国','印度','其它']
            area_id=['',110,111,112,113,114,115,116,117,118,119,109]
            aid= xbmcgui.Dialog().contextmenu(list=area)
            url = prefix+"/vod/list.html?type_id=1&cate_id={}&year_id=&area_id={}&page=1".format(str(cat_id[cid]),str(area_id[aid])) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            cat=['all','欧美剧','海外剧','国产剧','香港剧','日本剧','韩国剧','泰国剧','台湾剧']
            cat_id=['',232,237,238,239,240,241,246,249]
            cid= xbmcgui.Dialog().contextmenu(list=cat)
            url = prefix+"/vod/list.html?type_id=20&cate_id={}&page=1".format(str(cat_id[cid])) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            cat=['all','日本动漫','国产动漫','欧美动漫','海外动漫']
            cat_id=['',242,243,244,252]
            cid= xbmcgui.Dialog().contextmenu(list=cat)
            if region == -1:
                region == 1
            url = prefix+"/vod/list.html?type_id=148&cate_id={}&page=1".format(str(cat_id[cid])) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            cat=['All--全部','大陆综艺','港台综艺','欧美综艺','日韩综艺','海外综艺']
            cat_id=['',245,247,248,250,251]
            cid= xbmcgui.Dialog().contextmenu(list=cat)

            url = prefix+"/vod/list.html?type_id=142&cate_id={}&page=1".format(str(cat_id[cid]))# Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            query = get_user_input() # User input via onscreen keyboard
            if not query:
                return get_videos(category,index) # Return empty list if query is blank
            url = prefix+"/search.html?keyword={}&page=1".format(quote(query)) # Change this to a valid url for search results that you want to scrape
            return get_video_list(url,engines[index])

    elif engines[index] == 'pkmkv':
        if category == "Movies":
            page=[ '','动作','喜剧','爱情','科幻','恐怖','剧情','战争','纪录','悬疑','犯罪','奇幻','冒险','儿童','动画','歌舞','音乐','惊悚',
                 '丧尸','传记','西部','灾难','古装','武侠','家庭','短片','校园','文艺','运动','青春','励志','人性','美食','女性','治愈','历史']
            genre= xbmcgui.Dialog().contextmenu(list=['全部']+page[1:])
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
         
            region=['','大陆','香港','台湾','美国','法国','英国','日本','韩国','德国','泰国','法国','印度','丹麦','瑞典','荷兰','加拿大',
                    '俄罗斯','丹麦意大利','比利时','西班牙','澳大利亚','其他']
            r=xbmcgui.Dialog().contextmenu(list=['全部']+region[1:])
            
            
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
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
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
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
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
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
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
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
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = "https://www.pkmkv.com/ms/1-{}-{}-{}-----1---{}.html".format(region[r],sorting[s],page[genre],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])

    elif engines[index] == 'pianku':
        prefix='https://www.pian-ku.com'
        if category == "Movies":
            rr=['全部','动作片','喜剧片','爱情片','科幻片','恐怖片','剧情片','战争片','纪录片','惊悚片','奇幻片',
            '冒险片','电影解说','灾难片','犯罪片','悬疑片','动画片','经典片','网络片','歌舞片']
            pp= xbmcgui.Dialog().contextmenu(rr)
            rrr=[1,7,8,9,10,11,12,20,21,22,23,56,27,28,29,30,40,41,44]

            page=[ '','喜剧','爱情','恐怖','动作','科幻','剧情','战争','警匪','犯罪','动画','奇幻','武侠','冒险','枪战','恐怖','悬疑','惊悚','经典','青春','文艺',
                  '微电影','古装','历史','运动','农村','儿童','网络电影']
            genre= xbmcgui.Dialog().contextmenu(list=['全部']+page[1:])
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
         
            region=['','大陆','香港','台湾','美国','法国','英国','日本','韩国','德国','泰国','印度','意大利','西班牙','加拿大','其他']
            r=xbmcgui.Dialog().contextmenu(list=['全部']+region[1:])
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = prefix+"/vodshow/{}-{}-{}-{}-----1---{}.html".format(str(rrr[pp]),region[r],sorting[s],page[genre],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            page=[ '','古装','战争','青春偶像','喜剧','家庭','犯罪','动作','奇幻','剧情','历史','经典','乡村','情景','商战','网剧','其他']
            genre= xbmcgui.Dialog().contextmenu(list=['全部']+page[1:])
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
         
            region=['全部','国产剧','港台剧','日韩剧','欧美剧','新马剧','泰国剧','其他剧','短剧']
            r=xbmcgui.Dialog().contextmenu(list=['全部']+region[1:])
            re=[2,14,15,16,42,26,43,65]
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2006','2005','2004']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = prefix+"/vodshow/{}--{}-{}-----1---{}.html".format(str(re[r]),sorting[s],page[genre],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            page=[ '','情感','科幻','热血','推理','搞笑','冒险','萝莉','校园','动作','机战','运动','战争','少年','少女','社会','原创','亲子','益智','励志','其他']
            genre= xbmcgui.Dialog().contextmenu(list=['全部']+page[1:])
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
         
            region=['全部','国产动漫','欧美动漫','日本动漫','韩国动漫','港台动漫','其他动漫']
            r=xbmcgui.Dialog().contextmenu(list=['全部']+region[1:])
            re=[4,33,34,35,36,39,55]
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = prefix+"/vodshow/{}--{}-{}-----1---{}.html".format(str(re[r]),sorting[s],page[genre],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            region=['全部','国内综艺','欧美综艺','日本综艺','韩国综艺','港台综艺','其他综艺']

            r=xbmcgui.Dialog().contextmenu(region)
            re=[3,31,32,37,38,45,46]

            page=[ '','选秀','情感','访谈','播报','旅游','音乐','美食','纪实','曲艺','生活','游戏互动','财经','求职']
            genre= xbmcgui.Dialog().contextmenu(list=['全部']+page[1:])
            sorting=['time','hits','score']
            s=xbmcgui.Dialog().contextmenu(list=sorting)
         
            
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = prefix+"/vodshow/{}--{}-{}-----1---{}.html".format(str(re[r]),sorting[s],page[genre],year[y]) # Change this to a valid url that you want to scrape
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
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
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
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            url = "https://www.wjvod.com/vodshow/{}-{}-{}------1---{}.html".format(page[genre],region[r],sorting[s],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "TVshows":
            cat=['all--全部','Mainland--国产剧','Hongkong--香港剧','Taiwan--台湾剧','Japan--日本剧','Koren--韩国剧','US_EU--欧美剧','World--海外剧']
            page=[2,12,13,14,15,16,17,18]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            cat2=['time','hits','score']
            sorting=xbmcgui.Dialog().contextmenu(list=cat2)
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011']
            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            if region == -1:
                region == -2
            url = "https://www.wjvod.com/vodshow/{}--{}------1---{}.html".format(page[region],cat2[sorting],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Comics":
            cat=['all--全部','Mainland--国产动漫','JP_KR--日韩动漫','US_EU--欧美动漫','Animation--动漫电影']
            page=[4,28,30,31,33]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            cat2=['time','hits','score']
            sorting=xbmcgui.Dialog().contextmenu(list=cat2)

            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011']

            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            if region == -1:
                region == -2
            url = "https://www.wjvod.com/vodshow/{}--{}------1---{}.html".format(page[region],cat2[sorting],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Entertainment":
            cat=['all--全部','Mainland--大陆综艺','HK_TW--港台综艺','JP_KR--日韩综艺','US_EU--欧美综艺']
            page=[3,23,24,25,26]
            region= xbmcgui.Dialog().contextmenu(list=cat)
            cat2=['time','hits','score']
            sorting=xbmcgui.Dialog().contextmenu(list=cat2)
            year = [''] + [str(y) for y in range(current_year, current_year-15, -1)]
            #year=['','2023','2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']

            y=xbmcgui.Dialog().contextmenu(list=['全部']+year[1:])
            if region == -1:
                region == -2
            url = "https://www.wjvod.com/vodshow/{}--{}------1---{}.html".format(page[region],cat2[sorting],year[y]) # Change this to a valid url that you want to scrape
            return get_video_list(url,engines[index])
        elif category == "Search":
            query = get_user_input() # User input via onscreen keyboard
            if not query:
                return get_videos(category,index) # Return empty list if query is blank
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
                return get_videos(category,index) # Return empty list if query is blank
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
                return get_videos(category,index) # Return empty list if query is blank
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
                return get_videos(category,index) # Return empty list if query is blank
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
                return get_videos(category,index) # Return empty list if query is blank
            url = prefix+"index.php/vod/search/page/1/wd/{}.html".format(quote(query)) # Change this to a valid url for search results that you want to scrape
            return get_video_list(url,engines[index])

def home_list():
    categories = get_home()
    index = xbmcgui.Dialog().contextmenu(list=engines)
    if index == -1:
        index=0
    list_item = xbmcgui.ListItem(label='local')
    url = get_url(action='xiaoya_home')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    # Iterate through categories
    for category in categories:
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=category)
        url = get_url(action='searching', category=category,index=index)

        is_folder = True

        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    list_item = xbmcgui.ListItem(label='Change Engine')
    url = get_url(action='home')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    
    

    xbmcplugin.endOfDirectory(_handle)


def list_videos(category,index):
    
    videos,_next,engin = get_videos(category,int(index))
    for i,video in enumerate(videos):
        
        if engin == 'wujinvod':
            list_item = xbmcgui.ListItem(label=video[0]['title'])
            #list_item.setInfo('video', {'title': video[0]['title'] })
            list_item.setArt({'thumb': video[0]['thumb'], 'icon': video[0]['thumb'], 'fanart': video[0]['thumb']})
        elif engin == 'pianku':
            list_item = xbmcgui.ListItem(label=video[0]['title'])
            #list_item.setInfo('video', {'title': video[0]['title'], 'genre': video[0]['genre'], 'country': video[0]['region'],
                                       #'rating': float(video[0]['score'])})
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
            #list_item.setInfo('video', {'title': video['title']})
            list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        elif engin == 'pianku':
            list_item = xbmcgui.ListItem(label=video[0]['title']+'    '+video[0]['genre']+'    '+video[0]['region']+'    '+video[0]['lang']+'    '+video[0]['score'])
            #list_item.setInfo('video', {'title': video[0]['title'], 'genre': video[0]['genre'], 'country': video[0]['region'],
                                       #'rating': float(video[0]['score'])})
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
    # xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)
def get_content(file_path):
    types = ['mp4', 'mp3', 'mkv', 'avi', 'webm', 'mov','flv','ts','wmv','rm','m4v','3gp',
            'aac','flac','wav','wma','ogg','m4a']
    video_path=[]
    dir_path=[]
    xbmc.log('grab in :'+file_path,xbmc.LOGERROR)
    dirs,files_list = xbmcvfs.listdir(file_path)
    for d in dirs:
        dir_path.append(os.path.join(file_path,d))
    for item in files_list: 
        #xbmc.log('grab in :'+item,xbmc.LOGERROR)
        #file_name = to_text(item)          
        #if file_name.split('.')[-1].lower() in types:
            #xbmc.log('matching with :'+item,xbmc.LOGERROR) 
        video_path.append(os.path.join(file_path,item)) 
    return dir_path,video_path

def search_content(file_path,keywords,level = 1):
    if level <1 :
        return [],[]
    #xbmc.log('search in :'+file_path,xbmc.LOGERROR)    
    dirs,files_list = xbmcvfs.listdir(file_path) 
    temp = []
    temp2=[] 
    for d in files_list:
        #xbmc.log('search in :'+d,xbmc.LOGERROR)
        if keywords.lower() in to_text(d).lower():
            temp2.append(os.path.join(file_path,d))   
    for d in dirs[1:]:
        #xbmc.log('search in :'+d,xbmc.LOGERROR)
        if keywords.lower() in to_text(d).lower():
            temp.append(os.path.join(file_path,d))
        subfolder,subfile = search_content(os.path.join(file_path,d),keywords,level-1)
        temp+=subfolder 
        temp2+= subfile
    

    return temp,temp2
def home_xiaoya(server_path):
    #items = ['all','Search Xiaoya','xiaoya', 'PikPak', 'MyShare']
    #actions = ['xiaoya_list','xiaoya_search','xiaoya_list','xiaoya_list','xiaoya_list']
    #paths = ['dav','dav/Net/Xiaoya','dav/Net/Xiaoya','dav/pikpak','dav/Net/PikPakShare']
    items = ['all','Search Xiaoya','Movies', 'TVShows', 'Documentary', 'Comics']
    actions = ['xiaoya_list','xiaoya_search','xiaoya_list','xiaoya_list','xiaoya_list','xiaoya_list']
    paths = ['dav','dav','dav/电影','dav/电视剧','dav/纪录片','dav/教育/儿童合集']
    for i,item in enumerate(items):
        # Create a list item with a text label and a thumbnail image.
        list_item = xbmcgui.ListItem(label=item)
        url = get_url(action=actions[i],path=os.path.join(server_path,paths[i]))
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    list_item = xbmcgui.ListItem(label='Back Home')
    url = get_url(action='home')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder) 

    xbmcplugin.endOfDirectory(_handle)

def list_xiaoya(path):
    list_item = xbmcgui.ListItem(label='Back to xiaoya Home')
    url = get_url(action='xiaoya_home')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder) 

    list_item = xbmcgui.ListItem(label='search from here')
    url = get_url(action='xiaoya_find',path=path)
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder) 

    dir_path, video_path = get_content (path)
    for p in dir_path[1:]:
        list_item = xbmcgui.ListItem(label=to_text(os.path.basename(p)))
        url = get_url(action='xiaoya_list', path=p)
        is_folder = True   
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    for p in video_path:
        list_item = xbmcgui.ListItem(label=to_text(os.path.basename(p)))
        video_url = p.split('@')[-1].split('dav/')
        #url = get_url(action='play', video='http://'+video_url[0]+video_url[1])
        #url = get_url(action='xiaoya_play', video=p)
        #url = get_url(action='play', video='dav://'+p.split('@')[-1])
        url = p
        is_folder = False  
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    list_item = xbmcgui.ListItem(label='Back Home')
    url = get_url(action='home')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder) 
    xbmcplugin.endOfDirectory(_handle)

def find_xiaoya(path):

    list_item = xbmcgui.ListItem(label='Back to xiaoya Home')
    url = get_url(action='xiaoya_home')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder) 
    keywords = get_user_input()
    
    level = xbmcgui.Dialog().contextmenu(list=['search in current directory','search in 2 level','search in 3 level',
                                                    'search in 4 level','search in 5 level'])
    if level == -1:
        level = 0;
    dir_path, video_path= search_content (path,keywords,level+1)
    for p in dir_path:
        list_item = xbmcgui.ListItem(label=to_text(os.path.basename(p)))
        url = get_url(action='xiaoya_list', path=p)
        is_folder = True   
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    for p in video_path:
        list_item = xbmcgui.ListItem(label=to_text(os.path.basename(p)))
        #video_url = p.split('@')[-1].split('dav/')
        #url = get_url(action='play', video='http://'+video_url[0]+video_url[1])
        #url = get_url(action='xiaoya_play', video=p)
        #url = get_url(action='play', video='dav://'+p.split('@')[-1])
        url = p
        is_folder = False   
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    list_item = xbmcgui.ListItem(label='Back Home')
    url = get_url(action='home')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder) 
    xbmcplugin.endOfDirectory(_handle)

def search_xiaoya (path):
    server_ip = to_text(path).split('@')[-1].split(':')[0]
    search_string = get_user_input()
    url = f'http://{server_ip}:5678/search?box={search_string}&url=&type=video'
    headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }

    response=get(url,headers=headers)

    content=BS(response.content,'html.parser')
    links = content.find_all('ul')[-1].find_all('a')

    list_item = xbmcgui.ListItem(label='Back to xiaoya Home')
    url = get_url(action='xiaoya_home')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder) 

    for link in links:
        #p = link['href'].strip()
        p = link.text.strip()
        list_item = xbmcgui.ListItem(label=to_text(os.path.basename(p)))
        url = get_url(action='xiaoya_list', path=os.path.join(path,p))
        is_folder = True   
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)

    list_item = xbmcgui.ListItem(label='Back Home')
    url = get_url(action='home')
    is_folder = True
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder) 
    xbmcplugin.endOfDirectory(_handle)


def play_video(path):
    
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
    #video_url = path.split('@')[-1].split('dav/')
    #url = 'http://'+video_url[0]+video_url[1] 
    #xbmc.log('playing :'+to_text(url),xbmc.LOGERROR) 
    #xbmc.Player().play(path)
def play_xiaoya(path):

    video_url = 'dav://'+path.split('@')[-1]
    play_item = xbmcgui.ListItem(path=video_url)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'searching':
            # Display the list of videos in a provided category.
            list_videos(params['category'],params['index'])
        elif params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_episode(params['eposide'],params['engin'])
        elif params['action'] == 'listing_next':
            # Display the list of videos in a provided category.
            list_videos_next(params['url'],params['engin'])
        elif params['action'] == 'xiaoya_list':
            # Display the list of videos/folder in a xiaoya webdav.           
            list_xiaoya(params['path'])
        elif params['action'] == 'xiaoya_search':
            # Display the list of videos/folder in a xiaoya webdav.
            #index = xbmcgui.Dialog().contextmenu(list=['search 2 level','search 3 level','search 4 level','search 5 level'])           
            search_xiaoya(params['path'])
        elif params['action'] == 'xiaoya_find':
            # Display the list of videos/folder in a xiaoya webdav.
            #index = xbmcgui.Dialog().contextmenu(list=['search in current level','search 2 level','search 3 level','search 4 level'])           
            find_xiaoya(params['path'])
        elif params['action'] == 'xiaoya_home':
            # Display the list of videos/folder in a xiaoya webdav. 
                                  
            #home_xiaoya('dav://admin:root@{}:5244'.format(get_ip()))
            home_xiaoya('dav://guest:guest_Api789@{}:5678'.format(get_ip()))
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            #xbmc.log('Playing :'+to_text(params['video']),xbmc.LOGERROR)
            play_video(params['video'])
        elif params['action'] == 'xiaoya_play':
            # Play a video from a provided URL.
            #xbmc.log('Playing :'+to_text(params['video']),xbmc.LOGERROR)
            
            play_xiaoya(params['video'])
            #list_xiaoya(os.path.dirname(params['video'])) 
            #xbmc.Player().play(params['video'])     
        elif params['action'] == 'home':
            # Play a video from a provided URL.
            home_list()
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        home_list()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
