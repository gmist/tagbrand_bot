#!/usr/bin/env python
# coding: utf-8

import os
from selenium.common import exceptions as selexcept

import conf
import utils
import collect_me


def unfollow():
    collect_me.collect_me()
    following = utils.load_links(conf.FOLLOWING_FILE)
    followers = utils.load_links(conf.FOLLOWER_FILE)
    blacklist = utils.load_links(conf.BLACKLIST_FILE)
    to_unfollow = following.difference(followers)
    for user in to_unfollow:
        blacklist.add(user)
    utils.save_links(blacklist, conf.BLACKLIST_FILE)
    print 'Prepare to unfollow %s users' % len(to_unfollow)
    browser = utils.login(conf.LOGIN, conf.PASSWORD)
    for link in to_unfollow:
        try:
            browser.get(link)
            unfollow_btn = browser.find_element_by_class_name('follow')
            unfollow_btn.find_element_by_link_text('unfollow')
            unfollow_btn.click()
            utils.wait(1)
        except selexcept.NoSuchElementException:
            continue
        except selexcept.WebDriverException:
            print 'Lost session? Try to recconect.'
            browser.quit()
            utils.wait(1)
            browser = utils.login(conf.LOGIN, conf.PASSWORD)
        except Exception, ex:
            print 'Skip %s - %s' % (link, ex)

if __name__ == '__main__':
    unfollow()
