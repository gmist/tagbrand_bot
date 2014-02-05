#!/usr/bin/env python
# coding: utf-8

import conf
import utils
from collect import collect_follower, collect_following


def collect_me():
    followers = utils.load_links(conf.FOLLOWER_FILE)
    targets = collect_follower(conf.ME)
    for target in targets:
        followers.add(target)
    utils.save_links(followers, conf.FOLLOWER_FILE)

    following = utils.load_links(conf.FOLLOWING_FILE)
    targets = collect_following(conf.ME)
    for target in targets:
        following.add(target)
    utils.save_links(following, conf.FOLLOWING_FILE)

if __name__ == '__main__':
    collect_me()