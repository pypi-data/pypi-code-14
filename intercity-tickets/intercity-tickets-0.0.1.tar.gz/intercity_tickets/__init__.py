from collections import namedtuple
from datetime import date, datetime, timedelta
import logging
import os
import re

import requests
from bs4 import BeautifulSoup
from slugify import slugify
from tqdm import tqdm

from .notifications import EmailNotification

logger = logging.getLogger(__name__)
Ticket = namedtuple(
    'Ticket',
    'number, route_from, route_to, type_name, date, train, carriage, '
    'carriage_type, seat, location')
Train = namedtuple(
    'Train',
    'number, type, route_from, route_to, date_from, date_to, relation_id')


class Session(requests.Session):

    def request(self, method, url, **kwargs):
        logger.debug('%s: %s' % (method, url))
        return super(Session, self).request(method, url, **kwargs)


class PKPIntercity(object):
    SEARCH_URL = ('https://www.intercity.pl'
                 '/pl/site/dla-pasazera/informacje/wyszukiwarka-polaczen.html')
    BASE_URL = 'https://bilet.intercity.pl/'
    TICKET_LIST_URL = BASE_URL + 'lista_biletow.jsp'
    LOGIN_URL = BASE_URL + 'logowanie.jsp'
    TICKET_URL = BASE_URL + 'irez/jsp/rezerwacjaWPDF.jsp?bilet=%s&checkJS=true'
    PDF_URL = BASE_URL + 'BiletPDF?bilet=%s'

    def __init__(self, login, password):
        self.session = Session()
        self.session.get(self.TICKET_LIST_URL)
        self.session.post(self.LOGIN_URL, data={
            'login': login, 'password': password, 'ref': 30})

    def _get_first_date(self, content):
        date_list = re.search(r'(\d{4})\-(\d{2})\-(\d{2})', content).groups()
        ticket_date = datetime(*map(int, date_list))
        time_list = re.search(r'(\d{2})\:(\d{2})', content)
        if time_list:
            hour, minute = map(int, time_list.groups())
            return ticket_date.replace(hour=hour, minute=minute)
        else:
            return ticket_date.date()

    def _get_date(self, date_string):
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M')

    def is_archived(self, ticket_date):
        now = datetime.now()
        if type(ticket_date) == date:
            now = now.date()
        return ticket_date < now

    def _get_seat_reservation(self, ticket_content):
        rows = ticket_content.find_all(
            'td', {'class': 'tekstPDF', 'align': 'left'})
        data = rows[1].find_all('b')
        if not data:
            return {}
        seat, location = rows[2].get_text().strip().split(' ')[:2]
        return {'train': data[0].get_text(),
                'carriage': data[1].get_text(),
                'carriage_type': rows[18].get_text().strip(),
                'seat': seat,
                'location': location.lower()}

    def _get_type_name(self, ticket_content):
        type_name = ticket_content.find(
            'td', {'class': 'tekstPDFSmall', 'align': 'center'})
        return type_name.get_text().strip()

    def get_page(self, page=1, search_filter=None):
        data = {'typ': 7, 'offset': 5 * (page - 1)}
        if search_filter:
            data.update({
                'filter': search_filter})
        return self.session.post(self.TICKET_LIST_URL, data=data)

    def get_tickets(self, single=False, archived=False, max_pages=5,
                    search_filter=None):
        for page_number in range(1, max_pages + 1):
            page = self.get_page(page_number, search_filter=search_filter)
            soup = BeautifulSoup(page.text, 'html.parser')
            rows = soup.find_all('tr', {'class': 'orange'})
            if not rows:
                return
            for row in rows:
                first_td = row.find('td', {'class': 'first'})
                number = first_td.a.get_text()
                if first_td.font.get_text() != 'Krajowy' and single:
                    continue
                content = row.find('td', {'class': 'td_right'}).get_text()
                response = self.session.get(self.TICKET_URL % number[3:])
                ticket_content = BeautifulSoup(response.text, 'html.parser')
                seat_reservation = self._get_seat_reservation(ticket_content)
                ticket_date = self._get_first_date(content)
                route_from, route_to = map(
                    lambda x: x.strip(),
                    row.find_all('td')[1].get_text('|').split('|'))[:2]

                if not archived and self.is_archived(ticket_date):
                    return
                yield Ticket(
                    number=number,
                    route_from=route_from,
                    route_to=route_to,
                    type_name=self._get_type_name(ticket_content),
                    date=ticket_date,
                    train=seat_reservation.get('train'),
                    carriage=seat_reservation.get('carriage'),
                    carriage_type=seat_reservation.get('carriage_type'),
                    seat=seat_reservation.get('seat'),
                    location=seat_reservation.get('location'))

    def download_ticket(self, ticket, destination_dir='.', override=False):
        route = '%s_%s' % (slugify(ticket.route_from, separator='_')[:3],
                           slugify(ticket.route_to, separator='_')[:3])
        filename = '%s/%s_%s_%s.pdf' % (
            destination_dir, ticket.date.strftime('%Y%m%d%H%M'),
            route, ticket.number)
        if not os.path.exists(filename) or override:
            if not os.path.exists(destination_dir):
                os.mkdir(destination_dir)
            response = self.session.get(
                self.PDF_URL % ticket.number[3:], stream=True)
            total = int(response.headers.get('Content-Length', 0))
            if not total:
                return
            name = os.path.split(filename)[1]
            chunk_size = 1024
            progress = tqdm(
                total=total, leave=True, unit_scale=chunk_size, unit='B',
                desc='Downloading %s' % (name,))
            with open(filename, 'wb') as file_handler:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file_handler.write(chunk)
                        progress.update(chunk_size)
            progress.close()
        return open(filename)

    def get_trains(self, route_from, route_to, route_date=None):
        # available stations - http://www.intercity.pl/js/station.js
        if route_date is None:
            route_date = date.today()
        data = {
            'seek[stname][0]': '',
            'seek[stid][0]': route_from,
            'seek[stname][1]': '',
            'seek[stid][1]': route_to,
            'seek[date]': route_date,
            'seek[time]': '0:00',
            'seek[arr]': 0,
            'seek[type][2]': 2,
            'seek[type][3]': 3,
            'hafasPage': '',
            'hafasSort': ''}
        response = self.session.post(self.SEARCH_URL, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        inputs = soup.find_all('input', {'type': 'text'})
        response = self.session.post(
            self.BASE_URL + 'przekierowanie.jsp',
            data={input['name']: input['value'] for input in inputs})
        soup = BeautifulSoup(response.text, 'html.parser')
        trains = []
        for train in soup.find_all('div', {'box': True}):
            if 'trasa_' in train.get('id', ''):
                train_time = train.find_all('div', {'class': 'godziny'})
                route = train.find_all('div', {'class': 'stacje'})
                number = re.findall(r'[^(\g)]+', train.find(
                    'div', {'class': 'przesiadki'}).getText())[1]
                date_str = train.find_all(
                    'div', {'class': 'daty'})[1].getText()
                date_from_str = '%s %s' % (date_str, train_time[0].getText())
                date_to_str = '%s %s' % (date_str, train_time[1].getText())
                trains.append(
                    Train(
                        number=number,
                        type=re.findall(r'[^\W\d]+', number)[0],
                        route_from=route[0].getText(),
                        route_to=route[1].getText(),
                        date_from=self._get_date(date_from_str),
                        date_to=self._get_date(date_to_str),
                        relation_id=train['box']))
        return trains

    def reserve_seat(self, relation_id, username, ticket_number):
        self.session.post(
            self.BASE_URL + 'zakup_biletu_form.jsp',
            data={'id_relacji': relation_id, 'r': 1, 'm': 2})
        self.session.post(
            self.BASE_URL + 'podglad_biletu.jsp',
            data={
                'liczba_n': 0,
                'liczba_u': 1,
                'kod_znizki': 106, # bilet okresowy - miejscowka
                'klasa_wagonu': 2})
        response = self.session.post(
            self.BASE_URL + 'platnosc.jsp',
            data={
                'kodc': 10006,  # bilet dodatkowy
                'imie_nazwisko_podroznego': username,
                'nr_biletu_do_doplaty': ticket_number})
        soup = BeautifulSoup(response.text, 'html.parser')
        button = soup.find_all('input', {'type': 'button'})[-1]
        sposplat = button['onclick'].split(',')[1].strip()
        ticket_id = button['onclick'].split(',')[2].strip()
        self.session.post(
            self.BASE_URL + 'platnosc_weryfikacja.jsp',
            data={
                'checkJS': True,
                'bil_id': ticket_id,
                'faktura': False,
                'faktura_elektroniczna': True,
                'imie_nazwisko_podroznego': username,
                'sposplat': sposplat,
                'typ': 1,
                'promokod': False})
        self.session.post(
            self.BASE_URL + 'potwierdzenie.jsp',
            data={'sposplat': sposplat, 'checkJS': True})


def env_variables_required(variables):
    def decorated(func):
        def new_function():
            for variable in variables:
                if not variable in os.environ:
                    raise ValueError(
                        'Env variable %s is missing.' % variable)
            func()
        return new_function
    return decorated


@env_variables_required(['INTERCITY_LOGIN', 'INTERCITY_PASSWORD'])
def download_tickets():
    intercity = PKPIntercity(
        os.environ.get('INTERCITY_LOGIN'), os.environ.get('INTERCITY_PASSWORD'))
    for ticket in intercity.get_tickets(single=True):
        intercity.download_ticket(
            ticket, destination_dir=os.environ.get('TICKETS_DIR', 'tickets'))


@env_variables_required(['INTERCITY_LOGIN', 'INTERCITY_PASSWORD',
                         'EMAIL_URL', 'EMAIL_RECEIVER'])
def send_reminders():
    intercity = PKPIntercity(
        os.environ.get('INTERCITY_LOGIN'), os.environ.get('INTERCITY_PASSWORD'))
    max_pages = os.environ.get('INTERCITY_MAX_PAGES', 10)
    tickets = intercity.get_tickets(
        single=True, max_pages=max_pages, search_filter=date.today())
    email_notification = EmailNotification(
        os.environ.get('EMAIL_URL'), os.environ.get('EMAIL_RECEIVER'))
    date_offset = datetime.today() + timedelta(hours=2)
    tickets_dir = os.environ.get('TICKETS_DIR', '/tmp')
    for ticket in tickets:
        if datetime.today() <= ticket.date <= date_offset:
            pdf_file = intercity.download_ticket(
                ticket, destination_dir=tickets_dir)
            email_notification.notify(ticket, attachment=pdf_file)
