from c0200_query_patents import query_patents
from c0300_aggregate_patents import aggregate_patents
from c0400_check_claims import check_claims
from c0500_add_time import add_time
from c0600_count_metadata import count_metadata
from c0700_plot_patents import plot_patents
from c0800_map_patents import map_patents
from c0900_count_words import count_words
from c1100_build_webpage import build_webpage

def main():
    """
    Motivation:
    Gain objectivity by surveying across a public database

    Objective:
    What scaffold parameters have been used for scaffold guided tissue engineering of bone.

    Tasks:
        (1) Define search terms
        (2) Query US Patent database
        (3)
    """

    # List task numbers to complete
    tasks = [9, 11]

    print('beginning main')

    if 2 in tasks:  query_patents()
    if 3 in tasks:  aggregate_patents()
    if 4 in tasks:  check_claims()
    if 5 in tasks:  add_time()
    if 6 in tasks:  count_metadata()

    if 7 in tasks:  plot_patents()
    if 8 in tasks:  map_patents()
    if 9 in tasks:  count_words()



    if 11 in tasks: build_webpage()

    print('completed main')


if __name__ == "__main__":
    main()
