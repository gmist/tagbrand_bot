#!/usr/bin/env python
# coding: utf-8

import grab
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
    grab_ = grab.Grab()
    for link in to_unfollow:
        if 'http://tagbrand.com/id' in link:
            id_ = link.split('http://tagbrand.com/id')[1]
            if not id:
                print 'Skip %s - %s' % (link)
                continue
        else:
            try:
                grab_.go(link)
                div = grab_.doc.select(
                        '/html/body/div/div[4]/div/div[2]/div[*]/div').one()
                id_ = div.attr('data-user')
            except grab.error.DataNotFound, ex:
                print 'Skip %s - %s' % (link, ex)
                continue
            except grab.error.GrabTimeoutError, ex:
                print 'Skip %s - %s' % (link, ex)
                continue
        if id_:
            browser.execute_script(
            '$.post("http://tagbrand.com/followers/unfollow", {userId:%s});'\
                    % id_)

if __name__ == '__main__':
    unfollow()
