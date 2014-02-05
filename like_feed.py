#!/usr/bin/env python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import utils
import conf


if __name__ == '__main__':
    browser = utils.login(conf.LOGIN, conf.PASSWORD)
    feed = browser.get('http://tagbrand.com/feed')
    WebDriverWait(browser, timeout=10).until(utils.readystate_complete)
    for i in xrange(0, 30):
        print 'scroll down %s' % (i+1)
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        utils.wait(1)

    like_links = browser.find_elements_by_class_name('photo-like')
    print 'found %s photos' % len(like_links)
    browser.execute_script('document.body.scrollTop = document.documentElement.scrollTop = 0;')
    count = 0
    for i, like in enumerate(like_links):
        c = like.get_attribute('class')
        if 'voted' not in c:
            a = like.location_once_scrolled_into_view
            like.send_keys(Keys.RETURN)
            count += 1
            utils.wait(1)
    print 'liked %s photos' % count