# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
import re
import functools

DOMAIN = 'taskcluster.imbstack.com'
LOCAL_LINK_RE = re.compile('^https?://{}/(docs|reference|manual|tutorial|resources|people)'.format(DOMAIN))
TASKCLUSTER_NET_RE = re.compile('^https?://docs.taskcluster.net')


@functools.total_ordering
class Page:

    def __init__(self, response):
        self.url = response.url
        self.links = []

    def __eq__(self, other):
        return self.url == other.url

    def __lt__(self, other):
        return self.url < other.url

    def issues(self):
        for link in self.links:
            if link.url.startswith('http:'):
                yield 'has non-https link: {}'.format(link.url)
            mo = TASKCLUSTER_NET_RE.match(link.url)
            if mo:
                yield 'links to taskcluster.net: {}'.format(link.url)
            mo = LOCAL_LINK_RE.match(link.url)
            if mo and mo.group(1) != 'docs':
                yield 'links to path without /docs: {}'.format(link.url)


class DocsSpider(Spider):
    name = 'docs'
    allowed_domains = [DOMAIN]
    start_urls = ['https://taskcluster.imbstack.com/docs/']

    extractor = LinkExtractor(
        allow=(LOCAL_LINK_RE, TASKCLUSTER_NET_RE),
        unique=True)

    pages = {}  # url: Page

    def parse(self, response):
        request = response.request
        links = self.extractor.extract_links(response)

        page = Page(response)
        self.pages[response.url] = page
        page.links = links

        for link in links:
            # don't bother following http://...
            if link.url.startswith('https:'):
                yield response.follow(link)

    def closed(self, reason):
        if reason != 'finished':
            return

        for page in sorted(self.pages.values()):
            issues = list(page.issues())
            if issues:
                print("{}:".format(page.url))
                for issue in issues:
                    print("  {}".format(issue))
