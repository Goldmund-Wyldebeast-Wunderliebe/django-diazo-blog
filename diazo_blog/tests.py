from __future__ import print_function

import os
import re
import unittest
import subprocess
from time import sleep

PROJECT_DIR = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

PRINT_INFO = True

def print_info(func):
    """
    Prints some useful info.
    """
    if not PRINT_INFO:
        return func

    def inner(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        print('\n\n%s' % func.__name__)
        print('============================')
        if func.__doc__:
            print('""" %s """' % func.__doc__.strip())
        print('----------------------------')
        if result is not None:
            print(result)
        print('\n++++++++++++++++++++++++++++')

        return result
    return inner

clean_extra_spaces = lambda s: ' '.join(s.split())#re.sub(r'\s+', ' ', s)
clean_xml_content = lambda s: re.sub(r'\<view\>\&lt\;django_diazo_themes\.angled_theme\.view\.ExampleView.+</view>', '', s)

# Skipping from non-Django tests.
if os.environ.get("DJANGO_SETTINGS_MODULE", None):
    from optparse import OptionParser

    from django.test import LiveServerTestCase
    from django.contrib.auth.models import User
    from django.test import Client
    from selenium.webdriver.firefox.webdriver import WebDriver
    from selenium.webdriver.support.wait import WebDriverWait

    from logging import getLogger
    from django.conf import settings
    from django.utils.translation import ugettext as _
    from django.core.management import call_command
    from django.contrib.staticfiles.management.commands import collectstatic

    from django_diazo.models import Theme
    from django_diazo.theme import registry
    from django_diazo import autodiscover as django_diazo_autodiscover
    from django_diazo.models import Theme
    from django_diazo import autodiscover as django_diazo_autodiscover

    try:
        LIVE_SERVER_URL = settings.LIVE_SERVER_URL
    except:
        LIVE_SERVER_URL = ''

    # Ministerial theme rendered HTML
    theme_html = clean_extra_spaces("""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <!-- Design by Free CSS Templates http://www.freecsstemplates.org Released for free under a Creative Commons Attribution 2.5 License Name : Ministerial Description: A two-column, fixed-width design with dark color scheme. Version : 1.0 Released : 20121029 --> <html xmlns="http://www.w3.org/1999/xhtml"><head> <meta content="" name="keywords" /> <meta content="" name="description" /> <meta content="text/html; charset=utf-8" http-equiv="content-type" /> <title>Pagetitle</title> <link type="text/css" rel="stylesheet" href="http://fonts.googleapis.com/css?family=Oswald:400,300" /> <link type="text/css" rel="stylesheet" href="http://fonts.googleapis.com/css?family=Abel%7CSatisfy" /> <link media="all" type="text/css" rel="stylesheet" href="/static/ministerial/default.css" /> <!--[if IE 6]> <link href="/static/ministerial/default_ie6.css" rel="stylesheet" type="text/css" /> <![endif]--> </head> <body> <div id="wrapper"> <div id="header-wrapper"> <div id="header"> <div id="logo"> <h1> <a href="/">Brandname</a> </h1> <p>Subtitle</p> </div> <div id="menu"> <ul> <li class="current_page_item"><a href="/">Home</a></li><li><a href="/contact">Contact</a></li><li><a href="/test">Test</a></li><li><a href="/bla">Bla</a></li><li><a href="/more">More</a></li> </ul></div> </div> </div> <div id="banner"><img src="//lorempixel.com/1120/500/nightlife" /></div> <div id="page-wrapper"> <div id="page"> <div id="wide-content"> <h2>Pagetitle</h2> <p>Blablablablabla</p><p>Blablablablabla</p><p class="button-style"><a href="/">Home</a></p> </div> </div> </div> <div id="recent-news"><h2>Aaa</h2><div id="rbox1"><p class="date">21 october 2013</p><p>Bla</p><p class="button-style1"> <a href="/">Read more</a> </p></div><div id="rbox2"><p class="date">22 october 2013</p><p>Ble</p><p class="button-style1"> <a href="/">Read more</a> </p></div><div id="rbox3"><p class="date">23 october 2013</p><p>Bli</p><p class="button-style1"> <a href="/">Read more</a> </p></div><div id="rbox4"><p class="date">24 october 2013</p><p>Blo</p><p class="button-style1"> <a href="/">Read more</a> </p></div></div> <div id="footer-wrapper"> <div id="footer-content"> <div id="fbox1"> <h2>Left</h2> <ul class="style2"> <li class="first"><a href="/">Link 1</a></li><li><a href="/">Link 2</a></li><li><a href="/">Link 3</a></li><li><a href="/">Link 4</a></li><li><a href="/">Link 5</a></li><li><a href="/">Link 6</a></li> </ul> <p class="button-style"> <a href="/">More details</a> </p> </div> <div id="fbox2"> <h2>Center</h2> <content><p>blaaaaaaa</p><p><img src="//lorempixel.com/500/200/sports" /></p></content> <p class="button-style"> <a href="/">More details</a> </p> </div> <div id="fbox3"> <h2>Right</h2> <ul class="style3"> <li class="first"><img src="//lorempixel.com/78/78/technics" /><p>This is a text that should be long enough to cover two lines.</p><p class="posted"> 21 october 2013 | (2) Comments </p></li><li><img src="//lorempixel.com/78/78/food" /><p>This is a text that should be long enough to cover two lines.</p><p class="posted"> 22 october 2013 | (4) Comments </p></li><li><img src="//lorempixel.com/78/78/city" /><p>This is a text that should be long enough to cover two lines.</p><p class="posted"> 23 october 2013 </p></li> </ul> </div> </div> </div> </div> <div id="footer"> <p>This is the footer</p> </div> </body></html>
    """)

    # Original XML
    original_xml = clean_xml_content(clean_extra_spaces("""
<?xml version="1.0" encoding="UTF-8"?><context><banner>//lorempixel.com/1120/500/nightlife</banner><brand><name>Brandname</name><url>/</url></brand><center_portlet><content><p>blaaaaaaa</p><p><img src="//lorempixel.com/500/200/sports" /></p></content><more><name>More details</name><url>/</url></more><title>Center</title></center_portlet><content><p>Blablablablabla</p><p>Blablablablabla</p><p class="button-style"><a href="/">Home</a></p></content><footer><p>This is the footer</p></footer><lhs_portlet><content><item><name>Link 1</name><url>/</url></item><item><name>Link 2</name><url>/</url></item><item><name>Link 3</name><url>/</url></item><item><name>Link 4</name><url>/</url></item><item><name>Link 5</name><url>/</url></item><item><name>Link 6</name><url>/</url></item></content><more><name>More details</name><url>/</url></more><title>Left</title></lhs_portlet><menu><item class="active"><name>Home</name><url>/</url></item><item><name>Contact</name><url>/contact</url></item><item><name>Test</name><url>/test</url></item><item><name>Bla</name><url>/bla</url></item><item><name>More</name><url>/more</url></item></menu><news><newsitems><item><button><name>Read more</name><url>/</url></button><date>21 october 2013</date><text>Bla</text><title>Aaa</title></item><item><button><name>Read more</name><url>/</url></button><date>22 october 2013</date><text>Ble</text><title>Bbb</title></item><item><button><name>Read more</name><url>/</url></button><date>23 october 2013</date><text>Bli</text><title>Ccc</title></item><item><button><name>Read more</name><url>/</url></button><date>24 october 2013</date><text>Blo</text><title>Ddd</title></item></newsitems><title>News</title></news><rhs_portlet><content><item><image>//lorempixel.com/78/78/technics</image><posted><date>21 october 2013</date><extra>(2) Comments</extra></posted><text>This is a text that should be long enough to cover two lines.</text></item><item><image>//lorempixel.com/78/78/food</image><posted><date>22 october 2013</date><extra>(4) Comments</extra></posted><text>This is a text that should be long enough to cover two lines.</text></item><item><image>//lorempixel.com/78/78/city</image><posted><date>23 october 2013</date></posted><text>This is a text that should be long enough to cover two lines.</text></item></content><title>Right</title></rhs_portlet><subtitle>Subtitle</subtitle><title>Pagetitle</title><view>&lt;django_diazo_themes.angled_theme.view.ExampleView object at 0x7f30ec0104d0&gt;</view></context>
    """))

    def activate_ministerial_theme():
        # Set ministerial theme as default
        Theme._default_manager.update(enabled=False)
        ministerial_theme = Theme._default_manager.get(slug='ministerial')
        ministerial_theme.enabled = True
        ministerial_theme.debug = False
        ministerial_theme.save()
        print("Ministerial theme activated")

    def install_diazo():
        call_command('syncdb', noinput=True, traceback=True)
        call_command('migrate', noinput=True, traceback=True)
        #call_command('syncdb', migrate_all=True, noinput=True, traceback=True)
        #call_command('migrate', fake=True, noinput=True, traceback=True)
        call_command('collectstatic', verbosity=3, interactive=False)
        call_command('migrate', 'django_diazo', verbosity=3, interactive=False)
        call_command('syncthemes')

    def create_admin_user():
        # Create an admin user in order to be able to make changes (set the default themes)
        u = User()
        u.username = 'admin'
        u.email = 'admin@dev.django-diazo.com'
        u.is_superuser = True
        u.is_staff = True
        u.set_password('test')

        try:
            u.save()
            print("Admin user created")
        except:
            pass


    class DjangoDiazoBlogNoThemeTest(unittest.TestCase):
        """
        Basic testing of no theme.

        TODO: read both original XML and theme HTML from external files.
        """
        def setUp(self):
            pass

        @print_info
        def test_no_diazo(self):
            c = Client()
            #response = c.get('{0}/'.format(LIVE_SERVER_URL), {})
            response = c.get('{0}/'.format(''), {})
            self.assertTrue(response.status_code in (200, 201, 202))
            response_content = clean_xml_content(clean_extra_spaces(response.content))
            self.assertTrue(response_content == original_xml)


    class DjangoDiazoBlogThemeMinisterialSeleniumTest(LiveServerTestCase):
        """
        Basic testing of ministerial theme.

        TODO: read both original XML and theme HTML from external files.
        """
        try:
            LIVE_SERVER_URL = settings.LIVE_SERVER_URL
        except:
            LIVE_SERVER_URL = ''

        @classmethod
        def setUpClass(cls):
            cls.selenium = WebDriver()
            super(DjangoDiazoBlogThemeMinisterialSeleniumTest, cls).setUpClass()

        @classmethod
        def tearDownClass(cls):
            try:
                cls.selenium.quit()
            except Exception as e:
                print(e)

            super(DjangoDiazoBlogThemeMinisterialSeleniumTest, cls).tearDownClass()

        @print_info
        def __test_01_login(self):
            """
            Test login.
            """
            live_server_url = self.LIVE_SERVER_URL if self.LIVE_SERVER_URL else self.live_server_url
            self.selenium.get('{0}{1}'.format(live_server_url, '/admin/'))
            username_input = self.selenium.find_element_by_name("username")
            username_input.send_keys('admin')
            password_input = self.selenium.find_element_by_name("password")
            password_input.send_keys('test')
            self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

        @print_info
        def test_theme_enabled_no_debug(self):
            install_diazo()
            create_admin_user()
            activate_ministerial_theme()

            try:
                LIVE_SERVER_URL = settings.LIVE_SERVER_URL
            except:
                LIVE_SERVER_URL = ''

            live_server_url = self.LIVE_SERVER_URL if self.LIVE_SERVER_URL else self.live_server_url

            self.selenium.get('{0}{1}'.format(live_server_url, '/'))

            page_source = clean_extra_spaces(self.selenium.page_source)
            self.assertTrue(page_source == theme_html)
