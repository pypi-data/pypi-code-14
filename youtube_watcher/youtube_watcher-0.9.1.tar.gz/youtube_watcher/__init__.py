#!/usr/bin/env python3


import os
import sys
import json
import argparse
import shutil
import time
import math
import difflib
import urllib.request
import urllib
import socket
import re
import ssl
import subprocess
import threading
import curses
import youtube_dl
import difflib
from bs4 import BeautifulSoup
from youtube_watcher.cprint import cprint
from youtube_watcher.threads import asthread


FILE_DIR = '{}/.youtube_watcher'.format(os.getenv('HOME'))
VERSION = '0.9.1'


class VoidLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class VideoList:
    def __init__(self, title, videos, show_seen, reg, fav):
        self.title = title 
        self.show_seen = show_seen
        if reg is not None:
            self.regex = re.compile(reg, re.I)
        else:
            self.regex = None
        self.show_favorite = fav
        self.pos = 0
        self.off = 0
        self.selected = []
        self.videos = videos
        self.data = {}
        self.downloads = {}
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.screen.keypad(True)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_CYAN, -1)
        curses.init_pair(4, curses.COLOR_YELLOW, -1)

    def shutdown(self):
        curses.echo()
        curses.nocbreak()
        self.screen.keypad(False)
        curses.endwin()
        return None

    def main(self):
        while True:
            char = str(self.create_list())
            func = getattr(self, 'k_{}'.format(char), None)
            if func is not None:
                try:
                    quit = func()
                    if quit:
                        return None
                except Exception:
                    self.shutdown()
                    raise
        return None

    def create_list(self, getch=True):
        if self.show_seen:
            self.vidlist = self.videos
        else:
            self.vidlist = [x for x in self.videos if not x['seen']]
        if self.regex is not None:
            self.vidlist = [x for x in self.vidlist 
                            if re.search(self.regex, x['title'])]
        if self.show_favorite:
            self.vidlist = [x for x in self.vidlist if 
                            'fav' in x and x['fav']]
        self.screen.clear()
        self.screen.refresh()
        self.height, self.width = self.screen.getmaxyx()
        self.screen.addstr(self.title.center(self.width), curses.color_pair(1) 
                            | curses.A_BOLD)
        instructions = ('[D]ownload. Download [A]udio. Mark as [S]een. '
                        'Mark as [U]n-seen. [Q]uit.')
        self.screen.addstr(instructions.center(self.width))
        self.end = 4
        videos = self.vidlist[self.off:self.off+self.height-self.end]
        active = ''
        for y, i in enumerate(videos):
            opts = 0
            
            if i['seen']:
                opts |= curses.A_DIM

            if 'fav' in i and i['fav']:
                opts |= curses.color_pair(3)

            title = i['title']
            pref = '    '
            if title in self.data:
                pref = ' {} '.format(self.data[title]['perc'])
                if 'watch' in self.data[title] and self.data[title]['watch']:
                    opts |= curses.A_UNDERLINE
            if any(title == x['title'] for x in self.selected):
                opts |= curses.A_REVERSE
            space = self.width-len(title)-2
            pref = pref.center(6)
            if y == self.pos:
                opts =  curses.color_pair(1)
                active = i['title']
            self.screen.addstr(y+3, 0, '{}{}'.format(pref,
                               title).ljust(self.width), opts)
        if self.vidlist != []:
            perc = round((self.pos+self.off+1)/len(self.vidlist)*100)
            percstring = '({}/{}) {}%'.format(self.pos+self.off+1,
                         len(self.vidlist), perc)
            if active in self.data:
                status = ' {}'.format(self.data[active]['status'])
                if '_speed_str' in self.data[active]['info']:
                    inf = self.data[active]['info']
                    status += ' {} ETA {}'.format(inf['_speed_str'],
                              inf['_eta_str'])
            else:
                status = ''
            statbar = '{}{}'.format(status,
                      percstring.rjust(self.width-1-len(status)))
            self.screen.addstr(self.height-1, 0, statbar)
        if getch:
            return self.screen.getch()
        self.screen.refresh()
        return None

    def k_32(self):
        title = self.vidlist[self.off+self.pos]
        if title in self.selected:
            del self.selected[self.selected.index(title)]
        else:
            self.selected.append(title)
        self.k_258()
        return None

    
    def k_106(self):
        self.k_258()
        return None

    def k_107(self):
        self.k_259()
        return None
    
    def k_258(self):
        if self.pos + self.off == len(self.vidlist)-1:
            return None
        self.pos += 1
        if self.pos == self.height-self.end:
            self.pos -= 1
            self.off += 1
        return None

    def k_259(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = 0
            self.off -= 1
        if self.off < 0:
            self.off = 0
        return None

    def k_97(self):
        for item in self.get_active():
            self.start_download(item, True)
        self.selected = []
        return None

    @asthread()
    def start_download(self, item, audio=False):
        title = item['title']
        url = 'https://www.youtube.com/watch?v={}'.format(item['id'])
        options = {
            'logger': VoidLogger(),
            'progress_hooks': [lambda i: self.handle_program(title, i)]}
        if audio:
            options['format'] = 'bestaudio/best'
            options['postprocessors'] = [{'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'}]
        self.data[str(title)] = {'info': {}, 'perc': '0%', 'status': 'pending',
                                 'type': 'audio' if audio else 'video',
                                 'finished': 0}
        ydl = youtube_dl.YoutubeDL(options)
        ydl.download([url])
        self.create_list(False)
        return None
    
    def k_100(self):
        for item in self.get_active():
            self.start_download(item)
        self.selected = []
        return None

    def handle_program(self, title, i):
        self.data[title]['status'] = i['status']
        self.data[title]['info'] = i
        if i['status'] == 'downloading':
            perc = i['downloaded_bytes'] / i['total_bytes'] * 100
            self.data[title]['perc'] = str(round(perc)) + '%'
        if i['status'] == 'finished':
            self.data[title]['finished'] += 1
            if (self.data[title]['type'] == 'video'
            and self.data[title]['finished'] == 2):
                self.data[title]['perc'] = ':)'
            if (self.data[title]['type'] == 'audio'
            and self.data[title]['finished'] == 1):
                self.data[title]['perc'] = ':)'
        self.create_list(False)
        return None

    def get_active(self):
        active = []
        if self.selected == []:
            return [self.vidlist[self.off+self.pos]]
        return self.selected


    def k_410(self):
        return None

    def k_117(self):
        for item in self.get_active():
            item['seen'] = False
        self.selected = []
        return None

    def k_115(self):
        for item in self.get_active():
            item['seen'] = True
        self.selected = []
        return None

    def k_113(self):
        return True

    def k_114(self):
        del self.vidlist[self.pos+self.off]
        return None
    
    def k_102(self):
        for item in self.get_active():
            if 'fav' not in item:
                item['fav'] = False
            item['fav'] = not item['fav']
        self.selected = []
        return None

    def k_99(self):
        title = self.vidlist[self.pos+self.off]['title']
        self.downloads[title] = False
        return None


class UserList:
    def __init__(self, users):
        self.users = sorted([x for x in users])
        self.off = 0
        self.pos = 0
        self.data = users
        self.screen = curses.initscr()
        self.screen.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

    def shutdown(self):
        curses.echo()
        curses.nocbreak()
        self.screen.keypad(False)
        curses.endwin()
        return None

    def main(self):
        while True:
            char = str(self.create_list())
            func = getattr(self, 'k_{}'.format(char), None)
            if func is not None:
                quit = func()
                if quit:
                    return None
            else:
                return char
        return None

    def create_list(self):
        self.screen.clear()
        self.screen.refresh()
        self.height, self.width = self.screen.getmaxyx()
        self.screen.addstr('List of users'.center(self.width),
                           curses.color_pair(1) | curses.A_BOLD)
        instr = 'Mark all videos as [S]een. [Q]uit. [Enter] Check list'
        self.screen.addstr(instr.center(self.width))
        for y, i in enumerate(self.users[self.off:self.off+self.height-4]):
            if y == self.pos:
                options = curses.A_REVERSE
            else:
                options = 0
            if all(x['seen'] for x in self.data[i]['videos']):
                options |= curses.A_DIM
            title = ' {} '.format(i).ljust(self.width)
            self.screen.addstr(y+3, 0, title, options)
        return self.screen.getch()

    def k_258(self):
        if self.pos + self.off == len(self.users)-1:
            return None
        self.pos += 1
        if self.pos == self.height-4:
            self.pos -= 1
            self.off += 1
        return None

    def k_259(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = 0
            self.off -= 1
        if self.off < 0:
            self.off = 0
        return None


def make_request(url, data={}, headers={}, method='GET'):
    """make_request
    Makes a url request with headers / data.
    params:
        url: str: The base url.
        data: dict: The data to go along with the url.
        headers: dict: The headers to go along with the req.
        method: str: The request method.
    """
    data = urllib.parse.urlencode(data).encode('utf-8')
    request = urllib.request.Request(url, data=data, headers=headers)
    request.method = method
    response = urllib.request.urlopen(request)
    return response.read().decode('utf-8')


def search(query, site=''):
    """search
    Scrapes a google search for results.
    params:
        query: str: The query to search for.
        site: str: The site to use.
    """
    if site != '':
        site = 'site:{} '.format(site)
    query = urllib.parse.quote('{}{}'.format(site, query))
    query_url = 'http://www.google.com/search?safe=off&q={}'.format(query)
    user_agent = ('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; '
                  'rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
    request = urllib.request.Request(
                    query_url, None,
                    {'User-Agent': user_agent})
    response = urllib.request.urlopen(request)
    data = response.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    url = soup.find_all('h3')
    urls = []
    for index, item in enumerate(url):
        href = item.a.get('href')
        item_url = href.split('=', 1)[1].split('&')[0]
        if not item_url.startswith('http'):
            continue
        urls.append(urllib.parse.unquote(item_url))
    return urls


def _add(*name, args=None):
    """_add
    Adds a new user to watch.
    
    params:
        *name: tuple: The name of the user to add.
        args: Namespace: The arguments passed into the script.
    """
    name = ' '.join(name)
    if 'youtube.com/user/' in name:
        url = name
        _type = 'user'
    elif name.startswith('PL'):
        if 'youtube.com' in name:
            name = 'PL{}'.format(name.split('PL')[1])
        _type = 'playlist'
        url = name
    else:
        cprint('\rSearching for [bold]{}[/bold]'.format(name))
        try:
            user_results = search(name, 'www.youtube.com/user')
        except (socket.gaierror, urllib.error.URLError):
            cprint('[red]Could not find that[/red]')
            return None
        results = [x.split('?')[0] for x in user_results if x.count('/') == 4]
        url = None
        for name in results:
            cprint('Add: [bold]{}[/bold] [y/n] '.format(name), '', '')
            correct = input().lower()
            if correct == 'y':
                url = name
                break
        _type = 'user'


    if not os.path.exists('{}/data.json'.format(FILE_DIR)):
        data = {}
    else:
        with open('{}/data.json'.format(FILE_DIR), 'r') as f:
            data = json.loads(f.read())
    if url is None:
        return None
    if _type == 'user':
        name = url.split('/')[-1]
        username = name
        check_name = input('Name \033[1m{}\033[0m or: '.format(name))
        if check_name != '':
            name = check_name
    if _type == 'playlist':
        with open('{}/api_key'.format(FILE_DIR), 'r') as f:
            key = f.read().split('\n')[0]
        resp = make_request('https://www.googleapis.com/youtube/v3/'
                            'playlists?part=snippet&id={}&key={}'.format(name,
                            key))
        pl_info = json.loads(resp)
        name = json.loads(resp)['items'][0]['snippet']['title']
        check_name = input('Name \033[1m{}\033[0m or: '.format(name))
        if check_name != '':
            name = check_name
    data[name] = {'videos': [], 'url': url, 'type': _type}
    if _type == 'playlist':
        data[name]['playlistid'] = url
        data[name]['url'] = ('https://www.youtube.com/playlist?'
                             'list={}'.format(url))
    if _type == 'user':
        data[name]['username'] = username
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    cprint('[bold]{}[/bold] has been added.'.format(name))
    return None


def _update(*user, args=None):
    """_update
    Updates a specific user or all of them.
    
    params:
        *user: tuple: The username to update. If not specified,
                      updates all of them.
        args: Namespace: The other arguments passed to the script.
    """
    width = shutil.get_terminal_size().columns
    user = ' '.join(user)
    if user == '':
        user = None
    if not os.path.exists('{}/data.json'.format(FILE_DIR)):
        cprint('[red][bold]Could not find a data.json file. '
               'Please use add.')
        return None
    if not os.path.exists('{}/api_key'.format(FILE_DIR)):
        cprint('[red][bold]Could not find an api_key file. '
                'Please use youtube_watcher key API_KEY\n'
                'https://console.developers.google.com/ to get a youtube '
                'v3 key')
        return None
    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())
    if user is None:
        parsedata = dict(data)
    else:
        names = [x for x in data]
        close = difflib.get_close_matches(user, data, 1, 0)
        parsedata = {close[0]:data[close[0]]}
    with open('{}/api_key'.format(FILE_DIR), 'r') as f:
        key = f.read().split('\n')[0]
    for user in parsedata:
        updated = 0
        info = 0
        downloaded = False
        videos = []
        cprint('\r Updating [bold]{}[/bold]'.format(user), '', '', sys.stderr)
        for i in range(10):
            try:
                if data[user]['type'] == 'user':
                    if 'username' in  data[user]:
                        vidname = data[user]['username']
                    else:
                        vidname = user
                    videos = get_user_videos(vidname, key)
                if data[user]['type'] == 'playlist':
                    videos = get_playlist_videos(data[user]['playlistid'],
                                                 key)
            except (ssl.SSLEOFError, urllib.error.URLError, socket.gaierror):
                cprint('\r Updating [bold]{}[/bold]. Try {} '.format(user, i),
                       '', '', sys.stderr)
                continue
            except Exception:
                continue
            else:
                downloaded = True
                break
        if not downloaded:
            print('Failed')
            continue
        for index, item in enumerate(videos):
            if video_in(item, data[user]['videos']):
                item['seen'] = data[user]['videos'][index]['seen']
                continue
            updated += 1
        videos.reverse()
        data[user]['videos'] = videos
        sys.stderr.write('\r{}'.format(' '*width))
        cprint('\r Updating [bold]{}[/bold] - [bold]{}[/bold] '
                'new videos.'.format(user, updated), '', '', sys.stderr)
        print()
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    return None


def get_vid_info(item, api_key):
    """get_vid_info
    Gets information about a video.

    params:
        item: dict: The video item.
        api_key: str: The api key the user has set.
    """
    vid_id = item['id']
    for i in range(10):
        try:
            req = make_request('https://www.googleapis.com/youtube/v3/'
                               'videos?id={}&key={}&part=statistics,'
                               'contentDetails'.format(vid_id, api_key))
        except (ssl.SSLEOFError, urllib.error.URLError, socket.gaierror):
            continue
        return json.loads(req)
    return None


def video_in(item, data):
    """video_in
    Checks if a video item is in the data
    
    params:
        item: dict: Video item.
        data: dict: A dictionary of all videos.
    """
    for vid in data:
        if vid['id'] == item['id']:
            return True
    return False


def _list(*user, args=None):
    """_list
    Lists all of the users the person is watching.

    params:
        *user: tuple: The name of the user.
        args: Namespace: The other arguments passed.
    """
    user = ' '.join(user)
    if user == '':
        user = None
    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())
    if user is None:
        info = data
    else:
        close = difflib.get_close_matches(user, data, 1, 0)
        if len(close) == 0:
            cprint('[red]There are no users to list[/red]')
            return None
        info = {x:data[x] for x in close}
    if len(info) == 1:
        name = list(info.keys())[0]
        check_list(info[name]['videos'], name, args.s, args.regex,
                   args.reverse, args.favorite, single=True)
        return None
    pos = 0
    off = 0
    while True:
        ui = UserList(info)
        ui.pos = pos
        ui.off = off
        try:
            key = int(ui.main())
        except (KeyboardInterrupt, Exception):
            ui.shutdown()
            raise
        if key == 10:
            name = ui.users[ui.off+ui.pos]
            check_list(info[name]['videos'], name, args.s, args.regex,
                       args.reverse, args.favorite, True)
            ui.screen.refresh()
            off = ui.off
            pos = ui.pos
            continue
        if key in [113, 27]:
            ui.shutdown()
            break
        if key == 115:
            name = ui.users[ui.off+ui.pos]
            mark_all_watched(info[name]['videos'])
            off = ui.off
            pos = ui.pos
            continue
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    return None


def mark_all_watched(videos):
    """mark_all_watched
    Marks all of the videos in the list as watched.

    params:
        videos: list: A list of videos to mark as watched.
    """
    for video in videos:
        video['seen'] = True
    return None


def check_list(videos, name, show_seen=False, reg=None, reverse=False,
               favorite=False, single=False):
    """check_list
    Lists all of the videos from a user.
    """
    if not reverse:
        videos.reverse()
    with open('{}/settings.json'.format(FILE_DIR), 'r') as f:
        settings = json.loads(f.read())
    

    try:
        ui = VideoList(name, videos, show_seen, reg, favorite)
        key = ui.main()
    except KeyboardInterrupt:
        ui.shutdown()
    else:
        ui.shutdown() 
    
    if not reverse:
        videos.reverse()

    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())

    data[name]['videos'] = videos

    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    
    if single:
        return False
    size = shutil.get_terminal_size()
    width = size.columns
    text = '[C]ontinue. [Q]uit? '
    cont = input('{}{}'.format(' '*int(width/2-(len(text)/2)), text))
    cont = cont.lower()
    if cont == 'c' or cont.strip() == '':
        return True
    return False


def _remove(*name, args=None):
    """_remove
    Removes a specific user from the list.

    params:
        *name: tuple: The name of the video.
        args: Namespace: The other arguments passed.
    """
    name = ' '.join(name)
    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())

    close = difflib.get_close_matches(name, data, 1, 0)
    cprint('Remove [bold]{}[/bold]? [y/n] '.format(close[0]), suffix='[end]')
    rem = input()
    if rem != 'y':
        return None

    del data[close[0]]
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))

    cprint('Removed [bold]{}[/bold]'.format(close[0]))
    return None


def _clear(*_, args=None):
    """_clear
    Removes all data.
    """
    os.system('rm {}/data.json'.format(FILE_DIR))
    return None


def get_user_videos(user, key):
    resp = make_request('https://www.googleapis.com/youtube/v3/channels?'
                        'key={}'
                        '&part=contentDetails&forUsername={}'.format(
                        key, user))
    info = json.loads(resp)
    upload_id = info['items'][0]['contentDetails']['relatedPlaylists']['up'
                'loads']
    videos = get_playlist_videos(upload_id, key)
    return videos


def get_playlist_videos(pid, key):
    """get_playlist_videos
    Returns a list of videos from a playlist.

    params:
        pid: int: The ID of the pid.
        key: str: The api key the user set.
    """
    page_token = None
    videos = []
    while True:
        page_string = ('&pageToken={}'.format(page_token) if page_token
                       is not None else '')
        resp = make_request('https://www.googleapis.com/youtube/v3/'
                            'playlistItems?part=snippet,contentDetails'
                            '&playlistId'
                            '={}&maxResults=50&key={}{}'.format(pid,
                            key, page_string))
        page_info = json.loads(resp)
        page_vids = page_info['items']
        for item in page_vids:
            data = {'seen': False, 'desc': item['snippet']['description'],
                    'id': item['snippet']['resourceId']['videoId'],
                    'title': item['snippet']['title']}
            videos.append(data)
        if 'nextPageToken' not in page_info:
            break
        page_token = page_info['nextPageToken']
    return videos


def _key(key, args=None):
    """_key
    Sets the api key.

    params:
        key: str: The key to use.
        args: Namespace: The arguments passed to the script.
    """
    with open('{}/api_key'.format(FILE_DIR), 'w') as f:
        f.write(key)

    print('Set key to {}'.format(key))
    return None


def _users(*_, args=None):
    """_users
    Lists all of the users.

    params:
        args: Namespace: The other arguments passed to the script.
    """
    with open('{}/data.json'.format(FILE_DIR)) as f:
        data = json.loads(f.read())
    for user in data:
        length = len(data[user]['videos'])
        seen = len([x for x in data[user]['videos'] if x['seen']])
        cprint('[bold]{}[/bold] {}/{} (seen/total)'.format(user, seen,
               length))
    return None


def _setting(setting, *value, args=None):
    """_setting
    Adds a setting to the setting file.

    params:
        setting: str: The key of the setting.
        *value: tuple: A tuple, which will be joined by space.
        args: namespace: Other args passed to the script.
    """
    value = ' '.join(value)
    with open('{}/settings.json'.format(FILE_DIR), 'r') as f:
        settings = json.loads(f.read())

    settings[setting] = value

    with open('{}/settings.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(settings))
    return None


def main():
    # Create files / dir
    if not os.path.exists(FILE_DIR):
        os.mkdir(FILE_DIR)

    if not os.path.exists('{}/data.json'.format(FILE_DIR)):
        with open('{}/data.json'.format(FILE_DIR), 'w') as f:
            f.write('{}')

    if not os.path.exists('{}/settings.json'.format(FILE_DIR)):
        with open('{}/settings.json'.format(FILE_DIR), 'w') as f:
            f.write('{}')

    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='+')
    parser.add_argument('-s',  action='store_true', default=False,
                        help='Specifying this will list all videos even if'
                        ' they are marked as watched.')
    parser.add_argument('-r', '--regex', default=None,
                        help='Only shows video titles that match this regex.')
    parser.add_argument('-R', '--reverse', default=False,
                        help='Reverses the video list when using list.',
                        action='store_true')
    parser.add_argument('-f', '--favorite', default=False, action='store_true',
                        help='Only shows favorited videos.')
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    args = parser.parse_args()
    command = '_{}'.format(args.command[0])
    params = args.command[1:]
    if command in globals():
        globals()[command](*params, args=args)
    return None


if __name__ == "__main__":
    main()
