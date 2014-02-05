#!/usr/bin/env python
# coding: utf-8

import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions as selexcept

import conf
import utils
import collect_me


def get_profile_links(browser):
    profile_links = browser.find_elements_by_xpath(
        '//*[@id="content"]/dl[*]/dt/span[1]/a'
    )
    raw_links = set()
    for link_el in profile_links:
        link = link_el.get_attribute('href')
        if link:
            raw_links.add(link)
    raw_links = list(raw_links)
    return raw_links


def follow():
    collect_me.collect_me()
    already_follow = utils.load_links(conf.FOLLOWING_FILE)
    print 'Already following %s users' % len(already_follow)
    targets = utils.load_links(conf.TARGETS_FILE)
    print 'Load %s targets' % len(targets)
    targets = targets.difference(already_follow)
    print 'Found %s potential targets' % len(targets)
    blacklist = utils.load_links(conf.BLACKLIST_FILE)
    follower = utils.load_links(conf.FOLLOWER_FILE)
    clear_blacklist = follower.intersection(blacklist)
    for user in clear_blacklist:
        blacklist.remove(user)
    print 'Clear %s blacklist' % len(clear_blacklist)
    utils.save_links(blacklist, conf.BLACKLIST_FILE)
    targets = targets.difference(blacklist)
    print 'Found %s new different targets' % len(targets)
    browser = utils.login(conf.LOGIN, conf.PASSWORD)
    for link in targets:
        try:
            browser.get(link)
            WebDriverWait(browser, timeout=10).until(utils.readystate_complete)
            follow_btn = browser.find_element_by_class_name('follow')
            follow_btn.find_element_by_link_text('follow')
            browser.execute_script('window.scroll(0,200);')
            likes = browser.find_elements_by_class_name('photo-like')
            for i, like in enumerate(likes):
                if i >= 3:
                    break
                class_ = like.get_attribute('class')
                if 'voted' not in class_:
                    like.send_keys(Keys.RETURN)
            browser.execute_script(
                'document.body.scrollTop = '
                'document.documentElement.scrollTop = 0;'
            )
            follow_btn.click()
            utils.wait(1)
            already_follow.add(link)
        except selexcept.NoSuchElementException:
            print 'Invalid user or already followed, skip him %s' % link
        except selexcept.WebDriverException:
            print 'Lost session? Try to reconnect'
            browser.quit()
            utils.wait(3)
            browser = utils.login(conf.LOGIN, conf.PASSWORD)
        except Exception, ex:
            print 'Skip %s - %s' % (link, ex)

if __name__ == '__main__':
    follow()