from flask import Flask, jsonify, request

from gospel_search.nlp_server.rerank import Reranker
from gospel_search.utils import logger

reranker = Reranker()

app = Flask("HTTP NLP API Server")


@app.route("/api/rerank", methods=["POST"])
def append_to_sequence():
    req_body = request.get_json()

    if (
        "ranked_ids" not in req_body
        or "query" not in req_body
        or not isinstance(req_body["ranked_ids"], list)
    ):
        return (
            jsonify(
                {
                    "msg": 'Request must be of the form { "ranked_ids": [...], '
                    '"query: "your query..." }'
                }
            ),
            400,
        )

    result = reranker.rerank(req_body["query"], req_body["ranked_ids"], 10)

    return jsonify({"result": result})


if __name__ == "__main__":
    logger.info("starting up NLP API server...")
    app.run()
