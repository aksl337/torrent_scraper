#!/bin/python

from bs4 import BeautifulSoup
import requests
import clipboard
import sys
import signal
from time import sleep

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
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0", "Accept-Language": "en-US, en;q=0.5"}

# little ctrl+c handler


def signal_handler(signal, frame):
    print '\n{} Bye {}\n'.format('_' * 65, '_' * 65)
    sys.exit(0)


def soup_maker():
    iter_one = True
    while iter_one:
        search_string = raw_input(bcolors.OKGREEN + "\nsearch for files-->\n " + bcolors.ENDC)
        if not search_string.strip():
            print 'please enter something \nor ctrl+c to exit'
        else:
            main_url = "https://kickass-cd.pbproxy.lol/usearch/{}/?field=seeders&sorder=desc".format(search_string)
            iter_two = 1
            while iter_two:
                try:
                    response = requests.get(main_url, headers=headers, timeout=10)
                    break
                # check appropriate response code 200
                except requests.exceptions.HTTPError as e:
                    print ('connection refused by server')
                    print ('lemme try again...')
                    sleep(10)
                    continue
                except requests.Timeout as e:
                    print(str(e))
                    print 'timed out'
                except requests.ConnectionError:
                    print 'network problem, are you sure ,you are online?'
                    sys.exit()

                    # beautifulsoup extracter
            my_soup = BeautifulSoup(response.text, 'lxml')
            torrent_data = my_soup.findAll(class_="odd", id="torrent_latest_torrents12975568")
            if not torrent_data:
                "nothing found this time ,\nseems trusted source acting weird, see-->{}".format(torrent_data)
            else:
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

                if len(sizes_all) == 0:
                    print (bcolors.FAIL + 'Nothing found try different search string' + bcolors.ENDC)
                    soup_maker()
                iter_one = False
    print_movies()
    magnet_printer()


def print_movies():
    # printing stuff for users
    for i in range(len(sizes_all)):
        print (bcolors.OKGREEN + "{0}.  {1}\t".format(i, movies_all[i]) + bcolors.ENDC),
        print (bcolors.HEADER + "size{0}seeds-{1} leeches-{2}".format(sizes_all[i], seeders_all[i], leechers_all[i]) + bcolors.ENDC)


def magnet_printer():
    iter_one = True
    while iter_one:
        more_mag = raw_input("Enter num. from list for magnet link or 'ee' to exit or 'gg' for search again--->\n\t")
        if not more_mag.strip():
            print 'enter something'
        elif more_mag in str(range(len(movies_all))):
            print (bcolors.WARNING + "\n magnet link copied to your clipboard already" + bcolors.ENDC)
            clipboard.copy(magnet_links_all[int(more_mag)])
        elif more_mag.lower() == "ee":
            iter_one = False
            print '\n{} Bye {}\n'.format('_' * 65, '_' * 65)
            sys.exit()
        elif more_mag.lower() == "gg":
            soup_maker()
        else:
            print (bcolors.FAIL + "Unknown input !!! finger slipping detected...." + bcolors.ENDC)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    soup_maker()


if __name__ == "__main__":
    sys.exit(main())
