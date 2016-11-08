# -*- coding: utf-8 -*-

# this contains fixtures that can/should be loaded in conftest.py in your project to
# override some of the dependent pytest-plugins fixtures

import os
import pytest
import re

from django.core.urlresolvers import reverse
from splinter.exceptions import ElementDoesNotExist


# def pytest_addoption(parser):
#     group = parser.getgroup('dolphin')
#     group.addoption(
#         '--foo',
#         action='store',
#         dest='dest_foo',
#         default='2016',
#         help='Set the value for the fixture "bar".'
#     )
#
#     parser.addini('HELLO', 'Dummy pytest.ini setting')


@pytest.yield_fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Fixture that will clean up remaining connections, that might be hanging
    from threads or external processes. Extending pytest_django.django_db_setup
    """

    yield

    with django_db_blocker.unblock():
        from django.db import connections

        conn = connections['default']
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM pg_stat_activity;""")
        print('current connections')
        for r in cursor.fetchall():
            print(r)

        terminate_sql = """
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '%s'
                AND pid <> pg_backend_pid();
        """ % conn.settings_dict['NAME']
        print('Terminate SQL: ', terminate_sql)
        cursor.execute(terminate_sql)


@pytest.fixture(scope='session')
def splinter_webdriver():
    """Override splinter webdriver name."""
    return os.getenv('TEST_UI_DRIVER', 'phantomjs')


# @pytest.fixture(scope='session')
# def browser(live_server_url):
#     b = Browser('phantomjs', service_log_path=settings.GHOST_DRIVER_LOG)
#     b.driver.set_window_size(1024, 680)
#
#     def logout():
#         b.visit(live_server_url + reverse('base:logout'))
#         b.cookies.delete()
#         b.visit(live_server_url + reverse('base:login'))
#
#     def login(email, password='password', logout_first=True):
#         if logout_first:
#             logout()
#         form = b.find_by_tag('form')
#         form.find_by_name('username').first.fill(email)
#         form.find_by_name('password').first.fill(password)
#         form.find_by_tag('button').first.click()
#
#     def click_path(*path):
#         for link in path:
#             if link.startswith('id:'):
#                 b.find_by_id(link[3:]).first.click()
#             elif link.startswith('exact:'):
#                 b.find_link_by_text(link[6:]).first.click()
#             else:
#                 b.find_link_by_partial_text(link).first.click()
#
#     b.click_path = click_path
#     b.logout = logout
#     b.login = login
#     return b
#
#

def browser_patcher(browser, live_server_reverse, login_url=None, logout_url=None):

    def logout():
        browser.visit(logout_url)
        browser.cookies.delete()
        browser.visit(login_url)

    def login(username, password='password', logout_first=True):
        if logout_first:
            logout()
        form = browser.find_by_tag('form')
        form.find_by_name('username').first.fill(username)
        form.find_by_name('password').first.fill(password)
        form.find_by_tag('button').first.click()

    def click_path(*path):
        for link in path:
            item_offset = None

            # if we have # in the end, we should use the Nth item
            m = re.match(r'^(.+)#(\d+)$', link)
            if m:
                link = m.group(1)
                item_offset = int(m.group(2)) - 1

            wait_for_text_to_be_present = False
            if link.startswith('wait:'):
                link = link[5:]
                wait_for_text_to_be_present = True

            if link.startswith('id:'):
                if wait_for_text_to_be_present:
                    raise Exception('wait: and id: cannot be combined in click_path')
                element_finder, text = browser.find_by_id, link[3:]
            elif link.startswith('exact:'):
                element_finder, text = browser.find_link_by_text, link[6:]
            else:
                element_finder, text = browser.find_link_by_partial_text, link

            if wait_for_text_to_be_present:
                browser.is_text_present(text)

            elements = element_finder(text)
            if item_offset is None:
                elements.first.click()
            else:
                elements[item_offset].click()

    def visit_with_reverse(path, hostname=None, *args, **kwargs):
        browser.visit(live_server_reverse(path, hostname), *args, **kwargs)
        assert browser.status_code.code != 500, 'Visting %s caused server error 500' % live_server_reverse(path)

    def fill_and_submit_form(form_id, use_js_submit=False, **fields):
        try:
            form = browser.find_by_id(form_id).first
        except ElementDoesNotExist as find_exec:
            info_text = 'available forms: ' + ', '.join(
                ['<id:%s, class:%s>' % (f['id'], f['class']) for f in browser.find_by_tag('form')]
            )
            raise ElementDoesNotExist('%s - %s' % (find_exec, info_text))

        for k, v in fields.iteritems():
            input_element = form.find_by_name(k).first
            if isinstance(v, basestring) and v.startswith('select:'):
                for select_value in v[7:].split(','):
                    input_element.select(select_value)
            elif isinstance(v, basestring) and v.startswith('check:'):
                check, value = v.split(':')
                if value.lower() == 'true':
                    input_element.check()
                else:
                    input_element.uncheck()
            else:
                input_element.fill(v)

        if use_js_submit:
            browser.execute_script("document.getElementById('%s').submit();" % form_id)
        else:
            form.find_by_tag('button').first.click()

    if login_url is not None:
        browser.login = login
    if logout_url is not None:
        browser.logout = logout
    browser.django_visit = visit_with_reverse
    browser.click_path = click_path
    browser.fill_and_submit_form = fill_and_submit_form
    return browser


@pytest.fixture(scope='function')
def browser(request, browser_instance_getter, live_server_reverse, django_logout_url, django_login_url):
    obj = browser_instance_getter(request, browser)
    return browser_patcher(obj, live_server_reverse, login_url=django_login_url, logout_url=django_logout_url)
