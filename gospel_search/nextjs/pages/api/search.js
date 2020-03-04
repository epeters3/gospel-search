import fetch from "node-fetch";

import getConfig from "next/config";

// Only holds serverRuntimeConfig and publicRuntimeConfig
const { serverRuntimeConfig } = getConfig();
const { ES_HOST, NLP_HOST } = serverRuntimeConfig;

const elasticSearchEndpoint = ES_HOST + "/segments/_search";
const rerankingEndpoint = NLP_HOST + "/api/rerank";

/**
 *
 * @param {String} query - The text to search for in the ElasticSearch index.
 * could be key words, a sentence, or anything.
 */
const getElasticSearchResults = async query => {
  const req = await fetch(elasticSearchEndpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      _source: ["_id"], // we only get the _id field back
      size: 5, // only return the top 5 results
      query: {
        match: { "segments.text": query }
      }
    })
  });
  const json = await req.json();
  // Just return an array of the document _id's.
  return json.hits.hits.map(hit => hit._id);
};

const getRerankingResults = async (query, ranked_ids) => {
  const req = await fetch(rerankingEndpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      ranked_ids
    })
  });
  return req.json();
};

export default async (req, res) => {
  const { query } = req.body;
  if (req.method === "POST") {
    const ranked_ids = await getElasticSearchResults(query);
    const results = await getRerankingResults(query, ranked_ids);
    res.status(200).json(results);
  } else {
    // Handle any other HTTP method
    res.status(405).json({ msg: "This endpoint only supports POST requests." });
  }
};
