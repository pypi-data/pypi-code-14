# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Additional factory functions for common QR Codes.

The factory functions which return a QR Code use the minimum error correction
level "M". To create a (Micro) QR Code which should use a specific error
correction level or version etc., use the "_data" factory functions which return
a string which can be used as input for :py:func:`segno.make()`.
"""
from __future__ import absolute_import, unicode_literals
import segno
try:  # pragma: no cover
    str = unicode
    str_type = basestring
except NameError:  # pragma: no cover
    str_type = str


_MECARD_ESCAPE = {
    ord('\\'): '\\\\',
    ord(';'): '\\;',
    ord(':'): '\\:',
    ord('"'): '\\"',
}


def _mecard_escape(s):
    """\
    Escapes ``\\``, ``;``, ``"`` and ``:`` in the provided string.

    :param str|unicode s: The string to escape.
    :rtype unicode
    """
    return str(s).translate(_MECARD_ESCAPE)


_VCARD_ESCAPE = {
    ord(';'): '\\;',
    ord(','): '\\,',
}


def _vcard_escape(s):
    """\

    """
    return str(s).translate(_VCARD_ESCAPE)


def _geo_info(f):
    """\
    Returns the longitude or latitude as string with maximal 8 digits.
    """
    return '{0:.8f}'.format(f).rstrip('0')


def make_wifi_data(ssid, password, security, hidden=False):
    """\
    Creates WIFI configuration string.

    :param str|unicode ssid: The SSID of the network.
    :param str|unicode|None password: The password.
    :param str|unicode|None security: Authentication type; the value should
            be "WEP" or "WPA". Set to ``None`` to omit the value.
            "nopass" is equivalent to setting the value to ``None`` but in
            the former case, the value is not omitted.
    :param bool hidden: Indicates if the network is hidden (default: ``False``)
    :rtype: str
    """
    def quotation_mark(x):
        """\
        Returns '"' if x could be interpreted as hexadecimal value, otherwise
        an empty string.

        See: <https://github.com/zxing/zxing/wiki/Barcode-Contents>
        [...] Enclose in double quotes if it is an ASCII name, but could be
        interpreted as hex (i.e. "ABCD") [...]
        """
        try:
            int(x, 16)
        except ValueError:
            return ''
        return '"'

    data = 'WIFI:'
    if security:
        data += 'T:{0};'.format(security.upper() if security != 'nopass' else security)
    data += 'S:{1}{0}{1};'.format(_mecard_escape(ssid), quotation_mark(ssid))
    if password:
        data += 'P:{1}{0}{1};'.format(_mecard_escape(password), quotation_mark(password))
    data += 'H:true;' if hidden else ';'
    return data


def make_wifi(ssid, password, security, hidden=False):
    """\
    Creates a WIFI configuration QR Code.

    :param str|unicode ssid: The SSID of the network.
    :param str|unicode|None password: The password.
    :param str|unicode|None security: Authentication type; the value should
            be "WEP" or "WPA". Set to ``None`` to omit the value.
            "nopass" is equivalent to setting the value to ``None`` but in
            the former case, the value is not omitted.
    :param bool hidden: Indicates if the network is hidden (default: ``False``)
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_wifi_data(ssid, password, security, hidden))


def make_mecard_data(name, reading=None, email=None, phone=None, videophone=None,
                     memo=None, nickname=None, birthday=None, url=None,
                     pobox=None, roomno=None, houseno=None, city=None,
                     prefecture=None, zipcode=None, country=None):
    """\
    Creates a string encoding the contact information as MeCard.

    :param str|unicode name: Name. If it contains a comma, the first part
            is treated as lastname and the second part is treated as forename.
    :param str|unicode|None reading: Designates a text string to be set as the
            kana name in the phonebook
    :param str|unicode|iterable email: E-mail address. Multiple values are
            allowed.
    :param str|unicode|iterable phone: Phone number. Multiple values are
            allowed.
    :param str|unicode|iterable videophone: Phone number for video calls.
            Multiple values are allowed.
    :param str|unicode memo: A notice for the contact.
    :param str|unicode nickname: Nickname.
    :param (str|unicode|int|date) birthday: Birthday. If a string is provided,
            it should encode the date as YYYYMMDD value.
    :param str|unicode|iterable url: Homepage. Multiple values are allowed.
    :param str|unicode|None pobox: P.O. box (address information).
    :param str|unicode|None roomno: Room number (address information).
    :param str|unicode|None houseno: House number (address information).
    :param str|unicode|None city: City (address information).
    :param str|unicode|None prefecture: Prefecture (address information).
    :param str|unicode|None zipcode: Zip code (address information).
    :param str|unicode|None country: Country (address information).
    :rtype: str
    """
    def make_multifield(name, val):
        if val is None:
            return ()
        if isinstance(val, str_type):
            val = (val,)
        return ['{0}:{1};'.format(name, _mecard_escape(i)) for i in val]

    data = ['MECARD:N:{0};'.format(_mecard_escape(name))]
    if reading:
        data.append('SOUND:{0};'.format(_mecard_escape(reading)))
    data.extend(make_multifield('TEL', phone))
    data.extend(make_multifield('TELAV', videophone))
    data.extend(make_multifield('EMAIL', email))
    data.extend(make_multifield('NICKNAME', nickname))
    if birthday:
        try:
            birthday = birthday.strftime('%Y%m%d')
        except AttributeError:
            pass
        data.append('BDAY:{0};'.format(birthday))
    data.extend(make_multifield('URL', url))
    adr_properties = (pobox, roomno, houseno, city, prefecture, zipcode, country)
    if any(adr_properties):
        adr_data = [_mecard_escape(i or '') for i in adr_properties]
        data.append('ADR:{0},{1},{2},{3},{4},{5},{6};'.format(*adr_data))
    if memo:
        data.append('MEMO:{0};'.format(_mecard_escape(memo)))
    data.append(';')
    return ''.join(data)


def make_mecard(name, reading=None, email=None, phone=None, videophone=None,
                memo=None, nickname=None, birthday=None, url=None, pobox=None,
                roomno=None, houseno=None, city=None, prefecture=None,
                zipcode=None, country=None):
    """\
    Returns a QR Code which encodes a `MeCard <https://en.wikipedia.org/wiki/MeCard>`_

    :param str|unicode name: Name. If it contains a comma, the first part
            is treated as lastname and the second part is treated as forename.
    :param str|unicode|None reading: Designates a text string to be set as the
            kana name in the phonebook
    :param str|unicode|iterable email: E-mail address. Multiple values are
            allowed.
    :param str|unicode|iterable phone: Phone number. Multiple values are
            allowed.
    :param str|unicode|iterable videophone: Phone number for video calls.
            Multiple values are allowed.
    :param str|unicode memo: A notice for the contact.
    :param str|unicode nickname: Nickname.
    :param str|unicode|int|date birthday: Birthday. If a string is provided,
            it should encode the date as YYYYMMDD value.
    :param str|unicode|iterable url: Homepage. Multiple values are allowed.
    :param str|unicode|None pobox: P.O. box (address information).
    :param str|unicode|None roomno: Room number (address information).
    :param str|unicode|None houseno: House number (address information).
    :param str|unicode|None city: City (address information).
    :param str|unicode|None prefecture: Prefecture (address information).
    :param str|unicode|None zipcode: Zip code (address information).
    :param str|unicode|None country: Country (address information).
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_mecard_data(name=name, reading=reading,
                                          email=email, phone=phone,
                                          videophone=videophone, memo=memo,
                                          nickname=nickname, birthday=birthday,
                                          url=url, pobox=pobox, roomno=roomno,
                                          houseno=houseno, city=city,
                                          prefecture=prefecture, zipcode=zipcode,
                                          country=country))


def make_vcard_data(name, display_name, company=None, email=None, phone=None,
                    nickname=None, url=None, pobox=None, extended_adr=None,
                    street=None, city=None, state=None, zipcode=None,
                    country=None, gender=None, lat=None, lng=None):
    """\
    Creates a string encoding the contact information as vCard 3.0.
    
    :rtype: str
    """
    def make_multifield(name, val):
        if val is None:
            return ()
        if isinstance(val, str_type):
            val = (val,)
        return ['{0}:{1}'.format(name, _vcard_escape(i)) for i in val]

    data = ['BEGIN:VCARD', 'VERSION:3.0']
    data.append('N:{0}'.format(';'.join([_vcard_escape(item) for item in name.split(';')])))
    data.append('FN:{0}'.format(_vcard_escape(display_name)))
    if company:
        data.append('ORG:{0}'.format(_vcard_escape(company)))
    data.extend(make_multifield('EMAIL', email))
    data.extend(make_multifield('PHONE', phone))
    data.extend(make_multifield('URL', url))
    data.extend(make_multifield('NICKNAME', nickname))
    adr_properties = (pobox, extended_adr, street, city, state, zipcode, country)
    if any(adr_properties):
        adr_data = [_vcard_escape(i or '') for i in adr_properties]
        data.append('ADR:{0};{1};{2};{3};{4};{5};{6}'.format(*adr_data))
    if lat is not None and lng is not None:
        data.append('GEO:{0},{1}'.format(_geo_info(lat), _geo_info(lng)))
    if gender:
        if gender.upper() not in ('M', 'F'):
            raise ValueError('Illegal value for gender property. Expected "F" or "M", got "{0}"'.format(gender))
        gender = gender.upper()
        data.append('GENDER:{0}'.format(gender))
    data.append('END:VCARD')
    return '\n'.join(data)


def make_geo_data(lat, lng):
    """\
    Creates a geo location URI.

    :param float lat: Latitude
    :param float lng: Longitude
    :rtype: str
    """
    return 'geo:{0},{1}'.format(_geo_info(lat), _geo_info(lng))


def make_geo(lat, lng):
    """\
    Returns a QR Code which encodes geographic location using the ``geo`` URI
    scheme.

    :param float lat: Latitude
    :param float lng: Longitude
    :rtype: segno.QRCode
    """
    return segno.make_qr(make_geo_data(lat, lng))
