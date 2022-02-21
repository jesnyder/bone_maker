import numpy as np

from a0100_acquire_info import acquire_info
from a0200_aggregate_info import aggregate_info
from a0300_geolocate_articles import geolocate_articles
from a0400_untargeted_word_count import untargeted_word_count
from a0500_targeted_word_count import targeted_word_count
from a0600_map_maker import map_maker
from a9900_build_webpage import build_webpage

def main():
    """

    """
    print('beginning main')

    # List task numbers to complete
    tasks = [99]
    if  0 in tasks: tasks = np.arange(1, 101, 1)
    if  1 in tasks: acquire_info()
    if  2 in tasks: aggregate_info()
    if  3 in tasks: geolocate_articles()
    if  4 in tasks: untargeted_word_count()
    if  5 in tasks: targeted_word_count()
    if  6 in tasks: map_maker()
    if 99 in tasks: build_webpage()

    print('completed main')


if __name__ == "__main__":
    main()
