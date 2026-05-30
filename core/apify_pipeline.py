import re
import os
from apify_client import ApifyClient
from core.logger import get_logger

logger = get_logger("apify_pipeline")

def extract_url_content(text):
    logger.info("Checking for URLs in user message")
    logger.debug(f"Raw text: {text}")

    urls = re.findall(r'https?://[^\s]+', text)
    if not urls or not os.getenv("APIFY_TOKEN"):
        logger.info("No URLs found or Apify disabled")
        return ""

    url = urls[0]
    logger.info(f"Scraping URL: {url}")

    client = ApifyClient(os.getenv("APIFY_TOKEN"))
    actor = "apify/website-content-crawler"

    try:
        run = client.actor(actor).call(run_input={
            "startUrls": [{"url": url}],
            "maxCrawlPages": 1
        })
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items(limit=1))
        text = items[0].get("text", "")[:1000] if items else ""

        logger.info("Apify scrape complete")
        logger.debug(f"Scraped length: {len(text)}")

        return text

    except Exception as e:
        logger.error(f"Apify error: {e}")
        return ""
