import csv
import os
import random
import string

import time
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

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
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(3))


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

    def __init__(self, url, f_name, l_name, username, psw,
                 phone, month, day, year, psw_confirm=None, email=None,
                 gender=None, _zip=None, button=None, country=None):
        binary = FirefoxBinary(TOR_BINARY_PATH)

        prof = FirefoxProfile()

        prof.set_preference('network.proxy.type', 1)
        prof.set_preference('network.proxy.socks_host', '127.0.0.1')
        prof.set_preference('network.proxy.socks_port', 9150)
        prof.update_preferences()

        # self.driver = webdriver.Firefox(firefox_profile=prof,
        #                                 firefox_binary=binary)
        self.driver = webdriver.Firefox()
        self.driver.get(url)
        self.f_name_id = f_name
        self.f_name_el = self.driver.find_element_by_id(f_name)
        self.l_name_id = l_name
        self.l_name_el = self.driver.find_element_by_id(l_name)
        self.username_id = username
        self.username_el = self.driver.find_element_by_id(username)
        self.psw_id = psw
        self.psw_el = self.driver.find_element_by_id(psw)
        self.phone_id = phone
        self.phone_el = self.driver.find_element_by_id(phone)
        self.month_id = month
        self.month_el = self.driver.find_element_by_id(month)
        self.day_id = day
        self.day_el = self.driver.find_element_by_id(day)
        self.year_id = year
        self.year_el = self.driver.find_element_by_id(year)
        self.psw_confirm_id = psw_confirm
        self.psw_confirm_el = self.driver.find_element_by_id(
            psw_confirm) if psw_confirm else None
        self.gender_id = gender
        self.gender_el = self.driver.find_element_by_id(
            gender) if gender else None
        self.zip_id = _zip
        self.zip_el = self.driver.find_element_by_id(_zip) if _zip else None
        self.button_id = button
        self.button_el = self.driver.find_element_by_id(
            button) if button else None
        self.email_id = email
        self.email_el = self.driver.find_element_by_id(
            email) if email else None
        self.country_id = country
        self.country_el = self.driver.find_element_by_id(
            country) if country else None

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
    def get_full_name(cls):
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

    def run(self):
        self.fill_input(self.phone_id, Register.telephone)
        self.fill_input(self.psw_id, Register.password)
        self.fill_data(self.day_el, self.day_id, Register.DAY)
        self.fill_data(self.month_el, self.month_id, Register.MONTH)
        self.fill_data(self.year_el, self.year_id, Register.YEAR)
        self.fill_input(self.f_name_id, Register.first_name)
        self.fill_input(self.l_name_id, Register.last_name)
        self.fill_input(self.username_id, Register.get_full_name())
        self.fill_input(self.psw_confirm_id, Register.password)
        self.fill_data(self.country_el, self.country_id, Register.COUNTRY)
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
        self.click_el(self.button_id)
        time.sleep(3)
        try:
            self.driver.find_element_by_xpath("//button[@type='submit']").click()
        except Exception as e:
            print(e)
        print(user_msg)
        # user_to_file(user, self.username_el.text, full_adress)


class Hotmail(Register):
    def run(self):
        self.fill_input(self.username_id, '{}{}'.format(
            Register.get_full_name(), get_random('string'))
                        )
        Register.run(self)


if __name__ == '__main__':

    Register.get_users_from_file()
    for user in Register.users:
        hotmail = Hotmail(
            url='https://signup.live.com/?wa=wsignin1.0&rpsnv=13&ct=1497780750&rver=6.7.6643.0&wp=MBI_SSL_SHARED&wreply=https%3a%2f%2fmail.live.com%2fdefault.aspx&id=64855&cbcxt=mai&contextid=B8D329A03FEA83B1&bk=1497780755&uiflavor=web&uaid=f4f5e57bd31640058a5d98aeda47b15a&mkt=EN-US&lc=1033&lic=1',
            f_name='FirstName', l_name='LastName', username='MemberName',
            psw='Password', psw_confirm='RetypePassword', country='Country',
            phone='PhoneNumber', email='iAltEmail', month='BirthMonth',
            day='BirthDay', year='BirthYear', gender='Gender')
        yahoo = Yahoo(
            url="https://login.yahoo.com/account/create?specId=yidReg&lang=en-US&src=ym&done=https%3A%2F%2Fmail.yahoo.com&display=login&intl=us",
            f_name="usernamereg-firstName", l_name="usernamereg-lastName",
            username="usernamereg-yid", psw="usernamereg-password",
            phone="usernamereg-phone", day="usernamereg-day",
            year="usernamereg-year", button="reg-submit-button",
            month="usernamereg-month",
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
        Register.init_data(user)
        run_method(hotmail.run())
        run_method(yahoo.run())
        run_method(google.run())


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
