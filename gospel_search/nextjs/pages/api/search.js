import fetch from "node-fetch";

import getConfig from "next/config";

// Only holds serverRuntimeConfig and publicRuntimeConfig
const { serverRuntimeConfig } = getConfig();

const searchEndpoint = serverRuntimeConfig.ES_HOST + "/segments/_search";

/**
 *
 * @param {String} query - The text to search for in the ElasticSearch index.
 * could be key words, a sentence, or anything.
 */
const getElasticSearchResults = async query => {
  const req = await fetch(searchEndpoint, {
    method: "POST",
    body: JSON.stringify({
      query: {
        match: { "segments.text": query }
      }
    }),
    headers: { "Content-Type": "application/json" }
  });
  const json = await req.json();
  return json;
};

export default async (req, res) => {
  console.log(req.body);
  if (req.method === "POST") {
    // TODO: pass the results on to the Python AI server.
    const results = await getElasticSearchResults(req.body.query);
    res.status(200).json(results);
  } else {
    // Handle any other HTTP method
    res.status(405).json({ msg: "This endpoint only supports POST requests." });
  }
};
