import csv
import os
import random

import time
from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Presets
first_name = 'JOHN'
last_name = 'AGMA'
password = 'secret123'
# telephone = '+13105874561'
telephone = '+380995320999'
curr_email = 'test@ukr.net'
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
    username.send_keys('{}.{}'.format(first_name.lower(), last_name.lower()))
    psw.click()
    time.sleep(0.3)
    already_exists_txt = driver.find_element_by_id('errormsg_0_GmailAddress').text

    if already_exists_txt.startswith('Someone already has that username.'):
        new_username = driver.find_element_by_xpath('//div[@id="username-suggestions"]//a').text
        username.clear()
        username.send_keys(new_username)
    month_div.click()
    driver.find_element_by_xpath("//div[@class='goog-menuitem']").click()

    birth_day.send_keys(get_random('day'))
    birth_year.send_keys(get_random('year'))
    gender.click()
    driver.find_element_by_xpath("//div[@id=':e']").click()
    phone.clear()
    phone.send_keys(telephone)
    email.send_keys(curr_email)
    button.click()
    time.sleep(2)
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
    time.sleep(0.6)
    driver.find_element_by_css_selector(
        '#desktop-suggestion-list li:nth-child(1)').click()
    month_div.find_elements_by_tag_name('option')[3].click()
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
    print(user_msg)


def get_random(choice):
    if choice == 'day':
        return random.randrange(1, 30)
    if choice == 'year':
        return random.randrange(1970, 2000)


def get_data(psw, email):

    res = []
    path = os.path.join(os.getcwd(), 'names.txt')
    with open(path) as f:
        for line in f:
            full_name, tel = line.split(',')
            f_name, l_name = full_name.split(' ')
            res.append(User(f_name, l_name, psw, tel, email))
    return res


def user_to_file(user):
    filename = '{}/users.csv'.format(os.getcwd())
    with open(filename, 'a', newline='') as fp:
        a = csv.writer(fp)
        a.writerow(list(user))

if __name__ == '__main__':
    users = get_data('poikld54', 'test@ukr.net')
    for user in users:
        first_name, last_name, password, telephone, curr_email = list(user)
        try:
            yahoo()
        except Exception as e:
            print(e)
        telephone = '+1{}'.format(telephone)
        #gmail()
        #user_to_file(user)
