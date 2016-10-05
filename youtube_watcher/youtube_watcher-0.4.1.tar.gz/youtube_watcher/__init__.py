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
from bs4 import BeautifulSoup
from .cprint import cprint


FILE_DIR = '{}/.youtube_watcher'.format(os.getenv('HOME'))
VERSION = '0.4.1'


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
        for index, item in enumerate(videos):
            if video_in(item, data[user]['videos']) and not args.all:
                continue
            updated += 1
            data[user]['videos'].append(item)
            perc = index/len(videos)*100
            color_progress(perc, '', '', anti_fill='[_grey] [/_grey]',
                           prefix=' Updating [bold]{}[/bold] '.format(user))
            inf = get_vid_info(item, key)
            if inf is None:
                print('Failed')
                break
            stats = inf['items'][0]['statistics']
            details = inf['items'][0]['contentDetails']
            data[user]['videos'][index]['likecount'] = stats['likeCount']
            data[user]['videos'][index]['dislikecount'] = stats['dislikeCount']
            data[user]['videos'][index]['duration'] = details['duration']
        sys.stderr.write('\r{}'.format(' '*width))
        cprint('\r Updating [bold]{}[/bold] - [bold]{}[/bold] '
                'new videos.'.format(user, updated), '', '', sys.stderr)
        print()
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
        else:
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
    if reverse:
        videos.reverse()
    width = shutil.get_terminal_size().columns
    height = shutil.get_terminal_size().lines
    for index, video in enumerate(videos):
        if video['seen'] and not show_seen:
            continue
        if reg is not None:
            match = re.match(reg, video['title'])
            if match is None:
                continue
        os.system('clear')
        cprint('[_blue]{}[/_blue]'.format(
               video['title'].center(width)))
        vid_url = ('https://www.youtube.com/watch?'
                   'v={}'.format(video['id']))
        cprint('[_dblue]{}[/_dblue]\n\n'.format(
               vid_url.center(width)))
        likes = int(video['likecount'])
        dislikes = int(video['dislikecount'])
        total = likes + dislikes
        color_progress(likes/total*100, '', '', '[_green] [/_green]',
                       '[_red] [/_red]', 'Likes / Dislikes  ',
                       '{}/{}\n'.format(likes, dislikes))
        time = video['duration'].split('T')[1]
        tdata = []
        v = ''
        for c in time:
            try:
                check = int(c)
                v += c
            except ValueError:
                tdata.append(int(v))
                v = ''
        for i in range(3):
            try:
                a = tdata[i]
            except IndexError:
                tdata.insert(0, 0)
        tstring = '{:0>2}:{:0>2}:{:0>2}'.format(*tdata)
        print('Duration: {}\n'.format(tstring))


        pos = 2+math.ceil(len(video['title'])/width)
        print(video['desc'][:int((height-10-(pos-3))*width)].replace('\n', '- '),
              '...')

        print('\033[{};1H'.format(pos), end='')

        text = ('[M]ark as watched. [S]kip. [D]ownload. Download [A]udio. '
                '[Q]uit: ')
        key = input('{}{}'.format(' '*int(width/2-(len(text)/2)), text))
        key = key.lower()
        if key == 'q':
            break
        if key == 'm':
            video['seen'] = True
            continue
        if key.strip() == '':
            continue
        url = 'https://www.youtube.com/watch?v={}'.format(video['id'])
        proc = None
        downloaded = False
        try_again = False
        while not downloaded:
            if key == 'd':
                params = 'youtube-dl {}'.format(url)
                proc = subprocess.Popen(params.split(' '),
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT)
            if key == 'a':
                params = ('youtube-dl --extract-audio '
                          '--audio-format mp3 {}'.format(url))
                proc = subprocess.Popen(['youtube-dl', '--extract-audio',
                                         '--audio-format', 'mp3', url],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT)
            if proc is not None:
                try:
                    downloaded = handle_download(proc, video, try_again)
                except KeyboardInterrupt:
                    #key = input('\033[{};1H[Q]uit. [R]un the download in the '
                    #             'background. '.format(height))
                    #if key.lower() == 'r':
                    #    return None
                    break
            else:
                downloaded = True
                video['seen'] = True
                continue

            try_again = True
    if reverse:
        videos.reverse() 

    os.system('clear')
    title = 'Finished {} video list'.format(name)
    cprint('[_dgreen][bold]{}[/_dgreen][bold]'.format(title.center(width)))

    with open('{}/data.json'.format(FILE_DIR), 'r') as f:
        data = json.loads(f.read())

    data[name]['videos'] = videos

    with open('{}/data.json'.format(FILE_DIR), 'w') as f:
        f.write(json.dumps(data))

    text = '[C]ontinue. [Q]uit? '
    cont = input('{}{}'.format(' '*int(width/2-(len(text)/2)), text))
    cont = cont.lower()
    if cont == 'c' or cont.strip() == '':
        return True
    return False


def handle_download(proc, video, try_again=False):
    size = shutil.get_terminal_size()
    width = size.columns
    height = size.lines
    move = '\033[{};1H'.format(height)
    if try_again:
        text = 'Trying again.'
    else:
        text = 'Starting download.'
    sys.stderr.write('\r{}{} Press Ctrl+C to cancel.'.format(move, text))
    tmp = b''
    downloaded = False
    while proc.poll() is None:
        tmp += proc.stdout.read(1)
        if tmp.endswith(b'\n'):
            tmp = b''
            continue
        if tmp.endswith(b'\r'):
            if tmp == b'\r':
                continue
            data = [x for x in tmp.decode('utf-8').split(' ') if x != '']
            sys.stderr.write('\r{}'.format(' '*width))
            perc = int(float(data[1][:-1]))
            color_progress(perc, '', '', prefix=' Press Ctrl+C to cancel ',
                           suffix='{}%'.format(str(perc)),
                           anti_fill='[_grey] [/_grey]')
            downloaded = perc > 95
            tmp = b''
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


def main():
    # Create files / dir
    if not os.path.exists(FILE_DIR):
        os.mkdir(FILE_DIR)

    if not os.path.exists('{}/data.json'.format(FILE_DIR)):
        with open('{}/data.json'.format(FILE_DIR), 'w') as f:
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
    parser.add_argument('-a', '--all', help='Updates all videos '
                        'when you update', action='store_true', default=False)
    parser.add_argument('--version', action='version', version=VERSION)
    args = parser.parse_args()
    command = '_{}'.format(args.command[0])
    params = args.command[1:]
    if command in globals():
        globals()[command](*params, args=args)
    return None


if __name__ == "__main__":
    main()
