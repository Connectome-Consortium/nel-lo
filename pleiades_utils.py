from pleiades_search_api.search import Query, SearchInterface
from pprint import pprint

def get_pleiades_results(entity, fulltext=True):
    """
    For a given entity mention (extracted in a prior step) searches the Pleiades API 
    and returns all matches (no disambiguation).
    Parameters:
    - entity: a mention of a location entity (name of a place etc.)
    - fulltext: whether to search title (False) or title and description/additional information (True, default)
    """
    # define query
    q = Query()
    if fulltext:
        q.set_parameter("text", entity)
    else:
        q.set_parameter("title", entity)

    # establish search interface
    ua = "pleiades_search_api_demo/0.1 (+https://github.com/isawnyu/pleiades_search_api)"
    si = SearchInterface(user_agent=ua)

    # perform search
    results = si.search(q)

    return results["hits"]
