This is a simple, [Scrapy](https://scrapy.org/)-based scraper to help find
issues on the Taskcluster-docs site.

# Casual Usage Only

This is not meant for production use.  It is only for catching errors that can
easily sneak into a docs site.

## Usage

Using Python-3.5 or higher, `pip install scrapy`, then, to run the scraper:

```shell
scrapy crawl docs -a rootUrl=https://taskcluster-staging.net
```

(or whatever rootUrl you would like to look at)

## Output

The output is one JSON object per line, giving the `url` where an error occurred, and some kind of hint as to what the issue is.
For example:

```
{"taskcluster-net-link": "https://docs.taskcluster.net/reference/core/taskcluster-notify",
 "url": "https://taskcluster.imbstack.com/docs/reference/platform/taskcluster-queue/docs/actions"}
```

this shows that the `actions` doc has a link to `docs.taskcluster.net`, rather
than to the appropriate rootUrl.
