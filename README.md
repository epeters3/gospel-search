# Overview of directory structure:

- `gospel_search/elasticsearch/`: The code related to the ElasticSearch search engine server.
- `gospel_search/mongodb/`: The code related to the MongoDB database which stores all the segments and embedding vectors.
- `gospel_search/nextjs`: The code for the proxy server and user interface.
- `gospel_search/nlp_server`: The code for the NLP paragraph embedding re-ranking server.
- `gospel_search/web_scraping`: The code for the HTML scraper.

## Run Guide

### Step 1: Extract and index all content

1. To crawl, pull, and save all the raw HTML documets to the `gospel_search.pages` collection:

   ```
   ./scripts/crawl.sh
   ```

2. To extract segments from the previously crawled raw HTML documents and save them to the `gospel_search.segments` collection:

   ```
   ./scripts/extract.sh
   ```

3. To compute an embedding for each segment and add them to the `gospel_search_segments` collection:

   ```
   ./scripts/embed.sh
   ```

### TODO: left off getting nlp-server to start up successfully.
