# coding: utf-8
import os
import time
import random
from selenium.common import exceptions as selexcept, exceptions
from selenium.webdriver.chrome.webdriver import WebDriver as Browser
from selenium.webdriver.support.wait import WebDriverWait


def wait(min_=1, max_=None):
    if max_ is None:
        time.sleep(min_)
    else:
        time.sleep(random.choice(xrange(min_, max_)))


def check_destination(file_name):
    path = os.path.dirname(file_name)
    try:
        os.makedirs(path)
    except OSError:
        pass

def load_links(file_name=None):
    if not file_name or not os.path.exists(file_name):
        return set()
    file_ = open(file_name, 'r')
    links = [l.rstrip() for l in file_.readlines()]
    file_.close()
    return set(links)


def save_links(links_list, file_name=None, append=False):
    if not file_name or not links_list:
        return
    check_destination(file_name)
    if not append:
        file_ = open(file_name, 'w')
    else:
        file_ = open(file_name, 'a')
    for line in links_list:
        file_.write(line + os.linesep)
    file_.close()


def login(email, password):
    browser = Browser()
    browser.get('http://tagbrand.com/login')
    WebDriverWait(browser, timeout=10).until(readystate_complete)
    form = browser.find_element_by_xpath('//*[@id="form-register"]')
    if form:
        email_field = browser.find_element_by_xpath('//*[@id="login-email"]')
        email_field.send_keys(email)
        pwd_field = browser.find_element_by_xpath(
            '//*[@id="LoginForm_password"]'
        )
        pwd_field.send_keys(password)
        submit_btn = browser.find_element_by_xpath(
            '//*[@id="form-register"]/div[3]/a'
        )
        submit_btn.click()
    return browser


def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except selexcept.WebDriverException:
        pass


def tagbrand_comlete(driver):
    try:
        return 'undefined' != driver.execute_script("return tagbrand.initFollows")
    except selexcept.WebDriverException:
        pass


def readystate_complete(d):
    try:
        return d.execute_script("return document.readyState") == "complete"
    except selexcept.WebDriverException:
        pass