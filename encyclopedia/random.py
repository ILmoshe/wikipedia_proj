"""Module for getting random entry
"""
from random import randint

from . import util


lst = util.get_list_entries()
def random_entry():
    return lst[randint(0, len(lst) - 1)]
