#!/usr/bin/env python
# coding: utf-8

import grab
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
    grab_ = grab.Grab()
    for link in targets:
        if 'http://tagbrand.com/id' in link:
            continue
        user_id = None
        likes = []
        try:
            try:
                grab_.go(link)
                div = grab_.doc.select(
                    '//*[@id="content"]/div[1]/div[2]/div[*]/div[1]').one()
                user_id = div.attr('data-user')
                try:
                    likes = grab_.doc.select(
                        '//*[@id="content"]/div[*]/div[3]/div/div[1]')\
                        .attr_list('photo-id')
                except grab.error.DataNotFound, ex:
                    likes = []
            except grab.error.DataNotFound, ex:
                print 'Skip %s - %s' % (link, ex)
                continue
            if user_id:
                browser.execute_script(
                    '$.post(\
                        "http://tagbrand.com/followers/follow",\
                        {userId:%s});' % user_id)
                likes = likes[:2]
                for photo_id in likes:
                    if not utils.like_photo(browser, user_id, photo_id):
                        utils.like_photo(browser, user_id, photo_id)

        except selexcept.WebDriverException:
            print 'Lost session? Try to reconnect'
            browser.quit()
            utils.wait(3)
            browser = utils.login(conf.LOGIN, conf.PASSWORD)

if __name__ == '__main__':
    follow()
