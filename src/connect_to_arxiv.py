"""Connect to the arXiv API and return the results as entries of a FeedParserDict."""
from typing import Any

import feedparser


def GetResponseFromAPI(start: int, chunk_size: int) -> Any:
    feed = feedparser.parse(
        f"http://export.arxiv.org/api/query?search_query=start={start}&max_results={chunk_size}"
    )
    # if feed.status == 200:
    #     numberOfHeadlines = len(feed["entries"])

    #     for i in range(0, numberOfHeadlines):
    #         print(feed["entries"][i]["title"])
    # else:
    #     print("Something went wronge :", feed.status)

    return feed
