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
from bs4 import BeautifulSoup
from youtube_watcher.cprint import cprint


FILE_DIR = '{}/.youtube_watcher'.format(os.getenv('HOME'))
VERSION = '0.6.2'


class UI:
    def __init__(self, title, videos, show_seen, reg):
        self.title = title 
        self.show_seen = show_seen
        if reg is not None:
            self.regex = re.compile(reg, re.I)
        else:
            self.regex = None
        self.pos = 0
        self.off = 0
        self.videos = videos
        self.data = {}
        self.downloads = {}
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
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
                quit = func()
                if quit:
                    return None
            else:
                return char
        return None

    def create_list(self, getch=True):
        if self.show_seen:
            self.vidlist = self.videos
        else:
            self.vidlist = [x for x in self.videos if not x['seen']]
        if self.regex is not None:
            self.vidlist = [x for x in self.vidlist 
                            if re.search(self.regex, x['title'])]
        self.screen.clear()
        self.screen.refresh()
        self.height, self.width = self.screen.getmaxyx()
        self.screen.addstr(self.title.center(self.width), curses.color_pair(1) 
                            | curses.A_BOLD)
        instructions = ('[D]ownload. Download [A]udio. Mark as [S]een. '
                        'Mark as [U]n-seen. [Q]uit.')
        self.screen.addstr(instructions.center(self.width)) 
        for y, i in enumerate(self.vidlist[self.off:self.off+self.height-4]):
            if y == self.pos:
                opts = curses.A_REVERSE
            else:
                opts = 0
            
            if i['seen']:
                opts |= curses.A_DIM

            if 'fav' in i and i['fav']:
                opts |= curses.color_pair(3)

            title = i['title']
            pref = '[    ]'
            if title in self.data:
                if self.data[title] == ':)':
                    pref = '[{}]'.format(':)'.center(4))
                    opts |= curses.color_pair(2)
                elif self.data[title] == ':(':
                    pref = '[{}]'.format(':('.center(4))
                    opts |= curses.color_pair(4)
                else:
                    pref = '[{:>3}%]'.format(self.data[title])
            space = self.width-len(title)-2
            pref = pref.center(8)
            self.screen.addstr(y+3, 0, '{}{}'.format(pref, title).ljust(self.width),
                               opts)
        if self.vidlist != []:
            perc = round((self.pos+self.off+1)/len(self.vidlist)*100)
            percstring = '({}/{}) {}%'.format(self.pos+self.off+1,
                         len(self.vidlist), perc)
            self.screen.addstr(self.height-1, 0, percstring.rjust(self.width-1))
        if getch:
            return self.screen.getch()
        self.screen.refresh()
        return None

    def k_258(self):
        if self.pos + self.off == len(self.vidlist)-1:
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

    def k_97(self):
        video = self.vidlist[self.pos+self.off]
        title = video['title']
        self.data[title] = 0
        url = 'https://youtube.com/watch?v={}'.format(video['id'])
        program = 'youtube-dl --extract-audio --audio-format mp3 {}'.format(url)
        self.handle_program(program, title)
        return None
 
    def k_100(self):
        video = self.vidlist[self.pos+self.off]
        title = video['title']
        self.data[title] = 0
        url = 'https://youtube.com/watch?v={}'.format(video['id'])
        program = 'youtube-dl {}'.format(url)
        self.handle_program(program, title)
        return None
    
    def handle_program(self, program, title):
        proc = subprocess.Popen(program.split(' '), stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        thread = threading.Thread(target=handle_download,
                                  args=(proc, self, title))
        self.downloads[title] = True
        thread.start()
        return None

    def k_410(self):
        return None

    def k_117(self):
        self.vidlist[self.pos+self.off]['seen'] = False
        return None

    def k_115(self):
        self.vidlist[self.pos+self.off]['seen'] = True
        return None

    def k_113(self):
        return True

    def k_114(self):
        del self.vidlist[self.pos+self.off]
        return None
    
    def k_102(self):
        vid = self.vidlist[self.pos+self.off]
        if 'fav' not in vid:
            vid['fav'] = False
        vid['fav'] = not vid['fav']
        return None

    def k_99(self):
        title = self.vidlist[self.pos+self.off]['title']
        self.downloads[title] = False
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


def color_progress(percentage, start='|', end='|', fill='[_blue] [/_blue]',
                   anti_fill=' ', prefix=' ', suffix='', stderr=True):
    """color_progress
    Creates a color progress bar.
    params:
        percentage: int: The percentage of the progress bar to fill.
        start: str: The char to place at the start of the bar.
        end: str: The char to place at the end of the bar.
        fill: str: The string to fill with the bar with.
        anti_fill: str: The string to fill the empty areas of the bar with.
        prefix: str: The string to put before the bar.
        suffix: str: The string to put after the bar.
        stderr: bool: True if it should print to stderr.
    """
    width = (shutil.get_terminal_size().columns-len(prefix)-len(suffix)
             -len(start)-len(end)-3)
    perc = percentage / 100 * width
    fill_char = fill*math.ceil(perc)
    anti_char = anti_fill*math.floor((width-perc))
    bar = '{}{}{}{}'.format(start, fill_char, anti_char, end)
    string = '{} {} {}'.format(prefix, bar, suffix)
    if stderr:
        cprint('\r{}'.format(string), '', '', file=sys.stderr)
    else:
        cprint('{}'.format(string), '', '', file=sys.stdout)
    return None


def _add(*name, args=None):
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
        data[user]['videos'].reverse()
        for index, item in enumerate(videos[::-1]):
            if video_in(item, data[user]['videos']):
                continue
            updated += 1
            data[user]['videos'].insert(0, item)
        sys.stderr.write('\r{}'.format(' '*width))
        cprint('\r Updating [bold]{}[/bold] - [bold]{}[/bold] '
                'new videos.'.format(user, updated), '', '', sys.stderr)
        print()
        data[user]['videos'].reverse()
    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    return None


def get_vid_info(item, api_key):
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
    for vid in data:
        if vid['id'] == item['id']:
            return True
    return False


def _list(*user, args=None):
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
        info = {close[0]:data[close[0]]}
    width = shutil.get_terminal_size().columns
    for name in info:
        os.system('clear')
        cprint('[_blue][bold]{}[/_blue][/bold]'.format(name.center(width)))
        text = '[C]heck video list. [M]ark all as watched. [S]kip: '
        key = input('{}{}'.format(' '*int(width/2-(len(text)/2)), text))
        key = key.lower()
        if key == 's':
            continue
        if key == 'm':
            mark_all_watched(name)
            continue
        if key == 'c':
            contin = check_list(info[name]['videos'], name, args.s,
                                args.regex, args.reverse)
            if contin:
                continue
            return None
    return None


def mark_all_watched(name):
    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())

    for video in data[name]['videos']:
        video['seen'] = True

    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))
    return None



def check_list(videos, name, show_seen=False, reg=None, reverse=False):
    if not reverse:
        videos.reverse()
    with open('{}/settings.json'.format(FILE_DIR), 'r') as f:
        settings = json.loads(f.read())
    

    try:
        ui = UI(name, videos, show_seen, reg)
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
    
    size = shutil.get_terminal_size()
    width = size.columns
    text = '[C]ontinue. [Q]uit? '
    cont = input('{}{}'.format(' '*int(width/2-(len(text)/2)), text))
    cont = cont.lower()
    if cont == 'c' or cont.strip() == '':
        return True
    return False


def handle_download(proc, ui, title, try_again=False):
    tmp = b''
    downloaded = False
    while proc.poll() is None:
        if not ui.downloads[title]:
            ui.data[title] = ':('
            ui.create_list(False)
            return None
        tmp += proc.stdout.read(1)
        if tmp.endswith(b'\n'):
            tmp = b''
            continue
        if tmp.endswith(b'\r'):
            if tmp == b'\r':
                continue
            data = [x for x in tmp.decode('utf-8').split(' ') if x != '']
            perc = int(float(data[1][:-1]))
            ui.data[title] = perc
            ui.create_list(False)
            tmp = b''
    ui.data[title] = ':)'
    ui.create_list(False)
    return downloaded


def _remove(*name, args=None):
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
    with open('{}/api_key'.format(FILE_DIR), 'w') as f:
        f.write(key)

    print('Set key to {}'.format(key))
    return None


def _users(*_, args=None):
    with open('{}/data.json'.format(FILE_DIR)) as f:
        data = json.loads(f.read())
    for user in data:
        length = len(data[user]['videos'])
        seen = len([x for x in data[user]['videos'] if x['seen']])
        cprint('[bold]{}[/bold] {}/{} (seen/total)'.format(user, seen,
               length))
    return None


def _setting(setting, *value, args=None):
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
    parser.add_argument('-v', '--version', action='version', version=VERSION)
    args = parser.parse_args()
    command = '_{}'.format(args.command[0])
    params = args.command[1:]
    if command in globals():
        globals()[command](*params, args=args)
    return None


if __name__ == "__main__":
    main()
