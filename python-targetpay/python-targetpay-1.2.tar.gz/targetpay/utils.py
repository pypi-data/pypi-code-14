"""
    Targetpay Python module
    Copyright (C) 2016, Balkan Technologies EOOD & Co. KD

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    For more information: info@balkan.tech
"""
METHODS = (
    ('IDL', 'iDeal'),
    ('MRC', 'Mister Cash'),
    ('SOF', 'Sofort banking')
)

SOFORT_TYPES = {
    'PHYSICAL': 1,
    'DIGITAL': 2,
    'DIGITAL_ADULT': 3
}

SOFORT_COUNTRIES = {
    'DE': 49,
    'AT': 43,
    'CH': 41,
    'BE': 32,
    'IT': 39,
}