from distutils.core import setup

setup(
    name='torrent-grab',
    packages=['torrent-grab'],
    version='0.1',
    description='command line torrent scrapper',
    author='Akshay Jadhav',
    author_email='akshay111jadhav@gmail.com',
    license='MIT',
    url='https://github.com/aksl337/torrent_scraper',
    download_url='https://github.com/aksl337/torrent_scraper/archive/0.1.tar.gz',
    python_requires='>=2.7',
    scripts=['torrent-grab/torrent-grab.py'],
    install_requires=[
        'BeautifulSoup4',
        'clipboard',
        'requests'
    ],
    keywords=['torrent browse', 'scrapper', 'torrent'],
    classifiers=[],
)
