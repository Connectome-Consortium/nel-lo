from pleiades_search_api.search import Query, SearchInterface
from pprint import pprint

def get_pleiades_results(entity):
    """
    For a given entity mention (extracted in a prior step) searches the Pleiades API 
    and returns all matches (no disambiguation).
    """
    # define query
    q = Query()
    q.set_parameter("text", entity)

    # establish search interface
    ua = "pleiades_search_api_demo/0.1 (+https://github.com/isawnyu/pleiades_search_api)"
    si = SearchInterface(user_agent=ua)

    # perform search
    results = si.search(q)
    pprint(results["hits"], indent=4)

    return results
