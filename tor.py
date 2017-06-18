from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


profile = webdriver.FirefoxProfile('/home/oem/.tor-browser-en/INSTALL/Browser/TorBrowser/Data/Browser/profile.default')
binary =FirefoxBinary('/usr/bin/tor-browser-en.sh')

driver = webdriver.Firefox(firefox_binary=binary, firefox_profile=profile)