Overview of directory structure:

- `gospel_search/elasticsearch/`: The code related to the ElasticSearch search engine server.
- `gospel_search/mongodb/`: The code related to the MongoDB database which stores all the segments and embedding vectors.
- `gospel_search/nextjs`: The code for the proxy server and user interface.
- `gospel_search/nlp_server`: The code for the NLP paragraph embedding re-ranking server.
- `gospel_search/web_scraping`: The code for the HTML scraper.

To run the system locally in a Windows environment (requires powershell, Python 3, Node.js, and the Windows subsystem for Linux):

```powershell
# Start the MongoDB database
Start-Process -FilePath "<path_to_mongo_installation>\bin\mongod.exe" -ArgumentList "--dbpath=`"<path_to_mongo_data>`""
# Start ElasticSearch (source: source: elastic.co/guide/en/elasticsearch/reference/current/zip-windows.html)
Start-Process -FilePath "<path_to_elasticsearch_installation>\bin\elasticsearch.bat"
# Start the NLP server
Start-Process wsl -ArgumentList "python", "-m", "gospel_search.nlp_server"
# Start the Node.js proxy/UI server in dev mode
Start-Process npm -ArgumentList "run dev"
```
