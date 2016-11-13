#!/usr/bin/env python3


import curses
import youtube_dl
import webbrowser
import re
from threads import asthread


class VoidLogger:
    """VoidLogger
    Youtube-dl accepts a logger class.
    This just pass's on all of the messages to prevent the stdout 
    messing up my curses interface.
    """
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class ItemList:
    def __init__(self, title, comment, items, return_vals, **kwargs):
        self.title = title
        self.comment = comment
        self.items = items
        self.return_vals = return_vals
        self.off = 0
        self.pos = 0
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.start_screen()

    def start_screen(self):
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
        return None

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
            quit = False
            if func is not None:
                quit = func()
            if quit or int(char) in self.return_vals:
                return char
        return None

    def create_list(self, get_input=True):
        self.screen.clear()
        self.height, self.width = self.screen.getmaxyx()
        self.screen.addstr(self.title.center(self.width),
                           curses.color_pair(1) | curses.A_BOLD)
        self.screen.addstr(self.comment.center(self.width))
        self.draw_items()
        if not get_input:
            return None
        return self.screen.getch()
 
    def draw_items(self):
        pass
 
    def k_258(self):
        if self.pos + self.off == len(self.items)-1:
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

    def k_113(self):
        return True

    def k_106(self):
        self.k_258()
        return None

    def k_107(self):
        self.k_259()
        return None

    def k_410(self):
        return None

    def k_113(self):
        return True


class VideoList(ItemList):
    def __init__(self, title, videos, show_seen, reg, fav):
        """__init__
        Creates the video list.

        params:
            title: str: The title to display at the top.
            videos: list: A list of videos.
            show_seen: bool:
                True: Will show videos you have marked as seen.
                False: Will not show videos marked as seen.
            reg: str: Regex to match the titles with.
            fav: bool:
                True: Will only show favorited videos.
                False: Will not only show favorited videos.
        """
        instructions = ('[D]ownload. Download [A]udio. Mark as [S]een. '
                        'Mark as [U]n-seen. [Q]uit.')
        self.data = {}
        self._vidlist = []
        self.selected = []
        self.active_title = ''
        super().__init__(title, instructions, videos, [], end=4,
                         show_seen=show_seen, regex=reg,
                         show_favorite=fav)

    def draw_items(self):
        videos = self.vidlist[self.off:self.off+self.height-self.end]
        active = ''
        for y, i in enumerate(videos):
            options = self.video_options(i, y)
            title = i['title']
            pref = '    '
            if title in self.data:
                pref = ' {} '.format(self.data[title]['perc'])
            space = self.width-len(title)-2
            pref = pref.center(6)
            if y == self.pos:
                self.active_title = i['title']
            self.screen.addstr(y+3, 0, '{}{}'.format(pref,
                               title).ljust(self.width), options)
        self.draw_statusbar()
        return None

    def draw_statusbar(self):
        active = self.active_title
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
        return None

    @property
    def vidlist(self): 
        videolist = []
        if self.show_seen:
            videolist = self.items
        else:
            videolist = [x for x in self.items if not x['seen']]
        if self.regex is not None:
            videolist = [x for x in videolist
                         if re.search(self.regex, x['title'])]
        if self.show_favorite:
            videolist = [x for x in videolist if x.get('fav')]
        self._vidlist = videolist
        return self._vidlist

    def video_options(self, item, position):
        if position == self.pos:
            return curses.color_pair(1)
        
        options = 0
        options |= curses.A_DIM if item['seen'] else 0
        options |= curses.color_pair(3) if item.get('fav') else 0
        
        if item['title'] in self.data:
            info = self.data[item['title']]
            options |= curses.A_UNDERLINE if info.get('watch') else 0

        if any(item['title'] == i['title'] for i in self.selected):
            options |= curses.A_REVERSE
        return options

    @asthread()
    def start_download(self, item, audio=False):
        """start_download
        Starts downloading a video.

        params:
            item: dict: A dictionary of info about a video.
            audio: bool:
                True: Download the video as audio.
                False: Download as video and audio.
        """
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

    def handle_program(self, title, i):
        """handle_program
        Handles the downloading info from youtube-dl.

        params:
            title: str: The title of the video.
            i: dict: A dictionary of the youtube-dl info.
        """
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

    @property
    def active_rows(self):
        """active_rows
        Returns a list of active rows.
        """
        active = []
        if self.selected == []:
            return [self._vidlist[self.off+self.pos]]
        return self.selected

    def k_32(self):
        title = self._vidlist[self.off+self.pos]
        if title in self.selected:
            del self.selected[self.selected.index(title)]
        else:
            self.selected.append(title)
        self.k_258()
        return None
    
    def k_111(self):
        savout = os.dup(1)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)
        for item in self.active_rows:
            url = 'https://www.youtube.com/watch?v={}'.format(item['id'])
            webbrowser.open(url)
        os.dup2(savout, 1)
        self.selected = []
        return None
    
    
    def k_97(self):
        for item in self.active_rows:
            self.start_download(item, True)
        self.selected = []
        return None
    
    def k_100(self):
        for item in self.active_rows:
            self.start_download(item)
        self.selected = []
        return None


    def k_117(self):
        for item in self.active_rows:
            item['seen'] = False
        self.selected = []
        return None

    def k_115(self):
        for item in self.active_rows:
            item['seen'] = True
        self.selected = []
        return None

    def k_114(self):
        del self._vidlist[self.pos+self.off]
        return None
    
    def k_102(self):
        for item in self.active_rows:
            if 'fav' not in item:
                item['fav'] = False
            item['fav'] = not item['fav']
        self.selected = []
        return None

    def k_99(self):
        title = self._vidlist[self.pos+self.off]['title']
        self.downloads[title] = False
        return None


class UserList(ItemList):
    def __init__(self, users):
        self.data = users
        users = sorted(users.keys())
        title = 'List of users'
        instructions = 'Mark all videos as [S]een. [Q]uit. [Enter] Check list'
        super().__init__(title, instructions, users, [10, 113, 27, 115],
                         end=4)
        self.users = sorted([x for x in users])

    def draw_items(self):
        for y, i in enumerate(self.items[self.off:self.off+self.height-4]):
            if y == self.pos:
                options = curses.A_REVERSE
            else:
                options = 0
            if all(x['seen'] for x in self.data[i]['videos']):
                options |= curses.A_DIM
            title = ' {} '.format(i).ljust(self.width)
            self.screen.addstr(y+3, 0, title, options)
        return None
