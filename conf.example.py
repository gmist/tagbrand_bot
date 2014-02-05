# coding: utf-8
import os

ME = 'http://tagbrand.com/tagbrandshop'
LOGIN = 'shop@tagbrand.com'
PASSWORD = 'af2fWFV32cJuy7'

WORK_DIR = 'tmp'
ME_DIR = os.path.join(WORK_DIR, 'mine')
ALL_TARGETS_FILE = os.path.join(WORK_DIR, 'all_targets_list.txt')
TARGETS_FILE = os.path.join(WORK_DIR, 'targets_list.txt')
FOLLOWER_FILE = os.path.join(ME_DIR, 'follower_list.txt')
FOLLOWING_FILE = os.path.join(ME_DIR, 'following_list.txt')
BLACKLIST_FILE = os.path.join(ME_DIR, 'black_list.txt')