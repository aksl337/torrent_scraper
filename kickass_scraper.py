#!/bin/env python

from bs4 import BeautifulSoup
from warnings import warn
import requests
import clipboard

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
search_string = raw_input("search for torrent--> ")
main_url = "https://kickass-cd.pbproxy.lol/usearch/{}/?field=seeders&sorder=desc".format(search_string)
# grab the page from url
response = requests.get(main_url, headers=headers)
# check appropriate response code 200
if response.status_code != 200:
    warn('Request: {}; Status code: {}'.format(requests, response.status_code))
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


def print_movies(no_of_movies):
    # printing stuff for users
    for i in range(1, no_of_movies + 1):
        print (bcolors.OKGREEN + "{0}.  {1}\t".format(i, movies_all[i]) + bcolors.ENDC),
        print (bcolors.HEADER + "size{0}seeds-{1} leeches-{2}".format(sizes_all[i], seeders_all[i], leechers_all[i]) + bcolors.ENDC)
    in_num = int(raw_input("\nenter the no. of movie for graping magnet link--> "))
    print "magnet link for your movie--->\n{}->".format(magnet_links_all[in_num])
    print (bcolors.WARNING + "\n magnet link copied to your clipboard already" + bcolors.ENDC)
    clipboard.copy(magnet_links_all[in_num])


if __name__ == "__main__":
    noo = int(raw_input("enter no of movies to grape--> "))
    print_movies(noo)
