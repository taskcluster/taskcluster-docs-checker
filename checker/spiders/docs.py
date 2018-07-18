# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
import re
import functools
import urllib


class DocsSpider(Spider):
    name = 'docs'

    def __init__(self, rootUrl, *args, **kwargs):
        super(DocsSpider, self).__init__(*args, **kwargs)

        domain = urllib.parse.urlparse(rootUrl).netloc

        self.allowed_domains = [domain]
        self.start_urls = ['https://{}/docs/'.format(domain)]
        self.local_link_re = re.compile('^https?://{}/(docs|reference|manual|tutorial|resources|people)'.format(domain))
        self.taskcluster_net_re = re.compile('^https?://docs.taskcluster.net')
        self.extractor = LinkExtractor(
            allow=(self.local_link_re, self.taskcluster_net_re),
            unique=True)

    def parse(self, response):
        links = self.extractor.extract_links(response)

        for link in links:
            # don't bother following http://...
            if link.url.startswith('https:'):
                yield response.follow(link)

            if link.url.startswith('http:'):
                yield {'url': response.url, 'non-https-link': link.url}
            mo = self.taskcluster_net_re.match(link.url)
            if mo:
                yield {'url': response.url, 'taskcluster-net-link': link.url}
            mo = self.local_link_re.match(link.url)
            if mo and mo.group(1) != 'docs':
                yield {'url': response.url, 'missing-slash-docs': link.url}
