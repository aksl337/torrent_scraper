#!/bin/python

from bs4 import BeautifulSoup
from warnings import warn
import requests
import clipboard
import sys
import signal

# Colored output


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# some useful variables
movies_all = []
sizes_all = []
seeders_all = []
leechers_all = []
magnet_links_all = []
headers = {"Accept-Language": "en-US, en;q=0.5"}

# little ctrl+c handler


def signal_handler(signal, frame):
    print('      BYE............................')
    sys.exit(0)


# grab the page from url


def soup_maker():
    search_string = raw_input(bcolors.OKGREEN + "\nsearch for files-->\n " + bcolors.ENDC)
    main_url = "https://kickass-cd.pbproxy.lol/usearch/{}/?field=seeders&sorder=desc".format(search_string)
    response = requests.get(main_url, headers=headers)
    # check appropriate response code 200
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(main_url, response.status_code))
        sys.exit(0)
    # beautifulsoup extracter
    my_soup = BeautifulSoup(response.text, 'lxml')
    torrent_data = my_soup.findAll(class_="odd", id="torrent_latest_torrents12975568")

    for container in torrent_data:
        # cooking my soup adding data to lists
        movie = container.find_all('a')[-2].text.encode('utf-8')
        movies_all.append(movie)
        size = container.find(class_='nobr center').text.encode('utf-8')
        sizes_all.append(size)
        seeder = container.find(class_='green center').text.encode('utf-8')
        seeders_all.append(seeder)
        leecher = container.find(class_='red lasttd center').text
        leechers_all.append(leecher)
        magnet_link = container.find_all('a')[2].get('href')
        magnet_links_all.append(magnet_link)

    print "{} movies found with result containing {}....\n".format(len(sizes_all), search_string)
    if len(sizes_all) == 0:
        print (bcolors.FAIL + 'Nothing found try different search string' + bcolors.ENDC)
        soup_maker()
    print_movies()
    magnet_printer()


def print_movies():
    # printing stuff for users
    for i in range(len(sizes_all)):
        print (bcolors.OKGREEN + "{0}.  {1}\t".format(i, movies_all[i]) + bcolors.ENDC),
        print (bcolors.HEADER + "size{0}seeds-{1} leeches-{2}".format(sizes_all[i], seeders_all[i], leechers_all[i]) + bcolors.ENDC)


def magnet_printer():
    while True:
        more_mag = raw_input("Enter num. from list for graping magnet link or 'e' to exit,or 'g' for search again--->\n\t")
        if more_mag in str(range(len(movies_all))):
            # print "magnet link for your movie--->\n{}->".format(magnet_links_all[int(more_mag)])
            print (bcolors.WARNING + "\n magnet link copied to your clipboard already" + bcolors.ENDC)
            clipboard.copy(magnet_links_all[int(more_mag)])
        elif more_mag.lower() == "e":
            break
        elif more_mag.lower() == "g":
            soup_maker()
        else:
            print (bcolors.FAIL + "Unknown input !!! finger slipping detected...." + bcolors.ENDC)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    soup_maker()
