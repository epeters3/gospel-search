import type { NextApiRequest, NextApiResponse } from 'next'
import { search } from "./_utils";

export default async (req: NextApiRequest, res: NextApiResponse) => {
  const { query } = req.body;
  if (req.method === "POST") {
    const data = await search(query, 10);
    res.status(200).json(data);
  } else {
    // Handle any other HTTP method
    res.status(405).json({ msg: "This endpoint only supports POST requests." });
  }
};
