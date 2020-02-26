import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='torrent-grab',
    version='0.0.2dev1',
    description='command line torrent scraper',
    author='Akshay Jadhav',
    author_email='akshay111jadhav@gmail.com',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/aksl337/torrent_scraper',
    download_url='https://github.com/aksl337/torrent_scraper/archive/0.1.tar.gz',
    scripts=['torrent-grab/torrent-grab'],
    install_requires=['BeautifulSoup4', 'clipboard', 'requests'],
    keywords=['torrent browse', 'scraper', 'torrent'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
