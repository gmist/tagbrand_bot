#!/usr/bin/env python
# coding: utf-8

import conf
import utils
from collect import collect_follower, collect_following


def collect_me():
    followers = set()
    targets = collect_follower(conf.ME)
    for target in targets:
        followers.add(target)
    utils.save_links(followers, conf.FOLLOWER_FILE)

    following = set()
    targets = collect_following(conf.ME)
    for target in targets:
        following.add(target)
    utils.save_links(following, conf.FOLLOWING_FILE)

if __name__ == '__main__':
    collect_me()