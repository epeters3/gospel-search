import fetch from "node-fetch";

const { ES_HOST, NLP_HOST } = process.env;

const elasticSearchEndpoint = ES_HOST + "/segments/_search";
const rerankingEndpoint = NLP_HOST + "/api/rerank";

type BaseResult = {
  _id: string;
  parent_id: string;
  num: number;
  text: string;
  name: string;
  links: string[];
  score: number;
}

type TalkResult = BaseResult & {
  doc_type: "general-conference"
  talk_id: string;
  month: number;
  year: number;
}

type VerseResult = BaseResult & {
  doc_type: "scriptures"
}

export type SearchResult = TalkResult | VerseResult

type SearchResults = {
  result: SearchResult[]
}

const getElasticSearchResults = async (query: string, k: number) => {
  const req = await fetch(elasticSearchEndpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      _source: ["_id"], // we only get the _id field back
      size: k, // only return the top k results
      query: {
        match: { "segments.text": query },
      },
    }),
  });
  const json: any = await req.json();
  // Just return an array of the document _id's.
  return json.hits.hits.map((hit: { _id: string }) => hit._id);
};

const getRerankingResults = async (query: string, ranked_ids: string[]): Promise<SearchResults> => {
  const req = await fetch(rerankingEndpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      ranked_ids,
    }),
  });
  const result = await req.json() as SearchResults
  return result;
};

/**
 * 
 * @param query The text to search for in the ElasticSearch index.
 * could be key words, a sentence, or anything.
 * @param k The number of top hits to return
 */
export const search = async (query: string, k: number) => {
  const rankedIds = await getElasticSearchResults(query, k);
  return await getRerankingResults(query, rankedIds)
}