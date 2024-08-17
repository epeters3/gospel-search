import type { NextApiRequest, NextApiResponse } from 'next'
import { SearchResult, search } from "./_utils";
import OpenAI from 'openai';

const stringifySearchResult = (result: SearchResult): string => `Reference name: ${result.name}
Text: ${result.text}
Link: ${result.parent_id}
`

const makePrompt = (query: string, results: SearchResult[]): string => {
  return `You are a helpful assistant assisting with answering questions
related to the gospel of the Church of Jesus Christ of Latter-day Saints.
Only answer gospel and doctrine-related questions. Here are some retrieved
scripture verses and general conference talk paragraphs related to the user's
query. Use them to answer the user's question.

Related scripture verses and conference talk paragraphs:

${results.map(r => stringifySearchResult(r)).join("\n")}

User's query: ${query}

Your answer:`
}

const openai = new OpenAI()

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const { query } = req.body;
  if (req.method === "POST") {
    const data = await search(query, 100)
    const prompt = makePrompt(query, data.result)
    console.log(JSON.stringify({ prompt }))
    const completion = await openai.chat.completions.create({ messages: [{ role: 'system', content: prompt }], model: 'gpt-4o-2024-08-06' })
    const answer = completion.choices[0].message.content
    console.log(JSON.stringify({ answer }))
    res.status(200).json({ answer });
  } else {
    // Handle any other HTTP method
    res.status(405).json({ msg: "This endpoint only supports POST requests." });
  }
};
