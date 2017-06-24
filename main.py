import csv
import os
import random
import string

import time
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from captcha_solver import CaptchaSolver
from selenium.webdriver.common.proxy import *

# Presets
# first_name = 'JOHN'
# last_name = 'AGMA'
# usr_name = ''
# password = 'secret123'
# # telephone = '+13105874561'
# telephone = '+380995320999'
# curr_email = 'test2@ukr.net'
# full_adress = ''
user_msg = 'You should receive PIN code on your telephone for an activating ' \
           'account. Please, type it on web page and click confirmation button'

User = namedtuple('User', 'f_name l_name psw tel email')


def aol():
    driver = webdriver.Firefox()
    driver.get(
        "https://i.aol.com/reg/signup?ncid=txtlnkuswebr00000054&promocode=825329")
    # Page elements
    f_name = driver.find_element_by_id("firstName")
    l_name = driver.find_element_by_id("lastName")
    username = driver.find_element_by_id("desiredSN")
    psw = driver.find_element_by_id("password")
    psw_confirm = driver.find_element_by_id("verify-password-cont")
    country = driver.find_element_by_id("country-code_msdd")
    phone = driver.find_element_by_id("mobileNum")
    email = driver.find_element_by_id("altEMail")
    month = driver.find_element_by_id("dobMonth")
    day = driver.find_element_by_id("dobDay")
    year = driver.find_element_by_id("dobYear")
    gender = driver.find_element_by_id("gender")
    zip = driver.find_element_by_id("zipCode")

    f_name.send_keys(first_name)
    l_name.send_keys(last_name)


def get_random(choice):
    if choice == 'day':
        return random.randrange(1, 30)
    if choice == 'year':
        return random.randrange(1970, 2000)
    if choice == 'string':
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(5))


def get_data(psw, email):
    res = []
    path = os.path.join(os.getcwd(), 'names.txt')
    with open(path) as f:
        for line in f:
            full_name, tel = line.split(',')
            f_name, l_name = full_name.split(' ')
            res.append(User(f_name, l_name, psw, tel, email))
    return res


def user_to_file(user, usr_name, full_adress):
    filename = os.path.join(os.getcwd(), 'users.csv')
    with open(filename, 'a', newline='') as fp:
        a = csv.writer(fp)
        a.writerow(list(user) + [usr_name, full_adress])


def run_method(func):
    try:
        func()
    except Exception as e:
        print(e)


TOR_BINARY_PATH = '/usr/bin/tor-browser-en.sh'
RUCAPTCHA_API_KEY = '4dbbecf3bb7b40abeb99167e1c0e3fcb'


# TOR_BINARY_PATH = '/Applications/TorBrowser.app/Contents/MacOS/firefox'


class Register(object):
    User = namedtuple('User', 'f_name l_name psw tel mail')
    users = []
    first_name = ''
    last_name = ''
    password = ''
    telephone = ''
    curr_email = ''
    DAY = ('25',)
    MONTH = ('5', 'May', 'may',)
    YEAR = ('1987', '31',)
    COUNTRY = ('United States', 'US', 'us',)
    GENDER = ('Male', 'Female',)

    def __init__(self, url, f_name, l_name, username, psw, phone, month, day,
                 year, psw_confirm=None, email=None, gender=None, _zip=None,
                 button=None, country=None, captcha_img_alt=None,
                 captcha_input_label=None):
        self.url = url
        self.f_name_id = f_name
        self.l_name_id = l_name
        self.username_id = username
        self.psw_id = psw
        self.phone_id = phone
        self.month_id = month
        self.day_id = day
        self.year_id = year
        self.psw_confirm_id = psw_confirm
        self.gender_id = gender
        self.zip_id = _zip
        self.button_id = button
        self.email_id = email
        self.country_id = country
        self.captcha_img_alt = captcha_img_alt
        if captcha_img_alt:
            self.captcha_solver = CaptchaSolver('rucaptcha',
                                                api_key=RUCAPTCHA_API_KEY)
        self.captcha_input_label = captcha_input_label

    def run_selenium(self):
        port = "8118"  # The Privoxy (HTTP) port
        my_proxy = "127.0.0.1:" + port
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': my_proxy,
            'ftpProxy': my_proxy,
            'sslProxy': my_proxy,
            'noProxy': ''
        })

        # Launch the Firefox window and visit the given URL
        self.driver = webdriver.Firefox(proxy=proxy)
        self.driver.get(self.url)
        self.f_name_el = self.driver.find_element_by_id(self.f_name_id)
        self.l_name_el = self.driver.find_element_by_id(self.l_name_id)
        self.username_el = self.driver.find_element_by_id(self.username_id)
        self.psw_el = self.driver.find_element_by_id(self.psw_id)
        self.phone_el = self.driver.find_element_by_id(self.phone_id)
        self.month_el = self.driver.find_element_by_id(self.month_id)
        self.day_el = self.driver.find_element_by_id(self.day_id)
        self.year_el = self.driver.find_element_by_id(self.year_id)
        self.psw_confirm_el = self.driver.find_element_by_id(
            self.psw_confirm_id) if self.psw_confirm_id else None
        self.gender_el = self.driver.find_element_by_id(
            self.gender_id) if self.gender_id else None
        self.zip_el = self.driver.find_element_by_id(self.zip_id) if self.zip_id else None
        self.button_el = self.driver.find_element_by_id(
            self.button_id) if self.button_id else None
        self.email_el = self.driver.find_element_by_id(
            self.email_id) if self.email_id else None
        self.country_el = self.driver.find_element_by_id(
            self.country_id) if self.country_id else None
        self.captcha_img_el = self.driver.find_element_by_xpath(
            "//img[@alt='{}']".format(self.captcha_img_alt)
        ) if self.captcha_img_alt else None
        self.captcha_input_el = self.driver.find_element_by_xpath(
            "//input[@aria-label='{}']".format(self.captcha_input_label)
        ) if self.captcha_input_label else None

    @classmethod
    def get_users_from_file(cls, psw='dDD&sh21', email='test@ukr.net'):
        path = os.path.join(os.getcwd(), 'names.txt')
        with open(path) as f:
            for line in f:
                full_name, tel = line.split(',')
                f_name, l_name = full_name.split(' ')
                u = User(f_name, l_name, psw, tel, email)
                cls.users.append(u)

    @classmethod
    def init_data(cls, user):
        cls.first_name, cls.last_name, cls.password, \
        cls.telephone, cls.curr_email = list(user)

    @classmethod
    def get_full_name(cls, additional=False):
        if additional:
            return '{}{}{}'.format(
                cls.first_name.lower(),
                cls.last_name.lower(),
                get_random('string'))
        else:
            return '{}{}'.format(cls.first_name.lower(), cls.last_name.lower())

    def click_el(self, _id):
        self.driver.execute_script("""
            document.getElementById(arguments[0]).click();
        """, _id)

    def fill_input(self, _id, value):
        if not _id:
            return
        self.driver.execute_script("""
            document.getElementById(arguments[0]).setAttribute('value', arguments[1]);
            """, _id, value)

    def select_el(self, el, values):
        if not el:
            return
        for option in el.find_elements_by_tag_name('option'):
            if option.text in values:
                option.click()
                break

    def fill_data(self, el, _id, values):
        if not all([el, _id]):
            return
        if el.tag_name == 'input':
            self.fill_input(_id, values[0])
        self.select_el(el, values)

    def solve_captcha(self):
        if not self.captcha_img_el:
            return
        captcha_solver = CaptchaSolver('rucaptcha',
                                       api_key=RUCAPTCHA_API_KEY)
        img_path = os.path.join(os.getcwd(), 'captcha.png')
        self.captcha_img_el.screenshot(img_path)
        key = captcha_solver.solve_captcha(open(img_path, mode='rb').read())
        self.captcha_input_el.send_keys(key)

    def run(self):
        self.run_selenium()
        self.solve_captcha()
        self.fill_input(self.phone_id, Register.telephone)
        self.fill_input(self.psw_id, Register.password)
        self.fill_data(self.day_el, self.day_id, Register.DAY)
        self.fill_data(self.month_el, self.month_id, Register.MONTH)
        self.fill_data(self.year_el, self.year_id, Register.YEAR)
        self.fill_data(self.country_el, self.country_id, Register.COUNTRY)
        self.fill_data(self.gender_el, self.gender_id, Register.GENDER)
        self.fill_input(self.f_name_id, Register.first_name)
        self.fill_input(self.l_name_id, Register.last_name)
        self.fill_input(self.username_id, Register.get_full_name())
        self.fill_input(self.psw_confirm_id, Register.password)
        self.fill_input(self.psw_confirm_id, Register.password)
        self.fill_input(self.email_id, Register.curr_email)


class Google(Register):
    def run(self):
        Register.run(self)
        # Phone code
        self.phone_el.clear()
        telephone = '+1{}'.format(self.telephone)
        self.phone_el.send_keys(telephone)
        # Username code
        time.sleep(3)
        # Month code
        self.month_el.click()
        self.driver.find_element_by_xpath("//div[@class='goog-menuitem']").click()
        # Gender code
        self.gender_el.click()
        self.driver.find_element_by_xpath("//div[@id=':e']").click()
        # Sumbmit button
        self.click_el(self.button_id)
        time.sleep(5)
        already_exists_txt = self.driver.find_element_by_id(
            'errormsg_0_GmailAddress'
        ).text
        new_username = self.username_el.text
        if already_exists_txt.startswith('That user'):
            new_username = self.driver.find_element_by_xpath(
                '//div[@id="username-suggestions"]//a').text
            self.fill_input(self.username_id, new_username)
            self.fill_input(self.psw_id, Register.password)
            self.fill_input(self.psw_confirm_id, Register.password)
        time.sleep(3)
        tos_scroll = self.driver.find_element_by_xpath(
            '//div[@class="tos-scroll-button-content"]')
        tos_scroll.click()
        tos_scroll.click()
        time.sleep(2)
        agree_btn = self.driver.find_element_by_xpath('//input[@id="iagreebutton"]')
        agree_btn.click()
        time.sleep(2)
        try:
            next_btn = self.driver.find_element_by_xpath('//input[@id="next-button"]')
        except:
            print('Google error during registrating {}'.format(user))
        else:
            next_btn.click()
        print(user_msg)
        full_adress = '{}@gmail.com'.format(new_username)
        user_to_file(user, new_username, full_adress)


class Yahoo(Register):
    def run(self):
        Register.run(self)
        self.fill_input(self.username_id, self.get_full_name(additional=True))
        self.click_el(self.button_id)
        time.sleep(3)
        # try:
        #     self.driver.find_element_by_xpath("//button[@type='submit']").click()
        # except Exception as e:
        #     print(e)
        # print(user_msg)
        # user_to_file(user, self.username_el.text, full_adress)


class Hotmail(Register):
    def run(self):
        Register.run(self)
        self.fill_input(self.username_id, '{}{}'.format(
            Register.get_full_name(), get_random('string'))
                        )
        self.driver.find_element_by_id("CredentialsAction").click()


if __name__ == '__main__':

    Register.get_users_from_file()
    hotmail = Hotmail(
        url='https://signup.live.com/?wa=wsignin1.0&rpsnv=13&ct=1497780750&rver=6.7.6643.0&wp=MBI_SSL_SHARED&wreply=https%3a%2f%2fmail.live.com%2fdefault.aspx&id=64855&cbcxt=mai&contextid=B8D329A03FEA83B1&bk=1497780755&uiflavor=web&uaid=f4f5e57bd31640058a5d98aeda47b15a&mkt=EN-US&lc=1033&lic=1',
        f_name='FirstName', l_name='LastName', username='MemberName',
        psw='Password', psw_confirm='RetypePassword', country='Country',
        phone='PhoneNumber', email='iAltEmail', month='BirthMonth',
        day='BirthDay', year='BirthYear', gender='Gender',
        captcha_img_alt="Visual Challenge",
        captcha_input_label="Enter the characters you see")
    yahoo = Yahoo(
        url="https://login.yahoo.com/account/create?specId=yidReg&lang=en-US&src=ym&done=https%3A%2F%2Fmail.yahoo.com&display=login&intl=us",
        f_name="usernamereg-firstName", l_name="usernamereg-lastName",
        username="usernamereg-yid", psw="usernamereg-password",
        phone="usernamereg-phone", day="usernamereg-day",
        year="usernamereg-year", button="reg-submit-button",
        month="usernamereg-month"
    )
    google = Google(
        url="https://accounts.google.com/SignUp?service=mail&continue=https://mail.google.com/mail/?pc=topnav-about-en",
        f_name="FirstName",
        l_name="LastName",
        username="GmailAddress",
        psw="Passwd",
        psw_confirm="PasswdAgain",
        year="BirthYear",
        month="BirthMonth",
        day="BirthDay",
        gender="Gender",
        phone="RecoveryPhoneNumber",
        email="RecoveryEmailAddress",
        button="submitbutton"
    )
    for user in Register.users:
        Register.init_data(user)
        # run_method(hotmail.run())
        run_method(yahoo.run())
        # run_method(google.run())


        # aol = Register(
        #     url='https://i.aol.com/reg/signup?ncid=txtlnkuswebr00000054&promocode=825329',
        #     f_name='firstName', l_name='lastName', username='desiredSN',
        #     psw='password', psw_confirm='verify-password-cont', country='country-code_msdd',
        #     phone='mobileNum', email='altEMail',
        #     month='dobMonth', day='dobDay', year='dobYear', gender='gender',
        #     zip='zipCode'
        # )
        # users = Register.get_data()
        # for user in users:
        #     pass
