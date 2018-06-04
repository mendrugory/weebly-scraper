# Weebly Blog Post Scraper

Weebly provides the option to "back up" a site, but not the actual posts or content made to it. Which is predatory bullshit designed to prey upon clients who don't have any technical skills or understanding and then lock them into their service.

This is a very simple script to scrape a weebly site's blog posts into markdown files that can be used in things like Hugo or Jekyll, or just be viewed by hand. To import markdown files to Wordpress see [this link](https://tyler.io/importing-jekyll-posts-into-wordpress/).

To use run this script with python on the command line with the first argument being the website address (the weebly.com version) and the second being the target folder:

```shell
python3 weebly-scraper.py http://example.weebly.com ./content/
```

Requirements: [Python 3](https://wiki.python.org/moin/BeginnersGuide/Download
), [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

```shell
pip3 install -r requirements.txt
```
