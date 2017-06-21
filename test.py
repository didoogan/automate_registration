
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
import time


# path to the firefox binary inside the Tor package
binary = '/usr/bin/tor-browser-en.sh'

firefox_binary = FirefoxBinary(binary)
browser = webdriver.Firefox(executable_path=binary)
browser.get("https://www.google.com/")
time.sleep(20)
browser.get("https://www.google.com/")
