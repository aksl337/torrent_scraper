#!/bin/python
import re
from bs4 import BeautifulSoup
import requests
import clipboard
import sys
import signal
from time import sleep


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0", "Accept-Language": "en-US, en;q=0.5"}
numbers = []
linkss = []
names = []
leechers = []
seeders = []
sizes = []
date_time = []
page_count = 1


def signal_handler(signal, frame):
    print '\n{} Bye {}\n'.format('_' * 65, '_' * 65)
    sys.exit(0)


def soup_maker(page=page_count):
    iter_one = True
    while iter_one:
        search_string = raw_input(bcolors.OKGREEN + "\nsearch for files-->\n " + bcolors.ENDC)
        if not search_string.strip():
            print 'please enter something \nor ctrl+c to exit'
        else:
            main_url = "http://1337x.pbproxy.lol/sort-search/{}/seeders/desc/{}/".format(search_string, str(page))
            while True:
                try:
                    response = requests.get(main_url, headers=headers, timeout=10)
                    break
                # check appropriate response code 200
                except requests.exceptions.HTTPError as e:
                    print ('connection refused by server,make sure site is up and working...')
                    print ('lemme try again...')
                    sleep(5)
                    continue
                except requests.Timeout as e:
                    print(str(e))
                    print 'timed out'
                    print('lemme try again')
                    sleep(5)
                    continue
                except requests.ConnectionError:
                    print 'network problem, are you sure ,you are online?'
                    sys.exit()

            # beautifulsoup extracter
            my_soup = BeautifulSoup(response.text, 'lxml')

            # soup = BeautifulSoup(open("/root/new_scrape/1337x.html"), "html.parser")
            soup_data = my_soup.findAll(class_="table-list table table-responsive table-striped")
            if not soup_data:
                print "nothing found this time ,\ntry different search string, see-->{}".format(soup_data)
            else:
                for container in soup_data:
                    names_links = container.find_all('a', href=re.compile("torrent"))
                    seeds = container.find_all(class_="coll-2 seeds")
                    leeches = container.find_all(class_="coll-3 leeches")
                    sizes_all = container.find_all(class_="coll-4")
                    dates_all = container.find_all(class_="coll-date")
                for seed in seeds:
                    seeders.append(seed.text)
                for leech in leeches:
                    leechers.append(leech.text)
                for link in names_links:
                    names.append(link.text.replace(" ", "").replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\xf1", "'"))
                    linkss.append(link.get('href'))
                for size in sizes_all[1:]:
                    if size.span:
                        _ = size.span.extract()
                    sizes.append(size.text)
                del _
                for dates in dates_all:
                    date_time.append(dates.text.replace(" ", ""))

                for i in range(len(leeches)):
                    numbers.append(i)

                if len(sizes) == 0:
                    print (bcolors.FAIL + 'Nothing found try different search string' + bcolors.ENDC)
                    soup_maker()
                iter_one = False
    print_movies()
    magnet_printer()


def print_movies():
    # printing stuff for users
    '''print "links{} leec{} seeds{} names{} sizes{}".format(len(linkss), len(leechers), len(seeders), len(names), len(sizes))
    for size in sizes:
        print size
    for link in linkss:
        print linkss'''

    for i in range(len(linkss)):
        print (bcolors.OKGREEN + "{0}.  {1}\t".format(i, names[i]) + bcolors.ENDC),
        print (bcolors.HEADER + "size{0}seeds-{1} leeches-{2}".format(sizes[i], seeders[i], leechers[i]) + bcolors.ENDC)


def magnet_printer():
    iter_one = True
    magnets = []
    while iter_one:
        more_mag = raw_input("Enter num. from list for magnet link or 'mm' for more results of same or 'gg' for different search or \n 'ee' to exit   --->\n\t")
        if not more_mag.strip():
            print (bcolors.FAIL + "enter something\n" + bcolors.ENDC)
        elif more_mag in str(range(len(linkss))):
            sitelink = "http://1337x.pbproxy.lol" + str(linkss[int(more_mag)])
            while True:
                try:
                    response = requests.get(sitelink, headers=headers, timeout=10)
                    break
                # check appropriate response code 200
                except requests.exceptions.HTTPError as e:
                    print ('connection refused by server,make sure site is up and working...')
                    print ('lemme try again...')
                    sleep(5)
                    continue
                except requests.Timeout as e:
                    print(str(e))
                    print 'timed out'
                    print('lemme try again')
                    sleep(5)
                    continue
                except requests.ConnectionError:
                    print 'network problem, are you sure ,you are online?'
                    sys.exit()

            souped = BeautifulSoup(response.text, 'lxml')
            mainlink = souped.findAll('a', href=re.compile("magnet"))
            for contain in mainlink:
                magnets.append(contain.get('href'))
            clipboard.copy(magnets[-1])
            print (bcolors.WARNING + "\n magnet link copied to your clipboard already..." + bcolors.ENDC)
        elif more_mag.lower() == "ee":
            iter_one = False
            print '\n{} Bye {}\n'.format('_' * 65, '_' * 65)
            sys.exit()
        elif more_mag.lower() == "gg":
            soup_maker()
        elif more_mag.lower() == "mm":
            soup_maker(page=page_count + 1)
        else:
            print (bcolors.FAIL + "Unknown input !!! finger slipping detected...." + bcolors.ENDC)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    soup_maker()


if __name__ == "__main__":
    sys.exit(main())
