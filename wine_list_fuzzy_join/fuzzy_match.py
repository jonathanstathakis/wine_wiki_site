from rapidfuzz import process


def fuzzy_match(query, choices):
    """
    find a match for `search_string` from a collection `match_pool`
    """

    result = process.extractOne(query=query, choices=choices)
    return result
