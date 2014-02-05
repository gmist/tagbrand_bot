#!/usr/bin/env python
# coding: utf-8

from grab import Grab
import grab.error
import utils
import conf

TOP_PEOPLE_LIMIT = 300


def get_links(page, grab_=None):
    if grab_ is None:
        grab_ = Grab()
    grab_.go(page)
    return [
        'http://tagbrand.com%s' % link.attr('href')
        for link in grab_.doc.select('//dl[*]/dd/p[1]/a')]


def get_top(only_russian=False):
    if only_russian:
        url = 'http://tagbrand.com/users?q%%5Bcountry%%5D=4&page=%s'
    else:
        url = 'http://tagbrand.com/users?page=%s'
    loop_count = 0
    fail_load_count = 0
    users = []
    while len(users) < TOP_PEOPLE_LIMIT and fail_load_count < 5:
        loop_count += 1
        links = get_links(url % loop_count)
        if links:
            for l in links:
                users.append(l)
        else:
            fail_load_count += 1
    users = set(users[:TOP_PEOPLE_LIMIT])
    return users


def _collect_follow(follow_link, grab_=None):
    if grab_ is None:
        grab_ = Grab()
    followers = []
    if follow_link:
        follower_count = follow_link.select('.//b').one().text()
        if follower_count:
            follower_count = int(follower_count)
            follow_link = follow_link.attr('href')
            loop_count = 0
            fails_count = 0
            while len(followers) < follower_count and fails_count < 5:
                loop_count += 1
                links = get_links(
                    '%s&page=%s' % (follow_link, loop_count), grab_
                )
                if not links:
                    fails_count += 1
                    continue
                for l in links:
                    followers.append(l)
                print 'Grab %s of %s users' % (len(followers), follower_count)
    return set(followers)


def collect_follower(user_link):
    grab_ = Grab()
    grab_.go(user_link)
    follow_link = grab_.doc.select(
        '//*[@id="content"]/div[1]/div[3]/ul/li[2]/a').one()
    return _collect_follow(follow_link, grab_)


def collect_following(user_link):
    grab_ = Grab()
    grab_.go(user_link)
    follow_link = grab_.doc.select(
        '//*[@id="content"]/div[1]/div[3]/ul/li[3]/a').one()
    return _collect_follow(follow_link, grab_)


def _run_all():
    users = utils.load_links(conf.ALL_TARGETS_FILE)
    helen_bot = 'http://tagbrand.com/helen'
    targets = collect_following(helen_bot)
    for target in targets:
        users.add(target)
    targets = collect_follower(helen_bot)
    for target in targets:
        users.add(target)
    utils.save_links(users, conf.TARGETS_FILE)


def _run(only_russian=False):
    users = utils.load_links(conf.TARGETS_FILE)
    for top in get_top(only_russian):
        try:
            targets = collect_following(top)
            for target in targets:
                users.add(target)
            print 'Grab %s users' % len(users)
        except grab.error.GrabTimeoutError:
            print "Timeout error, skip it"
        try:
            targets = collect_follower(top)
            for target in targets:
                users.add(target)
            print 'Grab %s users' % len(users)
        except grab.error.GrabTimeoutError:
            print "Timeout error, skip it"

    utils.save_links(users, conf.TARGETS_FILE)

if __name__ == '__main__':
    _run(only_russian=True)