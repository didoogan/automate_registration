import csv
import os
import random
import string

import time
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Presets
first_name = 'JOHN'
last_name = 'AGMA'
usr_name = ''
password = 'secret123'
# telephone = '+13105874561'
telephone = '+380995320999'
curr_email = 'test2@ukr.net'
full_adress = ''
user_msg = 'You should receive PIN code on your telephone for an activating ' \
           'account. Please, type it on web page and click confirmation button'

User = namedtuple('User', 'f_name l_name psw tel email')


def gmail():
    driver = webdriver.Firefox()
    driver.get("https://accounts.google.com/SignUp?service=mail&continue=https://mail.google.com/mail/?pc=topnav-about-en")
    # Page elements
    f_name = driver.find_element_by_id("FirstName")
    l_name = driver.find_element_by_id("LastName")
    username = driver.find_element_by_xpath("//input[@id='GmailAddress']")
    psw = driver.find_element_by_id('Passwd')
    psw_conf = driver.find_element_by_id('PasswdAgain')
    month_div = driver.find_element_by_xpath('//span[@id="BirthMonth"]')
    birth_day = driver.find_element_by_xpath('//input[@id="BirthDay"]')
    birth_year = driver.find_element_by_xpath('//input[@id="BirthYear"]')
    gender = driver.find_element_by_xpath('//div[@id="Gender"]')
    phone = driver.find_element_by_xpath('//input[@id="RecoveryPhoneNumber"]')
    email = driver.find_element_by_xpath('//input[@id="RecoveryEmailAddress"]')
    button = driver.find_element_by_xpath('//input[@id="submitbutton"]')

    f_name.send_keys(first_name)
    l_name.send_keys(last_name)
    psw.send_keys(password)
    psw_conf.send_keys(password)
    new_username = '{}.{}'.format(first_name.lower(), last_name.lower())
    username.send_keys(new_username)
    usr_name = new_username
    psw.click()
    time.sleep(2.3)
    already_exists_txt = driver.find_element_by_id('errormsg_0_GmailAddress').text

    if already_exists_txt.startswith('Someone already has that username.'):
        print('======================')
        new_username = driver.find_element_by_xpath('//div[@id="username-suggestions"]//a').text
        username.clear()
        username.send_keys(new_username)
        usr_name = new_username
    full_adress = '{}@gmail.com'.format(new_username)
    month_div.click()
    driver.find_element_by_xpath("//div[@class='goog-menuitem']").click()

    birth_day.send_keys(get_random('day'))
    birth_year.send_keys(get_random('year'))
    gender.click()
    driver.find_element_by_xpath("//div[@id=':e']").click()
    phone.clear()
    tel = '+1{}'.format(telephone)
    phone.send_keys(tel)
    email.send_keys(curr_email)
    button.click()
    time.sleep(5)
    tos_scroll = driver.find_element_by_xpath('//div[@class="tos-scroll-button-content"]')
    tos_scroll.click()
    tos_scroll.click()
    time.sleep(2)
    agree_btn = driver.find_element_by_xpath('//input[@id="iagreebutton"]')
    agree_btn.click()
    time.sleep(2)
    next_btn = driver.find_element_by_xpath('//input[@id="next-button"]')
    next_btn.click()
    print(user_msg)
    user_to_file(user, usr_name, full_adress)
    # driver.close()


def yahoo():
    driver = webdriver.Firefox()
    driver.get("https://login.yahoo.com/account/create?specId=yidReg&lang=en-US&src=ym&done=https%3A%2F%2Fmail.yahoo.com&display=login&intl=us")
    # Page elements
    f_name = driver.find_element_by_id("usernamereg-firstName")
    l_name = driver.find_element_by_id("usernamereg-lastName")
    email = driver.find_element_by_id("usernamereg-yid")
    psw = driver.find_element_by_id("usernamereg-password")
    phone = driver.find_element_by_id("usernamereg-phone")
    month_div = driver.find_element_by_id("usernamereg-month")
    birth_day = driver.find_element_by_id("usernamereg-day")
    birth_year = driver.find_element_by_id('usernamereg-year')
    create_btn = driver.find_element_by_id('reg-submit-button')

    birth_day.click()
    birth_day.send_keys(get_random('day'))
    birth_year.send_keys(get_random('year'))
    birth_year.click()
    f_name.send_keys(first_name)
    l_name.send_keys(last_name)
    # email.send_keys('{}.{}{}'.format(first_name.lower(), last_name.lower(), 'dFg'))
    email.send_keys('{}.{}'.format(first_name.lower(), last_name.lower()))
    psw.send_keys(password)
    phone.send_keys(telephone)
    time.sleep(2.6)
    driver.find_element_by_css_selector(
        '#desktop-suggestion-list li:nth-child(1)').click()
    month_div.find_elements_by_tag_name('option')[3].click()
    usr_name = email.text
    try:
        r = driver.find_element_by_id('reg-error-phone').text
        if r.startswith("We don't"):
            raise AttributeError('You should provide real phone number '
                                 'for user {} {}'.format(first_name, last_name))
    except:
        pass
    create_btn.click()
    time.sleep(1)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    full_adress = '{}@yahoo.com'.format(usr_name)
    print(user_msg)
    user_to_file(user, usr_name, full_adress)


def hotmail():

    driver = webdriver.Firefox()
    driver.get("https://signup.live.com/?wa=wsignin1.0&rpsnv=13&ct=1497780750&rver=6.7.6643.0&wp=MBI_SSL_SHARED&wreply=https%3a%2f%2fmail.live.com%2fdefault.aspx&id=64855&cbcxt=mai&contextid=B8D329A03FEA83B1&bk=1497780755&uiflavor=web&uaid=f4f5e57bd31640058a5d98aeda47b15a&mkt=EN-US&lc=1033&lic=1")
    # Page elements
    f_name = driver.find_element_by_id("FirstName")
    l_name = driver.find_element_by_id("LastName")
    username = driver.find_element_by_id("MemberName")
    psw = driver.find_element_by_id("Password")
    psw_confirm = driver.find_element_by_id("RetypePassword")
    country = driver.find_element_by_id("Country")
    phone = driver.find_element_by_id("PhoneNumber")
    email = driver.find_element_by_id("iAltEmail")
    month = driver.find_element_by_id("BirthMonth")
    day = driver.find_element_by_id("BirthDay")
    year = driver.find_element_by_id("BirthYear")
    gender = driver.find_element_by_id("Gender")

    psw.send_keys(password)
    psw_confirm.click()
    psw_confirm.send_keys(password)
    phone.click()
    phone.send_keys(telephone)
    l_name.click()
    l_name.send_keys(last_name)
    username.click()
    usr_name = '{}.{}{}'.format(
        first_name.lower(), last_name.lower(), get_random('string'))
    username.send_keys(usr_name)
    email.click()
    email.send_keys(curr_email)
    f_name.click()
    f_name.send_keys(first_name)
    psw_confirm.clear()
    psw_confirm.send_keys(password)
    month.find_elements_by_tag_name('option')[5].click()
    day.find_elements_by_tag_name('option')[25].click()
    year.find_elements_by_tag_name('option')[31].click()
    gender.find_elements_by_tag_name('option')[1].click()

    for option in country.find_elements_by_tag_name('option'):
        if option.text == 'United States':
            option.click()
            break
    try:
        error = driver.find_element_by_id('MemberNameError').text
        if error.startswith('Someone already has this'):
            username.clear()
            username.click()
            usr_name = '{}{}{}'.format(
                first_name.lower(), last_name.lower(), get_random('string')
            )
            username.send_keys(usr_name)
    except:
        pass
    full_adress = '{}@outlook.com'.format(usr_name)
    print('You should enter captcha')
    user_to_file(user, usr_name, full_adress)
    # try:
    #     text = driver.find_element_by_xpath("//div[@id='hipSection']//div[contains(string(), 'Before proceeding, we need')]").text
    #     if text.startswith('Before proceeding,'):
    #         driver.find_element_by_id('wlspispHipSendCode752022fb06e54d4681a422b1c33646aa').click()
    # except:
    #     print('You should enter captcha')


def aol():
    driver = webdriver.Firefox()
    driver.get("https://i.aol.com/reg/signup?ncid=txtlnkuswebr00000054&promocode=825329")
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
    filename = '{}/users.csv'.format(os.getcwd())
    with open(filename, 'a', newline='') as fp:
        a = csv.writer(fp)
        a.writerow(list(user) + [usr_name, full_adress])


class Register(object):
    driver = webdriver.Firefox()

    def __init__(self, name, url, f_name, l_name, username, psw, psw_confirm, country,
                 phone, email, month, day, year, gender=None, zip=None):
        self.name = name
        self.driver.get(url)
        self.f_name_el = self.driver.find_element_by_id(f_name)
        self.l_name_el = self.driver.find_element_by_id(l_name)
        self.username_el = self.driver.find_element_by_id(username)
        self.psw_el = self.driver.find_element_by_id(psw)
        self.psw_confirm_el = self.driver.find_element_by_id(psw_confirm)
        self.country_el = self.driver.find_element_by_id(country)
        self.phone_el = self.driver.find_element_by_id(phone)
        self.email_el = self.driver.find_element_by_id(email)
        self.month_el = self.driver.find_element_by_id(month)
        self.day_el = self.driver.find_element_by_id(day)
        self.year_el = self.driver.find_element_by_id(year)
        if gender:
            self.gender_el = self.driver.find_element_by_id(gender)
        if zip:
            self.zip_el = self.driver.find_element_by_id(zip)

    @staticmethod
    def get_data(psw='dDD&sh21', email='test@ukr.net'):
        path = os.path.join(os.getcwd(), 'names.txt')
        res = []
        with open(path) as f:
            for line in f:
                full_name, tel = line.split(',')
                f_name, l_name = full_name.split(' ')
                res.append(User(f_name, l_name, psw, tel, email))
        return res


    def run(self):
        users = Register.get_data()
        for user in users:
            first_name, last_name, password, telephone, curr_email = list(user)
            self.f_name_el.click()
            self.f_name_el.send_keys(first_name)
            self.l_name_el.click()
            self.l_name_el.send_keys(last_name)
            self.username_el.click()
            if self.name == 'hotmail':
                self.username_el.send_keys('{}{}{}'.format(
                    first_name.lower(), last_name.lower(), get_random('string')
                ))
            else:
                self.username_el.send_keys('{}{}'.format(
                    first_name.lower(), last_name.lower()
                ))
            self.phone_el.click()
            self.phone_el.send_keys(telephone)
            self.psw_confirm_el.click()
            self.psw_confirm_el.send_keys(password)
            self.gender_el.find_elements_by_tag_name('option')[1].click()
            self.month_el.find_elements_by_tag_name('option')[5].click()
            self.psw_el.click()
            self.psw_el.send_keys(password)

            if self.name == 'hotmail':
                self.day_el.click()
                self.day_el.find_elements_by_tag_name('option')[25].click()
                self.year_el.find_elements_by_tag_name('option')[31].click()
                self.phone_el.clear()
                self.phone_el.click()
                self.phone_el.send_keys(telephone)
                for option in self.country_el.find_elements_by_tag_name('option'):
                    if option.text == 'United States':
                        option.click()
                        break



                        # l_name.click()
    # l_name.send_keys(last_name)
    # username.click()
    # usr_name = '{}.{}{}'.format(
    #     first_name.lower(), last_name.lower(), get_random('string'))
    # username.send_keys(usr_name)
    # email.click()
    # email.send_keys(curr_email)
    # f_name.click()
    # f_name.send_keys(first_name)
    # psw_confirm.clear()
    # psw_confirm.send_keys(password)
    # month.find_elements_by_tag_name('option')[5].click()
    # day.find_elements_by_tag_name('option')[25].click()
    # year.find_elements_by_tag_name('option')[31].click()
    # gender.find_elements_by_tag_name('option')[1].click()



if __name__ == '__main__':
    # users = get_data('poikld54', 'test@ukr.net')
    # for user in users:
    #     first_name, last_name, password, telephone, curr_email = list(user)
    #     try:
    #          gmail()
    #     except Exception as e:
    #         print(e)
    #     try:
    #         yahoo()
    #     except Exception as e:
    #         print(e)
    #     try:
    #         hotmail()
    #     except Exception as e:
    #         print(e)
        # aol()
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
    hotmail = Register(name='hotmail', url='https://signup.live.com/?wa=wsignin1.0&rpsnv=13&ct=1497780750&rver=6.7.6643.0&wp=MBI_SSL_SHARED&wreply=https%3a%2f%2fmail.live.com%2fdefault.aspx&id=64855&cbcxt=mai&contextid=B8D329A03FEA83B1&bk=1497780755&uiflavor=web&uaid=f4f5e57bd31640058a5d98aeda47b15a&mkt=EN-US&lc=1033&lic=1',
        f_name='FirstName', l_name='LastName', username='MemberName',
        psw='Password', psw_confirm='RetypePassword', country='Country',
        phone='PhoneNumber', email='iAltEmail', month='BirthMonth',
        day='BirthDay', year='BirthYear', gender='Gender')

    hotmail.run()

