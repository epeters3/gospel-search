import json
import random
from pprint import pprint

from fire import Fire


def safe_divide(n, d) -> float:
    return n / d if d else 0.0


def get_data() -> list:
    with open("evaluate/search-results.json", "r") as rf:
        data = json.load(rf)
    return data


def do_get_gold():
    data = get_data()
    for query in data:
        results = query["results"]
        query_text = query["query"]
        random.shuffle(results)

        # Get the gold standard relevance for this result.
        for result in results:
            result["relevance"] = int(
                input(
                    f"""
Given the query \"{query_text}\", how relevant is this passage, on a score of 1-100?

\"{result['text']}\"

>>> """
                )
            )
        # Compute the gold standard rankings for the results, given
        # the relevance scores
        results.sort(key=lambda result: result["relevance"], reverse=True)
        for i, result in enumerate(results):
            result["rank"]["gold"] = i

    # Finally, write out the results
    with open("evaluate/search-results.json", "w") as wf:
        json.dump(data, wf)


def get_precision(query_results: list, system_name: str) -> float:
    system_results = [r for r in query_results if r["rank"][system_name] is not None]
    return safe_divide(
        sum(1 for r in system_results if r["rank"]["gold"] < len(system_results)),
        len(system_results),
    )


def get_spearman_correlation(query_results: list, system_name: str) -> float:
    system_results = [r for r in query_results if r["rank"][system_name] is not None]
    if len(system_results) == 0:
        return 0.0

    n = len(query_results)
    return 1 - (
        6
        * sum((r["rank"][system_name] - r["rank"]["gold"]) ** 2 for r in system_results)
    ) / (n * (n ** 2 - 1))


def do_score() -> list:
    data = get_data()
    scores = []
    for query in data:
        query_results = query["results"]
        scores.append(
            {
                "name": query["name"],
                "precision": {
                    "them": get_precision(query_results, "them"),
                    "me": get_precision(query_results, "me"),
                },
                "spearman": {
                    "them": get_spearman_correlation(query_results, "them"),
                    "me": get_spearman_correlation(query_results, "me"),
                },
            }
        )
    return scores


def main(get_gold: bool = False, score: bool = False) -> None:
    if get_gold:
        do_get_gold()
    elif score:
        pprint(do_score())
    else:
        raise ValueError("please specify an option: `--get_gold`, `--score`")


if __name__ == "__main__":
    Fire(main)
